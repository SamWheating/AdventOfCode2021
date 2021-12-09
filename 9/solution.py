with open('9/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")
    grid = [[int(c) for c in line] for line in inputlines]

def part1():

    sum_risk = 0
    for y in range(0, len(grid)):
        for x in range(0, (len(grid[0]))):
            up = 100 if y <= 0 else grid[y-1][x]
            left = 100 if x <= 0 else grid[y][x-1]
            right = 100 if x >= len(grid[0])-1 else grid[y][x+1]
            down = 100 if y >= len(grid)-1 else grid[y+1][x]
            if min([up, left, right, down]) > grid[y][x]:
                sum_risk += (grid[y][x]+1) 

    return sum_risk
    
def part2():

    grid = [[int(c) for c in line] for line in inputlines]

    def get_basin_size(grid, x, y):
        # find the size of a basin starting at x, y
        # for all points in a basin, add any adjacent spots which are higher (but less than 9)
        # This could probably be done recursively?
        basin = [(x,y)]
        while True:
            done = True
            for (x,y) in basin:
                # left
                if x>0 and grid[y][x-1] > grid[y][x] and grid[y][x-1] < 9 and (x-1, y) not in basin:
                    basin.append((x-1, y))
                    done = False
                elif x<len(grid[0])-1 and grid[y][x+1] > grid[y][x] and grid[y][x+1] < 9 and (x+1, y) not in basin:
                    basin.append((x+1, y))
                    done = False
                elif y>0 and grid[y-1][x] > grid[y][x] and grid[y-1][x] < 9 and (x, y-1) not in basin:
                    basin.append((x, y-1))
                    done = False
                elif y<len(grid)-1 and grid[y+1][x] > grid[y][x] and grid[y+1][x] < 9 and (x, y+1) not in basin:
                    basin.append((x, y+1))
                    done = False
            if done:
                return len(basin)

    # get all low points:
    low_points = []
    for y in range(0, len(grid)):
        for x in range(0, (len(grid[0]))):
            up = 100 if y <= 0 else grid[y-1][x]
            left = 100 if x <= 0 else grid[y][x-1]
            right = 100 if x >= len(grid[0])-1 else grid[y][x+1]
            down = 100 if y >= len(grid)-1 else grid[y+1][x]
            if min([up, left, right, down]) > grid[y][x]:
                low_points.append((x,y))

    # get the size of the basin centered on each point
    basin_sizes = []
    for (x,y) in low_points:
        size = get_basin_size(grid, x, y)
        basin_sizes.append(size)
    
    # the product of the 3 largest basin sizes
    return sorted(basin_sizes)[-1] * sorted(basin_sizes)[-2] * sorted(basin_sizes)[-3]

if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
