

from .ecs import ECS
from .rds import RDS
from .slb import SLB


class Aliyun:

    def __init__(self, ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID):
        self.ecs = ECS(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
        self.rds = RDS(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
        self.slb = SLB(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
