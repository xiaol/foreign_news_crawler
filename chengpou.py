# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"正报"

def chengpou_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="n-width rbd-daily-news-c-two c-w-border"]//a')

    for story_link in story_links:
        story_text_link = story_link.get("href")
        try:
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story = tree.find('.//div[@id="rbd-daily-news-content"]//p').tail.strip()
    for br in tree.xpath('.//div[@id="rbd-daily-news-content"]//br'):
        story = story + br.tail
    return story

if __name__ == "__main__":
    # get_text("http://www.chengpou.com.mo/cp-page/dailynews/?d=41198")
    chengpou_crawler(url="http://www.chengpou.com.mo/cp-page/?d=41169")
    chengpou_crawler(url="http://www.chengpou.com.mo/cp-page/?d=41172")
    chengpou_crawler(url="http://www.chengpou.com.mo/cp-page/?d=41175")
    chengpou_crawler(url="http://www.chengpou.com.mo/cp-page/?d=41179")