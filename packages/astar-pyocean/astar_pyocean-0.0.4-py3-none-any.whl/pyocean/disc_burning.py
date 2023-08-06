#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: disc_burning .py
# @time: 2020/6/12 20:51
# @Software: PyCharm

import logging as log
import requests
from enum import Enum


class QueryCopiesTaskState(Enum):
    success = -2  # 归档任务执行成功
    loading = 3  # 归档任务运行中
    error = 4  # 归档任务异常/失败
    hang_up = 5  # 归档任务挂起


class Client():
    pass


class DefaultClientConfig():
    pass


class OpticalLibraryBurn(object):
    """
    数据刻录
    """

    def __init__(self):
        self.REST_CONNECT_URL = "http://10.18.16.9:8080/oss/rest/restServer"
        # c = Client.create(DefaultClientConfig())
        # r = c.resource(REST_CONNECT_URL)
        # pass

    def fileCopy(self):
        # TODO: 文件推送实现
        pass

    def mkdir(self, path, loginName):
        """
        参数
        path：文件路径 (是以卷池code开始的相对路径) 必填 备注:文件名称的长度不超过（255）
        loginName：用户名称  必填
        {'path':'/oda9/guangzhou11','loginName':'test'}
        返回:
        { "code": "0", "msg": "文件夹创建成功" }
        :return:
        """
        url = self.REST_CONNECT_URL + '/mkdir'
        data = {'path': path, 'loginName': loginName}
        response = requests.post(url, data=data)
        result = response.json()
        responseVal = result.get("code")
        # 返回code：0
        # 代表成功，1: 代表异常
        log.info(result.get('msg'))
        return responseVal

    def creatArcTask(self, loginName, path):
        """
          发起归档任务
          注释：系统会根据卷池的配置，对发起归档的数据进行策略刻录）备注：例如卷池配置强制刻录周期为0，也就是只有数据发起归档，系统就会自动刻录数据，如果
          	  强制刻录周期为7，那么系统会根据是否满盘，或者是否到达了强制刻录周期来发起刻录任务
          参数
          path:文件路径 (是以卷池code开始的相对路径) 必填
          loginName：用户名  用户登录名称 必填
          { "loginName": "test", "path": "/test/present" }
         	返回：
         	{ "code": "0", "msg": "创建归档任务成功！" }
        }"""
        url = self.REST_CONNECT_URL + '/creatArcTask'
        data = {'path': path, 'loginName': loginName}
        response = requests.post(url, data=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        if responseVal == "0":
            log.info("归档任务创建成功")
        else:
            log.info("归档任务创建失败")
        return responseVal

    def queryCopiesTaskState(self, loginName, relativePath):
        """
        归档任务查询
        参数
        relativePath:文件路径 (是以卷池code开始的相对路径) 必填
        loginName：用户名  用户登录名称 必填
        { 'loginName': 'test', 'relativePath':'/test/present' }
        返回：
        state-2：归档任务执行成功 3：归档任务运行中 4：归档任务异常/失败 5：归档任务挂起
        { "code": "0", "state":"2", "msg": "归档任务执行成功!" }
        """
        # TODO 查一下到底接口是什么
        url = self.REST_CONNECT_URL + '/queryCopiesTaskState'
        data = {'relativePath': relativePath, 'loginName': loginName}
        # data = {'loginName': 'test', 'c': '/oda9/AAA'}
        response = requests.post(url, data=data)
        result = response.json()
        log.info(result.get('msg'))
        return result.get('state')

    def queryDiscByFileId(self, path):
        """
        存储任务执行成功，查询分盘结果
        根据路径查询所刻录的光盘卷标
        参数：
        path ：以卷池code开始相对路径 必填
        {"path":"/Pool001/poolBurn001"}
        返回结果：
        discLabel:光盘卷标
        slotName：抽片名称 例如 722A91_10 "_"前是盘匣的rfid，"_"后表示再盘匣中位置 ，如果任务没有刻录成功，slotName为空值
        burnCopies：刻录份数标识
        { "code": "0", "msg": "查询成功！", "discs": [{ "discLabel": "100033_100042_23", "slotName": "722A91_10", "burnCopies": 1 }, { "discLabel": "100033_100042_23", "slotName": "722A91_11", "burnCopies": 2 }] }
        """
        url = self.REST_CONNECT_URL + '/queryDiscByFileId'
        data = {'path': path}
        response = requests.post(url, data=data)
        result = response.json()
        log.info(response)
        return result.get('discs')

    def queryBurnPrintTaskState(self, discLabel):
        """
        查询，discLabel对应刻录任务的执行状态
        参数：
        discLabel：光盘卷标    必填 备注：发送刻录打印任务，参数discLabel的值
        {'discLabel':'2019-07-01'}
        返回：
        part-刻录光盘部分（针对于数据刻录超盘的部分说明，每个部分为一个数组）
        code-0：调用接口成功，1：调用接口失败
        state-1，任务等待 2，任务完成 3，任务执行中 4，任务异常 5，资源离线等待 6，任务未开启
        isoProcess-镜像制作任务进程（数组，仅存在于镜像刻录模式）
        burnProcess-刻录任务进程（数组，可包含多个刻录任务）
        数组2对象说明:
        burnPart/printPart-任务标识，'刻录任务ID'+'任务类型'
        state-任务状态 1:任务等待,2:任务完成,3:任务执行中,4:任务异常,5:任务资源离线等待
        msg-提示信息
        burnProcess-如果是正在刻录中，则显示刻录进度（单位：%）
        追加刻录：[{"part":"第1份","discLabel":"20190612541","code":"0","state":"3","msg":"任务执行中",
        "burnProcess":[{"burnPart":"37：刻录任务","state":"3","msg":"数据刻录中"}]},
        {"part":"第2份","discLabel":"20190612541","code":"0","state":"3","msg":"任务执行中",
        "burnProcess":[{"burnPart":"37：刻录任务","state":"3","msg":"数据刻录中"}]}]
         """
        url = self.REST_CONNECT_URL + '/queryDiscByFileId'
        data = {'discLabel': discLabel}
        response = requests.post(url, data=data)
        result = response.json()
        log.info(response)
        return result
