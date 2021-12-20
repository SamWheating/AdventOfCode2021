from math import floor, ceil
from copy import deepcopy

class SFN: # snail fish number

    # this is pretty much just a binary tree from scratch, with a bunch of convenience functions.

    def __init__(self, sfn_string="[0,0]", parent=None):

        # need to find the delineation between two pairs:
        left, right = self.split_nested_list(sfn_string)
        self.left = SFN(left, parent=self) if "[" in left else int(left)
        self.right = SFN(right, parent=self) if "[" in right else int(right)
        self.parent=parent

    def __add__(self, other):

        sfn = SFN()
        sfn.left = self
        sfn.left.parent = sfn
        sfn.right = other
        sfn.right.parent = sfn
        sfn.reduce()
        return sfn

    def __repr__(self):

        return str(self.values())

    def enumerate_nodes(self, depth=0, idx=0):
        # recursively build a list of values and their depths
        nodes = []
        if isinstance(self.left, SFN):
            nodes.extend(self.left.enumerate_nodes(depth=depth+1))
        else:
            nodes.append({'val': self.left, 'depth': depth, 'parent': self, 'direction':'left'})
        if isinstance(self.right, SFN):
            nodes.extend(self.right.enumerate_nodes(depth=depth+1))
        else:
            nodes.append({'val': self.right, 'depth': depth, 'parent': self, 'direction':'right'})
        
        return nodes

    def split(self):

        if isinstance(self.left, int) and self.left > 9:
            self.left = SFN(f"[{floor(self.left/2)},{ceil(self.left/2)}]", parent=self)
            return True

        elif isinstance(self.left, SFN) and self.left.split():
            return True
        
        elif isinstance(self.right, int) and self.right > 9:
            self.right = SFN(f"[{floor(self.right/2)},{ceil(self.right/2)}]", parent=self)
            return True

        elif isinstance(self.right, SFN) and self.right.split():
            return True 

    def explode(self):

        # this is where things get really messy and my nice OOP falls apart

        nodes = self.enumerate_nodes()
        for i in range(len(nodes)):
            if nodes[i]["depth"] == 4:
                # try to increment the left value:
                if i != 0:
                    setattr(nodes[i-1]["parent"], nodes[i-1]["direction"], nodes[i-1]['val'] + nodes[i]["val"])
                # try to increment the right value
                if i < len(nodes)-2:
                    setattr(nodes[i+2]["parent"], nodes[i+2]["direction"], nodes[i+2]['val'] + nodes[i+1]["val"])
                # replace this pair with a zero
                if isinstance(nodes[i]["parent"].parent.left, SFN):
                    nodes[i]["parent"].parent.left = 0
                else:
                    nodes[i]["parent"].parent.right = 0
                return


    def reduce(self):

        while True:

            if self.depth() >= 4:
                self.explode()
                continue
        
            if max(self.values()) > 9:
                self.split()
                continue

            break
            
    def magnitude(self):

        if isinstance(self.left, SFN):
            mag = 3*self.left.magnitude()
        else:
            mag = 3*self.left

        if isinstance(self.right, SFN):
            mag += 2*self.right.magnitude()
        else:
            mag += 2*self.right

        return mag

    def values(self):
        vals = []
        for side in self.left, self.right:
            if isinstance(side, int):
                vals.append(side)
            else:
                vals.extend(side.values())
        return vals

    def depth(self):
        if isinstance(self.left, int) and isinstance(self.right, int):
            return 0
        
        return 1+ max([side.depth() for side in [self.left, self.right] if isinstance(side, SFN)])

    @staticmethod
    def split_nested_list(nested_list):
        # splits something like "[[1,2], 3]" into "[1,2]", "3"
        open = 0
        for i in range(1,len(nested_list)):
            if nested_list[i] == '[':
                open += 1
            elif nested_list[i] == ']':
                open -= 1
            if nested_list[i] == "," and open == 0:
                return nested_list[1:i], nested_list[i+1:-1]

def part1(lines):

    sfns = []
    for line in lines:
        sfns.append(SFN(line))

    sfn = sfns[0]
    for s in sfns[1:]:
        sfn = sfn + s

    return sfn.magnitude()


def part2(lines):

    max = 0
    for a in range(len(lines)):
        for b in range(len(lines)):
            if a != b:
                val = (SFN(lines[a]) + SFN(lines[b])).magnitude()
                if val > max:
                    max = val

    return max


if __name__ == "__main__":

    # Testing constructor
    test_sfn = SFN("[9,7]")
    assert test_sfn.right == 7 and test_sfn.left == 9
    test_sfn = SFN("[[1,2],3]")
    assert test_sfn.left.left == 1 and test_sfn.left.right == 2 and test_sfn.right == 3

    # Testing string parsing
    assert SFN.split_nested_list("[1,2]") == ('1','2')
    assert SFN.split_nested_list("[[1,2],3]") == ("[1,2]", "3")
    assert SFN.split_nested_list("[[1,[4,[9,9]]],[9,3]]") == ("[1,[4,[9,9]]]", "[9,3]")

    # testing depth:
    assert SFN("[1,1]").depth() == 0
    assert SFN("[[6,[5,[4,[3,2]]]],1]").depth() == 4

    # testing values:
    assert SFN("[1,1]").values() == [1,1]
    assert SFN("[[6,[5,[4,[3,2]]]],1]").values() == [6,5,4,3,2,1]

    # testing split:
    test_sfn = SFN("[15, 1]")
    test_sfn.split()
    assert test_sfn.values() == [7,8,1]

    test_sfn = SFN("[[[[15,1],3],4],1]")
    test_sfn.split()
    assert test_sfn.values() == [7,8,1,3,4,1]

    # testing reduce:
    test_sfn = SFN("[15, 1]")
    test_sfn.reduce()
    assert test_sfn.values() == [7,8,1]

    test_sfn = SFN("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    test_sfn.reduce()
    assert test_sfn.values() == [0,7,4,7,8,6,0,8,1]

    # testing add:
    test_sfn = SFN("[1,3]") + SFN("[6,7]")
    assert test_sfn.values() == [1,3,6,7]

    test_sfn = SFN("[1,3]") + SFN("[15,7]")
    assert test_sfn.values() == [1,3,7,8,7]

    # testing magnitude
    assert SFN("[9,1]").magnitude() == 29
    assert SFN("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude() == 1384

    # testing node explosion:
    test_sfn = SFN("[[[[[9,8],1],2],3],4]")
    test_sfn.explode()
    assert test_sfn.values() == [0,9,2,3,4]

    test_sfn = SFN("[7,[6,[5,[4,[3,2]]]]]")
    test_sfn.explode()
    assert test_sfn.values() == [7,6,5,7,0]

    # here's the actual problem

    with open("18/input.txt") as inputfile:
        lines = inputfile.read().split("\n")

    print(f"Part 1 solution: {part1(lines)}")
    print(f"Part 2 solution: {part2(lines)}")
