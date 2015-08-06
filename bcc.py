# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"中广新闻网"

def bcc_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = 'http://www.bcc.com.tw/' + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story = tree.find('.//div[@id="some-class-name"]//span').tail
    nodes = tree.xpath('.//div[@id="some-class-name"]//br')

    for node in nodes:
        try:
            story = story + node.tail.strip()
        except:
            pass
    return story

if __name__ == "__main__":
    bcc_crawler(url="http://www.bcc.com.tw/newsList.%E5%85%A9%E5%B2%B8")
