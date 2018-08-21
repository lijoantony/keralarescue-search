import pandas as pd

from common.config import CAMP_ALAPY_SHEET
from common.config import CAMP_TEST_SHEET
from common.data import get_dist_name, get_location_concact
from common.logger import log
from common.my_pandas import  pandas_read_tsv_str
from common.utils import get_data_from_url


def load_tsv(sheet_url):
    tsv_str = get_data_from_url(sheet_url, cache=True)
    dataf = pandas_read_tsv_str(tsv_str)
    log("Loaded data from ")
    log(dataf.shape)
    log(dataf.columns)
    return dataf

'''
['District', 'Camp Name', 'Address', 'Region', 'Contact Numbers', 'Men',
       'Women ', 'Kids', 'Infants', 'Total People', 'Requirement']
'''


def get_solr_feed_file(data_frame):
    data_frame['district_full'] = pd.Series([get_dist_name(code) for code in data_frame['District']])
    data_frame['location'] = pd.Series([get_location_concact(location) for location in
                                        zip(data_frame['Camp Name'], data_frame['Address'], data_frame['Region'])])
    #print(data_frame['location'][1])

    '''
    FIXME - work in progress

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
    '''


# get all camp data of alappy currently in solr ( ids can be marked as closed)

# get fresh data
log("Get fresh camp data from test sheet")
data_frame = load_tsv(CAMP_TEST_SHEET)
feed_file = get_solr_feed_file(data_frame)

