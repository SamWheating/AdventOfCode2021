def fold_vertical(points, fold_y):
    new_points = set()
    for point in points:
        if point[1] < fold_y:
            new_points.add(point)
        elif point[1] > fold_y:
            new_y = fold_y - (point[1] - fold_y)
            new_points.add((point[0], new_y))
    return new_points

assert fold_vertical({(0,0), (1,8)}, 5) == {(0,0), (1,2)}

def fold_horizontal(points, fold_x):
    new_points = set()
    for point in points:
        if point[0] < fold_x:
            new_points.add(point)
        elif point[0] > fold_x:
            new_x = fold_x - (point[0] - fold_x)
            new_points.add((new_x, point[1]))
    return new_points

assert fold_horizontal({(0,0), (8, 1)}, 5) == {(0,0), (2,1)}

def print_points(points):
    height = max([point[1] for point in points])
    width = max([point[0] for point in points])
    lines = [[" "] * (width+1) for _ in range(height+1)]
    for point in points:
        lines[point[1]][point[0]] = "#"
    output = "\n\n"
    for line in lines:
        output += "".join(line) +"\n"
    return output

def part1(points, folds):
    
    for fold in folds[:1]:
        if fold[0] == 'x':
            points = fold_horizontal(points, fold[1])
        else:
            points = fold_vertical(points, fold[1])
    
    return len(points)

def part2(points, folds):
    
    for fold in folds:
        if fold[0] == 'x':
            points = fold_horizontal(points, fold[1])
        else:
            points = fold_vertical(points, fold[1])
    
    return print_points(points)

if __name__ == "__main__":

    with open('13/input.txt') as inputfile:
        inputlines = inputfile.read()

    # parse points into a set of (x,y) tuples
    points = inputlines.split("\n\n")[0].split("\n")
    points = {(int(point.split(",")[0]), int(point.split(",")[1])) for point in points}

    # parse folds into a list of (axis, val) tuples
    folds = inputlines.split("\n\n")[1].split("\n")
    folds = [(fold[11], int(fold[13:])) for fold in folds]

    print(f"Part 1 solution: {part1(points, folds)}")
    print(f"Part 2 solution: {part2(points, folds)}")
