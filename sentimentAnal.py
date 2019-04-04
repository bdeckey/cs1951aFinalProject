import json
import re
from os.path import dirname, realpath
from textblob import TextBlob
from dateutil.parser import parse


def get_sub_sentiment(sub):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_sub(sub))
    score = analysis.sentiment.polarity
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive', score
    elif analysis.sentiment.polarity == 0:
        return 'neutral', score
    else:
        return 'negative', score

def clean_sub(sub):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", sub).split())


with open('redditFinal.json') as f:
    data = json.load(f)


# days = []
# newData = {}
#
# sentences = ["suck my dick you wonderful person.", "i love you cunt!",
#              "dirty filthy arab", "fuck you michael", "i love penis, but hate vagina",
#              "suck my dick you wonderful cunt", "suck my dick", ""]
# for i in sentences:
#     print(i, get_sub_sentiment(i)[1])

counter = 0
# each day of the year
for day in data:
    print(day)
    print("positive", data[day]["num_pos"])
    print("negative", data[day]["num_neg"])
    print("neutral", data[day]["num_neut"])
    counter += 1
    # get list of submissions
    subList = data[day]['submissions']
    # get set of titles to remove duplicates
    titles = set()
    # make new sub list
    newSubList = []
    # count pos, neg, nuetral
    pos, neg, nut = 0, 0, 0
    # for each submission
    for i in range(len(subList)):
        # get title
        title = subList[i]['title']
        if title in titles:
            print("dup")
            continue
        else:
            titles.add(title)
            # do sentiment analysis
            curSub = subList[i]
            decision, score = get_sub_sentiment(title)
            curSub['decision'] = decision
            curSub['sentiment'] = score
            if (decision is 'positive'):
                pos += 1
            elif (decision is 'negative'):
                neg += 1
            else:
                nut += 1
            newSubList.append(curSub)
    data[day]['num_pos'] = pos
    data[day]['num_neg'] = neg
    data[day]['num_neut']  = nut
    data[day]['submissions'] = newSubList
# #
with open(dirname(realpath(__file__)) + '/redditFinal.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

