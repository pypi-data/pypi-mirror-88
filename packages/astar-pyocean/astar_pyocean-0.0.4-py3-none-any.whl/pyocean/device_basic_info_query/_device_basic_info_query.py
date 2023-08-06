#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _device_basic_info_query .py
# @time: 2020/6/18 20:21
# @Software: PyCharm
import requests
from pyocean.base import BaseClient
from enum import Enum

__all__ = [
    'DeviceBasicInfoQuery'
]


class DoorState(Enum):
    """
    doorState - 设备门的状态
    1：准备门解锁，
    2：门解锁处理中，
    3：门解锁失败，
    4：门解锁成功，
    5：等待锁定，
    6：锁定处理中，
    7：加锁异常，
    8：门锁定成功(首次添加设备，激活设备这个状态是null，也代表门锁定成功)
    """
    # TODO
    READY = 1
    ON = 2
    FAIL = 3
    SUCCESSFUL = 4
    WAITING = 5


class DevState(Enum):
    """设备的状态
    0：激活，
    1：未激活，
    2：初始化，
    3：激活中，
    4：设备忙，
    5：同步失败，
    10：空闲，
    11：开门，
    12：设备重连，
    13：第一次添加，
    14：第一次运行
    """
    # TODO


class DevIsnear(Enum):
    """
    设备是否近线
    0：否，
    1：是
    """
    NO = 0
    YES = 1


