import re

test = False
part_two = True

test_input_one = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

cubes = {'red': 12, 'green': 13, 'blue': 14}

input = open('input', 'r')
lines = input.readlines() if not test else test_input_one.splitlines()

def check_game_validity(game, available_cubes):
    game_id = int(re.findall(r'\d+', game)[0])
    pulls = game[8:].split(';')
    
    pattern = re.compile(r'\d+ r|\d+ g|\d+ b')

    for pull in pulls:
        red = 0
        green = 0
        blue = 0

        pulled_cubes = re.findall(pattern, pull)

        for cubes in pulled_cubes:
            amount = int(cubes[:-2])

            if cubes[-1] == 'r':
                red += amount
            elif cubes[-1] == 'g':
                green += amount
            else:
                blue += amount

        if red > available_cubes['red'] or green > available_cubes['green'] or blue > available_cubes['blue']:
            return (game_id, False)

    return (game_id, True)

def minimal_possible_cubes(game):
    game_id = int(re.findall(r'\d+', game)[0])
    pulls = game[8:].split(';')

    pattern = re.compile(r'\d+ r|\d+ g|\d+ b')
    
    min_r = 0
    min_g = 0
    min_b = 0

    for pull in pulls:
        red = 0
        green = 0
        blue = 0

        pulled_cubes = re.findall(pattern, pull)

        for cubes in pulled_cubes:
            amount = int(cubes[:-2])

            if cubes[-1] == 'r':
                red += amount
            elif cubes[-1] == 'g':
                green += amount
            else:
                blue += amount

        max = lambda a, b: a if a > b else b

        min_r = max(min_r, red)
        min_g = max(min_g, green)
        min_b = max(min_b, blue)

    return {'red': min_r, 'green': min_g, 'blue': min_b}

def power(cubes):
    return cubes['red'] * cubes['blue'] * cubes['green']

sum = 0
for line in lines:
    if not part_two:
        (id, valid) = check_game_validity(line, cubes)
        if valid:
            sum += id
    else:
        sum += power(minimal_possible_cubes(line))

print("Result:", sum)

if test:
    if not part_two:
        assert sum == 8
    else:
        assert sum == 2286

