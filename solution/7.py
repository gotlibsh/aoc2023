import re

def ints(s: str):
    matches = re.findall('-?\d+', s)
    return [int(match) for match in matches]

class Card:
    def __init__(self, s: str):
        # card string format:
        # Card <num>: <x1> ... <xn> | <y1> ... <ym>
        post_colon = s.partition(':')[-1]
        winning_nums, nums = post_colon.split('|')
        self.winning_nums = set(ints(winning_nums))
        self.nums = set(ints(nums))

    def count_matches(self):
        return sum(1 for n in self.nums if n in self.winning_nums)

    def score(self):
        matches = self.count_matches()
        return int(2 ** (matches-1))

with open('../input/4.txt', 'r') as f:
    cards = f.read().split('\n')
    cards = [Card(c) for c in cards]

print(sum(c.score() for c in cards))
