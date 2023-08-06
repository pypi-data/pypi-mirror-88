import json
import sqlite3
import pandas as pd
from sany_wind_bi_report import data_message_pb2
from sany_wind_bi_report import data_message_pb2_grpc
import grpc
import datetime
import os

options = [('grpc.max_message_length', 64 * 1024 * 1024), ('grpc.max_receive_message_length', 64 * 1024 * 1024)]


# 保存结果三个分析模块的结果文件
def return_report_result(project_name, wind_farm, data_start_time, data_end_time,
                         turbine_type=None, turbine_num=None, status=None, result=None,
                         result_json=None, upload_fig_path=None, upload_log_path=None,
                         upload_file_path=None, local_fig_path=None, local_log_path=None,
                         local_file_path=None, Report_version=None, project_id=None):
    """
    将事件分析，发电量分析，健康分析三个模块的结果文件传入COS上(一次只传一个文件)
    project_name：报表英文名，不可省略
    wind_farm：风场拼音缩写，不可省略
    data_start_time：报表中使用的数据开始时间，不可省略（方便后续排查问题查询，格式统一为‘%Y-%m-%d %H:%M:%S’）
    data_end_time：报表中使用的数据结束时间，不可省略（格式统一为‘%Y-%m-%d %H:%M:%S’）
    turbine_type：机组型号（字符串，例如：‘14125’），可省略
    turbine_num：机组号（字符串，例如：01,02），可省略
    status：判断状态，共分为三种：正常、告警、故障（目的是前端显示颜色，分别为无色、黄色、红色）
    result：报表判断结果（例如：0.8、90，不可判断等），可省略
    result_json：报表产生的其他信息，json格式，可省略（主要留作后续给前段产生动态图的json数据）
    upload_fig_path：报表产生图片云端保存位置，可省略
    upload_log_path：报表产生日志云端保存位置，可省略
    upload_file_path：报表其他文件云端保存位置，可省略
    local_fig_paths：报表产生的图片本地保存位置，可省略
    local_log_path：报表产生的日志本地保存位置，可省略
    local_file_path：报表产生的其他文件本地保存位置，可省略
    Report_version：报表版本号（例如：1.0.0），可省略，(不建议省略)
    project_id：报表id号（例如：10001），可省略(目前可省略，后续统一之后再设置)
    return：返回为int数字，如果成果，则返回0，如果失败，则返回1
    注意：
    1）报表执行过程将产生的图片、日志、其他文件等暂保存为本地位置，最终通过调用接口，传入相关参数后，接口会自动将本地文件传入云端，并删除本地文件
    2）报表上传文件统一格式为：fig、log、file/{报表名字，project_name}/{wind_farm,风场名}/**.png、**.log、**.csv、其他；（**代表最终文件命名，命名时应尽可能说明机组号、报表所使用数据时间等信息，可以对报表每次执行结果进行区分）
    3）报表本地保存统一格式为：/tmp/sanydata_frpc_**.png、sanydata_frpc_**.log、sanydata_frpc_**.csv、其他（上述中**代表最终文件命名，命名时应尽可能避免多文件保存到本地时进行覆盖，建议采用当前时间）

    """

    Report_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Report_start_time = os.getenv('ReportStartTime')
    #task_id = int(os.getenv('TaskId'))
    task_id = 9999

    if not Report_version:
        Report_version = os.getenv('ProjectVersion')

    fig_fio = None
    log_fio = None
    file_fio = None

    # 本地图片处理
    if local_fig_path:
        with open(local_fig_path, 'rb') as f:
            fig_fio = f.read()
        os.remove(local_fig_path)
    # 本地日志处理
    if local_log_path:
        with open(local_log_path, 'rb') as f:
            log_fio = f.read()
        os.remove(local_log_path)
    # 本地文件处理
    if local_file_path:
        with open(local_file_path, 'rb') as f:
            file_fio = f.read()
        os.remove(local_file_path)

    with grpc.insecure_channel('120.53.224.50:9898', options=options) as channel:
    # with grpc.insecure_channel('localhost:9898', options=options) as channel:
        stub = data_message_pb2_grpc.BridgeMessageStub(channel)

        data_input = data_message_pb2.ReturnReportResultInput(projectname=project_name,
                                                              windfarm=wind_farm, turbinetype=turbine_type, turbine=turbine_num,
                                                              DataStartTime=data_start_time, DataEndTime=data_end_time,
                                                              ModeStartTime=Report_start_time, ModeEndTime=Report_end_time,
                                                              projectid=project_id, projectversion=Report_version, task_id=task_id,
                                                              result=result, resultjson=result_json, status=status,
                                                              uploadfigpath=upload_fig_path, uploadlogpath=upload_log_path,
                                                              uploadfilepath=upload_file_path,
                                                              fig=fig_fio, log=log_fio, file=file_fio)

        res = stub.ReturnReportResult(data_input, timeout=20000)
    return json.loads(res.code)


