# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"中华电视公司"

def cts_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="content_left"]//a')

    for story_link in story_links:
        try:
            story_text_link = story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass
            
def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@class="content_left"]//img'):
        try:
            imgurl = x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = ''

    for x in tree.xpath('.//p'):
        try:
            story_text = story_text + x.text.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    cts_crawler(url="http://news.cts.com.tw/politics/index.html#cat_list")