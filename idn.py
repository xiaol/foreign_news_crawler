# -*- coding: utf-8 -*-

# 编码有问题，暂时不管

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"自立晚报"

def idn_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = 'http://www.idn.com.tw/news/' + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass
            
def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_text = ''

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text("http://www.idn.com.tw/news/news_content.php?catid=2&catsid=5&catdid=0&artid=20150802abcd011")
    idn_crawler(url="http://www.idn.com.tw/news/news_list.php?catid=2&catsid=5")