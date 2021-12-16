from copy import copy

def part1(costs):

    # Super inefficient lowest-cost path algorithm written from scratch.
    # Importing networkx or using djikstra's wouldn't be any fun. 

    width = max([coord[0] for coord in costs.keys()])
    height = max([coord[1] for coord in costs.keys()])
    cost_to_reach = {(0,0): 0} # the lowest cost path to reach each point
    while True:
        starting = copy(cost_to_reach)
        for c in costs.keys():
            # get the cost of reaching neighbours
            neighbour_costs = []
            for neighbour in [(c[0]-1, c[1]),(c[0], c[1]-1),(c[0], c[1]+1),(c[0]+1, c[1])]:
                if 0 <= neighbour[0] <= width and 0 <= neighbour[1] <= width:
                    if neighbour in cost_to_reach:
                        neighbour_costs += [cost_to_reach[neighbour]]
            if neighbour_costs:
                cost_to_reach[c] = min([cost_to_reach.get(c, 1000000), min(neighbour_costs) + costs[c]])
        if cost_to_reach == starting:
            break

    return cost_to_reach[(width, height)]

def part2(costs):
    
    # we just have to tile the original input and then put it back into part 1
    width = max([coord[0] for coord in costs.keys()]) + 1
    height = max([coord[1] for coord in costs.keys()]) + 1
    new_costs = {}

    for coord in costs:
        for x_offset in range(5):
            for y_offset in range(5):
                new_coord = (coord[0] + (x_offset*width), coord[1] + y_offset*height)
                new_cost = costs[coord] + x_offset + y_offset
                if new_cost > 9:
                    new_cost -= 9
                new_costs[new_coord] = new_cost

    return part1(new_costs)


if __name__ == "__main__":

    costs = {}
    with open('15/input.txt') as inputfile:
        lines = inputfile.read().split("\n")
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                costs[(x,y)] = int(lines[y][x])

    print(f"Part 1 solution: {part1(costs)}")
    print(f"Part 2 solution: {part2(costs)}")
