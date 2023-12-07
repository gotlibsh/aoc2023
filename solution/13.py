from collections import Counter
from functools import cmp_to_key

cards = {letter:i for i,letter in enumerate('AKQJT98765432')}

def calc_type(hand):
    '''Return an integer between 1 and 7, lower number means higher rank.'''

    c = Counter(hand)
    common = sorted(c.values(), reverse=True)

    if common[0] == 5:
        return 1
    elif common[0] == 4:
        return 2
    elif common[0] == 3:
        if common[1] == 2:
            return 3
        return 4
    elif common[0] == 2:
        if common[1] == 2:
            return 5
        return 6
    return 7

def compare_hands(hand1, hand2):
    '''Compares the rank between 2 hands,
    returns -1 if the 1st hand is higher ranked and 1 if the 2nd hand is higher ranked.'''

    hand_type1 = calc_type(hand1)
    hand_type2 = calc_type(hand2)

    if hand_type1 < hand_type2:
        return -1
    elif hand_type1 > hand_type2:
        return 1
    
    for l1, l2 in zip(hand1, hand2):
        if cards[l1] < cards[l2]:
            return -1
        elif cards[l1] > cards[l2]:
            return 1

    assert 0, f'{hand1} and {hand2} have equal ranks'

with open('../input/7.txt', 'r') as f:
    lines = f.read().splitlines()

entries = [line.split() for line in lines]
entries = {hand: int(bid) for hand, bid in entries}
hands = sorted(entries.keys(), key=cmp_to_key(compare_hands), reverse=True)

print(sum(entries[hand] * rank for rank, hand in enumerate(hands, start=1)))
