import json
import logging

from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest, DescribeLoadBalancerAttributeRequest, CreateLoadBalancerHTTPListenerRequest, \
    CreateLoadBalancerTCPListenerRequest, AddBackendServersRequest, StartLoadBalancerListenerRequest, RemoveBackendServersRequest, \
    DeleteLoadBalancerRequest

from aliyunsdkslb.endpoint import endpoint_data

from .base import AliClient

logger = logging.getLogger(__name__)


class SLB(AliClient):
    totalstring = 'TotalCount'

    def _getInsList(self):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        for pagenum in range(1, self.get_totel_page(request) + 1):
            request.set_PageNumber(pagenum)
            request.set_PageSize(self.pagesize)
            ret = self.do_action(request)
            logger.debug(ret)
            for ins in ret['LoadBalancers']['LoadBalancer']:
                yield ins

    def getInsList(self, detail=None):

        if not detail:
            self.ins_list = list(self._getInsList())
            return self.ins_list
        else:
            self.ins_list = [self.getDetail(ins['LoadBalancerId']) for ins in self._getInsList()]

        return self.ins_list

    def getDetail(self, id):
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(id)
        ret = self.do_action(request)
        return ret

    def addBackendServer(self, id, ecs_instance_id):
        request = AddBackendServersRequest.AddBackendServersRequest()
        request.set_LoadBalancerId(id)
        data = [{"Type": "ecs", "ServerId": i, "Weight": 100} for i in ecs_instance_id]
        request.set_BackendServers(json.dumps(data))
        ret = self.do_action(request)
        return ret

    def removeBackendServer(self, id, BackendServers):
        '''

        :param id:
        :param BackendServers:  json'[{"Type":"ecs","ServerId":"i-t4n1epdcvalegf7doz0f","Weight":100}]'
        :return:
        '''
        request = RemoveBackendServersRequest.RemoveBackendServersRequest()
        request.set_LoadBalancerId(id)
        request.set_BackendServers(BackendServers)
        ret = self.do_action(request)
        return ret

    def createListener(self, id, port, type):
        if type == 'tcp':
            self.createTCPListener(id, port)
        else:
            self.createHttpListener(id, port)

    def createHttpListener(self, id, port):
        logger.debug('createHttpListener')
        request = CreateLoadBalancerHTTPListenerRequest.CreateLoadBalancerHTTPListenerRequest()
        request.set_LoadBalancerId(id)
        request.set_ListenerPort(port)
        request.set_StickySession('off')
        request.set_HealthCheck('on')
        request.set_HealthCheckURI('/')
        request.set_HealthCheckTimeout(5)
        request.set_HealthCheckInterval(2)
        request.set_HealthyThreshold(3)
        request.set_UnhealthyThreshold(3)
        request.set_BackendServerPort(port)
        ret = self.do_action(request)
        return ret

    def createTCPListener(self, id, port):
        logger.debug('createTCPListener')
        request = CreateLoadBalancerTCPListenerRequest.CreateLoadBalancerTCPListenerRequest()
        request.set_LoadBalancerId(id)
        request.set_ListenerPort(port)
        request.set_BackendServerPort(port)
        request.set_Bandwidth(-1)
        ret = self.do_action(request)
        return ret

    def startListener(self, id, port, type):
        request = StartLoadBalancerListenerRequest.StartLoadBalancerListenerRequest()
        request.set_LoadBalancerId(id)
        request.set_ListenerPort(port)
        request.set_protocol_type(type)
        ret = self.do_action(request)
        return ret

    def deleteLoadBalancerRequest(self, id):
        request = DeleteLoadBalancerRequest.DeleteLoadBalancerRequest()
        request.set_LoadBalancerId(id)
        ret = self.do_action(request)
        return ret


endpoint_map = endpoint_data.endpoint_map
