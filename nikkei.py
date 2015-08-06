# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"日经中文网"

def nikkei_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = "http://cn.nikkei.com" + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@class="text"]//img'):
        try:
            imgurl = 'http://cn.nikkei.com' + x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = tree.find('.//div[@class="text"]').text.strip()

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text('http://cn.nikkei.com/china/cfinancial/15413-20150728.html')
    nikkei_crawler(url="http://cn.nikkei.com/china.html")
    nikkei_crawler(url="http://cn.nikkei.com/politicsaeconomy.html")
    nikkei_crawler(url="http://cn.nikkei.com/columnviewpoint.html")