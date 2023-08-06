#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _file_system_operate .py
# @time: 2020/6/19 0:48
# @Software: PyCharm
import requests
import logging
from pyocean.base import BaseClient


class FileSystemOperate(BaseClient):
    def __init__(self, url):
        super(FileSystemOperate, self).__init__(url)
        self.deleteDirURL = self.url + 'deleteDir'
        self.fileMoveURL = self.url + 'fileMove'
        self.mkdirURL = self.url + 'mkdir'
        self.queryDiscByFileIdURL = self.url + 'queryDiscByFileId'
        self.queryDiscFileInfoURL = self.url + 'queryDiscFileInfo'
        self.queryFileInfoURL = self.url + 'queryFileInfo'

    def deleteDir(self, loginName, filepath):
        """说明:删除文件-删除卷池目录下得文件或文件夹 。
        参数:longinName - 必填 虚拟文件系统用户登录名filepath - 必填 文件路径或文件夹路径 说明：以卷池code开始的相对路径返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "loginName": "test", "filepath":"/test/present" }
        响应结果实例： { "code": "0", "msg": "删除成功！" }"""
        data = {"loginName": loginName, "filepath": filepath}
        try:
            req = requests.post(self.deleteDirURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def fileMove(self, loginName, path):
        """说明:文件移动-卷池内的文件移动（暂时不支持跨卷池移动文件） 。
        参数:longinName - 必填 虚拟文件系统用户登录名path - 必填 源目录 说明：以卷池code开始的相对路径target_path - 必填 目标目录 说明：以卷池code开始的相对路径返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "loginName": "test", "path": "/test/present", "target_path": "/test/branch" }
        响应结果实例： { "code": "0", "msg": "移动成功！" }"""
        data = {"loginName": loginName, "path": path}
        try:
            req = requests.post(self.deleteDirURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def mkdir(self, loginName, path):
        """
        参数
        path：文件路径 (是以卷池code开始的相对路径) 必填 备注:文件名称的长度不超过（255）
        loginName：用户名称  必填
        {'path':'oda9/guangzhou11','loginName':'test'}
        返回:
        { "code": "0", "msg": "文件夹创建成功" }
        :return:
        """
        data = {'path': path, 'loginName': loginName}
        try:
            response = requests.post(self.mkdirURL, json=data)
            result = response.json()
            responseVal = result.get("code")
            # 返回code：0
            # 代表成功，1: 代表异常
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryDiscByFileId(self, path):
        """说明:获取文件夹所在的光盘卷标-根据给定的文件路径查询所在的已刻录的光盘卷标
        参数:path - 必填 //以卷池code开始的相对路径 文件夹路径返回:
        code-0,调用接口成功, 1,调用接口失败
        msg-提示信息
        discs-光盘信息数组
        数组对象说明：
        slotName-抽片名称
        discLabel-光盘卷标
        burnCopies-刻录份数标识 （上述响应实例中参数解释 第一份刻录在了 722A91_10光盘上,第二份刻录在了722A91_11）另请参阅:
        输入参数实例： { "path": '存储卷池/test' }
        响应结果实例： { "code": "0", "msg": "查询成功！", "discs": [{ "discLabel": "100033_100042_23", "slotName": "722A91_10", "burnCopies": 1 }, { "discLabel": "100033_100042_23", "slotName": "722A91_11", "burnCopies": 2 },] }"""
        data = {'path': path}
        try:
            response = requests.post(self.queryDiscByFileIdURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryDiscFileInfo(self, baLabel, pageCurrent, pageSize):
        """说明:获取指定光盘中的文件信息-根据给定参数获取指定光盘中的文件信息，分页方式展示。
        参数:baLabel - 必填 卷标pageCurrent - 必填 当前页码pageSize - 必填 页大小返回:
        code-0,调用接口成功, 1,调用接口失败
        msg-提示信息
        totalCount-总记录数
        dataFileList-文件信息列表（数组）
        数组对象说明：
        id-文件Id
        poolId-卷池Id
        discId-光盘Id
        name-文件名
        fileSize-文件大小（单位：B|字节）
        filePath-文件路径
        fileType-文件类型 0：文件，1：文件夹
        fileState-文件状态 0：在线，1：在线+近线，2：近线，3：近线+离线，4：在线+近线+离线，5：在线+离线，6：离线另请参阅:
        输入参数实例： { "baLabel": "20180504-17", "pageCurrent": "1", "pageSize": "2" }
        响应结果实例： { "code": "0", "msg": "信息查询成功", "totalCount": "20", dataFileList:[ {"id": "1", "poolId": "12", "discId": "3", "name": "test", "fileSize": "1024", "filePath": "/存储卷池/test.zip", "fileType": "0", "fileState": "2" }, {"id": "1", "poolId": "12", "discId": "3", "name": "test", "fileSize": "785464", "filePath": "/存储卷池/jdklinux1.7.97.tar", "fileType": "0", "fileState": "2"} ] }"""
        data = {'baLabel': baLabel, 'pageCurrent': pageCurrent, 'pageSize': pageSize}
        try:
            response = requests.post(self.queryDiscFileURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryFileInfo(self, filePath):
        """说明:获取文件信息-根据指定文件路径获取该文件的详细信息 。
        参数:filePath - 必填 文件路径 说明：以卷池code开始的相对路径返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息
        fileId-文件Id
        filePath-文件路径
        fileName-文件名称
        fileState-文件状态 0：在线，1：在线近线，2：近线，3：近线离线，4：在线近线离线，5：在线离线，6：离线
        fileType-文件类型 0：文件，1：文件夹
        fileSize-文件大小（单位：B|字节）另请参阅:
        输入参数实例： { "filePath": "/存储卷池/test.zip" }
        响应结果实例： { "code ": "0", "msg ": "获取文件信息成功", "fileId ": "23", "filePath ": "/存储卷池/test.zip", "fileName ": "test", "fileState ": "1", "fileType ": "0", "fileSize ": "256" }"""
        data = {'filePath': filePath}
        try:
            response = requests.post(self.queryFileInfoURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()
