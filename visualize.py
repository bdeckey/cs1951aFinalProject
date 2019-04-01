import matplotlib.pyplot as plt
import json

with open('bitcoinCD.json') as f:
    bitcoin = json.load(f)

with open('redditCD.json') as f:
    reddit = json.load(f)


days = []
closings = []
submissions = []
for day in bitcoin:
    days += [day]
for day in reversed(days):
    closings += [bitcoin[day]['close']]
    if (day in reddit.keys()) :
        submissions += [reddit[day]['submissionCount']]
    else:
        submissions += [0]


plt.plot(submissions, "b")

plt.plot(closings, 'r')
plt.show()