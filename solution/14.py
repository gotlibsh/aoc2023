from collections import Counter
from functools import cmp_to_key

cards = {letter:i for i,letter in enumerate('AKQT98765432J')}

def calc_type(hand: str):
    '''Return an integer between 1 and 7, lower number means higher rank.'''

    common = Counter(hand).most_common()

    # get most common letter sorted from best card to worst
    common = sorted(common, key=lambda c: (-c[1], cards[c[0]]))
    most_common = common[0][0]

    # in case J is the most common, either replace it with the next
    # most common card, or with A if it's the only card present
    if most_common == 'J':
        if len(common) == 1:
            most_common = 'A'
        else:
            most_common = common[1][0]

    new_hand = hand.replace('J', most_common)
    c = Counter(new_hand)
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
