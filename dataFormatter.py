import json
import re
from os.path import dirname, realpath
from textblob import TextBlob
from dateutil.parser import parse
import datetime as dt
from dateutil.relativedelta import relativedelta

with open('redditFinal.json') as f:
    reddit = json.load(f)

with open('bitcoinCD.json') as g:
    bit = json.load(g)


def addZero(num):
    if num < 10:
        res = str(num)
        return "0" + res
    else:
        return str(num)

def getDayAfter(date):
    temp = date.split("-")
    month = int(temp[0])
    day = int(temp[1])
    year = int(temp[2])
    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        if (day != 31):
            newStr = addZero(month) + "-" + addZero(day+1) + "-" + str(year)
            return newStr
        else:
            if (month != 12):
                return addZero(month + 1) + "-" + addZero(1) + "-" + str(year)
            else:
                return addZero(1) + "-" + addZero(1) + "-" + str(year+1)
    if (month == 4 or month == 6 or month == 9 or month == 11):
        if (day != 30):
            newStr = addZero(month) + "-" + addZero(day + 1) + "-" + str(year)
            return newStr
        else:
            return addZero(month+1) + "-" + addZero(1) + "-" + str(year)
    if (month == 2):
        if (year == 2016):
            if (day != 29):
                return addZero(month) + "-" + addZero(day+1) + "-" + str(year)
            else:
                return addZero(month+1) + "-" + addZero(1) + "-" + str(year)
        else:
            if (day != 28):
                return addZero(month) + "-" + addZero(day+1) + "-" + str(year)
            else:
                return addZero(month+1) + "-" + addZero(1) + "-" + str(year)

def getXbefore(day, x):
    return (parse(day) - relativedelta(days=x)).strftime('%m-%d-%Y')

def getXDayTot(day, x):
    before = getXbefore(day, x)
    tot = 0
    totPos = 0
    totNeg = 0
    totNeut = 0
    counter = 0
    while(before != day):
        counter += 1
        tot += reddit[day]["submissionCount"]
        totPos += reddit[day]["num_pos"]
        totNeg += reddit[day]["num_neg"]
        totNeut += reddit[day]["num_neut"]
        before = getDayAfter(before)
        if counter > 10:
            print("error in x day tot")
            break
    return tot, totPos, totNeg, totNeut


# example = '03-06-2016'
#
# get7DayTot(example)


days = []
regData = {}

counter = 0

intersectDays = []
# get all the days that are in both bitcoin and reddit data
for item in reversed(list(bit.keys())):
    if item in reddit:
        intersectDays.append(item)
counter = 0
for day in intersectDays:
    sevDayTot, sevDayPos, sevDayNeg, sevDayNeut = getXDayTot(day, 7)
    threeDayTot, threeDayPos, threeDayNeg, threeDayNeut = getXDayTot(day, 3)
    twentyfourChange = bit[day]["change"]
    closing = bit[day]["close"]
    regData[day] = {"7DayTot":sevDayTot,"7DayPos":sevDayPos,"7DayNeg":sevDayNeg,"7DayNeut":sevDayNeut,
                    "3DayTot":threeDayTot, "3DayPos":threeDayPos,"3DayNeg":threeDayNeg,"3DayNeut":threeDayNeut,
                    "24Change":twentyfourChange,"close":closing}
    # progress print line, every 30 dates so we dont slow down code too much
    counter += 1
    if counter == 30:
        counter = 0
        print(day)

#
with open(dirname(realpath(__file__)) + '/regressionData.json', 'w') as outfile:
    json.dump(regData, outfile, indent=4)


