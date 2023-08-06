# coding:utf-8

# @Time: 2020/4/20 15:59
# @Auther: liyubin


import os
import sys
import time
import uuid
import json
import shutil
import socket
import platform
import requests
import configparser
from pathlib import Path


"""
自动注册和生成对应手机的 android/ios work
test_type: api/android/ios/web   对应：0/1/2/3
"""

def get_pc_ip():
    """
    :return: ip34name
    """
    #获取本机电脑名
    myname = socket.gethostname()
    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    ip = myaddr.split(".") if myaddr else ''
    ip34name = ip[2]+ip[3] if isinstance(ip, list) else 'get ip error'
    return ip34name


def get_initialization(test_type, platform_url, workspace_name):
    """
    注册到平台
    :param test_type:
    :param platform_url:
    :param workspace_name:
    :return:
    """
    # 对输入的URL做判断，末尾没加"/" 统一处理加上"/"
    if not platform_url.endswith('/'):
        platform_url += '/'
    # ATP平台端初始化执行端的API接口
    initialization_api_url = platform_url + 'software/execution/initialization/'
    # 如果执行工作区名称为默认值，生成随机数
    if workspace_name == '':
        # 根据当前网卡和时间组成随机数
        workspace_name = uuid.uuid4().hex
    # api、android、ios、web执行端的通用参数
    up_data = {'name': workspace_name, 'execution_type': test_type}
    # api执行端的特殊参数
    if test_type == 0:
        up_data['information'] = json.dumps({'system': platform.system()})
    # android
    elif test_type == 1:
        up_data['information'] = json.dumps({'system': platform.system()})
    # ios
    elif test_type == 2:
        up_data['information'] = json.dumps({'system': platform.system()})
    # 向ATP平台端发送初始化执行端请求
    requests_data = requests.post(initialization_api_url, data=up_data)
    requests_json = requests_data.json()
    print('[Cli info]> ' + str(requests_json))
    # 判断平台端初始化结果
    if requests_json['code'] != 200:
        print('[Cli Error]> 执行端服务初始化失败')
        sys.exit()
    # 附带上经过上面处理的ATP平台URl
    requests_json['data']['platform_url'] = platform_url
    requests_json['data']['redis_ip'] = platform_url.replace('http://','').replace('/','')
    requests_json['data']['test_type'] = test_type
    return requests_json


