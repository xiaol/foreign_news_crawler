# -*- coding: utf-8 -*-

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time

r = redis.StrictRedis(host='localhost', port=6379)

source = u"德国之声"

def dw_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = 'http://www.dw.com' + story_link.get("href")
        except:
            continue
        try:
            if r.sismember('duplicates', story_text_link) == True:
                continue
            story_title = story_link.find('.//h2').text.strip()
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

    story_text = []
    count = 0
    imgnum = 0

    for x in tree.find('.//div[@id="bodyContent"]').iter():
        try:
            if x.tag == "p":
                t = x.text.strip()
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
                dict[str(count)]["img"] = 'http://www.dw.com/zh' + x.get("src")
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
    # print get_text("http://www.dw.com/zh/%E9%80%83%E7%A5%A8%E7%BD%9A%E6%AC%BE%E6%9B%B4%E7%8B%A0-%E9%80%83%E7%A5%A8%E8%80%85%E6%AD%AA%E6%8B%9B%E6%9B%B4%E5%A4%9A/a-18620459")
    dw_crawler("http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E9%9D%9E%E5%B8%B8%E5%BE%B7%E5%9B%BD/s-101347")
    dw_crawler("http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E6%97%B6%E6%94%BF%E9%A3%8E%E4%BA%91/s-1681")
    dw_crawler("http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E8%AF%84%E8%AE%BA%E5%88%86%E6%9E%90/s-100993")