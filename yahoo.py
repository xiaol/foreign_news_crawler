# -*- coding: utf-8 -*-

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time
import re
from Cleaners.langconv import *

r = redis.StrictRedis(host='localhost', port=6379)

source = u"YAHOO新闻网"

def yahoo_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="content"]//a')

    for story_link in story_links:
        try:
            story_text_link = "https://hk.news.yahoo.com" + story_link.get("href")
            # print story_text_link
        except:
            continue
        try:
            if r.sismember('duplicates', story_text_link) == True:
                continue
            # story_title = re.search("<a.*?>(.+?)</a>", text).group(1)
            story_title = story_link.text
            if story_title == None:
                continue
            else:
                story_title = story_title.strip()
            story_title = Converter('zh-hans').convert(story_title)
            print story_title
            story_info = get_text(story_text_link, story_title)
            story_text = story_info['content']
            if len(story_text) == 0:
                continue
            r.sadd('duplicates', story_text_link)
            r.rpush('stories', story_info)
        except:
            # print traceback.format_exc()
            pass

def get_text(url, story_title):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    story_text = []
    count = 0
    imgnum = 0

    for x in tree.find('.//div[@class="yog-wrap yom-art-bd"]').iter():
        try:
            if x.tag == "p":
                t = x.text.strip()
                t = Converter('zh-hans').convert(t)
                print t
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
                print dict[str(count)]["img"]
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
    yahoo_crawler(url="https://hk.news.yahoo.com/")
    # text = get_page(url)
    # get_text("https://hk.news.yahoo.com/%E5%9C%8B%E6%B3%B0%E9%A3%9B%E7%B4%90%E7%B4%84%E8%88%AA%E7%8F%AD%E5%BB%B6%E9%98%BB17%E5%B0%8F%E6%99%82-214050238.html","")
    # text = '''<a href="http://hk.news.yahoo.com/%E4%BF%9D%E5%AE%89%E5%93%A1%E7%88%AC%E9%90%B5%E6%A2%AF%E8%90%BD%E6%B3%B5%E6%88%BF%E5%A4%B1%E8%B6%B3%E5%A2%AE%E5%9D%91%E4%BA%A1-125749917.html"   data-ylk="rspns:nav;t1:a4;t2:app-toph;t3:ct;sec:app-toph;elm:hdln;elmt:ct;itc:0;cpos:1;g:436c9873-a57a-3997-a32f-013d7842bc36;">保安員爬鐵梯落泵房失足墮坑亡</a>'''
    # get_text("https://hk.news.yahoo.com/-031217276.html","")

    # import re
    # print re.search("<a.*?>(.+?)</a>", text).group(1)