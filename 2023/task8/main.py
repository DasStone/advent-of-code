import re
import math

test = False
test_one = False
part_two = True

test_input_one = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test_input_two = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

if part_two:
    test_input_one = test_input_two = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

input = open('input', 'r')
lines = list(filter((lambda e: len(e) > 0), [l.strip('\n') for l in input.readlines()] if not test else test_input_one.splitlines() if test_one else test_input_two.splitlines()))

instructions = lines.pop(0)

map = dict()
for line in lines:
    line = line.replace(' ', '')

    [start, finish] = line.split('=')
    (l, r) = finish[1:-1].split(',')
    
    map[start] = (l, r)

current = []
if not part_two:
    current.append('AAA')
else:
    for key in map:
        if key[2] == 'A':
            current.append(key)

def check_goal(current):
    if not part_two:
        return current == 'ZZZ'
    else:
        if current[2] != 'Z':
            return False

        return True

def reach_goal(location, instructions):
    current = location
    steps = 0

    while True:
        direction_index = 0 if instructions[steps % len(instructions)] == 'L' else 1

        current = map[current][direction_index]
        steps += 1

        if check_goal(current):
            break

    assert steps % len(instructions) == 0

    return steps

steps = 0
if not part_two:
    steps = reach_goal(current[0], instructions)
else:
    # This only works, because the steps needed between reaching a goal and the one after that always stays the same
    cycles = [reach_goal(loc, instructions) for loc in current]
    steps = math.lcm(*cycles)

print(steps)

if test:
    if not part_two:
        if test_one:
            assert steps == 2
        else:
            assert steps == 6
    else:
        assert steps == 6

