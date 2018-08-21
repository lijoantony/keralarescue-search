import json
import os
import urllib.request

from feeder.common import config as config
from feeder.common.logger import log

RESCUE_COLLECTION = "krescue10"


def get_last_known_id_in_solr():
    url = config.SOLR_URL + "?fl=id&q=*:*&rows=1&sort=last_modified%20desc"
    req = urllib.request.Request(url, headers=config.get_req_header())
    response = urllib.request.urlopen(req).read()
    json_obj = json.loads(response.decode('utf-8'))
    if json_obj and isinstance(json_obj['response']['docs'], list):
        return json_obj['response']['docs'][0]['id']


def feed_csv_to_solr(collection, csv_file):
    log("Feeding data to solr")
    log(os.popen("/opt/solr/bin/post -c " + collection + csv_file).readlines())
