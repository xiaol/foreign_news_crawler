# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"头条日报"

def stheadline_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = "http://hd.stheadline.com/" + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@class="content"]//img'):
        try:
            imgurl = 'http:' + x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    print imgurl

    story_text = tree.find('.//span[@class="set-font-aera"]').text.strip()

    for x in tree.xpath('.//span[@class="set-font-aera"]//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text("http://hd.stheadline.com/news/realtime/hk/995366/")
    stheadline_crawler(url="http://hd.stheadline.com/news/realtime/hk/")