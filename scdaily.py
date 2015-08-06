# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"美南新闻"

def scdaily_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//tbody//a')

    for story_link in story_links:
        try:
            story_text_link = "http://www.scdaily.com/" + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_text = ''

    for x in tree.xpath('.//p'):
        try:
            story_text = story_text + x.text.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    scdaily_crawler(url="http://www.scdaily.com/Newslist_more.aspx?Bid=48&Cid=28")
    scdaily_crawler(url="http://www.scdaily.com/Newslist_more.aspx?Bid=48&Cid=34")