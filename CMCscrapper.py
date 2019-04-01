#!/usr/bin/env python

from bs4 import BeautifulSoup
import sqlite3
import argparse
import json
from os.path import dirname, realpath

def parse_args():
    parser = argparse.ArgumentParser(description='Program to turn CoinMarketCap html page into JSON and SQL db')
    parser.add_argument('-json', action='store_true')
    parser.add_argument('-sql', action='store_true')
    parser.add_argument('-f', help='path to HTML file')
    parser.add_argument('-n', help='name for files / cryptocurreny name')
    return parser.parse_args()

args = parse_args()


if args.f is None:
    print("Please give a file path.")
    exit()

file = args.f

with open(file) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# set up dictionary for data and get all the rows for scraping data
dataSQL = {}
dataJSON = {}
table = soup.find('table', attrs={'class':'table'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')

for row in rows:
    # set up variables
    date = 'date'
    openInfo = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    marketCap = 'marketCap'

    cols = row.find_all('td')
    vals = []
    # there are no labels so we set up a column counter
    col_num = 0
    for col in cols:
        if col_num == 0:
            date = col.text
        elif col_num == 1:
            openInfo = col.get('data-format-value')
        elif col_num == 2:
            high = col.get('data-format-value')
        elif col_num == 3:
            low = col.get('data-format-value')
        elif col_num == 4:
            close = col.get('data-format-value')
        elif col_num == 5:
            volume = col.get('data-format-value')
        elif col_num == 6:
            marketCap = col.get('data-format-value')
        col_num += 1
    if volume is '-':
        volume = 0
    #### for SQL creation
    dataSQL[date] = (float(openInfo), float(high), float(low), float(close), float(volume), float(marketCap))
    #### for JSON readability
    dataJSON[date] = {"open": float(openInfo), "high": float(high), "low": float(low), "close": float(close), "volume" : float(volume), "marketCap": float(marketCap)}

name = 'crypto'
if args.n is not None:
    name = args.n

if args.json:
    with open(dirname(realpath(__file__)) + '/' + name + '.json', 'w') as outfile:
        json.dump(dataJSON, outfile, indent=4)

if args.sql:
    conn = sqlite3.connect(name + '.db')
    c = conn.cursor()

    # Delete tables if they exist
    c.execute('DROP TABLE IF EXISTS "'+ name +'";')
    conn.commit()


    c.execute('CREATE TABLE ' + name + '(date text PRIMARY KEY, open REAL, high REAL, low REAL, close REAL, volume REAL, marketCap REAL)')
    conn.commit()

    for date in dataSQL.keys():
        info = dataSQL[date]
        c.execute('INSERT INTO '+ name +' VALUES (?, ?, ?, ?, ?, ?, ?)', (date, info[0], info[1], info[2], info[3], info[4], info[5]))
        conn.commit()







