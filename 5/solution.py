with open('5/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")

# parsing the input so that a list of "x1,y1 -> x2,y2" becomes a list of ((x1,y1), (x2,y2))
lines = []
for line in inputlines:
    split_line = line.replace(" -> ", ",").split(",")
    lines.append(((int(split_line[0]), int(split_line[1])), (int(split_line[2]), int(split_line[3]))))

def part1():
    # build a giant dictionary of all of the points that have lines crossing them.
    points = {}
    for line in lines:
        if line[0][0] != line[1][0] and line[0][1] != line[1][1]:  # skip angled lines
            continue
        d_x = 1 if line[0][0] < line[1][0] else -1 if line[0][0] > line[1][0] else 0
        d_y = 1 if line[0][1] < line[1][1] else -1 if line[0][1] > line[1][1] else 0
        length = max(abs(line[0][0] - line[1][0]), abs(line[0][1] - line[1][1]))
        for i in range(length+1):
            coord = (line[0][0] + i*d_x, line[0][1] + i*d_y)
            points.update({coord: points.get(coord, 0)+1})
    
    return len([i for i in points.values() if i > 1])


def part2():
    # the same as part 1 but with diagonal lines included too.
    points = {}
    for line in lines:
        d_x = 1 if line[0][0] < line[1][0] else -1 if line[0][0] > line[1][0] else 0
        d_y = 1 if line[0][1] < line[1][1] else -1 if line[0][1] > line[1][1] else 0
        length = max(abs(line[0][0] - line[1][0]), abs(line[0][1] - line[1][1]))
        for i in range(length+1):
            coord = (line[0][0] + i*d_x, line[0][1] + i*d_y)
            points.update({coord: points.get(coord, 0)+1})
    
    return len([i for i in points.values() if i > 1])


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
