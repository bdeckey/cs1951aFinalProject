#!/usr/bin/env python

import urllib
from urllib.parse import urlencode
import requests
import datetime
import time
import json
from os.path import dirname, realpath

api = 'https://api.pushshift.io/reddit/search/submission/?'


def getDayAfter(year, month, day):
    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        if (day != 31):
            return (year, month, day+1)
        else:
            if (month != 12):
                return (year, month+1, 1)
            else:
                return (year+1, 1, 1)
    if (month == 4 or month == 6 or month == 9 or month == 11):
        if (day != 30):
            return (year, month, day+1)
        else:
            return (year, month+1, 1)
    if (month == 2):
        if (day != 28):
            return (year, month, day+1)
        else:
            return (year, month+1, 1)

def collectData(year, month, day):
    nextDay = getDayAfter(year, month, day)
    after = datetime.datetime(year, month, day, 0).timestamp()
    before = datetime.datetime(nextDay[0], nextDay[1], nextDay[2], 0).timestamp()
    newUrl = urllib.parse.urlencode({'q': 'cryptocurrency', 'after': str(int(after)), 'before': str(int(before)), 'size': str(500)})
    res = requests.get(api + newUrl + "&score=>10")
    print(year, month, day)
    result = []
    if res.ok:
        data = json.loads(res.content)
        numSubmissions = len(data['data'])
        print("the number of results: ", len(data['data']))
        for item in data['data']:
            title = item['title']
            score = item['score']
            created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['created_utc']))
            result += [{'title': title, 'score':score, 'created':created}]
        return {'submissionCount':numSubmissions, 'submissions':result}
    else:
        print("Error Connectiong")
        return ("Error", result)



startYear = 2013
data = {}
for year in range(startYear, 2019):
    for month in range(1, 13):
        if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            for day in range(1, 32):
                date = str(month) + '-' + str(day) + '-' + str(year)
                data[date] = collectData(year, month, day)
        if (month == 4 or month == 6 or month == 9 or month == 11):
            for day in range(1, 31):
                date = str(month) + '-' + str(day) + '-' + str(year)
                data[date] = collectData(year, month, day)
        if (month == 2):
            for day in range(1, 29):
                date = str(month) + '-' + str(day) + '-' + str(year)
                data[date] = collectData(year, month, day)

with open(dirname(realpath(__file__)) + '/reddit.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)