# -*- coding: utf-8 -*-
# 修改完毕

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import redis
import traceback
import time

r = redis.StrictRedis(host='localhost', port=6379)

source = u"英国BBC中文网"

def bbc_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="column--primary"]//a')

    for story_link in story_links:
        story_text_link = 'http://www.bbc.com' + story_link.get("href")
        if r.sismember('duplicates', story_text_link) == True:
            continue
        else:
            try:
                story_title = story_link.text.strip()
                story_info = get_text(story_text_link, story_title)
                story_text = story_info['content']
                if len(story_text) == 0:
                    continue
                r.sadd('duplicates', story_text_link)
                r.rpush('stories', story_info)
            except:
                print traceback.format_exc(), url
                pass

def get_text(url, story_title):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    story_text = []
    count = 0
    imgnum = 0

    for x in tree.find('.//div[@class="column--primary"]').iter():
        if x.tag == "p":
            t = x.text.strip()
            if len(t) != 0:
                dict = {}
                dict[str(count)] = {}
                dict[str(count)]["txt"] = t
                count += 1
                story_text.append(dict)
        if x.tag == "img":
            dict = {}
            dict[str(count)] = {}
            dict[str(count)]["img"] = x.get("src")
            count += 1
            imgnum += 1
            story_text.append(dict)

    story_info = {
        'content': story_text,
        'source': source,
        'title': story_title,
        'url': url,
        'create_time': create_time,
        'imgnum': imgnum,
        'source_url': url,
        'sourceSiteName': source
        }


    return story_info

if __name__ == "__main__":
    # get_text('http://www.bbc.com/zhongwen/simp/business/2015/08/150803_china_pmi','')
    bbc_crawler(url="http://www.bbc.com/zhongwen/simp")
    bbc_crawler(url="http://www.bbc.com/zhongwen/simp/chinese_news")
    bbc_crawler(url="http://www.bbc.com/zhongwen/simp/indepth")