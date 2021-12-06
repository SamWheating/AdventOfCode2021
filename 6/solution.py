# Excuse the horrible variable names here

with open('6/input.txt') as inputfile:
    inputlines = inputfile.read()
    fishes = [int(i) for i in inputlines.split(",")]

def part1():
    fishes = [int(i) for i in inputlines.split(",")]
    for _ in range(80):
        new_fishes = []
        for fish in fishes:
            if fish > 0:
                new_fishes.append(fish-1)
            else:
                new_fishes.append(8)
                new_fishes.append(6)
        fishes = new_fishes
    return len(fishes)

def part2():
    opt_fishes = {}
    fishes = [int(i) for i in inputlines.split(",")]
    for fish in fishes:
        if fish in opt_fishes:
            opt_fishes[fish] += 1
        else:
            opt_fishes[fish] = 1
    
    for _ in range(256):
        new_fishes = {}
        new_fishes[8] = opt_fishes.get(0, 0)
        new_fishes[6] = opt_fishes.get(0, 0)
        for i in range(0,9):
            new_fishes[i] = new_fishes.get(i, 0) + opt_fishes.get(i+1, 0)
        opt_fishes = new_fishes
    
    return sum(list(opt_fishes.values()))

if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
