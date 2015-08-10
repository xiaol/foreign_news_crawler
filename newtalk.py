# -*- coding: utf-8 -*-

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time

r = redis.StrictRedis(host='localhost', port=6379)

source = u"新头壳"

def newtalk_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@id="left_column"]//a')

    for story_link in story_links:
        try:
            story_text_link = story_link.get("href")
        except:
            continue
        try:
            if r.sismember('duplicates', story_text_link) == True:
                continue
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

    update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    story_imgUrl = []

    for x in tree.xpath('.//div[@id="news_content"]//img'):
        try:
            imgurl = x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = tree.find('.//txt').text.strip()

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    story_info = {
        'content': story_text,
        'source': source,
        'title': story_title,
        'img': story_imgUrl,
        'url': url,
        'update_time': update_time
        }


    return story_info

if __name__ == "__main__":
    # print get_text("http://newtalk.tw/news/view/2015-08-04/63023")
    newtalk_crawler(url="http://newtalk.tw/news/category/2/%E5%9C%8B%E9%9A%9B%E4%B8%AD%E5%9C%8B")