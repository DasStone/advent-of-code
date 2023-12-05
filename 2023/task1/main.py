import regex as re

test = False
part_two = True

test_input_one = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

test_input_two = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

input = open('input', 'r')
lines = input.readlines() if not test else (test_input_one.splitlines() if not part_two else test_input_two.splitlines())

calibration_value = 0

pattern = re.compile(r'\d') if not part_two else re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine')
table ={'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9} 

for l in lines:
    numbers = re.findall(pattern, l, overlapped=True)
    
    if len(numbers) == 0:
        continue
    
    first = int(numbers[0]) if len(numbers[0]) <= 1 else table[numbers[0]]
    last = int(numbers[-1]) if len(numbers[-1]) <= 1 else table[numbers[-1]]
    transform = first * 10 + last

    calibration_value += transform

print("Calibration Value: " + str(calibration_value))

if test:
    if not part_two:
        assert calibration_value == 142
    else:
        assert calibration_value == 281

