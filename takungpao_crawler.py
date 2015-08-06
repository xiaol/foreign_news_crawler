# -*- coding: utf-8 -*-

from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

source = u"大公网"

#首页->要闻
def news_takungpao_crawler(url="http://news.takungpao.com/index.html"):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="txtImgListeach current"]//h3/a')

    for story_link in story_links:
        try:
            story_text_link = story_link.get("href")
            story_text = get_text(story_text_link)
            story_title = story_link.text.strip()
        except:
            pass

#首页->观点->栏目->大公社评
#首页->观点->栏目->指点香江
#首页->观点->栏目->井水集
#首页->观点->栏目->北京观察
def takungpao_crawler_others(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//div[@class="groom_title"]//a')

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

    story_text = ''

    for x in tree.xpath('.//p'):
        try:
            story_text = story_text + x.text.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    news_takungpao_crawler()
    takungpao_crawler_others(url="http://news.takungpao.com/special/zhdxj/")
    takungpao_crawler_others(url="http://news.takungpao.com/special/shp/")
    takungpao_crawler_others(url="http://news.takungpao.com/special/jshj/")
    takungpao_crawler_others(url="http://news.takungpao.com/special/bjgc/")
