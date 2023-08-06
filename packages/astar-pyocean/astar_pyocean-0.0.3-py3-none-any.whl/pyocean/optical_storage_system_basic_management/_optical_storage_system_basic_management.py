#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _optical_storage_system_basic_management .py
# @time: 2020/6/19 0:51
# @Software: PyCharm
from pyocean.base import BaseClient
import requests
import logging


class OpticalStorageSystemBasicManagement(BaseClient):
    def __init__(self, url):
        super(self, OpticalStorageSystemBasicManagement).__init__(url)
        self.creatArcTaskURL = self.url + 'creatArcTask'
        self.createAccDataTaskURL = self.url + 'createAccDataTask'
        self.createDiscReBurnTaskURL = self.url + 'createDiscReBurnTask'
        self.queryBurnPrintTaskStateURL = self.url + 'queryBurnPrintTaskState'
        self.queryCopiesTaskStateURL = self.url + 'queryCopiesTaskState'
        self.queryMoveBackTaskStateURL = self.url + 'queryMoveBackTaskState'

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
        data = {'path': path, 'loginName': loginName}
        response = requests.post(self.creatArcTaskURL, json=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        if responseVal == "0":
            logging.info("归档任务创建成功")
        else:
            logging.info("归档任务创建失败")
        return result

    def createAccDataTask(self, loginName, path):
        """说明:调阅任务创建-对已经刻录的文件或者文件夹发起调阅任务。
        参数:path - 必填 文件或文件夹路径（基于卷池Code开始的文件路径）loginName - 必填 用户名返回:
        filePath-文件或文件夹
        fileId-文件或文件夹Id
        code-0：成功， 1：失败
        msg-提示信息
        state-调阅任务状态 1：创建回迁任务，2：回迁文件正在下载中，3：回迁文件已经在线，4： 回迁文件不存在另请参阅:
        输入参数实例： { "path": '/存储卷池/test.zip', "loginName": "zdd" }
        响应结果实例： { "filePath": "/存储卷池/test.zip", "fileId ": "12", "code ": "0", "msg ": "回迁任务创建成功", "state ": "2" }"""
        data = {'path': path, 'loginName': loginName}
        response = requests.post(self.creatArcTaskURL, json=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        if responseVal == "0":
            logging.info("归档任务创建成功")
        else:
            logging.info("归档任务创建失败")
        return result

    def createDiscReBurnTask(self, discLable, slotName):
        """说明:单盘重刻-根据抽片名称和卷标重新创建刻录任务（人工重新组织数据放在原来的位置）。
        参数:discLable - 必填 光盘卷标slotName - 必填 抽片名称返回:
        taskId-单盘重刻任务Id
        code-0：表示成功， 1：表示失败
        msg-提示信息另请参阅:
        输入参数实例： { "discLable": "20180601-1", "slotName": "4964FB_1" }
        响应结果实例： { "taskId": "111", "code": "0", "msg": "刻录任务创建成功！" }"""
        data = {
            'discLable': discLable,
            'slotName': slotName,
        }
        try:
            response = requests.post(self.createDiscReBurnTaskURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryBurnPrintTaskState(self, discLabel):
        """说明:刻录打印任务查询-根据光盘卷标查询刻录打印任务状态。
        参数:discLabel - 必填 光盘卷标返回:
        数组1对象说明：
        part-刻录光盘部分（针对于数据刻录超盘的部分说明，每个部分为一个数组）
        code-0：调用接口成功，1：调用接口失败
        state-1，任务等待 2，任务完成 3，任务执行中 4，任务异常 5，资源离线等待 6，任务未开启
        isoProcess-镜像制作任务进程（数组，仅存在于镜像刻录模式）
        burnProcess-刻录任务进程（数组，可包含多个刻录任务）
        printProcess-打印任务进程（数据，可包含多个打印任务）
        数组2对象说明:
        burnPart/printPart-任务标识，'刻录任务ID'+'任务类型'
        state-任务状态 1:任务等待,2:任务完成,3:任务执行中,4:任务异常,5:任务资源离线等待
        msg-提示信息
        burnProcess-如果是正在刻录中，则显示刻录进度（单位：%）另请参阅:
        输入参数实例： { 'discLabel': 'jx02' }
        响应结果实例：
        追加刻录：[{"part":"第1份","discLabel":"20190612541","code":"0","state":"3","msg":"任务执行中", "burnProcess":[{"burnPart":"37：刻录任务","state":"3","msg":"数据刻录中"}], "printProcess":[{"printPart":"38:打印任务","state":"1","msg":"打印任务等待"}]}, {"part":"第2份","discLabel":"20190612541","code":"0","state":"3","msg":"任务执行中", "burnProcess":[{"burnPart":"37：刻录任务","state":"3","msg":"数据刻录中"}], "printProcess":[{"printPart":"38:打印任务","state":"1","msg":"打印任务等待"}]}]
        镜像刻录：[{"part":"第1份","discLabel":"2019068901","code":"0","state":"2","msg":"任务完成","isoProcess":[{"discLabel":"2019068901","code":"0","state":"2","msg":"ISO制作完成"}], "burnProcess":[{"burnPart":"22：刻录任务","state":"2","msg":"刻录任务完成"}],"printProcess":[{"printPart":"24:打印任务","state":"2","msg":"打印任务完成"}]}, {"part":"第2份","discLabel":"2019068901","code":"0","state":"2","msg":"任务完成","isoProcess":[{"discLabel":"2019068901","code":"0","state":"2","msg":"ISO制作完成"}], "burnProcess":[{"burnPart":"23：刻录任务","state":"2","msg":"刻录任务完成"}],"printProcess":[{"printPart":"25:打印任务","state":"2","msg":"打印任务完成"}]}] """
        data = {
            'discLabel': discLabel,
        }
        try:
            response = requests.post(self.queryBurnPrintTaskStateURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryCopiesTaskState(self, loginName, relativePath):
        """说明:文件归档任务查询-对发起的归档任务进行查询，获取文件的归档任务的状态。
        参数:longinName - 必填 虚拟文件系统用户登录名relativePath - 必填 归档路径 ，以卷池code开始的相对路径返回:
        code-0：调用接口成功, 1：调用接口失败
        state-2：归档任务执行成功 3：归档任务运行中 4：归档任务异常/失败 5：归档任务挂起
        msg-提示信息另请参阅:
        输入参数实例： { 'loginName': 'test', 'relativePath':'/test/present' }
        响应结果实例： { "code": "0", "state":"2", "msg": "归档任务执行成功!" }"""
        data = {
            'loginName': loginName,
            'relativePath': relativePath
        }
        try:
            response = requests.post(self.queryCopiesTaskStateURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryMoveBackTaskState(self, taskId):
        """说明:调阅任务查询-对发起的调阅任务查询状态。
        参数:taskId - 必填 任务Id返回:
        code-0：成功， 1：失败
        msg-提示信息
        taskId-任务Id
        state-调阅任务状态 0、等待，1、运行中，2、完成，3、异常，-2、资源离线等待另请参阅:
        输入参数实例： { "taskId":"944" }
        响应结果实例： { "code": "0", "msg": "任务查询成功！", "taskId": "944", "state": "0" }"""
        data = {
            'taskId': taskId,
        }
        try:
            response = requests.post(self.queryMoveBackTaskStateURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()
