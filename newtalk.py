# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"新头壳"

def newtalk_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@id="left_column"]//a')

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

    for x in tree.xpath('.//div[@id="news_content"]//img'):
        try:
            imgurl = x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = tree.find('.//txt').text.strip()

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text("http://newtalk.tw/news/view/2015-08-04/63023")
    newtalk_crawler(url="http://newtalk.tw/news/category/2/%E5%9C%8B%E9%9A%9B%E4%B8%AD%E5%9C%8B")