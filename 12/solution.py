from copy import deepcopy

with open('12/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")

# create a map of cave to accessible caves (repeated because bi-directional)
tunnel_map = {}
for line in inputlines:
    start, end = line.split("-")
    if start in tunnel_map:
        tunnel_map[start].append(end)
    else:
        tunnel_map[start] = [end]
    if end in tunnel_map:
        tunnel_map[end].append(start)
    else:
        tunnel_map[end] = [start]

def part1():

    def recurse_paths(tunnel_map, path):
        # given a prefix and a map of which paths go where, return all possible paths
        if path[-1] == 'end':
            return [path]
        next_stops = []
        for stop in tunnel_map[path[-1]]:
            if stop.islower() and stop in path:
               continue
            next_stops.append(stop)
        paths = []
        for stop in next_stops:
            paths.extend(recurse_paths(tunnel_map, path + [stop]))

        return paths
        
    return len(recurse_paths(tunnel_map, ['start']))


def part2():

    def has_duplicate_lowercase(path):
        # return True if the path already visits a small cave twice
        small_caves = [c for c in path if c.islower()]
        return len(small_caves) != len(set(small_caves))

    assert not has_duplicate_lowercase(['start'])
    assert not has_duplicate_lowercase(['start', 'a', 'b', 'C'])
    assert has_duplicate_lowercase(['start', 'a', 'b', 'a'])

    def recurse_paths(tunnel_map, path):
        # given a prefix and a map of which paths go where, return all possible paths
        if path[-1] == 'end':
            return [path]
        next_stops = []
        for stop in tunnel_map[path[-1]]:
            # allow no more than one set of duplicate small caves (`start` and `end` excluded)
            if stop.islower() and stop in path and has_duplicate_lowercase(path) or stop == 'start':
               continue
            next_stops.append(stop)
        paths = []
        for stop in next_stops:
            paths.extend(recurse_paths(tunnel_map, path + [stop]))

        return paths

    paths = recurse_paths(tunnel_map, ['start'])

    return len(paths)

if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
