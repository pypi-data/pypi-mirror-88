#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: gate_rest_api .py
# @time: 2020/7/13 1:19
# @Software: PyCharm

from pyocean.base import BaseClient
import requests
from datetime import datetime

class GateRestAPI(BaseClient):
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(url)
        self.queryDevInfoURL = self.url + 'queryDevInfo'
        self.createArcTaskURL = self.url + 'createArcTask'
        self.queryArcTaskStateURL = self.url + 'queryArcTaskState'
        self.queryFerreyFilesURL = self.url + 'queryFerreyFiles'
        self.createCleanFileTaskURL = self.url + 'createCleanFileTask'
        self.queryChildFileURL = self.url + 'queryChildFile'

    def queryDevInfo(self, devName):
        """说明：设备基础信息查询 - 根据设备名称查询设备基础信息，比如设备的IP，端口 ，总容量以及可用容量、光盘总数量和可用数量等。
        参数:
        devName - 必填
        设备名称
        返回:
        code - 0：调用接口成功, 1：调用接口失败
        driveCount - 光驱数量
        devId - 设备Id
        devIp - 设备Ip
        devPort - 设备端口
        nodeId - 节点Id
        binNum - 盘桶的数量
        canUseDiscCount - 可用的光盘数量
        msg - 提示信息
        另请参阅:
        输入参数实例： {'devName': 'odd400'}
        响应结果实例： {"driveCount": 4, "devName": "odd400", "devId": 1, "devIp": "10.18.16.240", "devPort": 3260, "nodeId": 1,
                 "binNum": 2, "canUseDiscCount": 13, "code": "0", "msg": "设备信息获取成功！"}
        """
        data = {"devName": devName}
        try:
            req = requests.post(self.queryDevInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def createArcTask(self, path, ferryLevel):
        """
        说明: 创建摆渡任务 - 根据路径创建摆渡任务（目前不支持同一文件或文件夹多次摆渡）。
        参数:
        path - 必填
        摆渡路径，以卷池code开始的相对路径
        ferryLevel - 必填
        摆渡优先级
        1 - 10
        之内的数字
        返回:
        code - 0：调用接口成功, 1：调用接口失败
        msg - 提示信息
        另请参阅:
        输入参数实例： {"path": "/test/present", "ferryLevel": "1"}
        响应结果实例： {"code": "0", "msg": "创建摆渡任务成功！"}
        """
        data = {"path": path, "ferryLevel": ferryLevel}
        try:
            req = requests.post(self.createArcTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryArcTaskState(self, path):
        """
        说明: 摆渡任务查询 - 对发起的摆渡任务进行查询。--外网接口查询
        参数:
        path - 必填
        发起摆渡的路径
        返回:
        code - 0：调用接口成功, 1：调用接口失败
        state：-3
        摆渡光盘资源等待，0 等待，1 运行中 3 任务异常 4
        待审批 5        审批通过 6         病毒文件拦截 7         敏感词拦截 8         任务销毁 9         等待摆渡 10         摆渡中 11         摆渡完成 12         摆渡异常 13         审批拒绝         msg - 提示信息
        另请参阅:
        输入参数实例： {'path': 'test/present'}
        响应结果实例： {"code": "0", "state": "1", "msg": "任务运行中!"}
        """
        data = {"path": path}
        try:
            req = requests.post(self.createArcTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryFerreyFiles(self, startTime, endTime=None):
        """
        说明: 查询时间内摆渡完成文件信息 - 内网信息查询
        参数:
        startTime - 必填
        开始时间
        endTime - 非必填
        不填按照当前时间作为结束时间
        结束时间
        返回:
        code - 0：调用接口成功, 1：调用接口失败
        fileList 摆渡成功的文件列表
        fileName 文件名称
        filePath 文件路径
        fileSize 文件大小
        fileType 文件类型
        ferrySucessTime 任务成功时间
        msg - 提示信息
        另请参阅:
        输入参数实例： {'startTime': '2020-05-12 15:30:21', 'endTime': '2020-05-12 18:30:54'}
        响应结果实例： {"fileList": [
            {"fileName": "中国1234.zip", "filePath": "/jie/中国1234.zip", "fileSize": "1640250196", "fileType": "0",
             "ferrySucessTime": "2020-05-20 14:30:29"},
            {"fileName": "gate_om.war", "filePath": "/wang/gate_om.war", "fileSize": "258211207", "fileType": "0",
             "ferrySucessTime": "2020-05-20 14:31:57"},
            {"fileName": "gate_inner.tar.gz", "filePath": "/wang/gate_inner.tar.gz", "fileSize": "590768561",
             "fileType": "0", "ferrySucessTime": "2020-05-21 10:04:49"}], "code": "0", "msg": "摆渡完成文件信息获取成功!"}
        """
        if isinstance(startTime, datetime):
            startTime = startTime.strftime("yyyy-mm-dd HH:MM:ss")
        if endTime:
            if isinstance(endTime, datetime):
                endTime = endTime.strftime("yyyy-mm-dd HH:MM:ss")
            data = {"startTime": startTime, 'endTime': endTime}
        else:
            data = {"startTime": startTime}
        try:
            req = requests.post(self.queryFerreyFilesURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def createCleanFileTask(self, path):
        """说明: 针对文件发起清理 - 针对文件或者目录发起清理。--内网清理接口创建
        参数:
        path - 必填
        清理路径 ，以卷池code开始的相对路径
        返回:
        code - 0：调用接口成功, 1：调用接口失败
        taskId 任务Id 用于查询
        msg - 提示信息
        另请参阅:
        输入参数实例： {'path': 'test/present'}
        响应结果实例： {"code": "0", "taskId": "2", "msg": "清理任务创建成功!"}
        """

        data = {"path": path}
        try:
            req = requests.post(self.createCleanFileTaskURL, json=data)
            return req.json()['msg']
        except:
            raise ValueError()

    def queryCleanTaskState(self, taskId):
        """
        说明：清理任务查询 - 根据任务Id查询任务状态 。--内网清理接口查询
        参数:
        taskId - 必填
        任务Id
        返回:
        code - 0：调用接口成功，1：调用接口失败
        state - 任务状态
        0：任务等待，1、任务运行中2：任务完成，3：任务异常，
        msg - 提示信息
        另请参阅:
        输入参数实例： {"taskId": '409'}
        响应结果实例： {"code": "0", "state": 0, "msg": "任务等待"}
        """

        data = {"taskId": taskId}
        try:
            req = requests.post(self.createCleanFileTaskURL, json=data)
            return req.json()['msg']
        except:
            raise ValueError()

    def queryChildFile(self, path):
        """说明: 获取文件信息 - 根据指定文件路径获取该文件的详细信息 。--内网使用，用于查询文件夹下所有的子文件或者子目录信息
        参数:
        path - 必填
        文件路径
        说明：以卷池code开始的相对路径
        返回:
        code - 0：调用接口成功, 1：调用接口失败
        msg - 提示信息
        filePath - 文件路径
        fileName - 文件名称
        fileType - 文件类型
        0：文件，1：文件夹
        fileSize - 文件大小（单位：B | 字节）
        另请参阅:
        输入参数实例： {"path": "/存储卷池/test"}
        响应结果实例： {"code ": "0", "msg ": "获取文件信息成功", "filePath ": "/存储卷池/test.zip", "fileName ": "test", "fileType ": "0",
                 "fileSize ": "256"}
        """
        data = {"path": path}
        try:
            req = requests.post(self.queryChildFileURL, json=data)
            return req.json()['msg']
        except:
            raise ValueError()
