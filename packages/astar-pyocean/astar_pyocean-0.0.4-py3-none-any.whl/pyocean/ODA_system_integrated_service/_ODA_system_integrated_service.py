#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _ODA_system_integrated_service .py
# @time: 2020/6/18 22:14
# @Software: PyCharm
from pyocean.base import BaseClient
import requests
import logging


class ODASystemIntegratedService(BaseClient):
    def __init__(self, url):
        super(ODASystemIntegratedService, self).__init__(url)
        self.createBurnPrintTaskURL = self.url + 'createBurnPrintTask'
        self.createBurnPrintTaskByImgURL = self.url + 'createBurnPrintTaskByImg'
        self.createErrorCleanTaskURL = self.url + 'createErrorCleanTask'
        self.createSnyTimeCopiesTaskURL = self.url + 'createSnyTimeCopiesTask'
        self.queryBurnPrintTaskStateURL = self.url + 'queryBurnPrintTaskState'
        self.queryCleanTaskStateURL = self.url + 'queryCleanTaskState'
        self.queryModelURL = self.url + 'queryModel'
        self.stopSnyTimeCopiesTaskURL = self.url + 'stopSnyTimeCopiesTask'

    def createBurnPrintTask(self, burnType, discLabel, imgmodCode, filePath, fileType, burnNum, labList, loginName):
        """说明:刻录打印-根据指定输入参数创建刻录打印任务。
        参数:burnType - 必填 刻录打印类型 1：刻录 2：刻录打印 3：打印filePath - 必填 需要刻录的数据路径以卷池code开始的相对路径fileType - 必填 刻录类型 ， disc：虚拟光盘刻录打印；file：数据目录刻录打印loginName - 必填 用户登录名discLabel - 必填（卷边规则：只能是数字，中英文，_-,而且开头不能以_-开始，长度校验在255字符以内） 光盘卷标burnNum - 必填 刻录份数labList - 标签（@前是标签code，后是自定义的内容，多个自定义标签中间逗号隔开）imgmodCode - 必填 模板code返回:
        code-0:调用接口成功，1:调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { 'burnType': '2', 'discLabel': '20178121', 'imgmodCode': 'CTmodel', 'filePath': 'test/client', 'fileType': 'disc', 'burnNum': '1', 'labList': 'name@sjdfk,date@sdfasdf', 'loginName': 'test' }
        响应结果实例： { "code": "0", "msg": "刻录打印任务发布成功！" }"""
        data = {
            'burnType': burnType,
            'discLabel': discLabel,
            'imgmodCode': imgmodCode,
            'filePath': filePath,
            'fileType': fileType,
            'burnNum': burnNum,
            'labList': labList,
            'loginName': loginName
        }
        try:
            response = requests.post(self.createBurnPrintTaskURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def createErrorCleanTask(self, discLabel, cleanMode):
        """说明:刻录打印-根据指定输入参数创建异常任务清理数据任务。
        参数:discLabel - 必填 cleanMode - 必填 0 清理文件 1、清理文件和记录 返回:
        code-0:调用接口成功，1:调用接口失败
        tasks-任务集合，数组
        msg-提示信息另请参阅:
        输入参数实例： { 'discLabel': '20178121', 'cleanMode': '1' }
        响应结果实例： { "tasks":[1,2,3] , "code": "0", "msg": "清理任务创建成功！" }"""
        data = {
            'cleanMode': cleanMode,
            'discLabel': discLabel,
        }
        try:
            response = requests.post(self.createErrorCleanTaskURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryCleanTaskState(self, taskId):
        """说明:刻录打印任务查询-根据光盘卷标查询刻录打印任务状态。
        参数:taskId - 任务Id返回:
        code-0：调用接口成功，1：调用接口失败
        state-1，任务等待 2，任务完成 3，任务执行中 4，任务异常 5，任务准备中
        输入参数实例： { 'taskId': '102' }
        响应结果实例： """
        data = {'taskId': taskId}
        try:
            response = requests.post(self.queryCleanTaskStateURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def createBurnPrintTaskByImg(self, discLabel):
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
        data = {'discLabel': discLabel}
        try:
            response = requests.post(self.queryCleanTaskStateURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def createSnyTimeCopiesTask(self, discLabel, filePath, imgPath, burnOrPrint, burnNum, loginName):
        """说明:指定图片刻录打印-根据给定输入参数创建图片刻录打印任务。
        参数:burnOrPrint - 必填 刻录打印类型 1：刻录 2：打印 3：刻录打印filePath - 必填 需要刻录的数据路径以卷池code开始的相对路径loginName - 必填 用户登录名discLabel - 必填（卷边规则：只能是数字，中英文，_-,而且开头不能以_-开始，长度校验在255字符以内） 光盘卷标burnNum - 必填 刻录份数imgPath - 必填 模板图片返回:
        code-0：调用接口成功 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { 'discLabel': '20178121', 'filePath': 'test/client', 'imgPath': 'D:/test/client/1.jpg', "burnOrPrint":"1", 'burnNum': '1', 'loginName': 'test' }
        响应结果实例： { "code": "0", "msg": "刻录打印任务发布成功！" }"""
        data = {
            'discLabel': discLabel,
            'filePath': filePath,
            'imgPath': imgPath,
            'burnOrPrint': burnOrPrint,
            'burnNum': burnNum,
            'loginName': loginName
        }
        try:
            response = requests.post(self.createSnyTimeCopiesTaskURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryBurnPrintTaskState(self, discLabel, filePath, imgPath, burnOrPrint, burnNum, loginName):
        """说明:指定图片刻录打印-根据给定输入参数创建图片刻录打印任务。
        参数:burnOrPrint - 必填 刻录打印类型 1：刻录 2：打印 3：刻录打印filePath - 必填 需要刻录的数据路径以卷池code开始的相对路径loginName - 必填 用户登录名discLabel - 必填（卷边规则：只能是数字，中英文，_-,而且开头不能以_-开始，长度校验在255字符以内） 光盘卷标burnNum - 必填 刻录份数imgPath - 必填 模板图片返回:
        code-0：调用接口成功 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { 'discLabel': '20178121', 'filePath': 'test/client', 'imgPath': 'D:/test/client/1.jpg', "burnOrPrint":"1", 'burnNum': '1', 'loginName': 'test' }
        响应结果实例： { "code": "0", "msg": "刻录打印任务发布成功！" }"""
        data = {
            'discLabel': discLabel,
            'filePath': filePath,
            'imgPath': imgPath,
            "burnOrPrint": burnOrPrint,
            'burnNum': burnNum,
            'loginName': loginName
        }
        try:
            response = requests.post(self.queryModelURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryModel(self):
        """查询所有的打印模板信息
        参数:无需输入参数 - 返回:
        code-0：调用接口成功，1：调用接口失败
        modeinfos-所有模板信息（数组）
        msg-提示信息
        modeinfos数组对象说明：
        imgmodId-模板Id
        imgmodName-模板名称
        labInfo-标签信息这里只查需要注入的标签信息（数组）
        labInfo数组对象说明：
        labdefId-标签id
        labdefName-标签名称另请参阅:
        输入参数实例：
        无
         响应结果实例： { "code": "0", "modeinfos": [{ "imgmodId": 6, "imgmodName": "yimeng", "labInfo": [{ "labdefId": 7, "labdefName": "受审人" }, { "labdefId": 8, "labdefName": "案件标识" }, { "labdefId": 9, "labdefName": "案件时间" }, { "imgmodId": 7, "imgmodName": "中威科技", "labInfo": [{ "labdefId": 7, "labdefName": "标题" }, { "labdefId": 8, "labdefName": "场景" }, { "labdefId": 9, "labdefName": "拍摄时间" }] "msg": "查询打印模板成功" }"""
        try:
            response = requests.post(self.queryModelURL)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def stopSnyTimeCopiesTask(self, poolCode, imgmodCode, labList, filePath, discLabel, loginName, burnNum):
        """说明:实时刻录-根据指定参数创建实时刻录打印任务，此接口不支持同一个目录多次发起实时刻录任务。
        参数:poolCode - 必填 卷池codeimgmodCode - 必填 打印模板codefilePath - 必填 需要刻录的数据路径以卷池code开始的相对路径（需要放数据的目录（此参数不传，系统会按照时间戳自动创建目录））格式：/卷池路径/时间戳 自动默认时间戳这一层就是要监控的实时刻录目录loginName - 必填 用户登录名discLabel - 必填（卷边规则：只能是数字，中英文，_-,而且开头不能以_-开始，长度校验在255字符以内） 光盘的标签burnNum - 必填 刻录打印份数labList - 必填 需要注入的标签 数组，数组参数解释(标签名称:对应的需要注入的文字（自定义）) 参数是标签code@自定义内容】组成，多个中间用逗号隔开返回:
        code-0：调用接口成功 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { 'poolCode': 'test', 'imgmodCode': 'starderedModel', 'labList': 'name@sjdfk,date@sdfasdf,person@ertt', 'filePath': 'test/jjwgx', 'discLabel': '2017-05-12', 'loginName': 'test', 'burnNum': '1' }
        响应结果实例： { "code": "0", "msg": "实时刻录任务发布成功！" }"""
        data = {
            'poolCode': poolCode,
            'imgmodCode': imgmodCode,
            'labList': labList,
            'filePath': filePath,
            'discLabel': discLabel,
            'loginName': loginName,
            'burnNum': burnNum
        }
        try:
            response = requests.post(self.stopSnyTimeCopiesTaskURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()
