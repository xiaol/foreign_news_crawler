# -*- coding: utf-8 -*-

import pymongo
import redis
import time

conn = pymongo.Connection('h213',27017)
db = conn['news_ver2']

r = redis.Redis(host='localhost', port=6379)

while r.llen('stories') != 0:
    story_info = r.lpop('stories')
    story_info = eval(story_info)
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    channel_id = '16'
    channel = u'外媒观光团'
    story_info['update_time'] = update_time
    story_info['channel_id'] = '16'
    story_info['channel'] = u'外媒观光团'

    db['NewsItems'].insert(story_info)

    # break

