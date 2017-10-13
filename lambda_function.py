#!/usr/bin/env python2.6
import os
import urllib.request
import csv
import io
import datetime


def lambda_handler(event, context):

    endpoint = os.environ.get('ES_ENDPOINT')
    older_than = os.environ.get('OLDER_THAN', 30)
    method = os.environ.get('METHOD', "HEAD")

    today = datetime.date.today()

    keep_suffix = tuple((today - datetime.timedelta(days=o)).isoformat()
                        for o in range(0, older_than))

    indices_url = endpoint + "/_cat/indices"
    res = urllib.request.urlopen(indices_url)
    cr = csv.reader(io.TextIOWrapper(res), delimiter=" ", skipinitialspace=True)

    indices = [c[2] for c in cr]

    METHOD = method
    for i in indices:
        if i.startswith("."):
            continue

        if not i.endswith(keep_suffix):
            request = urllib.request.Request(endpoint+"/"+i)
            request.get_method = lambda: METHOD
            response = urllib.request.urlopen(request)
            print(METHOD, endpoint+"/"+i, response.read().decode('utf-8'))

    return "end"
