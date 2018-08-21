#!/usr/bin/python3

import json
import os
import urllib.request

import pandas as pd

import feeder.common.config as config
from feeder.common.data import get_dist_name
from feeder.common.logger import log
from feeder.common.solr_helper import get_last_known_id_in_solr, feed_csv_to_solr, RESCUE_COLLECTION
from feeder.common.utils import my_sleep


def save_data_json(last_id, fetch=True):
    if fetch:
        url = config.API_URL + "?offset=" + last_id
        log("Downloading " + url)
        json_file1 = "/tmp/data_" + last_id + ".json"
        req = urllib.request.Request(url, headers=config.get_req_header())
        response = urllib.request.urlopen(req).read()
        json_obj = json.loads(response.decode('utf-8'))
        log("======= Meta ==========")
        log(json_obj['meta'])
        if json_obj and isinstance(json_obj['data'], list) and len(json_obj['data']) > 1:
            data = json_obj['data']
            with open(json_file1, "w") as fh:
                fh.write(json.dumps(data))
                return json_file1
    else:
        value = os.popen('ls -tr ../data*.json | tail -1').readlines()
        return str.strip(str(value[-1]))


def get_dist_place(dist, loc):
    return loc + "(" + dist + ")"


def convert_json_to_csv(json_file):
    csv_file = json_file.replace(".json", ".csv")
    with open(json_file) as fh:
        data_frame = pd.read_json(fh, dtype=False)
        data_frame['district_full'] = pd.Series([get_dist_name(code) for code in data_frame['district']])
        data_frame['dist_place'] = pd.Series([get_dist_place(dist, loc) for (dist, loc) in
                                              zip(data_frame['district_full'], data_frame['location'])])
        log("========= Json Data size ======")
        log(data_frame.shape)
        data_frame.rename(columns={
            'dateadded': 'last_modified',
            'detailcloth': 'detailcloth_t',
            'detailfood': 'detailfood_t',
            'detailkit_util': 'detailkit_util_t',
            'detailmed': 'detailmed_t',
            'detailrescue': 'detailrescue_t',
            'detailtoilet': 'detailtoilet_t',
            'detailwater': 'detailwater_t',
            'district': 'district_s',
            'dist_place': 'dist_place_t',
            'district_full': 'district_full_s',
            'id': 'id',
            'is_request_for_others': 'is_request_for_others_b',
            'latlng': 'location',
            'latlng_accuracy': 'latlng_accuracy_t',
            'location': 'place_s',
            'needcloth': 'needcloth_b',
            'needfood': 'needfood_b',
            'needkit_util': 'needkit_util_b',
            'needmed': 'needmed_b',
            'needothers': 'needothers_t',
            'needrescue': 'needrescue_b',
            'needtoilet': 'needtoilet_b',
            'needwater': 'needwater_b',
            'requestee': 'requestee_t',
            'requestee_phone': 'requestee_phone_t',
            'status': 'status_s',
            'supply_details': 'supply_details_t'
        }, inplace=True)
        data_frame.to_csv(csv_file, encoding="utf-8", index=False)
    return csv_file


def main():
    prev_last_id = 1
    iterations = 1
    has_more_data = True
    while has_more_data:
        last_id = get_last_known_id_in_solr()
        if int(prev_last_id) >= int(last_id):
            log("Failed Solr Not updating prev_last_id:" + prev_last_id + " cur_last_id:" + last_id)
            break
        json_file = save_data_json(last_id=last_id, fetch=True)
        if not json_file:
            log("No more data from api")
            break
        log("Saved Json File: " + json_file)
        csv_file_out = convert_json_to_csv(json_file)
        lines = os.popen("wc -l " + csv_file_out + "| awk '{print $1}'").read()
        lines = int(lines.strip())
        log("===============")
        log("Json converted to CSV: " + csv_file_out + " lines: " + str(lines))
        if lines > 1:
            feed_csv_to_solr(RESCUE_COLLECTION, csv_file_out)
            prev_last_id = last_id
            my_sleep(10)
        else:
            has_more_data = False
        iterations += 1
        if iterations > 10:
            break

# Run Main
main()
