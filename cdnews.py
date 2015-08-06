# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO
import traceback

source = u"中央日报"

def cdnews_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="pictxt_list"]//a')

    for story_link in story_links:
        story_text_link = "http://www.cdnews.com.tw/cdnews_site/" + story_link.get("href")
        try:
            story_text = get_text(story_text_link)
            if len(story_text) == 0:
                continue
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@class="content_body"]//img'):
        try:
            imgurl = "http://www.cdnews.com.tw" + x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    nodes = tree.xpath('.//div[@class="content_body"]//br')
    story = ''
    for node in nodes:
        try:
            story = story + node.tail.strip() + '\n'
        except:
            pass
    return story

if __name__ == "__main__":
    cdnews_crawler(url="http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=110")
    cdnews_crawler(url="http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=111")
