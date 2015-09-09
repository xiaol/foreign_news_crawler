from oss.oss_api import *
import urllib2
import time
from crawler_framework.page import get_page

def save_to_oss(url):
    now = time.localtime()
    year = now.tm_year
    month = now.tm_mon
    day = now.tm_mday
    folder = str(year)+str(month)+str(day)
    name = url.split('/')[-1]
    s = urllib2.urlopen(url).read()
    oss = OssAPI("oss-cn-qingdao.aliyuncs.com","QK8FahuiSCpzlWG8","TGXhTCwUoEU4yNEGsfZSDvp0dNqw2p")
    oss.put_object_from_string("news-baijia-waimei-pictures",name,s,"image/jpg")
    link = "http://news-baijia-waimei-pictures.oss-cn-qingdao.aliyuncs.com/" + name
    return link

if __name__ == "__main__":
    print save_to_oss('zuoyuan')
