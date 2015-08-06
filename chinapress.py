# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"中国报"

def chinapress_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.div[@class="listing"]//a')

    for story_link in story_links:
        try:
            story_text_link = "http://www.chinapress.com.my/" + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story = ''

    for x in tree.xpath('.//p'):
        try:
            story = story + x.text.strip() + '\n'
        except:
            pass
    return story

if __name__ == "__main__":
    # print get_text("http://www.chinapress.com.my/node/643110")
    chinapress_crawler(url="http://www.chinapress.com.my/taxonomy/term/93/all")