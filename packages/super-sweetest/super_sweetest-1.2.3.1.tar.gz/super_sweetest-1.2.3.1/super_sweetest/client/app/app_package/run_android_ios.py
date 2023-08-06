# coding:utf-8

# @Time: 2020/3/1 13:33
# @Auther: liyubin

import os
import sys
import time
import json
import datetime
import shutil
import configparser
import requests
import redis
from git import Repo
from super_sweetest.servers.teardown import tear_down
from super_sweetest.servers.common import read_data, write_data

"""
数据处理模块
"""

config_file = './config.ini'
# 创建配置文件对象
config = configparser.RawConfigParser()
# 读取配置文件内容
config.read(config_file, encoding='utf-8')
# ATP服务端的URL地址
PLATFORM_URL = "".join(map(chr, json.loads(dict(config.items('ATP-Server'))['platform_url'])))
# 服务端Redis的IP地址
REDIS_IP = "".join(map(chr, json.loads(dict(config.items('ATP-Server'))['redis_ip'])))
REDIS_KEY = "".join(map(chr, json.loads(dict(config.items('ATP-Server'))['redis_key'])))
REDIS_PORT = "".join(map(chr, json.loads(dict(config.items('ATP-Server'))['redis_port'])))
# 存放测试用例的git仓库
GIT_URL = "".join(map(chr, json.loads(dict(config.items('ATP-Server'))['git_url'])))
if GIT_URL.count('@') - 1 != 0:
    GIT_URL = GIT_URL.replace('@', '%40', GIT_URL.count('@') - 1)

# app执行配置
EXECUTION_ID = dict(config.items('ATP-Server'))['execution_id']
# 设备名称
DEVICE_NAME = dict(config.items('ATP-Server'))['name'].split('_')[1].replace('##', ':')
# iostagen_file
IOSTANGE_FILE = "".join(map(chr, json.loads(dict(config.items('ATP-Server'))['iostagen_file'])))

TEST_TYPE = dict(config.items('ATP-Server'))['test_type']


class CmdColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# 连接 Redis 数据库
POOL = redis.ConnectionPool(host=REDIS_IP, port=REDIS_PORT, db=REDIS_KEY, decode_responses=True)
REDIS_POOL = redis.Redis(connection_pool=POOL)


def write_log_none():
    """日志内容清空，预防日志上传到平台重复"""
    today_log = os.path.join(os.getcwd(), 'log', time.strftime('%Y%m%d.log'))
    new_log = os.path.join(os.getcwd(), 'log', 'new.log')
    write_data(today_log, '')
    write_data(new_log, '')


def mkdir_and_del(srcpath):
    if os.path.isdir(srcpath):
        shutil.rmtree(srcpath)
    os.mkdir(srcpath)


def reset_file(file_name, test_project, test_environment):
    case_path = os.path.join(os.getcwd(), "git_case")
    device_lower = DEVICE_NAME.lower()
    if 'iphone' in device_lower or 'lds' in device_lower or 'ipad' in device_lower:
        lib_dst_path = os.path.join(case_path, test_project + "-Project-ios", test_environment, file_name)
    else:
        lib_dst_path = os.path.join(case_path, test_project + "-Project-android", test_environment, file_name)
    if file_name != 'snapshot/expected/':  # 不删除预期图片，避免git拉取压力大，手动放置图片
        # 确定Git用例存储库中是否有一个lib_dst_path目录
        if os.path.isdir(lib_dst_path):
            lib_src_path = os.path.join(os.getcwd(), file_name)
            # 确定执行目录下是否有一个lib_src_path目录
            if os.path.isdir(lib_src_path):
                shutil.rmtree(lib_src_path)
            shutil.copytree(lib_dst_path, lib_src_path)


def all_mkdir_copy(test_project, test_environment):
    reset_file(file_name="lib", test_project=test_project, test_environment=test_environment)
    reset_file(file_name="data", test_project=test_project, test_environment=test_environment)
    reset_file(file_name="element", test_project=test_project, test_environment=test_environment)
    reset_file(file_name="testcase", test_project=test_project, test_environment=test_environment)
    reset_file(file_name="files", test_project=test_project, test_environment=test_environment)
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "JUnit"))
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "report"))
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "details"))


