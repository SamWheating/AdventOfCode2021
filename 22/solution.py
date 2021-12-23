import re

class Cube:

    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def __repr__(self):

        return f"x={self.x_min}..{self.x_max},y={self.y_min}..{self.y_max},z={self.z_min}..{self.z_max}"

    def volume(self):

        # rule out inside-out or zero-width cubes
        if min([(self.x_max - self.x_min), (self.y_max - self.y_min), (self.z_max - self.z_min)]) < 0:
            return 0

        return ((1+ self.x_max - self.x_min) * (1+ self.y_max - self.y_min) * (1+self.z_max - self.z_min))

    def crop(self, other):
        # trim a cube to the extents of another cube
        self.x_min = max(self.x_min, other.x_min)
        self.x_max = min(self.x_max, other.x_max)
        self.y_min = max(self.y_min, other.y_min)
        self.y_max = min(self.y_max, other.y_max)
        self.z_min = max(self.z_min, other.z_min)
        self.z_max = min(self.z_max, other.z_max)

    def difference(self, other):
        # split self into 27 sub-cubes based on the bounds of other cube
        # return only the cubes which have positive volume and don't overlap with the other cube.

        cubes = []
        for x in [(self.x_min, other.x_min-1), (other.x_min, other.x_max), (other.x_max+1, self.x_max)]:
            for y in [(self.y_min, other.y_min-1), (other.y_min, other.y_max), (other.y_max+1, self.y_max)]:
                for z in [(self.z_min, other.z_min-1), (other.z_min, other.z_max), (other.z_max+1, self.z_max)]:
                    cubes.append(Cube(x[0], x[1], y[0], y[1], z[0], z[1]))

        real_cubes = []
        for cube in cubes:
            cube.crop(self)
            if not cube.overlaps(other):
                if cube.volume() >= 1:
                    real_cubes.append(cube)

        return real_cubes
            

    def overlaps(self, other):
        # determine if two cubes overlap at all
        if self.x_max < other.x_min or self.x_min > other.x_max:
            return False
        if self.y_max < other.y_min or self.y_min > other.y_max:
            return False
        if self.z_max < other.z_min or self.z_min > other.z_max:
            return False
        return True

class Cubespace:

    def __init__(self):
        self.cubes = set()

    def total_active(self):
        return sum([c.volume() for c in self.cubes])

    def __add__(self, cube):

        # Add the new cube t the space while maintaining no overlaps
        # 1) clear out space for the new cube by subtracting it from the space.
        # 2) add the new cube

        self -= cube
        self.cubes.add(cube)

        return self

    def __sub__(self, cube):

        updated_cubes = set()

        for c in self.cubes:
            if c.overlaps(cube):
                new_cubes = c.difference(cube)
                updated_cubes.update(new_cubes)
            else:
                updated_cubes.add(c)

        self.cubes = updated_cubes

        return self

# lazy inline tests for the Cube class;

cube1 = Cube(1,10,1,10,1,10)
cube2 = Cube(6,15,6,15,6,15)
cube3 = Cube(11,20,11,20,11,20) # overlaps with cube2 but not cube1
cube4 = Cube(2,4,2,4,2,4)

assert cube1.volume() == 1000
assert cube2.volume() == 1000

assert cube1.overlaps(cube2)
assert cube2.overlaps(cube1)
assert not cube1.overlaps(cube3)
assert cube1.overlaps(cube4)

print(cube1.difference(cube2))
print(sum([c.volume() for c in cube1.difference(cube2)]))

assert len(cube1.difference(cube4)) == 26
assert sum([c.volume() for c in cube1.difference(cube4)]) == 1000-27

# Tests for the Cubespace class:

cs = Cubespace()
cs += cube1

assert cs.total_active() == 1000
cs += cube3
assert cs.total_active() == 2000

cs = Cubespace()
cs += cube1
cs += cube3
cs -= cube4
assert cs.total_active() == (cube1.volume() + cube3.volume() - cube4.volume())

def part1(commands):

    return part2([c for c in commands if max([abs(c[k]) for k in c.keys() if k != "op"]) < 50])

def part2(commands):

    cs = Cubespace()

    for command in commands:
        cube = Cube(command["x_min"], command["x_max"], command["y_min"], command["y_max"], command["z_min"], command["z_max"])
        if command["op"] == "on":
            cs += cube
        elif command["op"] == "off":
            cs -= cube

    return cs.total_active()

if __name__ == "__main__":

    with open("22/input.txt") as inputfile:
        input_lines = inputfile.read().split("\n")

    # on x=-17..35,y=-35..15,z=-27..25
    matchstring = r"([onf]+)\ x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"

    commands = []
    for line in input_lines:
        match = re.match(matchstring, line)
        op = match.groups()[0]
        assert op in ['on', 'off']
        x_min, x_max, y_min, y_max, z_min, z_max = (int(val) for val in match.groups()[1:])
        commands.append({"op": op, "x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max, "z_min": z_min, "z_max": z_max})

    print(f"Part 1 Solution: {part1(commands)}")
    print(f"Part 2 Solution: {part2(commands)}")