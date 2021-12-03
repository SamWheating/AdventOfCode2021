with open('3/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")

def part1():
    cols = [[int(row[i]) for row in inputlines] for i in range(len(inputlines[0]))]
    gamma = ""
    for column in cols:
        gamma += '1' if sum(column)/len(column) >= 0.5 else '0'
    
    gamma = int(gamma, 2)
    epsilon = (2**len(inputlines[0]))-1 - gamma # since epsilon is the binary opposite of gamma
    return gamma * epsilon


def part2():
    
    # oxygen
    prefix = ""
    rows = inputlines
    for i in range(len(inputlines[0])):
        rows = [row for row in rows if row.startswith(prefix)]
        if len(rows) == 1:
            prefix = rows[0]
            break
        counts = {'0': 0, '1': 0}
        for row in rows:
            counts[row[i]] += 1
        if counts['0'] > counts['1']:
            prefix += '0'
        else:
            prefix += '1'
    oxygen = int(prefix, 2)
    
    # co2
    prefix = ""
    rows = inputlines
    for i in range(len(inputlines[0])):
        rows = [row for row in rows if row.startswith(prefix)]
        if len(rows) == 1:
            prefix = rows[0]
            break
        counts = {'0': 0, '1': 0}
        for row in rows:
            counts[row[i]] += 1
        if counts['0'] <= counts['1']:
            prefix += '0'
        else:
            prefix += '1'
    co2 = int(prefix, 2)

    return oxygen * co2


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")