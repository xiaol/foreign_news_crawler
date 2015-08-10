# -*- coding: utf-8 -*-

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time

r = redis.StrictRedis(host='localhost', port=6379)

source = u"中央日报"

def cdnews_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="pictxt_list"]//a')

    for story_link in story_links:
        try:
            story_text_link = "http://www.cdnews.com.tw/cdnews_site/" + story_link.get("href")
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

    for x in tree.xpath('.//div[@class="content_body"]//img'):
        try:
            imgurl = "http://www.cdnews.com.tw" + x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    nodes = tree.xpath('.//div[@class="content_body"]//br')
    story_text = ''
    for node in nodes:
        try:
            story_text = story_text + node.tail.strip() + '\n'
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
    cdnews_crawler(url="http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=110")
    cdnews_crawler(url="http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=111")
