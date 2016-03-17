# -*- coding: utf-8 -*-

import pymongo
import redis
import time
import oss_img

mongo_host = 'h213'
mongo_db = 'news_ver2'
# mongo_host = 'localhost'
# mongo_db = 'test'
conn = pymongo.MongoClient(mongo_host, 27017)
db = conn[mongo_db]

r = redis.Redis(host='localhost', port=6379)


def upload_image_in_content(content):
    length = len(content)
    delete_indexes = []
    for index, item in enumerate(content):
        for key, value in item.items():
            k, v = value.items()[0]
            if k == "img":
                if v.startswith("//"):
                    v = "http:" + v
                info = oss_img.oss_image_upload(v)
                if info is None:
                    delete_indexes.append(index)
                else:
                    content[index][key] = info
    new_content = []
    for index, item in enumerate(content):
        if index not in delete_indexes:
            new_content.append(item)
    if len(new_content) == length:
        return new_content
    content = []
    for index, item in enumerate(new_content):
        key, value = item.items()[0]
        content.append({str(index): value})
    return content


while r.llen('stories') != 0:
    story_info = r.lpop('stories')
    story_info = eval(story_info)
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    channel_id = '16'
    channel = u'外媒观光团'
    story_info['update_time'] = update_time
    story_info['channel_id'] = '16'
    story_info['channel'] = u'外媒观光团'
    content = story_info['content']
    print(story_info['url'])
    story_info['content'] = upload_image_in_content(content)
    if story_info['content']:
        db['NewsItems'].insert(story_info)

    # break

