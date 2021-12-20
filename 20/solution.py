# this problem is complicated because the far away pixels are always changing.
# 9 dark pixels -> light pixel
# 9 light pixels -> dark pixel
# so we have to switch between explicitly storing light pixels and explicitly storing dark pixels

def get_neighbours_int(image, x, y, inverted=False):

    num = ""
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            if (x+dx, y+dy) in image:
                num += "1"
            else:
                num += "0"

    if inverted:
        num = "".join(["1" if c == "0" else "0" for c in num])
    
    return int(num, 2)

assert get_neighbours_int({(0,0), (2,2)}, 1, 1) == 257
assert get_neighbours_int({(0,2), (2,2)}, 1, 1) == 5
assert get_neighbours_int({(0,2), (2,2)}, 8, 8) == 0
assert get_neighbours_int({(0,2), (2,2)}, 8, 8, inverted=True) == 511

def enhance(image, codec, inverted=False):

    x_max = max([coord[0] for coord in image]) + 10
    x_min = min([coord[0] for coord in image]) - 10
    y_max = max([coord[1] for coord in image]) + 10
    y_min = min([coord[1] for coord in image]) - 10

    new_image = set()

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):

            num = get_neighbours_int(image, x, y, inverted)

            if codec[num] == "#" and not inverted:
                new_image.add((x,y))

            elif codec[num] == "." and inverted:
                new_image.add((x,y))

    return new_image

def invert(image):
    # switch the image from storing dark pixels to light pixels
    x_max = max([coord[0] for coord in image]) + 2
    x_min = min([coord[0] for coord in image]) - 2
    y_max = max([coord[1] for coord in image]) + 2
    y_min = min([coord[1] for coord in image]) - 2

    new_image = set()

    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            if (x,y) not in image:
                new_image.add((x,y))

    return new_image

def crop(image, n):
    # remove any pixels from n which are within n pixels of the edge
    x_max = max([coord[0] for coord in image])
    x_min = min([coord[0] for coord in image])
    y_max = max([coord[1] for coord in image])
    y_min = min([coord[1] for coord in image])

    new_image = set()

    for pixel in image:
        if pixel[0] < (x_min + n):
            continue
        if pixel[0] > (x_max - n):
            continue
        if pixel[1] < (y_min + n):
            continue
        if pixel[1] > (y_max - n):
            continue

        new_image.add(pixel)

    return new_image

def print_image(image):

    x_max = max([coord[0] for coord in image])
    x_min = min([coord[0] for coord in image])
    y_max = max([coord[1] for coord in image])
    y_min = min([coord[1] for coord in image])

    x_offset = -1*x_min

    line_length = x_max - x_min + 1
    for y in range(y_min, y_max+1):
        line = ["."] * line_length
        for x in range(x_min, x_max+1):
            if (x,y) in image:
                line[x+x_offset] = "#"

        print("".join(line))
    print("\n")


def part1(image, codec):

    # enhance the image twice
    # because background colour changes, we have to crop and invert between enhancements

    image = enhance(image, codec)
    image = invert(image) # image now tracks dark pixels
    image = crop(image, 4)
    image = enhance(image, codec, inverted=True)
    image = invert(image)
    image = crop(image, 4)
    return len(image)

def part2(image, codec):

    for _ in range(25):
        image = enhance(image, codec)
        image = invert(image) # image now tracks dark pixels
        image = crop(image, 4)
        image = enhance(image, codec, inverted=True)
        image = invert(image)  # image now tracks light pixels
        image = crop(image, 4)

    return len(image)

if __name__ == "__main__":

    with open("20/input.txt") as inputfile:
        lines = inputfile.read().split("\n")

    codec = lines[0]

    image = set()
    image_lines = lines[2:]
    for y in range(len(image_lines)):
        for x in range(len(image_lines[0])):
            if image_lines[y][x] == "#":
                image.add((x,y))

    print(f"Part 1 solution: {part1(image, codec)}")
    print(f"Part 2 solution: {part2(image, codec)}")
    