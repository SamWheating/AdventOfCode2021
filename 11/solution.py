from copy import deepcopy


def step(octos):
    # move the board forwards one step in time
    for y in range(len(octos)):
        for x in range(len(octos[0])):
            octos[y][x] += 1

    # now handle flashes (this will have to be repeated many times)
    while True:
        for y in range(len(octos)):
            for x in range(len(octos[0])):
                if octos[y][x] > 9:
                    # increment all of the neighbours by 1 (unless they are 0)
                    for nx in [x - 1, x, x + 1]:
                        for ny in [y - 1, y, y + 1]:
                            if 0 <= nx < len(octos[0]) and 0 <= ny < len(
                                octos
                            ):  # edge conditions
                                if octos[ny][nx] != 0:
                                    octos[ny][nx] += 1
                    octos[y][x] = 0

        # if nobody else is flashing, we can move on
        if max([max(row) for row in octos]) < 10:
            break

    return octos


def part1(octos):

    STEPS = 100
    total_flashes = 0
    for _ in range(STEPS):
        octos = step(octos)
        total_flashes += sum([row.count(0) for row in octos])

    return total_flashes


def part2(octos):

    steps = 0
    while max([max(row) for row in octos]) > 0:
        octos = step(octos)
        steps += 1

    return steps


if __name__ == "__main__":

    with open("11/input.txt") as inputfile:
        inputlines = inputfile.read().split("\n")
        octos = [[int(i) for i in line] for line in inputlines]

    print(f"Part 1 solution: {part1(deepcopy(octos))}")
    print(f"Part 2 solution: {part2(deepcopy(octos))}")
