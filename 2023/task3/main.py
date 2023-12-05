import re

test = False
part_two = True

test_input_one = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

input = open('input', 'r')
lines = [l.strip('\n') for l in input.readlines()] if not test else test_input_one.splitlines()

def get_all_symbols(lines):
    result = []
    for line in lines:
        for c in line:
            if c == '.' or c.isdigit():
                pass
            else:
                if c not in result:
                    result.append(c)
    return result

def span_adjacent_to_symbol(span, idx, schematic, symbols):
    (sl, sr) = span
    length = len(schematic[0])

    (l, r) = (max(sl-1, 0), min(sr+1, length))
    
    for offset in range(-1, 2, 1):
        if idx+offset >= 0 and idx+offset < len(schematic):
            for s in symbols:
                if s in schematic[idx+offset][l:r]:
                    return True
    
    return False

def find_overlaps_to_span(spans, span):
    predicate = lambda x: len((set(range(x[0], x[1])) & set(range(span[0], span[1])))) > 0
    return list(filter(predicate, spans))

symbols = get_all_symbols(lines)

schematic = lines
pattern = re.compile(r'\d+')

sum = 0
if not part_two:
    for idx, line in enumerate(schematic):
        number_spans = [(m.start(0), m.end(0)) for m in re.finditer(pattern, line)]

        for span in number_spans:
            if span_adjacent_to_symbol(span, idx, schematic, symbols):
                part = int(schematic[idx][span[0]:span[1]])
                sum += part
else:
    all_number_spans = [*([(m.start(0), m.end(0), idx) for m in re.finditer(pattern, line)] for idx, line in enumerate(schematic))]
    length = len(schematic[0])
    
    for idx, line in enumerate(schematic):
        for i in range(len(line)):
            if line[i] == '*':
                
                (l, r) = (max(i-1, 0), min(i+2, length))
                
                candidates = [*([] if idx-1 < 0 else all_number_spans[idx-1]), *(all_number_spans[idx]), *([] if idx+1 > len(all_number_spans) else all_number_spans[idx+1])]
                number_spans = find_overlaps_to_span(candidates, (l, r))
                
                if len(number_spans) != 2:
                    # not a gear
                    continue
                
                first = number_spans[0]
                second = number_spans[1]
                gear_ratio = int(schematic[first[2]][first[0]:first[1]]) * int(schematic[second[2]][second[0]:second[1]])

                sum += gear_ratio

print("Result:", sum)

if test:
    if not part_two:
        assert sum == 4361
    else:
        assert sum == 467835

