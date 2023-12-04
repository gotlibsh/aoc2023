import re

def ints(s: str):
    matches = re.findall('-?\d+', s)
    return [int(match) for match in matches]

class Card:
    def __init__(self, s: str):
        # card string format:
        # Card <num>: <x1> ... <xn> | <y1> ... <ym>
        pre_colon, _, post_colon = s.partition(':')
        winning_nums, nums = post_colon.split('|')
        self.winning_nums = set(ints(winning_nums))
        self.nums = set(ints(nums))
        self.id = int(pre_colon.split()[-1])

    def count_matches(self):
        return sum(1 for n in self.nums if n in self.winning_nums)

    def score(self):
        matches = self.count_matches()
        return int(2 ** (matches-1))

with open('../input/4.txt', 'r') as f:
    cards = f.read().split('\n')
    cards = [Card(c) for c in cards]
    cards = {card.id: card for card in cards}

proc_idx = 0
cards_to_process = list(cards.values())

while proc_idx < len(cards_to_process):
    card = cards_to_process[proc_idx]
    matches = card.count_matches()
    new_cards = [cards[id] for id in range(card.id+1, card.id+1+matches, 1)]
    cards_to_process.extend(new_cards)
    proc_idx += 1

print(len(cards_to_process))
