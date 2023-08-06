#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : nh_choice_ann
# @Time         : 2020/12/10 3:58 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.hash_utils import murmurhash
from meutils.zk_utils import zk_cfg, get_zk_config
from mi.db import Mongo, ANN, Hive
from milvus import DataType

mongo = Mongo()
nh_choice = mongo.db.nh_choice
mongo_ids = set(nh_choice.distinct('id'))

ann = ANN('10.119.28.8')
collection_name = 'nh_choice'


# # Create collection
# from milvus import DataType
#
# collection_param = {
#     "fields": [
#         #  Milvus doesn't support string type now, but we are considering supporting it soon.
#         #  {"name": "title", "type": DataType.STRING},
#         {"name": "category", "type": DataType.INT32},  # murmurhash()
#         {"name": "source", "type": DataType.INT32},
#         {"name": "title_vec", "type": DataType.FLOAT_VECTOR, "params": {"dim": 768}},
#     ],
#     "segment_row_limit": 4096,
#     #         "auto_id": False
# }
#
# ann.create_collection(collection_name, collection_param)
# ann.create_index(collection_name, 'title_vec')

# Insert entities
def get_articleinfo(docid):
    return requests.get(f"{zk_cfg.ac_assistant_url}/{docid}").json().get('item', {})


def get_title_vec(title):
    return requests.get(f"{zk_cfg.simbert_url}{title}").json().get('vectors')[0]


docids = set(get_zk_config('/mipush/nh_label/1').split()) - mongo_ids

if len(docids):
    logger.info(f"获取ArticleInfo")
    acs = docids | xThreadPoolExecutor(get_articleinfo, 16) | xlist
    df = (
        pd.DataFrame(acs)[['id', 'title', 'category', 'source']]
            .drop_duplicates('title')
            .assign(category=lambda df: df.category.str[0])
            .assign(category_hash=lambda df: df.category.map(murmurhash))
            .assign(source_hash=lambda df: df.source.map(murmurhash))
            .dropna(subset=['id'])
    )

    logger.info(f"获取TitleVec")
    df['title_vec'] = df.title.tolist() | xThreadPoolExecutor(get_title_vec, 8) | xlist

    # entities = ann.client.get_collection_info(collection_name)['fields']
    # for entity in entities:
    #     entity['values'] = df[entity['name'] + "_hash"]

    entities = [
        {"name": "title_vec", "type": DataType.FLOAT_VECTOR, "values": df['title_vec'].tolist()},
        {"name": "category", "type": DataType.INT32, "values": df['category_hash'].tolist()},
        {"name": "source", "type": DataType.INT32, "values": df['source_hash'].tolist()},
    ]

    df['ann_id'] = ann.client.insert(collection_name, entities)

    nh_choice.insert_many(df.to_dict('r'), False)

    logger.info(f"新增优质内容「{len(docids)}」条")
else:
    logger.info(f"新增优质内容「{len(docids)}」条")
