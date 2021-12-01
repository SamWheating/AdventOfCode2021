with open('1/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")
    numbers = [int(number) for number in inputlines]

def part1():
    count_increasing = 0
    prev = numbers[0]
    for i in range(1, len(numbers)):
        current = numbers[i]
        if current > prev: count_increasing += 1
        prev = current
    return count_increasing

def part2():
    count_increasing = 0
    prev = sum(numbers[0:3])
    for i in range(1, len(numbers)-2):
        current = sum(numbers[i:i+3])
        if current > prev: count_increasing += 1
        prev = current
    return count_increasing

if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
