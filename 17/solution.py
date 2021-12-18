import re


def simulate_trajectory(dx, dy, x_min, x_max, y_min, y_max):

    x = y = 0
    max_y = 1  # this tracks the highest arc
    while True:
        x += dx
        y += dy
        if y > max_y:
            max_y = y
        dx = dx + 1 if dx < 0 else dx - 1 if dx > 0 else 0
        dy -= 1
        if x_min <= x and x <= x_max and y_min <= y and y <= y_max:
            return max_y  # return value will be true for any hit
        if y < y_min:
            return None


def part1(x_min, x_max, y_min, y_max):

    y_range = range(
        abs(y_min) + 2
    )  # any y-velocity greater than this will way overshoot
    x_range = range(60) if x_min > 0 else range(0, -60, -1)

    max_y = 0
    for y in y_range:
        for x in x_range:
            peak_height = simulate_trajectory(x, y, x_min, x_max, y_min, y_max)
            if peak_height:
                max_y = peak_height
                break

    return max_y


def part2(x_min, x_max, y_min, y_max):

    y_magnitude = max([abs(y_min), abs(y_max)]) + 2
    x_magnitude = max([abs(x_min), abs(x_max)]) + 2

    y_range = range(
        -y_magnitude, y_magnitude
    )  # any y-velocity greater than this will overshoot
    x_range = range(-x_magnitude, x_magnitude)

    total_hits = 0
    for y in y_range:
        for x in x_range:
            if simulate_trajectory(x, y, x_min, x_max, y_min, y_max):
                total_hits += 1

    return total_hits


assert simulate_trajectory(23, -10, 20, 30, -10, -5)
assert part1(20, 30, -10, -5) == 45
assert part2(20, 30, -10, -5) == 112

if __name__ == "__main__":

    with open("17/input.txt") as inputfile:
        input_text = inputfile.read()

    match = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", input_text)
    x_min, x_max, y_min, y_max = (int(val) for val in match.groups())

    print(f"Part 1 solution: {part1(x_min, x_max, y_min, y_max)}")
    print(f"Part 2 solution: {part2(x_min, x_max, y_min, y_max)}")
