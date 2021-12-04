with open('4/input.txt') as inputfile:
    inputlines = inputfile.read()

# gross parsing logic, but need to separate the picks from the boards and unroll each board into a list of ints
DRAWS = [int(i) for i in inputlines[:inputlines.index('\n')].split(',')] # first line is the order of picks
BOARDS = inputlines[inputlines.index('\n')+2:].split("\n\n")
boardlines = []
for board in BOARDS:
    line = [int(i) for i in board.replace("\n", " ").replace('  ', ' ').lstrip().split(' ')]
    boardlines.append(line)
BOARDS = boardlines

def is_winner(board, picks):
    # if one row or column is entirely contained in picks, return True
    picks = set(picks) # faster membership checks
    board_size = int(len(board)**.5) # I don't want to hardcode this value just in case

    # check rows
    for row in range(0, int(len(board)/board_size)):
        winner = True
        for idx in range(row*board_size, (row+1)*board_size):
            if board[idx] not in picks:
                winner = False
                break
        if winner: return True

    # check cols
    for col in range(0, int(len(board)/board_size)):
        winner = True
        for idx in range(col, len(board), board_size):
            if board[idx] not in picks: 
                winner = False
                break
        if winner: return True

    # if we're here, then this board isn't a winner
    return False

def score(board, picks):
    # sum of all un-picked numbers * last picked number
    return sum([i for i in board if i not in picks])*picks[-1]

def part1():
    for i in range(5,len(DRAWS)): # takes at least 5 draws to win
        picks = DRAWS[:i]
        for board in BOARDS:
            if is_winner(board, picks):
                return score(board, picks)

def part2():
    boards = BOARDS
    for i in range(5,len(DRAWS)): # takes at least 5 draws to win
        picks = DRAWS[:i]
        for board in boards:
            if is_winner(board, picks):
                if len(boards) == 1:
                    return score(boards[0], picks)
                boards = [b for b in boards if b!=board]

if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")


# some tests
assert not is_winner([1,2,3,4,5,6,7,8,9], {1})
assert not is_winner([1,2,3,4,5,6,7,8,9], {1,2})
assert is_winner([1,2,3,4,5,6,7,8,9], {1,2,3})