class DeviceBasicInfoQuery(BaseClient):
    """
    设备基本信息查询
    """

    def __init__(self, url='http://localhost:8080/oss/rest/restServer/', username=None, password=None, *args, **kwargs):
        super(DeviceBasicInfoQuery, self).__init__(url=url, username=username, password=password)
        self.queryBindInfoURL = self.url + 'queryBindInfo'
        self.queryDevInfoURL = self.url + 'queryDevInfo'
        self.queryDevTypeURL = self.url + 'queryDevType'
        self.queryDrawInfoURL = self.url + 'queryDrawInfo'
        self.queryMagByDrawIdURL = self.url + 'queryMagByDrawId'
        self.queryMagDiscInfoURL = self.url + 'queryMagDiscInfo'
        self.queryMagInfoURL = self.url + 'queryMagInfo'
        self.queryOpticalDiscInfoURL = self.url + 'queryOpticalDiscInfo'
        self.querySlotInfoURL = self.url + 'querySlotInfo'
        self.queryDriverInfoURL = self.url + 'queryDriverInfo'
        self.queryPrintInfoURL = self.url + 'queryPrintInfo'
        self.session = requests.session()

    def queryBindInfo(self, devId):
        """说明：盘桶信息查询 -根据设备Id查询该设备下所有盘桶的基本信息。
        参数:devId - 必填 设备id返回:
        code-0,调用接口成功，1，调用接口失败
        msg-提示信息
        bindInfo-所有盘桶的信息（数组）
        数组对象说明：
        bindId-盘桶id
        binIndexInDevice-盘桶在设备中的位置
        discCount-光盘数量
        devId-设备Id
        binappType-盘桶类型 0：输入盘桶 1：输出盘桶 2：废盘桶
        phydiscType-盘桶光盘类型
        ed-是否禁用 0：启用，1：禁用另请参阅:
        输入参数实例： { 'devId': '1' }
        响应结果实例： { "code": "0", "msg": "获取盘桶对应信息成功", "bindInfo": [{ "bindId": 1, "devId": 1, "binIndexInDevice": 0, "discCount": 12, "binAppType": 0, "ed": 0, "phydiscType": "DVD+R$4.7G" }, { "bindId": 2, "devId": 1, "binIndexInDevice": 0, "discCount": 12, "binAppType": 1, "ed": 0, "phydiscType": "DVD+R$4.7G" }, { "bindId": 3, "devId": 1, "binIndexInDevice": 0, "discCount": 12, "binAppType": 2, "ed": 0, "phydiscType": "DVD+R$4.7G" }] }"""
        data = {'devId': devId}
        try:
            req = self.session.post(self.queryBindInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryDevInfo(self, devName):
        """
        说明：设备基础信息查询-根据设备名称查询设备基础信息，比如设备的IP，端口 ，总容量以及可用容量、光盘总数量和可用数量等。
        参数:devName - 必填 设备名称返回:
        结果一：光盘库设备：
        driveCount-设备的光驱数量
        devName-设备的名称
        devId-设备Id
        devIp-设备的Ip
        devPort-设备的端口
        nodeId-所属节点Id
        doorState-设备门的状态 1：准备门解锁，2：门解锁处理中，3：门解锁失败，4：门解锁成功，5：等待锁定，6：锁定处理中，7：加锁异常，8：门锁定成功(首次添加设备，激活设备这个状态是null，也代表门锁定成功)
        devState-设备的状态 0：激活，1：未激活，2：初始化，3：激活中，4：设备忙，5：同步失败，10：空闲，11：开门，12：设备重连，13：第一次添加，14：第一次运行
        devIsnear-设备是否近线 0：否，1：是
        devSize-总容量|可用容量
        devMagCount-盘匣个数（已满盘匣|未满盘匣）
        devDiscCount-光盘数量（已满光盘|空光盘）
        devActivateState-设备的激活状态 0：激活状态,1：未激活
        drawCount-抽屉数
        expnum-弹出屉的数量
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        结果二：ODA设备：
        driveCount-设备的光驱数量
        devName-设备的名称
        devId-设备Id
        devIp-设备的Ip
        devPort-设备的端口
        nodeId-所属节点Id
        doorState-设备门的状态 1：准备门解锁，2：门解锁处理中，3：门解锁失败，4：门解锁成功，5：等待锁定，6：锁定处理中，7：加锁异常，8：门锁定成功(首次添加设备，激活设备这个状态是null，也代表门锁定成功)
        devState-设备的状态 0：激活，1：未激活，2：初始化，3：激活中，4：设备忙，5：同步失败，10：空闲，11：开门，12：设备重连，13：第一次添加，14：第一次运行
        devIsnear-设备是否近线 0：否，1：是
        printCount-打印机的数量
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { 'devName': 'HMS 2105' }
        响应结果实例： { "driveCount": 2, "devName": "HMS 2105", "devId": 13, "devIp": "192.168.1.100", "devPort": 3260, "nodeId": 123, "doorState": 8, "devState": 10, "devIsnear": 1, "devSize": "208.28 GB|157.37 GB", "devMagCount": "0|3", "devDiscCount": "39|8", "devActivateState": 0, "drawCount": 1, "expnum": 1, "code": "0", "msg": "设备信息查询成功" }
        """
        data = {'devName': devName}
        try:
            req = self.session.post(self.queryDevInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryDevType(self):
        """\
        说明：设备类型信息查询-此接口主要查询所有设备类型。
        参数:此方法无需参数 - 返回:
        code-0：调用接口成功，1：调用接口失败
        devTypeInfos[]-设备类型信息 （数组）
        数组对象说明：
        id-设备类型ID
        devType-设备类型信息 1：光盘库 ，2：离线库 3：oda设备
        devTypeName-设备类型名称
        msg-提示信息另请参阅:
        输入参数实例： 无
        响应结果实例： { "code": "0", "devTypeInfos": [{ "id": 1, "devType": 1, "devTypeName": "HMS 1035" }], "msg": "设备类型信息查询成功" }
        """
        try:
            req = self.session.post(self.queryDevTypeURL)
            return req.json()
        except:
            raise ValueError()

    def queryDrawInfo(self, devId):
        """说明：抽屉信息查询 -根据设备Id查询该设备中所有的抽屉信息。
        参数:devId - 必填 设备Id返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        drawInfo-所有抽屉的信息（数组）
        数组对象说明：
        drawId-抽屉Id
        drawIndex-抽屉在设备中的位置
        devId-设备Id另请参阅:
        输入参数实例： { 'devId': '1' }
        响应结果实例： { "code": "0", "msg": "获取抽屉对应信息成功", "drawInfo": [{ "drawId": 1, "devId": 1, "drawIndex": 0, }, { "drawId": 2, "devId": 1, "drawIndex": 1, }, { "drawId": 3, "devId": 1, "drawIndex": 2, }] }"""
        data = {'devId': devId}
        try:
            req = self.session.post(self.queryDrawInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryDriverInfo(self, devId):
        """说明：光驱信息查询-根据设备Id查询该设备下所有光驱的详细信息。
        参数:devId - 必填 设备Id返回:
        code-0：调用接口成功，1：调用接口失败
        driveInfo-设备下所有驱动详细信息（数组）
        msg-提示信息
        数组对象说明：
        driId-光驱Id
        driveName-光驱名称
        driveIndexInDevice-光驱在设备中的位置
        ed-是否禁用 0：启用，1：禁用
        devId-设备Id
        drvRunState-光驱运行状态 0：设备禁用；1：启用；2：空闲无盘；3：空闲有盘；4：刻录；5：读取；6：扫描;7:校验；8：系统禁用
        driveUsageCount-光驱的使用次数
        readCdUsedTime-读取CD时长 （单位：分钟|min）
        readBdUsedTime-读取BD时长 （单位：分钟|min）
        readDvdUsedTime-读取DVD时长（单位：分钟|min）
        writeCdUsedTime-写入CD时长（单位：分钟|min）
        writeBdUsedTime-写入BD时长（单位：分钟|min）
        writeDvdUsedTime-写入DVD时长（单位：分钟|min）另请参阅:
        输入参数实例： { 'devId': '1' }
        响应结果实例： { "code": "0", "msg": "获取到光驱对应信息成功", "driveInfo": [{ "driId": 1, 'devId': '1', "driveName": "G:", "drvRunState": 1, "ed": 0, "driveUsageCount": 0, "driveIndexInDevice": 0, "readCdUsedTime": 4, "readBdUsedTime": 276, "readDvdUsedTime": 874, "writeCdUsedTime": 12, "writeBdUsedTime": 54, "writeDvdUsedTime": 266 }, { "driId": 2, 'devId': '1', "driveName": "F:", "drvRunState": 1, "ed": 0, "driveUsageCount": 0, "driveIndexInDevice": 0, "readCdUsedTime": 4, "readBdUsedTime": 276, "readDvdUsedTime": 874, "writeCdUsedTime": 12, "writeBdUsedTime": 54, "writeDvdUsedTime": 266 }, { "driId": 3, 'devId': '1', "driveName": "H:", "drvRunState": 1, "ed": 0, "driveUsageCount": 0, "driveIndexInDevice": 0, "readCdUsedTime": 4, "readBdUsedTime": 276, "readDvdUsedTime": 874, "writeCdUsedTime": 12, "writeBdUsedTime": 54, "writeDvdUsedTime": 266 }] }"""
        data = {'devId': devId}
        try:
            req = self.session.post(self.queryDriverInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryMagByDrawId(self, drawId):
        """说明：抽屉盘匣信息查询 -根据抽屉Id查询该抽屉对应的所有盘匣信息。
        参数:drawId - 必填 抽屉Id返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        magzineInfo-盘匣的信息（数组）
        数组对象说明：
        magId-盘匣Id
        rfid-盘匣的唯一标识
        magPos-盘匣在设备中的位置
        devId-设备Id
        mtype- Online：在线 ， OffLine： 离线， Other： 其他， Except： 游离另请参阅:
        输入参数实例： { 'drawId': '1' }
        响应结果实例： { "code": "0", "msg": "获取抽屉对应信息成功", "magzineInfo": [{ "magId": 1, "rfid": 'F365C5', "magPos": 0, "devId":1, "mtype":"Online" }, { "magId": 1, "rfid": 'E243C5', "magPos": 1, "devId":1, "mtype":"Online" }, { "magId": 1, "rfid": 'F698C5', "magPos": 2, "devId":1, "mtype":"Online" }] }"""

        data = {'drawId': drawId}
        try:
            req = self.session.post(self.queryMagByDrawIdURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryMagDiscInfo(self, rfid):
        """说明：盘匣中光盘信息查询-根据盘匣唯一标识获取盘匣、盘匣中光盘信息。
        参数:rfid - 必填 盘匣唯一标识返回:
        rfid-盘匣唯一标识
        totleSpace-盘匣总空间（单位：字节|B）
        useSpace-使用空间（单位：字节|B）
        totleDisc-总光盘数量
        useDisc-已经使用光盘数量
        badDisc-坏盘数量
        goodDiscsInfo-好盘信息（数组）
        badDiscsInfo-坏盘信息（数组）
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        （goodDiscsInfo|badDiscsInfo）数组对象说明：
        Tsize-光盘容量（单位：字节|B）
        Usize-光盘使用大小（单位：字节|B）
        discType-光盘类型
        pdiscId-物理光盘Id
        slotName-抽片名称另请参阅:
        输入参数实例： { 'rfid': '1E15F4', }
        响应结果实例： { "rfid": "1E15F4", "totleSpace": 4651762, "useSpace": 61554, "totleDisc": 1, "useDisc": 0, "badDisc": 0, "badDiscsInfo": [ { "Tsize": 54621, "Usize": 54621, "discType": "DVD+R$4.7G", "pdiscId":"192", "slotName": "E243C5_3" } ], "goodDiscsInfo": [{ "Tsize": 61554, "Usize": 61554, "pdiscId":"192", "discType": "DVD+R$4.7G", "slotName": "E243C5_1" }], "code": "0", "msg": "获取指定盘匣中光盘信息成功！" }"""
        data = {'rfid': rfid}
        try:
            req = self.session.post(self.queryMagDiscInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryMagInfo(self, devId, rfid=None):
        """说明：盘匣信息查询-查询盘匣的基本信息。
        参数:rfid - 选填 盘匣唯一标识devId - 必填 设备Id返回:
        code-0：调用接口成功，1：调用接口失败
        omagazineInfoArray-盘匣信息列表（数组）
        msg-提示信息
        数组对象说明：
        magId-盘匣Id
        rfid-盘匣唯一标识
        devId-设备Id
        drawId-抽屉Id
        addrInDev-在设备中的位置
        remDiskCount-可用光盘数量
        magDiscCount-总光盘数量
        badDiscCount-坏盘数量
        magState-盘匣状态 OnLine：在线，OffLine:离线，Other:游离，Except:未知
        diskFullCount-已用光盘数量另请参阅:
        响应结果实例：
         一：输入参数（rfid、devId）返回盘匣数组，数组中只有单一盘匣信息。 { 'rfid': '1E15F4', 'devId':'1' }
        { "code": "0", "omagazineInfoArray": [{ "magId": 50, "rfid": "E2552A", "devId": 13, "drawId": 18, "addrInDev": 0, "remDiskCount": 2, "magDiscCount": 8, "magState": "OnLine", "diskFullCount": 6 }], "msg": "盘匣信息列表查询成功！" }
        二： 输入参数（devId）返回盘匣数组，数组中包含所有盘匣信息。 { 'devId':'1' }
        { "code": "0", "omagazineInfoArray": [{ "magId": 50, "rfid": "E25554A", "devId": 13, "drawId": 8, "addrInDev": 0, "remDiskCount": 6, "magDiscCount": 12, "magState": "OnLine", "diskFullCount": 18 }, { "magId": 50, "rfid": "E74352A", "devId": 13, "drawId": 6, "addrInDev": 1, "remDiskCount": 5, "magDiscCount": 20, "magState": "OnLine", "diskFullCount": 25 }, { "magId": 50, "rfid": "E8946A", "devId": 13, "drawId": 4, "addrInDev": 2, "remDiskCount":3, "magDiscCount": 26, "magState": "OnLine", "diskFullCount": 29 }], "msg": "盘匣信息列表查询成功！" } """
        if rfid:
            data = {'devId': devId, 'rfid': rfid}
            try:
                req = self.session.post(self.queryMagInfoURL, json=data)
                return req.json()
            except:
                raise ValueError()
        else:
            data = {'devId': devId}
            try:
                req = self.session.post(self.queryMagInfoURL, json=data)
                return req.json()
            except:
                raise ValueError()

    def queryOpticalDiscInfo(self, discLabel):
        """说明：逻辑光盘信息查询-主要查询逻辑光盘详细信息。
        参数:discLabel - 必填 卷标返回:
        discLabel-逻辑光盘卷标
        poolId-卷池Id
        discRunState-光盘运行状态 0：空白盘，1：分盘中，2：分盘完成，3：生成虚拟光盘中， 4：等待刻录， 5：刻录成功，7：异常，20：等待下载， 21： 下载中， 22 ：下载成功， 23： 下载失败，31：生成虚拟光盘完成
        discState-光盘状态 NOFULL： 未满盘 ， FULL： 满盘， ISO：镜像制作， NearLine：近线 ，OffLine：离线 ， DataMove：数据移动
        discSize-光盘容量（单位：字节|B）
        discType-光盘类型
        discUsize-光盘使用大小（单位：字节|B）
        discFileId-光盘文件Id
        ophyDiscInfo[]-物理光盘信息（数组） 注：在多份刻录情况下，一个逻辑光盘对应多个物理光盘
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        数组对象说明：
        pdiscId-物理光盘Id
        slotName-抽片名称另请参阅:
        输入参数实例： { 'discLabel': '201836125-1', }
        响应结果实例： { "discLabel": "201836125-1", "poolId": 1, "discRunState": 5, "discState": "NearLine", "discSize": 4706074624, "discType": "DVD-R$4.7G", "discUsize": 126005248, "ophyDiscInfo": [{ "pdiscId": 1, "slotName": "E243C5_1" }], "code": "0", "msg", "查询逻辑光盘信息成功" }"""
        data = {'discLabel': discLabel}
        try:
            req = self.session.post(self.queryOpticalDiscInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def queryPrintInfo(self, devId):
        """说明：打印机信息查询 -根据设备Id查询该设备下打印机信息。
        参数:devId - 必填 设备Id返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        printInfo-所有打印机的信息（数组）
        数组对象说明：
        printId-打印机Id
        printIndexInDevice-打印机在设备中的位置
        discNumber-是否有盘 0：无盘，1：有盘
        ed-是否禁用 0：启用,1：禁用
        devId-设备Id
        status-打印机状态 0：正常，1：硬件故障
        printRunState-运行状态 0：禁用；1：启用；2：空闲有盘；3：空闲无盘；4：打印
        inkblack-黑色墨（30 加墨，10 不能再继续使用，必须加墨）
        inkcolor-彩色墨 （30 加墨，10 不能再继续使用，必须加墨）两个墨水任意一个达到标准，都要提示加墨另请参阅:
        输入参数实例： { 'devId': '1' }
        响应结果实例： { "code": "0", "msg": "获取打印机对应信息成功", "printInfo": [{ "printId": 1, "devId": 1, "printIndexInDevice": 0, "discNumber": 0, "ed": 0, "printRunState":1, "inkcolor": 60, "inkblack":80, "status": 0 }] }"""
        data = {'devId': devId}
        try:
            req = self.session.post(self.queryPrintInfoURL, json=data)
            return req.json()
        except:
            raise ValueError()

    def querySlotInfo(self, rfid, slotPosition=None):
        """说明：抽片信息查询-根据条件查询一条或多条抽片的详细信息 。
        参数:rfid - 必填 盘匣的唯一标识
        slotPosition - 选填
        注：抽片的位置若不写，则查询当前盘匣下所有抽片的详细信息返回:
        code：0：调用接口成功，1：调用接口失败
        oslotInfo-抽片信息列表（数组）
        msg-提示信息
        数组对象说明：
        slotId-抽片Id
        magId-盘匣Id
        slotStatus-抽片的状态 （当前状态暂时停用）
        ed-是否禁用 0：启用，1：禁用
        devId-设备Id另请参阅:
        输入参数实例： { 'rfid': 'E243C5', 'slotPosition':1 }
        响应结果实例： { "code": "0", "msg": "查询抽片信息成功", "oslotInfo": [{ "slotId": 1, "magId": 1, "slotStatus": 8, "devId": 1, "ed": 0 }] }"""
        if slotPosition:
            data = {'rfid': rfid, 'slotPosition': slotPosition}
            try:
                req = self.session.post(self.querySlotInfoURL, json=data)
                return req.json()
            except:
                raise ValueError()
        else:
            data = {'rfid': rfid}
            try:
                req = self.session.post(self.querySlotInfoURL, json=data)
                return req.json()
            except:
                raise ValueError()
