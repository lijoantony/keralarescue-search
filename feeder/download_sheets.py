#!/usr/local/bin/python3

import json
import os
import sys
import time
import datetime as dt

import pandas as pd

import common.config as config
from common.logger import log

TOKEN = "<token>";

SHEETS = [{
    "name": "Camps profile_RCIS_KeralaFloods2018 (Responses)",
    "id": "1GGNN8DuqbreSOo8Pw_3A0C_Pl6HJn2tcZaicMNyv9sk",
    "worksheet": 0,
    "ignoreRows": [],
}, {
    "name": "Emergency supplies: non-food, non-medical  (Responses)",
    "id": "1HxH7z7f0UZQ6LeIHxUClOLoMtZkvHlLeyGT4mG9fSfM",
    "worksheet": 0,
    "ignoreRows": [],
}, {
    "name": "Food Donor Registration Form (Responses)",
    "id": "14JKwRWLFG1w_j6e02lUlSRqfXyPvlq1fLzQwHWfhuX0",
    "worksheet": 0,
    "ignoreRows": [],
}, {
    "name": "Inventory Updates_KeralaFloods2018 (Responses)",
    "id": "1UWP8AJkKYNp2pyEwfxnWOlbRMFStW8kBnatLYbFITAE",
    "worksheet": 0,
    "ignoreRows": [],
}, {
    "name": "Medical Emergency Requirement Form (Responses)",
    "id": "1FEsr2eI_6Ph5BbxAVF699gpKjp_-yDThhPl4WUDo7L0",
    "worksheet": 0,
    "ignoreRows": [],
}, {
    "name": "Non-emergency materials requirement_v1.0",
    "id": "1ZjQP-rTh9RTr2APaRLOmXI6_-sX6HwhT2XKVOGDZRSc",
    "worksheet": 0,
    "ignoreRows": [1],
}, {
    "name": "Refugee Profile_RCIS_KeralaFloods2018 (Responses)",
    "id": "18ybIz_z9Dw8T069jIMPMWgLEntn5CzbeFNC7sWpgXAE",
    "worksheet": 0,
    "ignoreRows": [],
}, {
    "name": "Volunteer Profile_RCIS_KeralaFloods2018 (Responses)",
    "id": "1rOn5R9j5ciHJE4e5QUdQI-PjNLhHpvLtDUzOOGvS99w",
    "worksheet": 0,
    "ignoreRows": [],
# }, {
#     "name": "Emergency Food: Supply-Demand-Delivery Form (Responses)",
#     "id": "1qgGVGS2SOd5JkkFsXcWKwQol2TFwhB",
#     "worksheet": 0,
#     "ignoreRows": [],
# }, {
#     "name": "Food Distributor Registration Form (Responses)",
#     "id": "11662sIeMZBoYZ73IsAONRrLpBIntgPtv6x2",
#     "worksheet": 0,
#     "ignoreRows": [],
}
]


def save_csv_file(csv, filename):
    with open(filename, "w") as fh:
        fh.write(csv)
        return filename

def fix_excel_date(data_frame):
    epoch = dt.datetime(1899, 12, 30)
    if 'timestamp' in data_frame.columns:
        data_frame['timestamp'] = pd.TimedeltaIndex(data_frame['timestamp'], unit='d') + epoch
    if 'campOpeningDate' in data_frame.columns:
        data_frame['campOpeningDate'] = pd.TimedeltaIndex(data_frame['campOpeningDate'], unit='d') + epoch
    if 'campClosingDate' in data_frame.columns:
        data_frame['campClosingDate'] = pd.TimedeltaIndex(data_frame['campClosingDate'], unit='d') + epoch

def convert_json_to_csv(json):
    data_frame = pd.read_json(json, dtype=False)

    log("===============================")
    log(data_frame.shape)

    data_frame.rename(columns={
        'campClosingDate(ifApplicable)': 'campClosingDate',
        'location(whereYouCan/areVolunteering)': 'location',
        'pinCode(ofThePlaceYouCan/areServing)': 'pinCode',
    }, inplace=True)

    fix_excel_date(data_frame)

    csv = data_frame.to_csv(None, encoding="utf-8", index=False)
    return csv


def download_sheet(sheet):
    prev_last_id = 1
    has_more_data = True

    while has_more_data:
        cmd = "gsjson {} -w {} -t {}".format(sheet["id"], str(sheet["worksheet"]), TOKEN)

        if len(sheet["ignoreRows"]):
            cmd += " --ignore-row " + " --ignore-row ".join(str(i) for i in sheet["ignoreRows"])

        json = os.popen(cmd).read()

        csv = convert_json_to_csv(json)
        filename = sheet["name"] + "_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        log(filename)
        json_file = save_csv_file(csv, filename)
        has_more_data = False


def main():
    for sheet in SHEETS:
        download_sheet(sheet)


# Run Main
main()
