import json
from os.path import dirname, realpath
from dateutil.parser import parse

with open('reddit.json') as f:
    data = json.load(f)
# prev = 134.210006714
days = []
newData = {}
for day in data:
    print(day)
    # days += [day]
    # print(day)
    dt = parse(day)
    # print(dt)
    newData[dt.strftime('%m-%d-%Y')] = data[day]



# for day in reversed(days):
    # cur = float(data[day]['close'])
    # change = ((cur - prev) / prev)
    # data[day]['change'] = change
    # print('cur', cur, 'prev', prev, 'change', change)
    # prev = cur

with open(dirname(realpath(__file__)) + '/redditCor.json', 'w') as outfile:
    json.dump(newData, outfile, indent=4)



# dt = parse('Mon Feb 15 2010')
# print(dt)
# # datetime.datetime(2010, 2, 15, 0, 0)
# print(dt.strftime('%d/%m/%Y'))
# # 15/02/2010