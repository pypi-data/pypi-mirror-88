#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : http_utils
# @Time         : 2020/11/12 11:49 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import logger
from meutils.zk_utils import zk_cfg

from requests import get, post


@logger.catch()
def get_articleinfo(docid):
    return get(f"{zk_cfg.ac_assistant_url}/{docid}").json().get('item', {})


@logger.catch()
def get_simbert_vectors(titles):
    if isinstance(titles, str):
        titles = [titles]
    return post(f"{zk_cfg.simbert_url}", json={"texts": titles}).json().get('vectors')  # [[...]]


@logger.catch()
def ann_search(url, text='不知道', topk=5, vector_name='embedding', fields=None, only_return_ids=False):
    query_embeddings = get_simbert_vectors(text)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "vector": {
                            vector_name: {
                                "topk": topk,
                                "values": query_embeddings,
                                "metric_type": "IP",
                                "params": {
                                    "nprobe": 1
                                }
                            }
                        }
                    }
                ]
            }
        },
        "fields": fields if fields else []
    }

    r = get(url, json=body).json()
    if only_return_ids:
        return [i['id'] for i in r['data']['result'][0]]
    else:
        return r


@logger.catch()
def mongo_find(collection, attribute='find_one', filter_=None):
    if filter_ is None:
        filter_ = {}
    r = get(f"{zk_cfg.mongo_find_url}/{collection}/{attribute}?filter={filter_}").json()
    return r.get(f"{collection}.{attribute}", {})


if __name__ == '__main__':
    from pprint import pprint

    title = '社区团购“团战”正酣，变革与较量中如何走出“最优”路径'
    pprint(
        ann_search(
            zk_cfg.nh_choice_search_url,
            text=title,
            topk=5,
            only_return_ids=False,
            vector_name='title_vec',
            fields=[],
        )
    )

    ids = ann_search(
        zk_cfg.nh_choice_search_url,
        text=title,
        topk=5,
        only_return_ids=True,
        vector_name='title_vec',
        fields=[],
    )
    for id in ids:
        print(mongo_find('nh_choice', filter_={'ann_id': int(id)}).get('title'))

    # print(mongo_find('nh_choice', filter_={'ann_id': 1607597490101257887}))
