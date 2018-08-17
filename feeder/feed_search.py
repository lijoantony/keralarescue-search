#!/usr/bin/python
import urllib
import datetime
import pandas as pd
now = datetime.datetime.now()
run_id = now.strftime("%m%d_%H%M")

# 1. get data from database
# DATA_FILE = "../data_" + run_id # FIXME - now the url returns 403
# avoid download if file already downloaded in last 10mins


def save_data_json(url="https://keralarescue.in/data/", fetch=False):
    json_file = "../data.json"
    if fetch:
        json_file = "../data_" + run_id + ".json"
        urlFile = urllib.URLopener()
        urlFile.retrieve(url, json_file)
    return json_file


def getDistPlace(dist, loc):
    return loc + "(" + dist + ")"


def convert_json_to_csv(input_json):
    csv_file = "../data_" + run_id + ".csv"
    with open(input_json) as fh:
        data_frame = pd.read_json(fh)
        data_frame['district_full'] = pd.Series([getDistName(code) for code in data_frame['district']])
        data_frame['dist_place'] = pd.Series([getDistPlace(dist, loc) for (dist, loc) in
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


def getDistName(code):
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



json_file = save_data_json()

csv_file = convert_json_to_csv(json_file)

