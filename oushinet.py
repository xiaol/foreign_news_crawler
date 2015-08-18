# -*- coding: utf-8 -*-

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time

r = redis.StrictRedis(host='localhost', port=6379)

source = u"欧洲时报"

def oushinet_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="main"]//a')

    for story_link in story_links:
        try:
            story_text_link = url + story_link.get("href")
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
            print traceback.format_exc(),url
            pass

def get_text(url, story_title):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    story_text = []
    count = 0
    imgnum = 0

    for x in tree.find('.//div[@id="artMain"]').iter():
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
    oushinet_crawler(url="http://dujia.oushinet.com/")
    oushinet_crawler(url="http://huashe.oushinet.com/")
    oushinet_crawler(url="http://huashe.oushinet.com/csac/")
    oushinet_crawler(url="http://huashe.oushinet.com/cbs/")
    oushinet_crawler(url="http://huashe.oushinet.com/tmal/")
    oushinet_crawler(url="http://huashe.oushinet.com/cstw/")
    oushinet_crawler(url="http://huashe.oushinet.com/sd/")
    oushinet_crawler(url="http://huashe.oushinet.com/aooc/")
    oushinet_crawler(url="http://zhongguo.oushinet.com/")
    oushinet_crawler(url="http://zhongguo.oushinet.com/fmsc/")
    oushinet_crawler(url="http://zhongguo.oushinet.com/gmsc/")
    oushinet_crawler(url="http://zhongguo.oushinet.com/fic/")
    oushinet_crawler(url="http://zhongguo.oushinet.com/pocet/")