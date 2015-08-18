# -*- coding: utf-8 -*-
# 繁体

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time
from Cleaners.langconv import *

r = redis.StrictRedis(host='localhost', port=6379)

source = u"文汇报"

def weiwenpo_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    story_text = []
    count = 0
    imgnum = 0

    story_links = tree.xpath('.//td[@align="center"]//a')

    for story_link in story_links:
        try:
            story_text_link = story_link.get("href")
        except:
            continue
        try:
            if r.sismember('duplicates', story_text_link) == True:
                continue
            story_title = story_link.text.strip()
            story_title = Converter('zh-hans').convert(story_title)
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

    update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    for x in tree.find('.//td[@align="left"]').iter():
        try:
            if x.tag == "p":
                t = x.text.strip()
                t = Converter('zh-hans').convert(t)
                if len(t) != 0:
                    dict = {}
                    dict[str(count)] = {}
                    dict[str(count)]["txt"] = t
                    count += 1
                    story_text.append(dict)
            if x.tag == "br":
                t = x.tail.strip()
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
                story_text.append(dict)
                imgnum += 1
        except:
            pass

    story_info = {
        'content': story_text,
        'source': source,
        'title': story_title,
        'url': url,
        'update_time': update_time,
        'imgnum': imgnum,
        'source_url': url,
        'sourceSiteName': source
        }

    return story_info

if __name__ == "__main__":
    weiwenpo_crawler(url="http://paper.wenweipo.com/001YO/")
    weiwenpo_crawler(url="http://paper.wenweipo.com/other/index-005WW-0.html")
    weiwenpo_crawler(url="http://paper.wenweipo.com/catList-s.php?cat=057PL&loc=any")
    weiwenpo_crawler(url="http://news.wenweipo.com/list_news.php?cat=000IN&instantCat=hk")
