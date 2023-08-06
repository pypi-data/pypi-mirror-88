#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _gate_rest_api .py
# @time: 2020/9/16 1:58
# @Software: PyCharm

import pytest
from astartool.project import std_logging
from pyocean.gate_rest_api import GateRestAPI
import configparser

cp = configparser.ConfigParser()
cp.read('test_config.ini', encoding='utf8')
url = cp.get('conf', 'url') + 'rest/gateServer'
username = cp.get('conf', 'username')
password = cp.get('conf', 'password')
dev_name = cp.get('conf', 'dev_name')
path = cp.get('conf', 'path')
api = GateRestAPI(url=url, username=username, password=password)

class TestGateRestAPI:

    @classmethod
    @std_logging()
    def setup_class(cls):
        pass

    @classmethod
    @std_logging()
    def teardown_class(cls):
        print('teardown_class()')

    @std_logging()
    def setup_method(self, method):
        pass

    @std_logging()
    def teardown_method(self, method):
        pass

    def test_get_dev_info(self):
        res = api.queryDevInfo(dev_name)
        assert res['code'] == '0', res

    def test_create_clean_file_task(self):
        # todo task
        res = api.createCleanFileTask('409')
        assert res['code'] == '0', res

    def test_create_arc_task(self):
        res = api.createArcTask(path=path, ferryLevel='1')
        assert res['code'] == '0', res

    def test_query_child_file(self):
        res = api.queryChildFile(path=path)
        assert res['code'] == '0', res

    def test_query_ferry_file(self):
        res = api.queryFerreyFiles(startTime='2020-09-14 00:00:00')
        assert res['code'] == '0', res

    def test_query_arc_task_state(self):
        res = api.queryArcTaskState(path)
        assert res['code'] == '0', res

    def test_query_clean_task_state(self):
        # todo: TASK
        res = api.queryCleanTaskState('409')
        assert res['code'] == '0', res
