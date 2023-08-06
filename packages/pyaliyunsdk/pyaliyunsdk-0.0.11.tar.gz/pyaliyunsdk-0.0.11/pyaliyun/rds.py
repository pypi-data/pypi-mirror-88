import datetime
import logging
from typing import Dict

from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeDBInstanceAttributeRequest, DescribeResourceUsageRequest, \
    DescribeBackupsRequest, CreateBackupRequest, DescribeBackupTasksRequest, CreateDBInstanceRequest, ModifySecurityIpsRequest,TransformDBInstancePayTypeRequest

from aliyunsdkrds.endpoint import endpoint_data

from .base import AliClient

class RDS(AliClient):
    totalstring = 'TotalRecordCount'

    def _getInsList(self):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        for pagenum in range(1, self.get_totel_page(request) + 1):
            request.set_PageNumber(pagenum)
            request.set_PageSize(self.pagesize)
            ret = self.do_action(request)
            for ins in ret['Items']['DBInstance']:
                # self.ins_list.append(i)
                yield ins
        # if not self.ins_list:
        #     logging.error('rds_list {} 為空 {}'.format(self.client, self.rds_list))
        # return self.ins_list

    def getInsList(self, detail=None):

        if not detail:
            self.ins_list = list(self._getInsList())
            return self.ins_list
        else:
            self.ins_list = [self.getDetail(ins['DBInstanceId']) for ins in self._getInsList()]

        return self.ins_list

    def getDetail(self, id):
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)

        data = ret['Items']['DBInstanceAttribute'][0]
        use_data = self.getUsage(id)

        if use_data:
            pass
        else:
            logging.error("use_data %s %s %s" % (id, data['DBInstanceDescription'], use_data))
            raise Exception('use_data 空 %s ' % use_data)

        data.update(use_data)

        return data

    def getUsage(self, id):
        request = DescribeResourceUsageRequest.DescribeResourceUsageRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)
        return ret

    def getDBInstanceID(self, name: str) -> str:
        '''

        :param name:
        :return:
        '''
        ids = [i['DBInstanceId'] for i in self.ins_list if i['DBInstanceDescription'] == name]
        print(ids)
        if ids:
            return ids[0]
        else:
            print('找不到名稱或當前名稱錯誤')
            raise ValueError("輸入錯誤,找不到名稱或當前名稱錯誤")

    def getBackupList(self, name: str = None, id: str = None):
        '''返回備份列表

        :param name:
        :param id:
        :return:
        '''
        if name:
            id = self.getDBInstanceID(name)

        request = DescribeBackupsRequest.DescribeBackupsRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)
        backup_list = []
        for lst in ret['Items']['Backup']:
            lst['Datetime'] = datetime.datetime.strptime(lst['BackupEndTime'], '%Y-%m-%dT%H:%M:%S%z')
            backup_list.append(lst)

        return backup_list

    def getBackupLastet(self, name=None, id=None):
        '''返回最新一筆備份資料

        :param name:
        :param id:
        :return:
        '''
        backup_list = self.getBackupList(name=name, id=id)
        d = max([i['Datetime'] for i in backup_list])
        _data = [i for i in backup_list if i['Datetime'] == d][0]
        data = {
            'Name': name,
            'DBInstanceId': _data['DBInstanceId'],
            'BackupIntranetDownloadURL': _data['BackupIntranetDownloadURL'],
            'BackupDownloadURL': _data['BackupDownloadURL'],
            'BackupEndTime': datetime.datetime.fromtimestamp(_data['Datetime'].timestamp()).strftime("%Y/%m/%d %H:%M:%S"),
            'BackupSize': f"{int(_data['BackupSize'] / 1024 / 1024 // 1024)}G",
            'FileName': _data['BackupIntranetDownloadURL'].split('/')[-1].split('?Expires')[0]

        }
        return data

    def createBackup(self, name=None, id=None) -> dict:
        '''創建備份任務

        :param name:
        :param id:
        :return:
        '''
        if name:
            id = self.getDBInstanceID(name)

        request = CreateBackupRequest.CreateBackupRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)
        return ret

    def getBackupTasks(self, id, jobid) -> Dict:
        '''返回備份任務狀態

        :param id:
        :param jobid:
        :return:
        '''
        request = DescribeBackupTasksRequest.DescribeBackupTasksRequest()
        request.set_DBInstanceId(id)
        request.set_BackupJobId(jobid)
        ret = self.do_action(request)

        return ret['Items']['BackupJob'][0] if ret['Items']['BackupJob'] else {}

    def createInstance(self, name, type, version, storage, paytype, dbclass, security_ip_list='127.0.0.1', vpcid=None):
        '''創建實例

        :param name: 實例名稱
        :param type: mysql
        :param version: 5.7
        :param storage: 100
        :param paytype: Postpaid, Prepaid
        :param dbclass: rds.mysql.s3.large, mysql.n4.large.1
        :param security_ip_list: "127.0.0.1,"
        :param vpcid:
        :return:
        '''

        request = CreateDBInstanceRequest.CreateDBInstanceRequest()
        request.set_Engine(type)
        request.set_EngineVersion(version)
        request.set_DBInstanceClass(dbclass)  # rds.mysql.s3.large , mysql.n4.large.1
        request.set_DBInstanceStorage(storage)
        request.set_DBInstanceNetType("Intranet")
        request.set_DBInstanceDescription(name)  # 描述
        request.set_SecurityIPList(security_ip_list)
        if vpcid:
            request.set_VPCId(vpcid)  # VPCID

        request.set_PayType(paytype)  # Postpaid, Prepaid
        # request.set_ZoneId("cn-hongkong-b")
        request.set_InstanceNetworkType("VPC")
        # request.set_Period("Month") # ??
        # request.set_UsedTime("2") # ??
        self.do_action(request)

    def updateModifySecurityIps(self, id, iplist):
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(id)
        request.set_SecurityIps(iplist)
        ret = self.do_action(request)
        return ret


    def updatePayTypeInstance(self,id,paytype,period,usedtime=1):
        """调用TransformDBInstancePayType接口变更RDS实例的计费方式。

        :param id:
            实例ID。
        :param paytype:
            实例的付费类型。取值：
                Postpaid：后付费（按量付费）
                Prepaid：预付费（包年包月）
        :param period:
            指定预付费实例为包年或者包月类型。取值：
                Year：包年
                Month：包月
            说明 若PayType=Prepaid，需要传入该参数。
        :param usedtime:
            指定购买时长。取值：
                当参数Period为Year时，UsedTime取值为1~5。
                当参数Period为Month时，UsedTime取值为1~9。
            说明 若PayType=Prepaid，需要传入该参数。
        :return:
        """
        request =TransformDBInstancePayTypeRequest.TransformDBInstancePayTypeRequest()
        request.set_DBInstanceId(id)
        request.set_PayType(paytype)
        request.set_Period(period)
        request.set_UsedTime(usedtime)
        ret = self.do_action(request)
        return ret


endpoint_map = endpoint_data.endpoint_map