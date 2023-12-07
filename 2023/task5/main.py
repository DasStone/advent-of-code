import re

test = False
part_two = True

test_input_one = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

input = open('input', 'r')
lines = list(filter((lambda e: len(e) > 0), [l.strip('\n') for l in input.readlines()] if not test else test_input_one.splitlines()))

pattern = re.compile(r'\d+')

if part_two:
    tmp = [int(e) for e in re.findall(pattern, lines.pop(0))]
    seeds = [(tmp[i], tmp[i] + tmp[i+1]) for i in range(0, len(tmp), 2)]
else:
    seeds = [int(e) for e in re.findall(pattern, lines.pop(0))]

maps = []

# parse maps
for idx, line in enumerate(lines):
    if "map" in line:
        map = []

        for offset in range(idx + 1, len(lines)):
            if "map" in lines[offset]:
                break

            mapping = [int(e) for e in re.findall(pattern, lines[offset])]
            map.append(mapping)

        maps.append(map)

def apply_map(value, map):
    for mapping in map:
        [dst_start, src_start, size] = mapping
        if value in range(src_start, src_start + size):
            value = value - src_start + dst_start
            break

    return value

# basically interval arithmetic
# note: all "spans" have an inclusive lower bound and exclusive upper bound
def apply_map_to_spans(spans, map):
    output_spans = []
    workset = spans
    
    for mapping in map:
        tmp = []
        for span in workset:
            (l, u) = span
            (src_l, src_u) = (mapping[1], mapping[1] + mapping[2])
            (dst_l, dst_u) = (mapping[0], mapping[0] + mapping[2])

            if src_u < l or src_l > u:
                tmp.append(span)
                continue

            (intersect_l, intersect_u) = (max(l, src_l), min(u, src_u))
            
            output_spans.append((intersect_l - src_l + dst_l, intersect_u - src_u + dst_u))

            lu = l + (intersect_l - l)
            ul = u - (u - intersect_u)
            
            if lu - l >= 1:
                tmp.append((l, lu))

            if u - ul >= 1:
                tmp.append((ul, u))

        workset = tmp

    output_spans.extend(workset)
    return output_spans

result = float('inf')
if not part_two:
    for seed in seeds:
        value = seed

        for map in maps:
            value = apply_map(value, map)

        if value < result:
            result = value
else:
    for map in maps:
        seeds = apply_map_to_spans(seeds, map)

    for locations in seeds:
        if locations[0] < result:
            result = locations[0]

print(result)

if test:
    if not part_two:
        assert result == 35
    else:
        assert result == 46

