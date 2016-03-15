# coding: utf-8

import sys
import logging
import requests
from hashlib import sha256
import oss2


_logger = logging.getLogger(__name__)


access_key_id = "QK8FahuiSCpzlWG8"
access_key_secret = "TGXhTCwUoEU4yNEGsfZSDvp0dNqw2p"
auth = oss2.Auth(access_key_id, access_key_secret)
region = "http://oss-cn-qingdao.aliyuncs.com"
name = "news-images"
bucket = oss2.Bucket(auth, region, name)
image_url_prefix = "http://news-images.deeporiginalx.com"


image_type_mapping = {
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/x-png": ".png",
    "image/png": ".png",
}


def download_image(url):
    try:
        r = requests.get(url, timeout=10)
    except Exception:
        _logger.error("download image error: %s" % url)
        return None, None
    if r.status_code != 200:
        _logger.error("download image error: %s" % url)
        return None, None
    content_type = r.headers["Content-Type"]
    suffix = image_type_mapping.get(content_type, None)
    if suffix is None:
        _logger.error("error type: %s" % content_type)
        return None, None
    else:
        image_name = sha256(r.content).hexdigest() + suffix
        return image_name, r.content


def upload_image_to_oss(image_name, string):
    try:
        r = bucket.put_object(image_name, string)
    except Exception:
        _logger.error("upload image exception")
        return False
    if r.status != 200:
        _logger.error("upload image to oss error: %s" % r.status)
        return False
    return True


def oss_image_upload(url):
    image_name, string = download_image(url)
    if image_name is None and string is None:
        return None
    status = upload_image_to_oss(image_name, string)
    if not status:
        return None
    oss_image_url = region.replace("oss", name + ".img") + "/" + image_name
    oss_image_info = oss_image_url + "@info"
    try:
        response = requests.get(oss_image_info)
        info = response.json()
        image = {
            "img": image_url_prefix+"/"+image_name,
            "width": info["width"],
            "height": info["height"],
            "size": info["size"]
        }
    except Exception:
        return None
    else:
        return image


if __name__ == "__main__":
    url = sys.argv[1]
    print oss_image_upload(url)



