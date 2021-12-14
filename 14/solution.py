from collections import Counter

def part1(sequence, insertion_pairs):
    
    for _ in range(10):
        new_sequence = ""
        for i in range(len(sequence)-1):
            if sequence[i:i+2] in insertion_pairs:
                new_sequence += (sequence[i] + insertion_pairs[sequence[i:i+2]])
            else:
                raise Exception
        new_sequence += sequence[-1]
        sequence = new_sequence

    counts = Counter(new_sequence)
    print(counts)
    return counts.most_common()[0][1] - counts.most_common()[-1][1]

def part2(sequence, insertion_pairs):
    
    # we need to count pairs here, can't keep track of the whole string
    pairs = {}
    for pair in [sequence[i:i+2] for i in range(len(sequence)-1)]:
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1

    for _ in range(40):
        new_pairs = {}
        for pair in pairs.keys():
            leftpair = pair[0] + insertion_pairs[pair]
            right_pair = insertion_pairs[pair] + pair[1]
            for new_pair in [leftpair, right_pair]:
                if new_pair in new_pairs:
                    new_pairs[new_pair] += pairs[pair]
                else:
                    new_pairs[new_pair] = pairs[pair]
        
        pairs = new_pairs
    
    counts = Counter()
    for pair in pairs:
        counts[pair[0]] += pairs[pair]
        counts[pair[1]] += pairs[pair]
    
    # need to divide each character count by 2, since every atom is counted twice 
    # as a part of the pair before and the pair after
    # (except for the first and last atoms, which are only counted once).
    counts[sequence[0]] += 1
    counts[sequence[-1]] += 1

    for atom in counts:
        counts[atom] /= 2

    return int(counts.most_common()[0][1] - counts.most_common()[-1][1])

if __name__ == "__main__":

    with open('14/input.txt') as inputfile:
        text = inputfile.read()
        sequence = text.split("\n")[0]
        insertion_pairs = {line[:2]: line[6] for line in text.split("\n\n")[1].split("\n")}

    print(f"Part 1 solution: {part1(sequence, insertion_pairs)}")
    print(f"Part 2 solution: {part2(sequence, insertion_pairs)}")
