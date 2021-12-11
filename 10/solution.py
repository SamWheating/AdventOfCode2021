with open("10/input.txt") as inputfile:
    inputlines = inputfile.read().split("\n")

CLOSERS = {"(": ")", "<": ">", "[": "]", "{": "}"}

CORRUPT_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
INCOMPLETE_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def part1():
    def score_line(line):
        # returns a score (or 0 if no errors)
        stack = []
        for char in line:
            if char in CLOSERS.keys():
                stack.append(char)
            else:
                if len(stack) > 0 and char == CLOSERS[stack[-1]]:
                    stack.pop()
                else:
                    return CORRUPT_SCORES[char]
        return 0

    assert score_line("{([(<{}[<>[]}>{[]{[(<()>") == 1197

    total_score = 0
    for line in inputlines:
        total_score += score_line(line)

    return total_score


def part2():
    def score_line(line):
        stack = []
        for char in line:
            if char in CLOSERS.keys():
                stack.append(char)
            else:
                if len(stack) > 0 and char == CLOSERS[stack[-1]]:
                    stack.pop()
                else:
                    return  # this line is corrupted

        if len(stack) == 0:
            return  # this is a balanced string

        score = 0
        for c in stack[::-1]:
            score *= 5
            score += INCOMPLETE_SCORES[CLOSERS[c]]

        return score

    assert score_line("[({(<(())[]>[[{[]{<()<>>") == 288957

    scores = []
    for line in inputlines:
        score = score_line(line)
        if score:
            scores.append(score)

    scores.sort()
    return scores[int(len(scores) / 2 - 0.5)]


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
