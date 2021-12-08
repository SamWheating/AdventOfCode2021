import copy
import itertools

with open('8/input.txt') as inputfile:
    inputlines = inputfile.read().split("\n")

def part1():
    outputs = [line.split(" | ")[1] for line in inputlines]
    characters = 0
    for output in outputs:
        for character in output.split(" "):
            if len(character) in set([2,4,7,3]):
                characters += 1
    return characters

def part2():

    # there's only 7! (5040) possible mappings, so we can probably just brute force + validate
    def generate_mappings(characters):
        
        mappings = []
        for inputs in itertools.permutations(characters):
            mappings.append({characters[i]: inputs[i] for i in range(len(characters))})

        return mappings

    ALL_MAPPINGS = generate_mappings(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    assert len(ALL_MAPPINGS) == 5040

    # 0:      1:      2:      3:      4:
    #  aaaa    ....    aaaa    aaaa    ....
    # b    c  .    c  .    c  .    c  b    c
    # b    c  .    c  .    c  .    c  b    c
    #  ....    ....    dddd    dddd    dddd
    # e    f  .    f  e    .  .    f  .    f
    # e    f  .    f  e    .  .    f  .    f
    #  gggg    ....    gggg    gggg    ....

    # 5:      6:      7:      8:      9:
    #  aaaa    aaaa    aaaa    aaaa    aaaa
    # b    .  b    .  .    c  b    c  b    c
    # b    .  b    .  .    c  b    c  b    c
    #  dddd    dddd    ....    dddd    dddd
    # .    f  e    f  .    f  e    f  .    f
    # .    f  e    f  .    f  e    f  .    f
    #  gggg    gggg    ....    gggg    gggg

    DIGIT_SHAPES = {
        frozenset({'a', 'b', 'c', 'e', 'f', 'g'}): '0',
        frozenset({'c', 'f'}): '1',
        frozenset({'a', 'c', 'd', 'e', 'g'}): '2',
        frozenset({'a', 'c', 'd', 'f', 'g'}): '3',
        frozenset({'b', 'c', 'd', 'f'}): '4',
        frozenset({'a', 'b', 'd', 'f', 'g'}): '5',
        frozenset({'a', 'b', 'd', 'e', 'f', 'g'}): '6',
        frozenset({'a', 'c', 'f'}): '7',
        frozenset({'a', 'b', 'c', 'd', 'e', 'f', 'g'}): '8',
        frozenset({'a', 'b', 'c', 'd', 'f', 'g'}): '9'
    }

    def validate_mapping(mapping, digits):
        # input is a list of all displayed digits like:
        #  [cdbga acbde eacdfbg adbgf gdebcf bcg decabf cg ebdgac egca]
        # and a mapping which maps input connection to output segment.
        # check that every to_output(input_char) is in DIGIT_SHAPES
        for digit in digits:
            word = frozenset([mapping[l] for l in digit])
            if word not in DIGIT_SHAPES:
                return False
        return True


    sample_chars = ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab']
    sample_mapping = {'d':'a', 'e':'b', 'a':'c', 'f':'d', 'g':'e', 'b':'f', 'c':'g'}
    assert validate_mapping(sample_mapping, sample_chars)

    # Now we can just find the correct mapping for every input sample, decode the display and sum the result.
    sum_of_displays = 0
    for line in inputlines:
        key, code = line.split(" | ")
        sample_chars = key.split(" ")
        codec = None
        for mapping in ALL_MAPPINGS:
            if validate_mapping(mapping, sample_chars):
                codec = mapping
        if not codec:
            raise Exception("no match found!")
        # now we have the codec,  decode the digits and cast to int
        code_words = code.split(" ")
        output_int = ""
        for digit in code_words:
            decoded_digit = frozenset([codec[c] for c in digit])
            output_int += DIGIT_SHAPES[decoded_digit]
        
        sum_of_displays += int(output_int)
        
    return sum_of_displays


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
