#!/usr/bin/python3
import datetime
import os
import urllib.request
import json
import time

import pandas as pd

now = datetime.datetime.now()
run_id = now.strftime("%m%d_%H%M")

# 1. get data from database
# DATA_FILE = "../data_" + run_id # FIXME - now the url returns 403
# avoid download if file already downloaded in last 10mins

customHeader = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}

API_URL = "https://keralarescue.in/data"
SOLR_URL = "http://localhost:8983/solr/krescue10/select"


def log(message, error=False):
    error_str = "ERROR" if error else "INFO"
    print("[%s] %s: %s" % (run_id, error_str, message))


def get_last_known_id_in_solr():
    url = SOLR_URL + "?fl=id&q=*:*&rows=1&sort=last_modified%20desc"
    req = urllib.request.Request(url, headers=customHeader)
    response = urllib.request.urlopen(req).read()
    json_obj = json.loads(response.decode('utf-8'))
    if json_obj and isinstance(json_obj['response']['docs'], list):
        return json_obj['response']['docs'][0]['id']


def save_data_json(last_id, fetch=True):
    if fetch:
        url = API_URL + "?offset=" + last_id
        log("Downloading " + url)
        json_file1 = "/tmp/data_" + last_id + ".json"
        req = urllib.request.Request(url, headers=customHeader)
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


def get_dist_name(code):
    code_to_name = {
         'tvm': 'Thiruvananthapuram',
         'ptm': 'Pathanamthitta',
         'alp': 'Alappuzha',
         'ktm': 'Kottayam',
         'idk': 'Idukki',
         'mpm': 'Malappuram',
         'koz': 'Kozhikode',
         'wnd': 'Wayanad',
         'knr': 'Kannur',
         'ksr': 'Kasaragod',
         'pkd': 'Palakkad',
         'tcr': 'Thrissur',
         'ekm': 'Ernakulam',
         'kol': 'Kollam'
    }
    return code_to_name[code]


def feed_csv_to_solr(csv_file):
    log("Feeding data to solr")
    log(os.popen("/opt/solr/bin/post -c krescue10  " + csv_file).readlines())


def my_sleep(sec):
    if sec < 2:
        log("Sleeping. < 2sec")
        time.sleep(sec)
        return
    for i in range(sec):
        log("Sleeping...")
        time.sleep(1)


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
            feed_csv_to_solr(csv_file_out)
            prev_last_id = last_id
            my_sleep(10)
        else:
            has_more_data = False
        iterations += 1
        if iterations > 10:
            break

# Run Main
main()