def read_log_file():
    """
    从以日期为维度统计的日志中提取出本次的日志文件，保存至log/new11111111111.log
    """
    # 初始日志文件的起始行号
    # initial_log_line = 0
    # 初始日志文件的日期前缀
    # initial_log_time = ''
    # 如果日志文件的日期前缀不是当天的日期
    # if initial_log_time != time.strftime('%Y%m%d'):
    # 重置日志文件的前缀、起始行数
    # initial_log_time = time.strftime('%Y%m%d')

    initial_log_line = 0
    # 读取日志文件的全部字符串
    with open(os.path.join(os.getcwd(), 'log', time.strftime('%Y%m%d.log')), "r", encoding='utf-8') as f:
        # 将日志字符串按换行符拆成列表
        log_file_data = f.read().split('\n')
    # 如果起始日志行反而比最大行数都大的话
    if initial_log_line > len(log_file_data):
        # 重置日志文件的起始行数
        initial_log_line = 0
    # 按行号增量取出本次测试的日志
    log_file_list = log_file_data[initial_log_line:]
    # 更新日志文件的起始行号
    initial_log_line = len(log_file_data)
    # 存储日志信息的字典
    log_file_dict = {}
    # 用这个变量控制每一行都是不重复的
    previous_row = ''
    # 整理每一行日志
    for i in range(len(log_file_list)):
        # 不读取空行
        if log_file_list[i] == '':
            continue
        # 不读取和上一行重复的数据
        if log_file_list[i] == previous_row:
            continue
        # 判断当前行是否包含特殊分割符
        if ']: #  ' in log_file_list[i]:
            # 将日志信息按用途分类
            log_file_dict[i] = {
                'time': log_file_list[i][:23],
                'grade': log_file_list[i][25:log_file_list[i].find(']')],
                'message': log_file_list[i][log_file_list[i].find(']') + 6:],
            }
        else:
            # 如果是错误信息，上传特殊格式
            log_file_dict[i] = {
                'time': '',
                'grade': '',
                'message': log_file_list[i].replace(' ', '&nbsp;'),
            }
        # 更新上一行的数据
        previous_row = log_file_list[i]

    # 在log目录下写入新的日志文件
    with open(os.path.join('log', 'new.log'), "w", encoding='utf-8') as fp:
        json.dump(log_file_dict, fp)


