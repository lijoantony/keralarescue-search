import datetime
import time
import urllib.request

from feeder.common import config as config


def get_run_id():
    now = datetime.datetime.now()
    return now.strftime("%m%d_%H%M")


def my_sleep(sec):
    from feeder.common.logger import log
    if sec < 2:
        log("Sleeping. < 2sec")
        time.sleep(sec)
        return
    for i in range(sec):
        log("Sleeping...")
        time.sleep(1)


def get_data_from_url(url):
    req = urllib.request.Request(url, headers=config.get_req_header())
    response = urllib.request.urlopen(req).read()
    return response.decode('utf-8')


