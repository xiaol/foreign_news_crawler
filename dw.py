# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"德国之声"

def dw_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = 'http://www.dw.com/' + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass
            
def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@id="bodyContent"]//img'):
        try:
            imgurl = "http://www.dw.com" + x.get('src')
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
    # print get_text("http://www.dw.com/zh/%E9%80%83%E7%A5%A8%E7%BD%9A%E6%AC%BE%E6%9B%B4%E7%8B%A0-%E9%80%83%E7%A5%A8%E8%80%85%E6%AD%AA%E6%8B%9B%E6%9B%B4%E5%A4%9A/a-18620459")
    dw_crawler("http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E9%9D%9E%E5%B8%B8%E5%BE%B7%E5%9B%BD/s-101347")
    dw_crawler("http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E6%97%B6%E6%94%BF%E9%A3%8E%E4%BA%91/s-1681")
    dw_crawler("http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E8%AF%84%E8%AE%BA%E5%88%86%E6%9E%90/s-100993")