def post_heartbeat(status, localtime=None, task_dict=None, remark=None):
    """
    # 描述:
        发送心跳请求到ATP服务器（失败重试，直至恢复连接）
    # 用法0（第一次）:
        post_heartbeat(status=0)
    # 用法1（正常）:
        post_heartbeat(status=1, localtime=[调用时间])
    # 用法2（任务无法完成/放弃任务，需要在备注中提交错误信息）:
        post_heartbeat(status=2, localtime=[调用时间], task_dict=[任务字典], remark=[备注])
    # 用法3（开始执行任务）:
        post_heartbeat(status=3, localtime=[调用时间], task_dict=[任务字典])
    # 用法4（任务执行完成，上传测试报告）:
        post_heartbeat(status=4, localtime=[调用时间], task_dict=[任务字典])
    # 用法5（执行端异常，需要在备注中提交异常信息）:
        post_heartbeat(status=5, remark=[备注])
    """

    # 已连接手机list 设备离线设置平台离线 6
    device_list = read_data('../device_list.json', 'json', 'r')
    if DEVICE_NAME not in device_list:
        status = 6

    if not localtime:
        localtime = time.asctime(time.localtime(time.time()))
    # ATP平台端上执行端心跳的API接口
    heartbeat_api_url = PLATFORM_URL + 'software/execution/heartbeat/'
    # 心跳请求连接次数
    connect = 0
    # 开始发送心跳请求
    while True:
        # 捕获异常
        try:
            # 执行端心跳参数
            up_data = {'id': EXECUTION_ID, 'status': status, 'task_dict': json.dumps(task_dict),
                       'remark': remark}
            # 状态为4时，组织待上传的次数报告文件
            if status == 4:
                # 拔高变量的层级
                files_report = None
                files_junit = None
                # 取出XXX-Report@XXXXXX_XXX.xlsx的测试报告文件名
                for _root, _dirs, files in os.walk(os.path.join('report', task_dict['test_name'])):
                    if files:
                        files_report = files[0]
                # 取出XXX-Report@XXXXXX_XXX.xml的测试汇总文件名
                for _root, _dirs, files in os.walk('JUnit'):
                    if files:
                        files_junit = files[0]
                # 读取测试报告文件
                files_report_obj = read_data(os.path.join('report', task_dict['test_name'], files_report), '', 'rb')
                # 读取测试汇总文件
                files_junit_obj = read_data(os.path.join('JUnit', files_junit), '', 'rb')
                # 读取测试详情文件
                files_details_obj = read_data(os.path.join('details', 'details.txt'), '', 'rb')
                # 读取测试日志文件
                read_log_file()
                with open(os.path.join('log', 'new.log'), 'rb') as fp4:
                    files_log_obj = fp4.read()
                # 汇总XXX-Report@XXXXXX_XXX.xlsx、XXX-Report@XXXXXX_XXX.xml、details.txt文件对象
                files_obj = {
                    'file_obj': (str(task_dict['queue_id']) + '.xlsx', files_report_obj),
                    'file_obj_junit': (str(task_dict['queue_id']) + '.xml', files_junit_obj),
                    'file_obj_details': (str(task_dict['queue_id']) + '.txt', files_details_obj),
                    'file_obj_log': (str(task_dict['queue_id']) + '.log', files_log_obj)
                }
            else:
                files_obj = {}
            # 向ATP平台端发送执行端心跳请求
            requests_data = requests.post(heartbeat_api_url, data=up_data, files=files_obj)
            requests_json = requests_data.json()
            # 判断平台端心跳状态处理结果
            if requests_json['code'] == 200:
                # 心跳请求响应成功，结束死循环
                print('[Heartbeat][' + localtime + ']> ' + str(requests_json['data']))
                break
            # 服务器内部错误错误
            else:
                print('[Heartbeat Error][' + localtime + ']> > ' + str(requests_json))
                break
        # 网络请求错误
        except Exception as exc:
            print('[Heartbeat Error][' + localtime + ']> ' + str(exc))
        # 30秒后重新发送心跳请求
        time.sleep(30)
        connect += 1
        print('[Heartbeat Error][' + localtime + ']> 进行第 ' + str(connect) + ' 次重新连接')
        # 防止 异常后文件找不到 进入死循环 join argument must be str or bytes, not 'NoneType'
        if connect > 2:
            break


def write_testdata_and_run(test_name, connect_type):
    """
     写入测试所需数据
    :param test_name:
    """

    connect_type_dict = json.loads(connect_type)

    if TEST_TYPE == '1':
        # 如果平台没同步当前设备connect_type_dict / {"iphone":"ios"} 时，手动输入
        connect_type_dict[DEVICE_NAME] = [input('当前手机未在平台同步connect_type，请输入：')] if connect_type_dict.get(DEVICE_NAME) == "" or 'iphone' in connect_type_dict else connect_type_dict.get(DEVICE_NAME)
        # android
        run_case_data = {'test_name': test_name, 'status': False, 'device_name': DEVICE_NAME,
                         'connect_type_list': connect_type_dict.get(DEVICE_NAME)}
        write_data('./run_case_data.json', run_case_data, 'json', 'w+')

        # 启动test_case模块
        os.popen('start python ./test_case.py')
    else:
        # ios
        run_case_data = {'test_name': test_name, 'status': False, 'device_name': DEVICE_NAME,
                         'iostagen_file':IOSTANGE_FILE}
        write_data('./run_case_data.json', run_case_data, 'json', 'w+')

        # 启动test_case模块
        os.system('nohup python3 ./test_case.py &')

    # 如果运行结束状态status：True，继续下一步
    # 隐式等待/避免执行端假死
    now_time_flag = datetime.datetime.now()
    while True:
        time.sleep(5)
        if (datetime.datetime.now() - now_time_flag).seconds > 3600:
            break
        else:
            status = read_data('./run_case_data.json', 'json', 'r')
            if status['status']:
                return status.get('msg', '')


