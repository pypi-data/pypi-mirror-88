#!usrbinenv python
# -*-  coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: disc_recording.py
# @time: 2020/6/12 20:52
# @Software: PyCharm


import logging as log
import requests
from enum import Enum


# log = logger.
class Client():
    pass


class DefaultClientConfig():
    pass


class QueryMoveBackTaskState(Enum):
    waiting = 0  # 等待
    sended = 1  # 已发送
    finished = 2  # 完成
    error = 3  # 异常
    offline_waiting = -2  # 资源离线等待


class CreateAccDataTask(Enum):
    successful = 1  # 创建回迁任务成功
    loading = 2  # 回迁文件正在下载中
    loaded = 3  # 回迁文件已经在线
    not_found = 4  # 回迁文件不存在


class OpricalLibraryAcc(object):
    def __init__(self):
        self.REST_CONNECT_URL = "http://10.18.16.9:8080/oss/rest/restServer"

    def createAccDataTask(self, path, loginName):
        """
        对指定文件进行调阅，利用
        输入参数：
        path:路径 (是以卷池code开始的相对路径)
        loginName:用户名
        {'path':'卷池Code_1广州','loginName':'yuan'}
        返回结果
        state:1：创建回迁任务成功，2：回迁文件正在下载中，3：回迁文件已经在线，4： 回迁文件不存在
        响应结果实例： { "filePath": "存储卷池test.zip", "taskId ": "12", "code": "0", "msg": "回迁任务创建成功", "state": "1" }
         
         """
        url = self.REST_CONNECT_URL + '/createAccDataTask'
        data = {'path': path, 'loginName': loginName}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            responseVal = result.get("code")
            # 返回code：0代表成功，1:代表失败
            if responseVal == "0":
                log.info("回迁任务创建成功")
            else:
                log.info("回迁任务创建失败")
            return result.get('filePath'), result.get('taskId'), result.get('state')
        else:
            log.info("网络连接问题，回迁任务创建失败")
            return None, None

    def queryMoveBackTaskState(self, taskId):
        """
        查询会签任务执行情况
        参数：
        taskId:任务Id 必填
        返回
        state:0：等待，1：已发送 2：完成，3：异常 -2、资源离线等待
        响应结果实例： { "state": "-2", "code": "0", "msg": "资源离线等待" }
        """
        url = self.REST_CONNECT_URL + '/queryMoveBackTaskState'
        data = {'taskId': taskId}
        response = requests.post(url, data=data)
        result = response.json()
        log.info(result.get('msg'))
        return result.get('state')
