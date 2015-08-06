# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"联合国新闻"

def un_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        try:
            story_text_link = "http://www.un.org/chinese/News/" + story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_imgUrl = []

    for x in tree.xpath('.//div[@id="story-block"]//img'):
        try:
            imgurl = 'http:' + x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = tree.find('.//span[@class="date"]').tail.strip()

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text("http://www.un.org/chinese/News/story.asp?NewsID=24446")
    un_crawler(url="http://www.un.org/chinese/News/region.asp?regioncode=AS")