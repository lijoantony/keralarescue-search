#!/usr/bin/python
import datetime
import os
import urllib

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


def save_data_json(url="https://keralarescue.in/data/", fetch=False):
    if fetch:
        json_file1 = "../data_" + run_id + ".json"
        request = urllib.request.Request(url, headers=customHeader)
        json_str = urllib.urlopen(request).read()
        with open(json_file1, "w") as fh:
            fh.write(json_str)
            return json_file1
    else:
        value = os.popen('ls -tr ../data* | tail -1').readlines()
        return str.strip(str(value[-1]))


def get_dist_place(dist, loc):
    return loc + "(" + dist + ")"


def convert_json_to_csv(input_json):
    csv_file = "../data_" + run_id + ".csv"
    with open(input_json) as fh:
        data_frame = pd.read_json(fh)
        data_frame['district_full'] = pd.Series([get_dist_name(code) for code in data_frame['district']])
        data_frame['dist_place'] = pd.Series([get_dist_place(dist, loc) for (dist, loc) in
                                              zip(data_frame['district_full'], data_frame['location'])])
        print(data_frame.shape)
        print("============")
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
    print("Feeding data to solr")
    print(os.popen("/opt/solr/bin/post -c krescue10  " + csv_file).readlines());

json_file = save_data_json(fetch=False)
print("Saved Json File: ", json_file)
csv_file_out = convert_json_to_csv(json_file)
print("Json converted to CSV: ", csv_file_out)
feed_csv_to_solr(csv_file_out)
