# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"中文导报网"

def chubun_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.td[@id="centercolumn"]//a')

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

    for x in tree.xpath('.//div[@id="content"]//img'):
        try:
            imgurl = x.get('src')
            story_imgUrl.append(imgurl)
        except:
            pass

    story_text = ''

    for x in tree.xpath('.//br'):
        try:
            story_text = story_text + x.tail.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    # print get_text("http://www.chubun.com/modules/article/view.article.php/c130/160142")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/120")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/5")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/6")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/91")
    chubun_crawler(url="http://www.chubun.com/modules/article/view.category.php/7")

