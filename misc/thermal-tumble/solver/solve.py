from __future__ import annotations

FLAG_LEN = 43
STREAM = [
    0, 21, 238, 223, 181, 141, 111, 123, 79, 43, 48, 220,
    230, 152, 146, 110, 70, 33, 41, 37, 244, 205, 178, 130,
    110, 91, 26, 10, 22, 248, 220, 137, 135, 120, 72, 21,
    6, 234, 210, 201, 190, 138, 104,
]


def find_parameters() -> tuple[int, int]:
    matches = []
    for cycle in range(8):
        for temperature in range(30, 91):
            selector = (
                (cycle * 0x31 + temperature * 0x17 + 0x29)
                ^ ((cycle + 3) * temperature)
            ) & 0xFFF
            band = (cycle * 13 + temperature * 5) % 17
            if selector == 0x54F and band == 1:
                matches.append((cycle, temperature))
    if len(matches) != 1:
        raise ValueError(f"expected one parameter pair, found {matches}")
    return matches[0]


def decode() -> str:
    return bytes(
        value ^ ((index * 0x1D + 0x53) & 0xFF)
        for index, value in enumerate(STREAM[:FLAG_LEN])
    ).decode("ascii")


if __name__ == "__main__":
    cycle, temperature = find_parameters()
    print(f"parameters: cycle={cycle}, temperature={temperature}")
    print(decode())
