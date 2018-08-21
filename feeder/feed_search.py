#!/usr/bin/python3

import json
import os
import sys
import datetime as dt

import pandas as pd

import common.config as config
from common.data import get_dist_name
from common.logger import log
from common.solr_helper import get_last_known_id_in_solr, feed_csv_to_solr, RESCUE_COLLECTION
from common.utils import my_sleep, get_data_from_url


def excel_date(date1):
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def save_csv_file(csv):
    filename = "./data" + "" + ".csv"

    with open(filename, "w") as fh:
        fh.write(csv)
        return filename

def convert_json_to_csv(json):
    data_frame = pd.read_json(json, dtype=False)
    data_frame['timestamp'] = pd.TimedeltaIndex(data_frame['timestamp'], unit='d') + dt.datetime(1899, 12, 30)

    log("========= Json Data size ======")
    log(data_frame.shape)
    # data_frame.rename(columns={
    #     'timestamp': 'created_at',
    # }, inplace=True)
    csv = data_frame.to_csv(None, encoding="utf-8", index=False)
    print (csv)
    return csv


def main():
    prev_last_id = 1
    iterations = 1
    has_more_data = True
    spreadsheet_id = "1wghH0mfgkvJiTZQAeNr57aWiiS6D2Pfy6FRTLhjhDaU"

    while has_more_data:

        cmd = "gsjson " + spreadsheet_id + " -b -t " + TOKEN
        json = os.popen(cmd).read()
        #print(json)

        csv = convert_json_to_csv(json)
        json_file = save_csv_file(csv)
        print (json_file)
        has_more_data = False

# Run Main
main()
