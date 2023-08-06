#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ANNEntity
# @Time         : 2020/12/9 6:19 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from typing import *
from pydantic import BaseModel, ValidationError


# #  {"name": "title", "type": DataType.STRING},
# {"name": "category_", "type": DataType.INT32},
# {"name": "vector", "type": DataType.FLOAT_VECTOR, "params": {"dim": 768}},

class MilvusField(BaseModel):
    name: str
    values: List[float]
    type = None
