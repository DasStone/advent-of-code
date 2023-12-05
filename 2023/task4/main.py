import re

test = False
part_two = True

test_input_one = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

input = open('input', 'r')
lines = list(filter((lambda e: len(e) > 0), [l.strip('\n') for l in input.readlines()] if not test else test_input_one.splitlines()))
pattern = re.compile(r'\d+')

def get_card_info(card):
    card = line.split(":")
    id = int(re.findall(pattern, card[0])[0])
    [winning, current] = card[1].split("|")
    (winning, current) = (re.findall(pattern, winning), re.findall(pattern, current))

    amount_winning = len(list(filter((lambda e: e in winning), current)))

    value = min(amount_winning, 1) * (1 << max(amount_winning - 1, 0))

    return (id, amount_winning, value)

result = 0
repetitions = [1 for i in range(len(lines))]

for idx, line in enumerate(lines):
    if not part_two:
        (_, _, value) = get_card_info(line)
        result += value
    else:
        (id, amount_winning, _) = get_card_info(line)
        
        for _ in range(repetitions[idx]):
            for i in range(id, min(id+amount_winning, len(repetitions))):
                repetitions[i] += 1

if part_two:
    result = sum(repetitions)

print(result)
if test:
    if not part_two:
        assert result == 13
    else:
        assert result == 30
