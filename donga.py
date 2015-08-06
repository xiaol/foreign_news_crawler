# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"东亚日报"

def donga_crawler(url):
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

    story_text = tree.find('.//td[@class="dotum-16-2d2d2d"]').text.strip()

    for x in tree.xpath('.//p'):
        try:
            story_text = story_text + x.text.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text("http://chinese.donga.com/gb/srv/service.php3?bicode=040000&biid=2015080403018")
    donga_crawler(url="http://chinese.donga.com/gb/national/")