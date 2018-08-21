import hashlib
import time
import urllib.request

from feeder.common import config as config


def my_sleep(sec):
    from feeder.common.logger import log
    if sec < 2:
        log("Sleeping. < 2sec")
        time.sleep(sec)
        return
    for i in range(sec):
        log("Sleeping...")
        time.sleep(1)


def get_data_from_url(url, cache=False):
    from feeder.common.logger import log

    if not cache:
        log("Getting data from " + url)
        return _get_data_from_url(url)

    cache_file_name = "/tmp/" + hashlib.md5(url.encode('utf-8')).hexdigest()
    log("Using cache " + cache_file_name)
    try:
        fh = open(cache_file_name, "r")
        cache_str = fh.read()
        fh.close()
        return cache_str
    except IOError:
        log("Cahe Miss - Failed to read " + cache_file_name, error=True)
        log("Getting data from " + url)
        string = _get_data_from_url(url)
        with open(cache_file_name, "w") as fw:
            fw.write(string)
            fw.close()
        return string


def _get_data_from_url(url):
    req = urllib.request.Request(url, headers=config.get_req_header())
    response = urllib.request.urlopen(req).read()
    string = response.decode('utf-8')
    return string

