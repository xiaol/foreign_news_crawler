# -*- coding: utf-8 -*-
# 修改完毕

from crawler_framework.page import get_page
from crawler_framework.Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback
import redis
import time

r = redis.StrictRedis(host='localhost', port=6379)

source = u"中文导报网"

def chubun_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//td[@id="centercolumn"]//a')

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

    create_time = time.strftime('%Y-%m-%d %H:%M:%S')

    story_text = []
    count = 0
    imgnum = 0

    for x in tree.find('.//div[@id="content"]').iter():
        try:
            if x.tag == "p":
                t = x.find('.//font').text.strip()
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
                if "uploads" in x.get("src"):
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
        'create_time': create_time,
        'imgnum': imgnum,
        'source_url': url,
        'sourceSiteName': source
        }


    return story_info

if __name__ == "__main__":
    # print get_text("http://www.chubun.com/modules/article/view.article.php/c130/160142")
    # print get_text("http://www.chubun.com/modules/article/view.article.php/c7/160448",'')
    # get_text("http://www.chubun.com/modules/article/view.article.php/c145/160586",'')
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/120")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/5")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/6")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/91")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/7")