def run_test_main(execution_id, localtime):
    """
    执行app主方法
    :param queu_type:
    :param test_type:
    """
    print(localtime + CmdColors.HEADER + " →_→ 发现有新任务" + CmdColors.END)
    value_dict = json.loads(REDIS_POOL.lpop(execution_id))
    # 上报开始执行任务的心跳
    post_heartbeat(status=3, localtime=localtime, task_dict=value_dict)

    try:
        print('[Queue Task Dict]> ' + str(value_dict))

        print(CmdColors.BLUE + "重置 Sweetest 测试运行环境 ……" + CmdColors.END)
        all_mkdir_copy(test_project=value_dict['test_project'], test_environment=value_dict['test_environment'])

        print(CmdColors.GREEN + "Sweetest 测试运行环境就绪, 开始执行 ……%s " % CmdColors.END)
        global run_msg
        run_msg = write_testdata_and_run(test_name=value_dict['test_name'], connect_type=value_dict.get('connect_type','{"iphone":"ios"}'))

        print('[App Server Run Info]> X-Sweetest 测试完成并上传测试报告')
        # 上报任务执行完成的心跳
        post_heartbeat(status=4, localtime=localtime, task_dict=value_dict)
        print('[App Server Run Info]> 测试报告上传完毕')

        # 清空日志
        write_log_none()
    except Exception as exc:
        # 上报任务无法完成的心跳
        post_heartbeat(status=2, localtime=localtime, task_dict=value_dict, remark=str(exc)+ '---' +str(run_msg))
        print('[App Server Run Error]> ' + str(exc))


def pull_case():
    """
    拉取最新case
    每次执行用例时pull，保持数据同步
    """
    try:
        git_case_path = os.path.join(os.getcwd(), "git_case")
        if os.path.isdir(git_case_path):
            print(CmdColors.BLUE + " *_* 发现 git_case 目录, 执行更新最新用例流程 ……" + CmdColors.END)
            repo = Repo.init(path=git_case_path)
            remote = repo.remote()
            remote.pull()
            print(CmdColors.GREEN + " ^_^ 已更新 GitLab 仓库中 git_case 项目的用例" + CmdColors.END)
        else:
            print(CmdColors.FAIL + " @_@ 找不到 git_case 目录, 执行下载新用例流程 ……" + CmdColors.END)
            Repo.clone_from(url=GIT_URL, to_path=git_case_path)
            print(CmdColors.GREEN + " ^_^ 已下载 GitLab 仓库中 git_case 项目的用例" + CmdColors.END)
    except Exception as e:
        print(' --- 用例下载失败，请检查Git-Server配置信息 --- \n\t%s' % e)
    time.sleep(3)


def main_():
    """
    主运行程序
    :return:
    """
    # mkdir_and_del(srcpath=os.path.join(os.getcwd(), "log"))
    # mkdir_and_del(srcpath=os.path.join(os.getcwd(), "snapshot"))  #不删除历史日志和预期图片
    tear_down(git_case=False, snapshot=False)  # 如需提交代码，取消注释执行

    logo = """
   :f###.    ;#:
     ,###    #:
      G##,  G,             X-ATP执行终端
      .### :#              APP自动化测试
        # DW
        :##:               监听Redis数据库:
         # .               {0}
        G:###
       tE ,##,             atp服务运行地址:
      ,#   G##:            {1}
     .#:    ###
    :#;     :###.
    """.format(REDIS_IP, PLATFORM_URL)
    print(CmdColors.BLUE + logo + CmdColors.END)
    pull_case()

    print('[App Server Run Info]> 检测是否有历史任务未完成')
    # 上报第一次/刚启动执行端的心跳
    post_heartbeat(status=0)

    while True:
        time.sleep(5)
        try:
            length = REDIS_POOL.llen(EXECUTION_ID)
            localtime = time.asctime(time.localtime(time.time()))
            if length > 0:
                pull_case()
                run_test_main(EXECUTION_ID, localtime)
            else:
                # 上报正常的心跳
                post_heartbeat(status=1, localtime=localtime)
            # 调用Flush，从内存中刷入日志文件
            sys.stdout.flush()
        except Exception as exc:
            # 上报执行端异常的心跳
            post_heartbeat(status=5, remark=str(exc))
            print('[App Server Run Error]> ' + str(exc))
