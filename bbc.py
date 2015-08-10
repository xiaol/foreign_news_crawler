# -*- coding: utf-8 -*-

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

    update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    story_imgUrl = []

    for x in tree.xpath('.//div[@class="column--primary"]//img'):
        try:
            imgurl = x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = ''

    for x in tree.xpath('.//div[@class="column--primary"]//p'):
        try:
            story_text = story_text + x.text.strip() + '\n'
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
    # print get_text('http://www.bbc.com/zhongwen/simp/business/2015/08/150803_china_pmi')
    bbc_crawler(url="http://www.bbc.com/zhongwen/simp")
    bbc_crawler(url="http://www.bbc.com/zhongwen/simp/chinese_news")
    bbc_crawler(url="http://www.bbc.com/zhongwen/simp/indepth")