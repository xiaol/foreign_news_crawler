# -*- coding: utf-8 -*-
# 从这里开始
from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"今日新闻"

def nownews_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//ul[@id="result-list"]//a')

    for story_link in story_links:
        try:
            story_text_link = "http://huasons.nownews.com/" + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@class="story_content"]//img'):
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
    nownews_crawler(url="http://www.nownews.com/cat/china/r")
    nownews_crawler(url="http://huasons.nownews.com/cat/topic")