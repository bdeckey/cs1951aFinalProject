
def expected(values):
    tot = 0
    for i in values:
        val = i[0]
        chance = i[1]
        tot += val * chance
    return tot

def expectedx2(values):
    tot = 0
    for i in values:
        val = i[0]
        chance = i[1]
        tot += (val * val) * chance
    return tot

def variance(values):
    e = expected(values)
    return expectedx2(values) - (e * e)

p1 = [(10, 0.55), (-5, 0.25), (28, 0.15), (100, 0.05)]

dice = [-5, -2, 1, 2, 3, 4]
diceProb = [(-5, 1/6), (-2, 1/6), (1, 1/6), (2, 1/6), (3, 1/6), (4, 1/6)]

def createSum(d):
    res = []
    for i in d:
        for j in d:
            res += [((i + j), (1/36))]
    return res


def pos(d):
    answer = 0
    for i in d:
        if i[0] > 0:
            answer += i[1]
    return answer

def printExpected():
    reward = (9,2)
    p = 0.99
    p1 = 0.01
    while (p > 0.02):
        print("expected", (reward[0] * p + reward[1] * p1), " p", p, " p - 1", p1)
        p -= 0.01
        p1 += 0.01


print("p1 expected", expected(p1))
print("p1 variance", variance(p1))
print("p2 expected sum", expected(createSum(dice)))
print("p2 pos chance", pos(createSum(dice)))
# printExpected()
print("p3 expected", expected([(9,0.575), (2, 0.425)]))