def return_fault_analy(fault_detail_df, farmid=None, farmname=None, turbineid=None, turbinetype=None, faulttype=None):
    '''
    将故障明细表插入mysql中
    :param fault_detail_df:  故障明细表
    :param farmid:           风场id
    :param farmname:
    :param turbineid:
    :param turbinetype:
    :param faulttype:
    :return:返回为int数字，如果成果，则返回0，如果失败，则返回1
    '''

    from datetime import datetime

    with grpc.insecure_channel('120.53.224.50:9898', options=options) as channel:
    # with grpc.insecure_channel('localhost:9898', options=options) as channel:
        stub = data_message_pb2_grpc.BridgeMessageStub(channel)

        res_l = list()
        for index,row in fault_detail_df.iterrows():
            pinyincode = row['farm']
            turbinename = row['fan']
            statuscode = row['list_code']
            faultdesc = row['list_name']
            faultpart = row['list_partstyle']
            faultstarttime = row['list_stime']
            faultendtime = row['list_etime']
            downtime = row['list_timest']
            dentatime = row['list_mt']
            updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            data_input = data_message_pb2.ReturnFaultAnalyInput(farmid=farmid, pinyincode=pinyincode, farmname=farmname,
                                                                turbineid=turbineid, turbinename=turbinename,
                                                                turbinetype=turbinetype, statuscode=statuscode,
                                                                faultdesc=faultdesc, faulttype=faulttype,
                                                                faultpart=faultpart, faultstarttime=faultstarttime,
                                                                faultendtime=faultendtime, downtime=downtime,
                                                                dentatime=dentatime, updatetime=updatetime)
            res = stub.ReturnFaultAnaly(data_input, timeout=20000)
            res_l.append({index:res})
    return res_l


