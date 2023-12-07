import re

test = False
part_two = True

test_input_one = """Time:      7  15   30
Distance:  9  40  200
"""

input = open('input', 'r')
lines = list(filter((lambda e: len(e) > 0), [l.strip('\n') for l in input.readlines()] if not test else test_input_one.splitlines()))

pattern = re.compile(r'\d+')

if not part_two:
    times = [int(t) for t in re.findall(pattern, lines[0])]
    dists = [int(d) for d in re.findall(pattern, lines[1])]
else:
    times = [int(''.join(re.findall(pattern, lines[0])))]
    dists = [int(''.join(re.findall(pattern, lines[1])))]

# bruteforce approach
result = 1
for idx, time in enumerate(times):
    ctr = 0
    for t in range(0, time):
        velocity = t
        distance = velocity * (time - t)

        if distance > dists[idx]:
            ctr += 1

    if ctr != 0:
        result *= ctr

print(result)

if test:
    if not part_two:
        assert result == 288
    else:
        assert result == 71503

