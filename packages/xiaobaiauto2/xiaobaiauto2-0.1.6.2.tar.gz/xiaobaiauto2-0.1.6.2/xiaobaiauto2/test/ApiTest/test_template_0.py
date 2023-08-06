#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'test_template_0.py'
__create_time__ = '2020/7/17 2:15'

'''
    v1版，脚本与数据不分离，适合业务变更不频繁的场景
'''

import pytest

@pytest.fixture(scope='session')
def login(caplog):
    print('验证token是否有效，无效则重新执行登陆接口获取token')

def setup_module(caplog):
    print("整个文档执行前执行一次")
    # global_vars = {'变量名': '变量值', '变量2': '值2'}

def teardown_module():
    print("整个文件执行后执行一次")

def setup_function():
    print("执行每个方法前执行一次，不适合单接口")

def teardown_function():
    print("执行每个方法后执行一次，不适合单接口")


def test_xiaobai_api():
    print("执行接口测试")
    assert '实际返回值' != '预期值'

class TestClass(object):

    def setup_class(self):
        print("setup_class(self)：每个类之前执行一次")

    def teardown_class(self):
        print("teardown_class(self)：每个类之后执行一次")

    def test_xiaobai_api2(self):
        print("执行接口测试")
        assert '实际返回值' != '预期值'

# if __name__=="__main__":
#     pytest.main(["-s", "test_xiaobai_api_v1.py"])
    # pytest --html=report.html --self-contained-html