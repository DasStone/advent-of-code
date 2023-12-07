import re
from enum import Enum
from operator import itemgetter

test = False
part_two = True

class Hand(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

test_input_one = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

input = open('input', 'r')
lines = list(filter((lambda e: len(e) > 0), [l.strip('\n') for l in input.readlines()] if not test else test_input_one.splitlines()))

pattern = re.compile(r'\d+')

def get_hand_value(input):
    distinct = list(set(input))
    size = len(distinct)

    if size == 1:
        return Hand.FIVE_OF_A_KIND.value
    elif size == 2:
        if input.count(distinct[0]) == 4 or input.count(distinct[1]) == 4:
            return Hand.FOUR_OF_A_KIND.value
        return Hand.FULL_HOUSE.value
    elif size == 3:
        if input.count(distinct[0]) == 3 or input.count(distinct[1]) == 3 or input.count(distinct[2]) == 3:
            return Hand.THREE_OF_A_KIND.value
        return Hand.TWO_PAIR.value
    elif size == 4:
        return Hand.ONE_PAIR.value
    else: # size == 5
        return Hand.HIGH_CARD.value

def transform_hand(hand):
    map = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    if part_two:
        map['J'] = 1 # make J the weakest card

    out = []
    for i in range(len(hand)):
        if hand[i].isnumeric():
            out.append(int(hand[i]))
        else:
            out.append(map[hand[i]])

    return out

hands = [[], [], [], [], [], [], []]
for line in lines:
    [hand_str, bet] = line.split(" ")

    value = 0
    if not part_two:
        value = get_hand_value(hand_str)
    else:
        # == No Bruteforce:
        # with 4 (and also 5) jokers you will always have 5 of a kind
        # if you have 3 jokers, the best you will have is either 4 of a kind or 5 of a kind

        # == Bruteforce:
        # with 2 jokers there are many options, but you will not find a better option by setting them to different values
        # 1 joker, just bruteforce

        amount_jokers = hand_str.count('J')

        if amount_jokers == 0:
            value = get_hand_value(hand_str)
        elif amount_jokers == 4 or amount_jokers == 5:
            value = Hand.FIVE_OF_A_KIND.value
        elif amount_jokers == 3:
            value = Hand.FIVE_OF_A_KIND.value if len(set(hand_str)) == 2 else Hand.FOUR_OF_A_KIND.value
        else: # case 1 or 2
            cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
            tmp = 1

            for c in cards:
                res = get_hand_value(hand_str.replace('J', c))
                if res > tmp:
                    tmp = res

            value = tmp

    
    hand = transform_hand(hand_str)
    hand.append(int(bet))
    hands[value - 1].append(hand)

result = 0
rank = 1
for e in hands:
    if len(e) == 0:
        continue
    
    e.sort(key=itemgetter(0, 1, 2, 3, 4))
    
    print(e)
    for hand in e:
        result += rank * hand[5]
        rank += 1

print(result)

if test:
    if not part_two:
        assert result == 6440
    else:
        assert result == 5905

