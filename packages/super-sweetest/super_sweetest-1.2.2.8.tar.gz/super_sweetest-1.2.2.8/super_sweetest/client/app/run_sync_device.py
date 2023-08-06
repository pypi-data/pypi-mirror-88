# coding:utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin


import json
import time
import requests
from super_sweetest.client.app.android_ios_cli import create_android_ios_work
from super_sweetest.servers.common import write_data
from super_sweetest.servers.ios_server import get_ios_devices
from super_sweetest.servers.cmd_server import get_devices, get_mobile_desc

"""
1、 手机信息同步，单独运行保障执行用例过程中同步

2、 检测接入手机和创建Android/ios自动化work 目录

    部署需关注：配置 TEST_TYPE 、PLATFORM_URL
"""



def sync_devices(platform_url, test_type):
    """
    同步mobile状态/手机详情
    """
    localtime = time.asctime(time.localtime(time.time()))

    if test_type == 1:
        device_list = get_devices()  # 获取设备列表
        mobile_desc_list = get_mobile_desc(device_list)  # 获取处理后手机详情
    else:
        device_list, mobile_desc_list = get_ios_devices()  # 获取ios设备列表

    write_data('./device_list.json', device_list, 'json', 'w+')  # 写入连接设备

    try:
        # 同步手机详情信息
        connect_url = platform_url + 'software/sweetest/mobile/collect/'

        res = requests.post(connect_url, {'mobile_desc_list': json.dumps(mobile_desc_list)}).json()

        if res['code'] == 200:
            print(localtime + ' --- sync device success --- ')
        else:
            print(localtime + ' --- sync device fails --- ')
    except Exception as e:
        pass
    return mobile_desc_list


def run_sync_device_(test_type=None, platform_url=None, copy_file_list=None, iosTange_file=None, diy_redis_ip=None):
    """
    主方法
    :return:
    """
    TEST_TYPE = 1  if not test_type else test_type  # 创建 Android 标识 1, iOS 标识 2

    PLATFORM_URL = 'http://atp.leedarson.com/'  if not platform_url else platform_url  # 正式
    # PLATFORM_URL = 'http://127.0.0.1:8000/'  # 本地

    COPY_FILE_LIST = ['test_case.py', 'run_this.py', '__init__.py']   if not copy_file_list else copy_file_list  # copy_file 下需要拷贝的文件

    IOSTANGE_FILE = '/Users/liyubin1/Desktop/xcode11.5--iOS-Tagent'  if not iosTange_file else iosTange_file  # iOS-Tagent 服务在mac的目录位置

    DIY_REDIS_IP = '172.24.185.62' if not diy_redis_ip else diy_redis_ip  # 自定义配置不同的redis地址

    while True:
        time.sleep(5)
        try:
            # 同步手机
            MOBILE_LIST = sync_devices(PLATFORM_URL, TEST_TYPE)
            # 检测接入手机和创建Android/ios自动化work 目录
            create_android_ios_work(MOBILE_LIST, TEST_TYPE, PLATFORM_URL, COPY_FILE_LIST, IOSTANGE_FILE, DIY_REDIS_IP)
        except Exception as e:
            print('同步手机失败：', e)
