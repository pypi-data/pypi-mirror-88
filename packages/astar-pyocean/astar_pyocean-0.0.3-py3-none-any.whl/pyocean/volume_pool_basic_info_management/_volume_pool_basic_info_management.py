from pyocean.base import BaseClient
import requests
import logging


class VolumePoolBasicInfoManagement(BaseClient):
    def __init__(self, url):
        super(self, VolumePoolBasicInfoManagement).__init__(url)
        self.deletePoolURL = self.url + 'deletePool'
        self.pausePoolURL = self.url + 'pausePool'
        self.queryMagListByPoolIdURL = self.url + 'queryMagListByPoolId'
        self.queryPoolInfoURL = self.url + 'queryPoolInfo'
        self.startPoolURL = self.url + 'startPool'
        self.mkDiscURL = self.url + 'mkDisc'

    def deletePool(self, poolId):
        """说明:删除卷池-根据卷池Id删除指定的卷池信息。
        参数:poolId - 必填 卷池Id返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "poolId": "1" }
        响应结果实例： { "code": "0", "msg": "卷池删除成功！" }"""
        data = {
            "poolId": poolId
        }
        try:
            response = requests.post(self.deletePoolURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def pausePool(self, poolId):
        """说明:暂停卷池-根据卷池Id暂停已激活的卷池 。
        参数:poolId - 必填 卷池Id返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "poolId": "test" }
        响应结果实例： { "code": "0", "msg": "卷池暂停成功！" }"""
        data = {
            "poolId": poolId
        }
        try:
            response = requests.post(self.pausePoolURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryMagListByPoolId(self, poolId):
        """说明:根据卷池查询盘匣 -根据卷池Id查询所关联的所有盘匣信息。
        参数:poolId - 必填 卷池Id返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息
        magList-盘匣列表信息（数组）
        数组对象说明：
        magState-盘匣状态 0 ：在线， 1：离线 ，2： 游离
        emptyDisc-空盘数量
        totle-总光盘数
        useDisc-已经使用光盘数
        badDisc-坏光盘
        magId-盘匣id
        rfid-盘匣rfid
        magPos-盘匣位置
        devId-设备id
        discType-光盘类型另请参阅:
        输入参数实例： { "poolId": "1" }
        响应结果实例： { "code": "0", "msg": "查询成功！", magList:[{ "magState": "0", "emptyDisc": "10", "totle": "70", "useDisc": "60", "badDisc": "0", "magId": "1", "rfid": "4964FB", "magPos": "1", "devId": "12", "discType": "DVD+R$4.7G" }, {"magState": "0", "emptyDisc": "25", "totle": "80", "useDisc": "55", "badDisc": "0", "magId": "2", "rfid": "FB64FB", "magPos": "2", "devId": "12", "discType": "DVD+R$4.7G" }] }"""
        data = {
            "poolId": poolId
        }
        try:
            response = requests.post(self.pausePoolURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def queryPoolInfo(self):
        """说明:获取卷池信息-获取所有卷池卷池基本信息 。
        返回:
        code-0：调用接口成功, 1：调用接口失败
        msg-提示信息
        poolList-所有卷池信息（数组）
        数组对象说明：
        poolId-卷池Id
        poolType-卷池类型 4：存储卷池，5：输出卷池
        poolIsAdd-归档模式 0：迁移模式，1：存储模式
        fourceBurnDat-强制刻录周期
        poolMode-触发模式 0：手动/定时触发，1：接口文件触发，2：虚拟文件系统触发
        poolUseSize-卷池使用大小（单位：字节|B）
        volPath-卷池路径
        poolName-卷池名称
        writeWarningSize-归档预留 （单位：字节|B）
        maxIncrementLevel-扫描层级 2：一级，3：二级，4：三级，5：四级，6：五级，11：文件
        minSplitLevel-分盘层级 2：一级，3：二级，4：三级，5：四级，6：五级，7：六级，8：七级，9：八级，10：九级，11：文件
        poolSize-卷池大小 （单位：字节|B）
        poolState-卷池状态 0：暂停, 1：激活, 3：激活(即时运行)
        poolRunState-卷池运行状态 0：空闲, 1：存储处理中, 2：清理处理中
        writeBufferDate-归档缓存时间
        readBufferDate-查询缓存时间
        discType-光盘类型
        clearMode-数据清理模式
        ftpServerId-FTP服务Id另请参阅:
        响应结果实例： {"code": "0", "msg": "查询成功！", "poolList"[{ "poolId": "12", "poolType": "4", "poolCode": "pool1", "poolIsAdd": "0", "fourceBurnDate": "1", "poolMode": "0", "poolUseSize": "1024", "volPath": "D:/test/zdd", "poolName": "test", "writeWarningSize": "10", "maxIncrementLevel": "11", "minSplitLevel": "11", "poolSize": "1024", "poolState": "0", "poolRunState": "0", "writeBufferDate": "7", "readBufferDate": "7", "discType": "DVD+R$4.7G", "clearMode": "1", "ftpServerId": "1", },{"poolId": "12", "poolType": "4", "poolCode": "test", "poolIsAdd": "0", "fourceBurnDate": "1", "poolMode": "0", "poolUseSize": "1024", "volPath": "D:/test/data", "poolName": "test1", "writeWarningSize": "10", "maxIncrementLevel": "11", "minSplitLevel": "11", "poolSize": "1024", "poolState": "0", "poolRunState": "0", "writeBufferDate": "7", "readBufferDate": "7", "discType": "DVD+R$4.7G", "clearMode": "1", "ftpServerId": "1"} ]}"""
        try:
            response = requests.post(self.queryPoolInfoURL)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def startPool(self, poolId: str):
        """说明:激活卷池-根据卷池Id激活卷池，卷池激活后系统自动扫描增量文件，对文件发起归档。
        参数:poolId - 必填 卷池Id返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息
        startTime-开始时间另请参阅:
        输入参数实例： { "poolId": "1" }
        响应结果实例： { "code": "0", "msg": "卷池激活成功", "startTime": "2012-1-12" }"""
        data = {
            "poolId": poolId
        }
        try:
            response = requests.post(self.startPoolURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()

    def mkDisc(self, loginName, path):
        """说明:创建逻辑光盘（内部使用）
        参数:poolCode - 必填 卷池CodediscLabel - 必填 光盘卷标返回:
        code-0：调用接口成功，1：调用接口失败
        msg-提示信息另请参阅:
        输入参数实例： { "loginName": "test", "path":"2019061812" }
        响应结果实例： { "code": "0", "msg": "光盘创建成功！" }"""
        data = {
            "loginName": loginName,
            'path': path
        }
        try:
            response = requests.post(self.mkDiscURL, json=data)
            result = response.json()
            logging.info(result.get('msg'))
            return result
        except:
            raise ValueError()
