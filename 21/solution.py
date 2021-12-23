import re
from math import floor
from copy import deepcopy

def part1(start_1, start_2):
    # this could be refactored a ton

    score_1 = 0
    pos_1 = start_1    
    score_2 = 0
    pos_2 = start_2
    total_rolls = 0
    roll = 0

    while True:

        # player 1:
        rolls = 0
        for _ in range(3):
            roll = (roll % 100) + 1
            rolls += roll

        total_rolls += 3
        pos_1 = ((pos_1+rolls))
        pos_1 -= floor((pos_1-1)/10)*10
        score_1 += pos_1
        
        if score_1 >= 1000:
            break

        # player 2:
        rolls = 0
        for _ in range(3):
            roll = (roll % 100) + 1
            rolls += roll

        total_rolls += 3
        pos_2 = ((pos_2+rolls))
        pos_2 -= floor((pos_2-1)/10)*10

        score_2 += pos_2

        if score_2 >= 1000:
            break

    return min([score_1, score_2]) * total_rolls

# there are 27 possible rolls of 3d3
# this is the distribution of their sums
THREE_D3_DISTRIBUTION = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

def multiverse_games(state, cache={}):

    # check for a winner:
    if state["player_1"]["score"] >= state["winning_score"]:
        return (1, 0)
    elif state["player_2"]["score"] >= state["winning_score"]:
        return (0, 1)

    # return the total number of wins and losses for each player from the current state
    player = state["next_turn"]
    state["next_turn"] = "player_1" if state["next_turn"] == "player_2" else "player_2"

    # there's a finite number of states (10*10*21*21 = 44100), so maybe we can avoid re-computation here.
    if str(state) in cache:
        return cache[str(state)]

    # each turn splits the universe into 27 unique possibilities
    # (which are really just weighted copies of 7 possibilities)
    p1_wins = p2_wins = 0
    for possible_roll in THREE_D3_DISTRIBUTION.keys():

        localstate = deepcopy(state)
        localstate[player]['position'] += possible_roll

        # lazy circular list (since never incrementing by more than 9)
        if localstate[player]['position'] > 10:
            localstate[player]['position'] -= 10

        localstate[player]['score'] += localstate[player]['position']
        p1_subwins, p2_subwins = multiverse_games(localstate)
        
        p1_wins += (p1_subwins * THREE_D3_DISTRIBUTION[possible_roll])
        p2_wins += (p2_subwins * THREE_D3_DISTRIBUTION[possible_roll])

    cache[str(state)] = (p1_wins, p2_wins)
    return p1_wins, p2_wins

# some tests for the above code
assert multiverse_games({"winning_score": 21, "next_turn": "player_1", "player_1": {"score": 19, "position": 6}, "player_2": {"score": 25, "position": 6}}) == (0, 1)
assert multiverse_games({"winning_score": 21, "next_turn": "player_1", "player_1": {"score": 0, "position": 4}, "player_2": {"score": 0, "position": 8}}) == (444356092776315, 341960390180808)

def part2(start_1, start_2):

    state = {
        "winning_score": 21, 
        "next_turn": "player_1",
        "player_1": {
            "position": start_1,
            "score": 0
        },
        "player_2": {
            "position": start_2,
            "score": 0
        }
    }

    p1_wins, p2_wins = multiverse_games(state)
    return max([p1_wins, p2_wins])


if __name__ == "__main__":

    with open('21/input.txt') as inputfile:
        puzzleinput = inputfile.read()
    
    matchstring = r"Player 1 starting position: (\d+)\nPlayer 2 starting position: (\d+)"
    matches = re.match(matchstring, puzzleinput)
    p1_start, p2_start = (int(position) for position in matches.groups())

    print(f"Part 1 solution: {part1(p1_start, p2_start)}")
    print(f"Part 2 solution: {part2(p1_start, p2_start)}")