def create_profile(data, work_space, current_dir, copy_file_list):
    """
    在程序执行的当前目录下创建配置文件和执行程序
    :param data: config.ini 配置信息
    :param work_space: 新创建的work
    :param current_dir: 源执行文件
    :param copy_file_list: 需要拷贝的文件list
    """
    # 处理GIT仓库URL里的特殊字符
    data['git_url'] = data['git_url'].replace('%40', '@')
    config = configparser.ConfigParser()
    # 创建config配置文件
    file = 'config.ini'
    config.read(work_space / file)
    config.add_section('ATP-Server')
    # 平台URL、GIT仓库URL、工作空间名、队列IP、队列KEY、队列端口号、注册ID
    config.set('ATP-Server', 'platform_url', json.dumps(list(map(ord, data['platform_url']))))
    config.set('ATP-Server', 'name', data['name'])
    config.set('ATP-Server', 'git_url', json.dumps(list(map(ord, data['git_url']))))
    config.set('ATP-Server', 'redis_ip', json.dumps(list(map(ord, data['redis_ip']))))
    config.set('ATP-Server', 'redis_key', json.dumps(list(map(ord, str(data['redis_key'])))))
    config.set('ATP-Server', 'redis_port', json.dumps(list(map(ord, str(data['redis_port'])))))
    config.set('ATP-Server', 'execution_id', str(data['execution_id']))
    config.set('ATP-Server', 'iostagen_file', json.dumps(list(map(ord, str(data['iostagen_file'])))))
    config.set('ATP-Server', 'test_type', str(data['test_type']))
    # 保存config配置文件
    with open(work_space / file, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    # 拷贝Android_IOS_Work执行文件到工作空间

    for py in copy_file_list:
        shutil.copy(current_dir / py, work_space / py)

def new_workspace(sys_name, data, copy_file_list, iostagen_file, diy_redis_ip):
    """
    创建新的work
    :param sys_name:
    :param data:
    :param copy_file_list:
    :param iostagen_file:
    :return:
    """
    data_dict = {
        'name': data['name'],
        'platform_url': data['platform_url'],
        'git_url': data['git_url'],
        'redis_ip': data['redis_ip'] if not diy_redis_ip else diy_redis_ip,
        'redis_key': data['redis_key'],
        'redis_port': data['redis_port'],
        'execution_id': data['execution_id'],
        'iostagen_file': iostagen_file,
        'test_type': data['test_type'],
    }
    current_path = os.path.abspath(__file__)
    # 需要拷贝的x-app-package下的文件
    current_dir = Path(os.path.join(os.path.dirname(current_path), 'copy_file'))
    cwd_dir = Path.cwd()
    work_space = cwd_dir / ('Android_IOS_Work_%s' % data_dict['name'])
    os.mkdir(str(work_space))
    create_profile(data=data_dict, work_space=work_space, current_dir=current_dir, copy_file_list=copy_file_list)

    # 新app服务路径
    # new_server_path = Path(os.path.join(os.path.dirname(current_path), 'Android_IOS_Work_' + data_dict['name']))
    new_server_path = 'Android_IOS_Work_' + data_dict['name'] # client放在内部调用后，不展示super-sweetest的安装路径
    # print('\n###   工作空间   ###\n%s\n' % new_server_path)

    # 后台执行atp执行端
    if sys_name == 'Linux':
        # daemon_start(data=data_dict, work_space=work_space)
        print('###   X-ATP自动化测试执行端服务已在后台运行   ###')
    elif sys_name == 'Windows':
        print('###   您需要手动启动Android自动化work 服务   ###\n1、进入目录：%s\n2、双击运行程序： %s\n' % (new_server_path, 'run_this.py'))
    else:
        print('###   您需要手动启动ios自动化work 服务   ###\n1、进入目录：%s\n2、运行程序： %s\n' % (new_server_path, 'run_this.py'))


def create_android_ios_work(mobile_list, test_type, platform_url, copy_file_list, iostagen_file, diy_redis_ip=None):
    """
    创建当前接入手机的Android/ios自动化work
    :param mobile_list:
    :param test_type:
    :param platform_url:
    :param copy_file_list:
    :param iostagen_file:
    :param diy_redis_ip: 自定义redis地址
    :return:
    """

    localtime_ = time.asctime(time.localtime(time.time()))
    work_list_file = './work_name_list.json'

    for device in mobile_list:
        # 获取已连接的android手机名称
        device_ = device.get('device_name')
        if 'unauthorized' in device_:
            break
        mobile_name = device.get('mobile_name') if int(test_type) == 1 else device.get('version')

        # mobilename_devicesname
        ip34 = get_pc_ip()
        if ip34 == '01':
            break
        work_name = mobile_name.replace(' ', '') + '-' + ip34 + '_' + device_.replace(':', '##')

        # 首次创建
        if not os.path.exists(work_list_file):
            with open(work_list_file, 'w+')as fp:
                json.dump(['work_name'], fp)


        # 读取work_list_file 创建历史
        with open(work_list_file, 'rb')as fp1:
            work_name_list = json.load(fp1)

        # 已存在历史中
        if work_name in work_name_list:
            # 是否存在 Android自动化work 目录
            if not os.path.exists('./Android_IOS_Work_%s' % work_name):
                print(localtime_ + ' 本机创建过，但不存在  对应手机: %s 的Android/ios自动化 work 目录...   \n正在创建...' % work_name)
                # 注册到平台
                data_json = get_initialization(test_type, platform_url, work_name)
                # 创建新的执行程序
                new_workspace(sys_name=platform.system(), data=data_json['data'], copy_file_list=copy_file_list, iostagen_file=iostagen_file, diy_redis_ip=diy_redis_ip)
                # 已在work_list历史不添加

        else:
            # 清理历史清单信息异常时，可能存在的 Android/ios自动化work 目录
            if os.path.exists('./Android_IOS_Work_%s' % work_name):
                print(localtime_ + ' 清理已存在: %s  的Android/ios自动化work 目录...' % work_name)
                shutil.rmtree('./Android_IOS_Work_%s' % work_name)

            print(localtime_ + ' 不存在 对应手机: %s  的Android/ios自动化work 目录...   \n正在创建...' % work_name)
            # 注册到平台
            data_json = get_initialization(test_type, platform_url, work_name)
            # 创建新的执行程序
            new_workspace(sys_name=platform.system(), data=data_json['data'], copy_file_list=copy_file_list, iostagen_file=iostagen_file, diy_redis_ip=diy_redis_ip)

            # 将此设备加入已创建历史
            with open(work_list_file, 'w+')as fp2:
                work_name_list.append(work_name)
                json.dump(work_name_list, fp2)


if __name__ == '__main__':

    DEVICE_LIST = ['1197cd5e']  # 建议写手机名和下划线devicename
    TEST_TYPE = 1  # android
    PLATFORM_URL = 'http://127.0.0.1'  # 平台地址
    COPY_FILE_LIST = ['test_case.py', 'run_this.py']  # copy_file下需要拷贝的文件

    while True:
        time.sleep(5)
        create_android_ios_work(DEVICE_LIST, TEST_TYPE, PLATFORM_URL, COPY_FILE_LIST,'iostagen_file')
