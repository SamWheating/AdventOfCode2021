with open('7/input.txt') as inputfile:
    inputlines = inputfile.read()
    numbers = [int(number) for number in inputlines.split(",")]

def part1():
    costs = []
    for num in range(max(numbers)):
        costs.append(sum([abs(num-other_num) for other_num in numbers]))
    return min(costs)

def part2():

    #simple caching / precomputing of values makes this >30x faster
    def cost(distance, cache):
        if distance in cache:
            return cache[distance]
        val =  sum(range(distance+1))
        cache[distance] = val
        return val

    costs = []
    cached_values = {}
    for num in range(max(numbers)):
        costs.append(sum([cost(abs(num-other_num), cached_values) for other_num in numbers]))
    return min(costs)

if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
