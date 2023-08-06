import logging
import functools
import time
import json
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.client import AcsClient

logger = logging.getLogger(__name__)

def retry(loop=3,delay=5):
    def trace(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1,loop+1):
                logger.debug(f'第{i}次請求 {args} {kwargs}')
                try:
                    return func(*args, **kwargs)
                except ClientException as e:
                    logger.warning(f'超時 重試第{i}次 {e}')
                    time.sleep(delay)
                except Exception as e:
                    logger.warning(f'重試第{i}次 {e} {args} {kwargs}')
                    time.sleep(delay)

        return wrapper

    return trace


class AliClient:
    pagesize = 100
    totalstring = ""

    def __init__(self, ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID):
        self.client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
        self.ins_list = []

    @retry()
    def do_action(self, request):
        response = self.client.do_action_with_exception(request)
        response = json.loads(str(response, encoding='utf-8'))
        logger.debug(response)
        return response

    def get_totel_page(self, request):
        request.set_PageSize(1)
        data = self.do_action(request)
        pagenum = data[self.totalstring] // self.pagesize
        if data[self.totalstring] % self.pagesize != 0:
            pagenum += 1
        return pagenum