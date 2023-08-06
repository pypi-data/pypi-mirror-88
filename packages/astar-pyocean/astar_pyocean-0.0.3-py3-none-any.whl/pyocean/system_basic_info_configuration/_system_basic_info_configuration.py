#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _system_basic_info_configuration .py
# @time: 2020/6/18 21:59
# @Software: PyCharm
from pyocean.base import BaseClient
import requests
import logging


class SystemBasicInfoConfiguration(BaseClient):
    def __init__(self, url):
        super(self, SystemBasicInfoConfiguration).__init__(url)
        self.createCnfInfURL = self.url + 'createCnfInf'
        self.createFtpUserURL = self.url + 'createFtpUser'
        self.queryCnfInfURL = self.url + 'queryCnfInf'
        self.queryMsgInfURL = self.url + 'queryMsgInf'
        self.rightFtpUserURL = self.url + 'rightFtpUser'

    def createCnfInf(self, cnfName, cnfCode, cnfKindcode, cnfValue, remark):
        """说明:变量配置添加 -根据传入参数创建配置信息。
        参数:cnfName - 必填 配置名称cnfCode - 必填 配置CodecnfKindcode - 必填 配置父节点CodecnfValue - 必填 配置值remark - 必填 描述返回:
        code-0：调用接口成功，1：调用接口失败
        cnfInfId-创建的配置信息Id
        msg-提示信息另请参阅:
        输入参数实例： { "cnfName":"虚拟系统权限", "cnfCode":"Vam", "cnfKindcode":"PidCode", "cnfValue":"PidCode", "remark":"true" }
        响应结果实例： { "code": "0", "cnfInfId": "2", "msg": "添加配置信息成功！" }"""
        data = {
            'cnfName': cnfName,
            'cnfCode': cnfCode,
            'cnfKindcode': cnfKindcode,
            'cnfValue': cnfValue,
            'remark': remark
        }
        response = requests.post(self.createCnfInfURL, json=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        if responseVal == "0":
            logging.info("归档任务创建成功")
        else:
            logging.info("归档任务创建失败")
        return result

    def createFtpUser(self, loginName, password, username):
        """说明:FTP用户创建-根据传入参数创建FTP用户信息。
        参数:loginName - 必填 系统用户登录名称password - 必填 密码username - 必填 用户名称返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "loginName":"test", "password":"test", "username":"MrLiu" }
        响应结果实例： { "code": "0", "msg": "ftp用户创建成功！" }"""
        data = {
            'loginName': loginName,
            'password': password,
            'username': username
        }
        response = requests.post(self.createFtpUserURL, json=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        if responseVal == "0":
            logging.info("归档任务创建成功")
        else:
            logging.info("归档任务创建失败")
        return result

    def queryCnfInf(self, cnfId):
        """说明:变量配置查询-根据配置Id查询系统变量
        参数:cnfId - 必填 配置信息ID返回:
        code-0：调用接口成功,1：调用接口失败
        msg-提示信息
        cnfId-配置Id
        cnfName-配置名称
        cnfCode-配置Code
        cnfKindcode-父节点code
        cnfValue-配置值
        remark-描述
        creatTime-创建时间另请参阅:
        输入参数实例： { "cnfId":"2" }
        响应结果实例： { "code": "0", "msg": "添加配置信息成功！", "cnfId":"2", "cnfName":"虚拟系统权限", "cnfCode":"Vam", "cnfKindcode":PidCode, "cnfValue":"PidCode", "remark":"true", "creatTime":"2012-01-12" }"""
        data = {
            'cnfId': cnfId,
        }
        response = requests.post(self.queryCnfInfURL, json=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        if responseVal == "0":
            logging.info("归档任务创建成功")
        else:
            logging.info("归档任务创建失败")
        return result

    def queryMsgInf(self, loginName):
        """说明:站内信信息查询-此接口是站内消息查询使用
        参数:loginName - 必填 系统用登录名称返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        msgInf-消息列表（数组）
        数组对象说明：
        msgId-消息ID
        msgTitle-消息标题
        msgContext-消息内容另请参阅:
        输入参数实例： { "loginName":"test" }
        响应结果实例： { "code": "0", "msg": "消息获取成功", "msgInf": [{ "msgId": "1", "msgTitle": "[EN9018]创建ISO异常", "msgContext": "创建ISO异常" }] }"""
        data = {
            'loginName': loginName,
        }
        response = requests.post(self.queryMsgInfURL, json=data)
        result = response.json()
        responseVal = result.get('code')
        # 返回code：0
        # 代表成功，1: 代表异常
        return result

    def rightFtpUser(self, canCreate, canDelete, canWrite, canRead, filePath, poolId, loginName):
        """说明:FTP用户授权-此接口是针对文件系统用户进行可读写权限的授权 。
        参数:canCreate - 必填 是否可创建 1：是 0：否canDelete - 必填 是否可删除 1：是 0：否canWrite - 必填 是否可写 1：是 0：否canRead - 必填 是否可读可下载 1：是 0：否filePath - 必填 需要授权的目录 说明：以卷池code开始的目录路径poolId - 必填 卷池IdloginName - 必填 ftp用户登录名称返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "canCreate":"1", "canDelete":"1", "canWrite":"1", "canRead":"1", "filePath":"/test", "poolId":"1", "loginName":"test" }
        响应结果实例： { "code": "0", "msg": "ftp用户授权成功！" }"""
        data = {
            "canCreate": canCreate,
            "canDelete": canDelete,
            "canWrite": canWrite,
            "canRead": canRead,
            "filePath": filePath,
            "poolId": poolId,
            "loginName": loginName
        }
        try:
            response = requests.post(self.rightFtpUserURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()
