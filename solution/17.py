import re
from itertools import pairwise

def ints(s: str):
    matches = re.findall('-?\d+', s)
    return [int(match) for match in matches]

def diff(record):
    return [b-a for a,b in pairwise(record)]

def predict(history):
    last = [history[-1]]
    d = diff(history)

    while any(x for x in d):
        last.append(d[-1])
        d = diff(d)

    return sum(last)

with open('../input/9.txt', 'r') as f:
    lines = f.read().splitlines()

histories = [ints(line) for line in lines]
predictions = [predict(h) for h in histories]
print(sum(predictions))
