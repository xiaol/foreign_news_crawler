# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR, openlog
from lxml import etree
from StringIO import StringIO
import re
from HTMLParser import HTMLParser
from sys import stderr
from traceback import print_exc

source = u"FT中文网"

def FTchinese_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="columncontent"]//div[@class="thcover" or @class="thleft" or @class="thright"]/a')

    for story_link in story_links:
        story_text_link = "http://www.ftchinese.com" + story_link.get("href")
        story_title = story_link.text.strip()
        story_text = get_text(story_text_link)

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_text = ''
    story_imgUrl = []

    for x in tree.xpath('.//p'):
        try:
            story_text = story_text + x.text.strip() + '\n'
        except:
            pass

    for x in tree.xpath('.//img'):
        try:
            story_imgUrl.append(x.get('src'))
        except:
            pass
    return story_text


if __name__ == "__main__":
    FTchinese_crawler(url = "http://www.ftchinese.com/channel/china.html")
    FTchinese_crawler(url="http://www.ftchinese.com/channel/asia.html")
    FTchinese_crawler(url="http://www.ftchinese.com/channel/chinaeconomy.html")
    FTchinese_crawler(url="http://www.ftchinese.com/channel/opinion.html")
