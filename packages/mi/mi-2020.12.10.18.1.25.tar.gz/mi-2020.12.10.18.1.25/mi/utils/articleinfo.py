#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : articleinfo
# @Time         : 2020/12/9 2:52 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import get_zk_config
from mi.db import Mongo

mongo_cache_url = get_zk_config()['mongo_cache_url']

mongo = Mongo()
ac = mongo.db.articleinfo


def get_articleinfo(docid='0003899b202871b7fd3dab15f2f9549a'):
    """
    todo: 定义ac结构
    :param docid:
    :return:
    """
    doc = ac.find_one({'id': docid})
    if doc:
        articleinfo = eval(doc['ac'])

    else:
        url = f"{mongo_cache_url}/ac?id={docid}"
        r = requests.request('get',
                             url)  # 包含插入逻辑 doc = {'id': docid, 'ac': str(articleinfo)} _ = ac.insert(doc, continue_on_error=False)
        articleinfo = r.json()['result']
    return articleinfo
