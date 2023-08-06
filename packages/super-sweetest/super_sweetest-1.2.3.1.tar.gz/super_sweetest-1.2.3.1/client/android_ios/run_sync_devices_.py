# coding:utf-8

# @Time: 2020/12/10 12:16
# @Auther: liyubin

from super_sweetest.client.app.run_sync_device import run_sync_device_


"""
1、 手机信息同步，单独运行保障执行用例过程中同步

2、 检测接入的手机和创建Android/ios自动化work 目录

    部署需关注：配置 TEST_TYPE 、PLATFORM_URL
"""

TEST_TYPE = 1  # 创建 Android 标识 1, iOS 标识 2


run_sync_device_(test_type=TEST_TYPE)

