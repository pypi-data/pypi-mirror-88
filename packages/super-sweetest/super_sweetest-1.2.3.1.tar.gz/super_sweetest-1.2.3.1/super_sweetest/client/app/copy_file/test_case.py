# coding:utf-8

# @Time: 2020/3/19 15:59
# @Auther: liyubin

import os
import xlrd
import unittest
from super_sweetest import Autotest
from super_sweetest.servers.common import write_data, read_data

"""
独立执行模块
"""

class TESTCASE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        case_data = read_data('./run_case_data.json', 'json', 'r')
        cls.test_name = case_data.get('test_name', '')
        cls.device_name = case_data.get('device_name', '')
        cls.platform_version = case_data.get('platform_version', '')
        cls.connect_type_list = case_data.get('connect_type_list', '')
        cls.iostagen_file = case_data.get('iostagen_file', '')

    def test_run(self):
        """
        测试主方法
        项目名称，和测试用例、页面元素表文件名称中的项目名称必须一致
        """
        global msg
        plan_name = self.test_name

        # 环境配置信息
        if os.path.exists('./lib/app_config.json') and os.path.exists('testcase/' + plan_name + '-TestCase.xlsx'):
            # 读取用例的sheet列表
            book = xlrd.open_workbook('testcase/' + plan_name + '-TestCase.xlsx')
            sheet_list = book.sheet_names()
            # 多sheet页面模式
            sheet_name = sheet_list

            # 读取启动app配置文件
            app_config = read_data('./lib/app_config.json', 'json', 'r')

            desired_caps_ = app_config.get('DESIRED_CAPS')
            mobile_desc = {'platformVersion': self.platform_version, 'deviceName': self.device_name,
                           'connect_type_list': self.connect_type_list, 'iostagen_file': self.iostagen_file}
            desired_caps_.update(mobile_desc)
            desired_caps = desired_caps_
            # appium server
            server_url = app_config.get('SERVER_URL')

            msg = '数据准备正常'
        else:
            desired_caps = {}
            server_url = ''
            sheet_name = ''
            msg = '未获取有效数据'

        # 初始化自动化实例
        sweet = Autotest(plan_name, sheet_name, desired_caps, server_url)
        # 执行自动化测试
        sweet.plan()
        # 保存txt格式的详情信息 + 运行报告的手机信息
        sweet.report_data.update({'deviceName': self.device_name})
        write_data('details/details.txt', sweet.report_data, 'json', 'w+')

    @classmethod
    def tearDownClass(cls):
        # 写入执行完成状态，数据处理模块确认状态后上传报告
        write_data('./run_case_data.json', {'status': True, 'msg': msg}, flag='json', mode='w+')


if __name__ == '__main__':
    unittest.main()
