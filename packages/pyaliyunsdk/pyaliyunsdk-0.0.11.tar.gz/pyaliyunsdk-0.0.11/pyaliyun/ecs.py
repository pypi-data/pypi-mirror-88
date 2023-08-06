import time
import logging

from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceAttributeRequest, DescribeDisksRequest, \
    DescribeInstanceTypesRequest, AllocatePublicIpAddressRequest, StartInstanceRequest, DescribeVpcsRequest, AddTagsRequest, JoinSecurityGroupRequest, \
    StopInstanceRequest, ModifyInstanceSpecRequest, ModifyPrepayInstanceSpecRequest

from aliyunsdkecs.endpoint import endpoint_data

from .base import AliClient

logger = logging.getLogger(__name__)



class ECS(AliClient):
    totalstring = 'TotalCount'

    def _getInsList(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        for pagenum in range(1, self.get_totel_page(request) + 1):
            request.set_PageNumber(pagenum)
            request.set_PageSize(self.pagesize)
            ret = self.do_action(request)
            for ins in ret['Instances']['Instance']:
                yield ins

    def getInsList(self, detail=None):

        if not detail:
            self.ins_list = list(self._getInsList())
            return self.ins_list
        else:
            self.ins_list = [self.getDetail(ins['InstanceId']) for ins in self._getInsList()]

        return self.ins_list

    def getDetail(self, id):
        request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
        request.set_InstanceId(id)
        status = False

        # 重試次數
        for loop in range(3):

            ret = self.do_action(request)
            logger.debug(ret)
            if not ret['VpcAttributes']['PrivateIpAddress']['IpAddress']:
                logging.error('獲取不到私有IP detail %s' % ret)
                time.sleep(5)
                continue

            size = self.getDiskSize(ret['InstanceId'])
            ret.update({"Disk": size})
            status = True
            break

        if not status:
            raise Exception('%s 獲取不到私有IP' % id)
        else:
            return ret

    def getDiskSize(self, id):
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)
        disk_size = ret['Disks']['Disk'][0]['Size']
        return disk_size

    def getTypeAll(self):
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        ret = self.do_action(request)
        return ret['InstanceTypes']['InstanceType']

    def setPublicIP(self, id):
        """取得公網iP

        :param id:
        :return:
        """
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)

        return ret

    def startInstance(self, id):
        '''啟動實例

        :param id:
        :return:
        '''
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)
        return ret

    def getDisk(self, id):
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)
        return ret

    def getVpcList(self):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageSize(10)
        response = self.do_action(request)
        return response

    def addTagsRequest(self, id, k, y):
        request = AddTagsRequest.AddTagsRequest()
        request.set_ResourceId(id)
        request.set_ResourceType('instance')
        request.set_Tags([{'Key': k, 'Value': y}])
        response = self.do_action(request)
        return response

    def addSecurityGroup(self, id, securitygroupid):
        request = JoinSecurityGroupRequest.JoinSecurityGroupRequest()
        request.set_InstanceId(id)
        request.set_SecurityGroupId(securitygroupid)
        response = self.do_action(request)
        return response

    def updateModifyInstance(self, id, instancetype):
        """调用ModifyInstanceSpec调整一台按量付费ECS实例的实例规格和公网带宽大小。

        :param id:
        :param instancetype:
        :return:
        """
        request = ModifyInstanceSpecRequest.ModifyInstanceSpecRequest()
        request.set_InstanceId(id)
        request.set_InstanceType(instancetype)
        response = self.do_action(request)
        return response

    def updateModifyPrepayInstance(self, id, instancetype):
        """调用ModifyPrepayInstanceSpec升级或者降低一台包年包月ECS实例的实例规格，新实例规格将会覆盖实例的整个生命周期。

        :param id:
        :param instancetype:
        :return:
        """
        request = ModifyPrepayInstanceSpecRequest.ModifyPrepayInstanceSpecRequest()
        request.set_InstanceId(id)
        request.set_InstanceType(instancetype)
        response = self.do_action(request)
        return response

    def stopInstance(self, id):
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_InstanceId(id)
        response = self.do_action(request)
        return response

    def get_mapping_site_ip(self):
        data = {}
        for i in self.ins_list:
            data[i['InstanceName']] = {
                'PrivateIpAddress': i['VpcAttributes']['PrivateIpAddress']['IpAddress'],
                'PublicIpAddress': i['PublicIpAddress']['IpAddress']
            }
        return data

endpoint_map = endpoint_data.endpoint_map
