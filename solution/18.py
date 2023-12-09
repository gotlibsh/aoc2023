import re
from itertools import pairwise
from functools import reduce

def ints(s: str):
    matches = re.findall('-?\d+', s)
    return [int(match) for match in matches]

def diff(record):
    return [b-a for a,b in pairwise(record)]

def predict(history):
    first = [history[0]]
    d = diff(history)

    while any(x for x in d):
        first.append(d[0])
        d = diff(d)

    return reduce(lambda x,y: y-x, reversed(first), 0)

with open('../input/9.txt', 'r') as f:
    lines = f.read().splitlines()

histories = [ints(line) for line in lines]
predictions = [predict(h) for h in histories]
print(sum(predictions))
