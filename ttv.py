# -*- coding: utf-8 -*-
# 编码为big5 是乱码
from page import get_page
from Logger import INFO, DBG, ERR
from lxml import etree
from StringIO import StringIO

def ttv_crawler(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_links = tree.xpath('.//a')

    for story_link in story_links:
        story_text_link = 'http://www.ttv.com.tw' + story_link.get("href")
        story_text = get_text(story_text_link)
        story_title = story_link.text.strip()

def get_text(url):
    text = get_page(url)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), parser)

    story_text = ''

    for x in tree.xpath('.//div[@id="VarTxtS0"]'):
        try:
            story_text = story_text + x.text.strip() + '\n'
        except:
            pass
    return story_text

if __name__ == "__main__":
    print get_text("http://www.ttv.com.tw/104/08/1040804/10408040012100A.htm?from=579")
    # ttv_crawler(url="http://www.ttv.com.tw/news/newsContentG.htm")