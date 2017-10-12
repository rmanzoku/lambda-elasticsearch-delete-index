#!/usr/bin/env python2.6
import os
import urllib.request
import csv
import io


def lambda_handler(event, context):

    endpoint = os.environ.get('ES_ENDPOINT')

    url = endpoint + "/_cat/indices"
    res = urllib.request.urlopen(url)
    cr = csv.reader(io.TextIOWrapper(res), delimiter=" ", skipinitialspace=True)

    indices = [c[2] for c in cr]

    print(indices)
    return "end"
