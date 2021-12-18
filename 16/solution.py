from pprint import pprint


def hex_to_bin(hex_string):

    hex_to_bits = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    return "".join([hex_to_bits[c] for c in hex_string])


def parse_packets(packet_string, count=None):

    packets = []
    while True:
        packet = parse_packet(packet_string)
        packets.append(packet)
        packet_string = packet_string[packet["length"] :]
        if len(packets) == count or len(packet_string) == 0:
            return packets


def parse_packet(packet):

    version = int(packet[:3], 2)
    type_id = int(packet[3:6], 2)

    if type_id == 4:

        cursor = 6
        binary_number = ""
        while True:
            chunk = packet[cursor : cursor + 5]
            binary_number += chunk[1:]
            cursor += 5
            if chunk[0] == "0":
                break
        number = int(binary_number, 2)

        return {
            "version": version,
            "type_id": type_id,
            "number": number,
            "length": cursor,
        }

    else:

        length_id = packet[6]
        if length_id == "0":  # get n bits of sub-packets
            length_id_length = 15
            sub_packet_length = int(packet[7:22], 2)
            sub_packets = parse_packets(
                packet[7 + length_id_length : 7 + length_id_length + sub_packet_length]
            )
            total_length = 22 + sub_packet_length

        else:  # get n subpackets
            num_packets = int(packet[7:18], 2)
            sub_packets = parse_packets(packet[18:], count=num_packets)
            total_length = 18 + sum([p["length"] for p in sub_packets])

        return {
            "version": version,
            "type_id": type_id,
            "sub_packets": sub_packets,
            "length": total_length,
        }


def decode_packet(packet):
    binary_packet = hex_to_bin(packet)
    return parse_packet(binary_packet)


def sum_versions(packet):

    if len(packet.get("sub_packets", [])) == 0:
        return packet["version"]

    version_sum = packet["version"]
    for packet in packet["sub_packets"]:
        version_sum += sum_versions(packet)

    return version_sum


def evaluate_packet(packet):

    if packet["type_id"] == 4:
        return packet["number"]

    if packet["type_id"] == 0:
        return sum([evaluate_packet(p) for p in packet["sub_packets"]])

    if packet["type_id"] == 1:
        val = 1
        for p in packet["sub_packets"]:
            val *= evaluate_packet(p)
        return val

    if packet["type_id"] == 2:
        return min([evaluate_packet(p) for p in packet["sub_packets"]])

    if packet["type_id"] == 3:
        return max([evaluate_packet(p) for p in packet["sub_packets"]])

    if packet["type_id"] == 5:
        return (
            1
            if evaluate_packet(packet["sub_packets"][0])
            > evaluate_packet(packet["sub_packets"][1])
            else 0
        )

    if packet["type_id"] == 6:
        return (
            1
            if evaluate_packet(packet["sub_packets"][0])
            < evaluate_packet(packet["sub_packets"][1])
            else 0
        )

    if packet["type_id"] == 7:
        return (
            1
            if evaluate_packet(packet["sub_packets"][0])
            == evaluate_packet(packet["sub_packets"][1])
            else 0
        )


def part1(packet):

    binary_packet = hex_to_bin(packet)
    packets = parse_packet(binary_packet)
    return sum_versions(packets)


def part2(packet):

    binary_packet = hex_to_bin(packet)
    packets = parse_packet(binary_packet)
    return evaluate_packet(packets)


# quick tests

assert hex_to_bin("FF0FF") == "11111111000011111111"

assert len(parse_packets("010100000011001000001000110000011")) == 3
assert parse_packet("110100101111111000101000") == {
    "version": 6,
    "type_id": 4,
    "number": 2021,
    "length": 21,
}

# this contains two subpackets with literal values 10 and 20
assert len(decode_packet("38006F45291200")["sub_packets"]) == 2
assert decode_packet("38006F45291200")["sub_packets"][0]["number"] == 10
assert decode_packet("38006F45291200")["sub_packets"][1]["number"] == 20

# testing part 1 with supplied input
assert part1("8A004A801A8002F478") == 16

# testing part 2 with supplied input
assert part2("C200B40A82") == 3
assert part2("04005AC33890") == 54

if __name__ == "__main__":

    with open("16/input.txt") as inputfile:
        binary_packet = inputfile.read()

    print(f"Part 1 solution: {part1(binary_packet)}")
    print(f"Part 2 solution: {part2(binary_packet)}")
