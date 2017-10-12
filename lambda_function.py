#!/usr/bin/env python2.6
import os
import urllib.request
import csv
import io
import datetime


def lambda_handler(event, context):

    endpoint = os.environ.get('ES_ENDPOINT')
    older_than = os.environ.get('OLDER_THAN', 30)

    today = datetime.date.today()

    keep_suffix = tuple((today - datetime.timedelta(days=o)).isoformat()
                        for o in range(0, older_than))

    url = endpoint + "/_cat/indices"
    res = urllib.request.urlopen(url)
    cr = csv.reader(io.TextIOWrapper(res), delimiter=" ", skipinitialspace=True)

    indices = [c[2] for c in cr]
    delete_indices = []

    for i in indices:
        if i.startswith("."):
            continue

        if not i.endswith(keep_suffix):
            delete_indices.append(i)

    print(delete_indices)
    return "end"
