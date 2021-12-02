with open('2/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")
    directions = [(line.split(" ")[0], int(line.split(' ')[1])) for line in inputlines]        

def part1():
    # python 3.10 pattern matching would be super cool here
    depth = horizontal = 0
    for direction in directions:
        if direction[0] == 'forward':
            horizontal += direction[1]
        elif direction[0] == 'down':
            depth += direction[1]
        elif direction[0] == 'up':
            depth -= direction[1]
    return depth*horizontal

def part2():
    depth = horizontal = aim = 0
    for direction in directions:
        if direction[0] == 'forward':
            horizontal += direction[1]
            depth += (direction[1] * aim)
        elif direction[0] == 'down':
            aim += direction[1]
        elif direction[0] == 'up':
            aim -= direction[1]
    return depth*horizontal


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