def return_report_result_status(page_feature_sta, page_power_sta, taskname, jobname, farmid=None,
                                farmname=None, reporttype=None, datestring=None, reportargs=None,
                                analyzingsummary=None, analyzingreports=None, taskid=None,
                                createdat=None, updatedat=None):
    '''
    将页面显示的指标及文件地址插入mysql中
    :param page_feature_sta: 页面显示前9个指标
    :param page_power_sta:   页面显示的关于发电量3个指标
    :param farmid:
    :param farmname:
    :param turbineid:
    :param turbinetype:
    :param faulttype:
    :param analyzingsummary：分析总结html文件
    :param analyzingreports：分析报表json格式，文件与cos地址
    :return: 返回为int数字，如果成果，则返回0，如果失败，则返回1
    '''

    taskname = taskname
    jobname = jobname
    farmid = farmid
    farmname = farmname
    reporttype = reporttype
    datestring = datestring
    reportargs = reportargs
    turbinecount = page_feature_sta.iloc[0]['风机台数']
    averageavailability = page_feature_sta.iloc[0]['平均可利用率']
    averagehalttime = page_feature_sta.iloc[0]['总停机时长']
    haltfrequency = page_feature_sta.iloc[0]['停机频次']
    totalhaltcount = page_feature_sta.iloc[0]['总停机次数']
    totalhalttime = page_feature_sta.iloc[0]['平均停机时长']
    totalhaltturbines = page_feature_sta.iloc[0]['总停机台数']
    mtbf = page_feature_sta.iloc[0]['平均无故障时间']
    mttr = page_feature_sta.iloc[0]['平均恢复时间']

    averagespeed = page_power_sta.iloc[0]['平均风速']
    totalpower = page_power_sta.iloc[0]['总发电量']
    cyclepower = page_power_sta.iloc[0]['发电量']
    analyzingsummary = analyzingsummary
    analyzingreports = analyzingreports
    taskid = taskid
    createdat = createdat
    updatedat = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with grpc.insecure_channel('120.53.224.50:9898', options=options) as channel:
    # with grpc.insecure_channel('localhost:9898', options=options) as channel:
        stub = data_message_pb2_grpc.BridgeMessageStub(channel)
        data_input = data_message_pb2.ReturnReportResultStatusInput(taskname=taskname, jobname=jobname, farmid=farmid,
                                                                    farmname=farmname, reporttype=reporttype, datestring=datestring,
                                                                    reportargs=reportargs, turbinecount=turbinecount,
                                                                    averageavailability=averageavailability,
                                                                    averagehalttime=averagehalttime,
                                                                    haltfrequency=haltfrequency,
                                                                    totalhaltcount=totalhaltcount,
                                                                    totalhalttime=totalhalttime,
                                                                    totalhaltturbines=totalhaltturbines,
                                                                    mtbf=mtbf, mttr=mttr, averagespeed=averagespeed,
                                                                    totalpower=totalpower, cyclepower=cyclepower,
                                                                    analyzingsummary=analyzingsummary,
                                                                    analyzingreports=analyzingreports, taskid=taskid,
                                                                    createdat=createdat, updatedat=updatedat)
        res = stub.ReturnReportResultStatus(data_input, timeout=20000)

    return res

'''
示例演示：
from sany_wind_bi_report.bi_report_return_result import *
import pandas as pd

# test return result status
df1 = pd.DataFrame({'平均可利用率': 99, '总停机时长': 200, '总停机次数': 2, '总停机台数': 4, '平均停机时长': 2,
                    '停机频次': 5, '平均无故障时间': 1, '平均恢复时间': 6, '风机台数': 1}, index=[0])
df2 = pd.DataFrame({'平均风速': 6, '总发电量': 100, '发电量': 59}, index=[0])
res = return_report_result_status(df1, df2, 'page_xianshi', '01')


# test return_report_result(file_path)
res = return_report_result('report_result_test', 'ALSFC', '2020-09-11 10:55:20', '2020-09-11 11:55:20',
                         turbine_type=None, turbine_num=None, status=None, result=None,
                         result_json=None, upload_fig_path=None, upload_log_path=None,
                         upload_file_path='/report/day/ALSFC/20200801/test_cui/04#.txt', local_fig_path=None,
                           local_log_path=None,
                           local_file_path="/data02/jupyter_data/Cuibingwei/data/BI_report_demodata/05#.csv",
                           Report_version=None, project_id=None)
print(str(res))

# test return_fault_analy(df)
fault_detail_df = pd.DataFrame({'list_stime': '2020-09-11 10:55:20',  'list_etime': '2020-09-11 11:55:20',
                                'list_name': 'adb', 'list_code': '123', 'list_num': 5, 'list_time': 321,
                                'list_timest': 18000, 'list_mt': 20000, 'list_partstyle': 'jubu','farm':"TYSFC",
                                'fan':'001'},index=[0])

res = return_fault_analy(fault_detail_df, farmid=None, farmname=None, turbineid=None, turbinetype=None, faulttype=None)
print(str(res))
'''
