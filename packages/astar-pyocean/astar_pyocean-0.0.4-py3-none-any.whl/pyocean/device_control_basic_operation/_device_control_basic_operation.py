
from pyocean.base import BaseClient
import requests
class DeviceControlBasicOperation(BaseClient):
    def __init__(self, url):
        super(DeviceControlBasicOperation, self).__init__(url)
        self.checkDevURL = self.url + 'checkDev'
        self.createActiveDevTaskURL = self.url + 'createActiveDevTask'
        self.createDevURL = self.url + 'createDev'
        self.createScanDevTaskURL = self.url + 'createScanDevTask'
        self.createDevDoorUnLockTaskURL = self.url = 'createDevDoorUnLockTask'
        self.queryOcTaskStateURL = self.url + 'queryOcTaskState'
        self.queryDoorLockTaskStateURL = self.url + 'queryDoorLockTaskState'
        self.createCheckDiscTaskURL = self.url + 'createCheckDiscTask'
        self.queryCheckDiscTaskStateURL = self.url + 'queryCheckDiscTaskState'
        self.createMoveSlot2ImpTaskURL = self.url + 'createMoveSlot2ImpTask'
        self.createMoveSlot2DrvTaskURL = self.url + 'createMoveSlot2DrvTask'
        self.createMoveBin2DriverTaskURL = self.url + 'createMoveBin2DriverTask'
        self.createMoveDriver2BinTaskURL = self.url + 'createMoveDriver2BinTaskURL'
        self.createMoveImp2SlotTaskURL = self.url + 'createMoveImp2SlotTask'
        self.createMoveImp2BinTaskURL = self.url + 'createMoveImp2BinTask'




    def checkDev(self, devName):
        """说明： 校验设备-根据设备名称，校验设备的可用性。
        参数:devName - 必填 设备名称返回:
        code-0:调用接口成功，1:调用接口失败
        devName-设备名称
        msg-提示信息另请参阅:
        输入参数实例： { 'devName': 'HMS 2105' }
        响应结果实例： { "code": "0", "msg": "校验成功，设备可用" }"""
        data = {'devName': devName}
        try:
            req = requests.post(self.checkDevURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createActiveDevTask(self, id):
        """
        说明：设备激活-根据设备Id创建设备激活任务。
        参数:id - 必填 设备id返回:
        code-0：调用接口成功，1：调用接口失败
        otaskId-生成任务Id
        msg-提示信息另请参阅:
        输入参数实例： { ' ': '1' }
        响应结果实例： { "code": "0", "otaskId":104, "msg": "激活任务发布成功" }
        """
        data = {'id': id}
        try:
            req = requests.post(self.createActiveDevTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createCheckDiscTask(self, slotName):
        """说明:检测光盘任务创建-根据抽片名称创建光盘检测任务。
        参数:slotName - 必填 抽片名称 说明：例如 E89R7_1 以_符号作为分界线,_前是盘匣的唯一标识 ，_后是在盘匣中的位置返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { 'slotName':'E89R7_1' }
        响应结果实例： { "code": "0", "taskId":"1325", "msg": "光盘检测任务创建成功！" }"""
        data = {'slotName': slotName}
        try:
            req = requests.post(self.createCheckDiscTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createDev(self, devName, devPort, devIp, devTypeId, nodeIp):
        """说明： 设备添加-根据输入信息添加设备信息。
        参数:devName - 必填 设备名称devPort - 必填 设备端口号devIp - 必填 设备IpdevTypeId - 必填 设备类型 （获取方法见queryDevType方法）nodeIp单机模式下可不填，集群模式下必填 设备类型 （获取方法见queryDevType方法）返回:
        code-0:调用接口成功，1:调用接口失败
        devName-设备名称
        msg-提示信息另请参阅:
        输入参数实例： { 'devName': 'HMS 2105', 'devPort': '3260', 'devIp': '192.168.199.100', 'devTypeId': '2' , 'nodeIp':'192.168.1.123' }
        响应结果实例： { "code": "0", "devName": "HMS 2105", "msg": "添加设备成功" }"""
        data = {'devName': devName, 'devPort': devPort, 'devIp': devIp, 'devTypeId': devTypeId, 'nodeIp': nodeIp}
        try:
            req = requests.post(self.createDevURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createDevDoorLockTask(self, devName):
        pass
    def createDevDoorUnLockTask(self, devName):
        """说明：门锁定-根据设备名称创建门锁定任务。
        参数:devName - 必填 设备名称返回:
        code-0：调用接口成功，1：调用接口失败
        state-1：门锁定任务创建成功！ 5 ：门锁定任务创建异常！ 6 ：门锁定任务创建失败，目前门的状态是：准备门解锁！ 7 ：门锁定任务创建失败，目前门的状态是：门解锁处理中！ 8 ：门锁定任务创建失败，目前门的状态是：门解锁异常！ 9 ：门锁定任务创建失败，目前门的状态是：锁定状态！ 10 ：门锁定任务创建失败，目前门的状态是：门锁定等待中！ 11 ：门锁定任务创建失败，目前门的状态是：门锁定处理中！ 12 ：门锁定任务创建失败，目前门的状态是：门锁定异常！
        taskId-任务id
        msg-提示信息另请参阅:
        输入参数实例： { 'devName': 'HMS 2105' }
        响应结果实例： { "code": "0", "taskId":"1232", "state":"1", "msg": "门锁定任务创建成功！" }"""
        data = {'devName': devName}
        try:
            req = requests.post(self.createDevDoorUnLockTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def queryOcTaskState(self, taskId):
        """说明：综合任务状态查询-根据任务Id查询任务状态 。
        参数:taskId - 必填 任务Id返回:
        code-0：调用接口成功，1：调用接口失败
        state-任务状态 0：任务等待，2：任务完成，3：任务异常，4：任务执行中
        msg-提示信息另请参阅:
        输入参数实例： { "taskId": '409' }
        响应结果实例： { "code": "0", "state":0, "msg": "任务等待" }"""
        data = {'taskId': taskId}
        try:
            req = requests.post(self.queryOcTaskStateURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createInitDevTask(self, parameter):
        """说明：设备初始化-根据设备Id和初始化类型创建设备初始化任务。
        参数:id - 必填 设备id;initType - 必填 1：初始化弹出屉，2：初始化打印机，3：初始化光驱，4：初始化盘匣，5：初始化盘桶，6：初始化全库返回:
        code-0：调用接口成功，1：调用接口失败
        otaskId-生成任务Id
        msg-提示信息另请参阅:
        输入参数实例： { 'id': '1', 'initType':'1' }
        响应结果实例： { "code": "0", "otaskId":105, "msg": "初始化任务发布成功" }"""
        data = {'id': id}
        try:
            req = requests.post(self.createDevDoorUnLockTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createMoveBin2DriverTask(self, drvId, binId):
        """说明：盘桶到光驱-根据光驱Id和盘桶Id创建移盘任务（将ODA设备盘桶里的光盘移动到光驱）。
        参数:binId - 必填 盘桶IddrvId - 必填 光驱Id返回:
        code-0：调用接口成功，1：调用接口失败
        state-任务状态，1：移盘任务创建成功；2：光盘已经在抽片，无需移盘；3：移盘任务创建失败,输入盘桶无可用光盘
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { 'drvId':"1", 'binId':'2' }
        响应结果实例： { "code": "0", "msg": "移盘任务创建成功", "state":"1", "taskId":"3" }"""
        data = {'drvId': drvId, 'binId': binId}
        try:
            req = requests.post(self.createMoveBin2DriverTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createMoveDriver2BinTask(self, drvId, binId):
        """说明：光驱到盘桶-根据光驱Id和盘桶Id创建移盘任务（将ODA设备光驱里的光盘移动到盘桶）。
        参数:binId - 必填 盘桶IddrvId - 必填 光驱Id返回:
        code-0：调用接口成功，1：调用接口失败
        state-任务状态，1：移盘任务创建成功；3：移盘任务创建失败
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { 'drvId':"1", 'binId':'2' }
        响应结果实例： { "code": "0", "msg": "移盘任务创建成功", "state":"1", "taskId":"3" }"""
        data = {'drvId': drvId, 'binId': binId}
        try:
            req = requests.post(self.createMoveDriver2BinTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createMoveDrv2SlotTask(self, parameter):
        """说明:移动光驱的光盘到抽片-根据光驱Id和抽片名称创建移盘任务。"""
    def createMoveImp2BinTask(self, impExpId, binId):
        """说明：弹出屉移动光盘到盘桶-根据盘桶Id和弹出屉Id创建移盘任务（将弹出屉的光盘移动到盘桶）。
        参数:binId - 必填 盘桶IdimpExpId - 必填 弹出屉Id返回:
        code-0：调用接口成功，1：调用接口失败
        state-任务状态，1：移盘任务创建成功；3：移盘任务创建失败
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { "impExpId": "1", "binId": "E56TR_1" }
        响应结果实例： { "code": "0", "msg": "移盘任务创建成功", "state":"1", "taskId":"3" }"""
        data = { "impExpId": impExpId, "binId": impExpId }
        try:
            req = requests.post(self.createMoveImp2BinTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()


    def createMoveImp2SlotTask(self, impExpId, slotName):
        """说明：抽片移动到弹出屉-根据抽片名称和弹出屉Id创建移盘任务（将弹出屉的光盘移动到抽盘）。
        参数:impExpId - 必填 弹出提slotName - 必填 抽片名称返回:
        code-0：调用接口成功，1：调用接口失败
        state-任务状态，1：移盘任务创建成功；3：移盘任务创建失败
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { "impExpId": "1", "slotName": "E56TR_1" }
        响应结果实例： { "code": "0", "msg": "移盘任务创建成功", "state":"1", "taskId":"3" }"""
        data = {"impExpId": impExpId, "slotName": slotName}
        try:
            req = requests.post(self.createMoveImp2SlotTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createMoveSlot2DrvTask(self, drvId, slotName):
        """说明：抽片移动到光驱-根据光驱Id和抽片名称创建移盘任务。
        参数:drvId - 必填 光驱IdslotName - 必填 抽片名称返回:
        code-0：调用接口成功，1:调用接口失败
        state-任务状态，1：移盘任务创建成功；2：光盘已经在抽片，无需移盘；3：移盘任务创建失败,未找到指定光盘的位置
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { 'slotName':"E56TR_1", 'drvId':'2' }
        响应结果实例： { "code": "0", "msg": "移盘任务创建成功", "state":"1", "taskId":"3" }"""
        data = {'drvId': drvId, 'slotName': slotName}
        try:
            req = requests.post(self.createMoveSlot2DrvTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createMoveSlot2ImpTask(self, drvId, slotName):
        """说明:移动光驱的光盘到抽片-根据光驱Id和抽片名称创建移盘任务。
        参数:drvId - 必填 光驱IdslotName - 必填 抽片名称返回:
        code-0：调用接口成功，1：调用接口失败
        state-任务状态 ，1：移盘任务创建成功；2：光盘已经在抽片，无需移盘；3：指定光盘未在指定光驱，无法创建移盘任务
        msg-提示信息
        taskId-任务Id另请参阅:
        输入参数实例： { 'drvId':'2', 'slotName':"E56TR_1" }
        响应结果实例： { "code": "0", "state":"1", "msg": "移盘任务创建成功", "taskId":"2" }"""
        data = {'drvId': drvId, 'slotName': slotName}
        try:
            req = requests.post(self.createMoveSlot2ImpTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def createScanDevTask(self, id):
        """说明：设备扫描-根据设备Id和扫描类型创建设备扫描任务。
        参数:id - 必填 设备idscanType - 必填 扫描类型 1：全库扫描(id为设备id)，2：盘匣扫描(id为盘匣的id)，3：光盘扫描(id为光盘id)返回:
        code-0：调用接口成功，1：调用接口失败
        ocTaskid-生成任务Id
        msg-提示信息另请参阅:
        输入参数实例： { 'id': '2', 'scanType':'1' }
        响应结果实例： { "code": "0", "ocTaskid":106, "msg": "扫描任务发布成功" }"""
        data = {'id': id}
        try:
            req = requests.post(self.createScanDevTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def opticalDriveState(self, parameter):
        """说明:光驱状态管控-根据光驱Id和状态操作光驱（启用、禁用）。"""
    def queryCheckDiscTaskState(self, taskId):
        """说明：检测光盘任务状态-根据任务Id查询光盘检测任务状态。
        参数:taskId - 必填 任务Id返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        discMsg-光盘卷标信息
        state-1：任务已发送 ，2：任务完成 ，3：任务异常 ，4：任务执行中，　9：任务等待
        resultPath-检测结果报告（文件）存放位置另请参阅:
        输入参数实例： { 'taskId':'1325' }
        响应结果实例： { "code": "0", "msg": "任务完成", "state":"2", "discMsg":"201951251", "resultPath":"/home/vildataResult/" }"""
        data = {'taskId': taskId}
        try:
            req = requests.post(self.queryCheckDiscTaskStateURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def queryDoorLockTaskState(self, taskId, IddevName):
        """说明：门锁定任务状态查询-根据任务Id和设备名称查询门锁定任务状态 。
        参数:taskId - 必填 综合任务IddevName - 必填 设备名称返回:
        code-0：调用接口成功，1：调用接口失败
        state-2： 门锁定任务运行中! 4： 门锁定任务执行成功! 5： 门锁定任务异常！ 15： 查询异常，请检查参数devName对应值是否正确！
        msg-提示信息另请参阅:
        输入参数实例： { 'taskId': '1', 'devName': 'HMS 2105' }
        响应结果实例： { "code": "0", "state":"1", "msg": "门锁定任务执行成功!" }"""
        data = {'taskId': taskId, 'IddevName':IddevName}
        try:
            req = requests.post(self.queryDoorLockTaskStateURL, json=data)
            return req.json()
        except:
            raise ValueError()
    def queryDoorUnLockTaskState(self, devName):
        """"说明：门解锁-根据设备名称创建门解锁任务 。
        参数:devName - 必填 设备名称返回:
        code-0：调用接口成功，1：调用接口失败
        state-1：门解锁任务创建成功，准备门解锁！ 5 ：门解锁任务创建异常！ 6 ：门解锁任务创建失败，目前门的状态是：准备门解锁！ 7 ：门解锁任务创建失败，目前门的状态是：门解锁处理中！ 8：门解锁任务创建失败，目前门的状态是：门解锁异常！ 9 ：门解锁任务创建失败，目前门的状态是：解锁状态！ 10：门解锁任务创建失败，目前门的状态是：门锁定等待中！ 11： 门解锁任务创建失败，目前门的状态是：门锁定处理中！ 12 ：门解锁任务创建失败，目前门的状态是：门锁定异常！ 13 ：有系统任务在运行，请稍后操作！
        ocTaskId-任务id
        msg-提示信息另请参阅:
        输入参数实例： { 'devName': 'HMS 2105' }
        响应结果实例： { "code": "0", "state":"1", "ocTaskId":"1232", "msg": "门解锁任务创建成功，准备门解锁！" }"""
        data = {'devName': devName}
        try:
            req = requests.post(self.createDevDoorUnLockTaskURL, json=data)
            return req.json()
        except:
            raise ValueError()
