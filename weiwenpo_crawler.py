# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"文汇报"

def weiwenpo_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

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

    for x in tree.xpath('.//td[@align="center"]//img'):
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
    weiwenpo_crawler(url="http://paper.wenweipo.com/001YO/")
    weiwenpo_crawler(url="http://paper.wenweipo.com/other/index-005WW-0.html")
    weiwenpo_crawler(url="http://paper.wenweipo.com/catList-s.php?cat=057PL&loc=any")
    weiwenpo_crawler(url="http://news.wenweipo.com/list_news.php?cat=000IN&instantCat=hk")
