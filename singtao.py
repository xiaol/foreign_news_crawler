# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"星岛日报"

def singtao_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@id="left_ver2"]//a')

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

    story_text = tree.find('.//div[@class="content"]').text.strip()

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text('http://news.singtao.ca/toronto/2015-08-03/world1438590454d5707035.html')
    singtao_crawler(url="http://news.singtao.ca/toronto/world.html")
    singtao_crawler(url="http://news.singtao.ca/toronto/china.html")