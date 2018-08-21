import datetime
import time


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
