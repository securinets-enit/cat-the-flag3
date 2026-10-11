import sys

def check(candidate):
    b = candidate.encode("ascii")
    if len(b) != 49:
        return False
    assert ((b[0] ^ 49) + b[1]) & 255 == 199
    assert ((b[1] ^ 50) + b[2]) & 255 == 186
    assert ((b[2] ^ 51) + b[3]) & 255 == 197
    assert ((b[3] ^ 52) + b[4]) & 255 == 179
    assert ((b[4] ^ 53) + b[5]) & 255 == 176
    assert ((b[5] ^ 54) + b[6]) & 255 == 205
    assert ((b[6] ^ 55) + b[7]) & 255 == 190
    assert ((b[7] ^ 56) + b[8]) & 255 == 209
    assert ((b[8] ^ 57) + b[9]) & 255 == 192
    assert ((b[9] ^ 58) + b[10]) & 255 == 142
    assert ((b[10] ^ 59) + b[11]) & 255 == 204
    assert ((b[11] ^ 60) + b[12]) & 255 == 187
    assert ((b[12] ^ 61) + b[13]) & 255 == 200
    assert ((b[13] ^ 62) + b[14]) & 255 == 229
    assert ((b[14] ^ 63) + b[15]) & 255 == 190
    assert ((b[15] ^ 64) + b[16]) & 255 == 109
    assert ((b[16] ^ 65) + b[17]) & 255 == 209
    assert ((b[17] ^ 66) + b[18]) & 255 == 131
    assert ((b[18] ^ 67) + b[19]) & 255 == 142
    assert ((b[19] ^ 68) + b[20]) & 255 == 155
    assert ((b[20] ^ 69) + b[21]) & 255 == 143
    assert ((b[21] ^ 70) + b[22]) & 255 == 149
    assert ((b[22] ^ 71) + b[23]) & 255 == 147
    assert ((b[23] ^ 72) + b[24]) & 255 == 139
    assert ((b[24] ^ 73) + b[25]) & 255 == 165
    assert ((b[25] ^ 74) + b[26]) & 255 == 135
    assert ((b[26] ^ 75) + b[27]) & 255 == 141
    assert ((b[27] ^ 76) + b[28]) & 255 == 123
    assert ((b[28] ^ 77) + b[29]) & 255 == 142
    assert ((b[29] ^ 78) + b[30]) & 255 == 139
    assert ((b[30] ^ 79) + b[31]) & 255 == 143
    assert ((b[31] ^ 80) + b[32]) & 255 == 153
    assert ((b[32] ^ 81) + b[33]) & 255 == 162
    assert ((b[33] ^ 82) + b[34]) & 255 == 155
    assert ((b[34] ^ 83) + b[35]) & 255 == 111
    assert ((b[35] ^ 84) + b[36]) & 255 == 166
    assert ((b[36] ^ 85) + b[37]) & 255 == 168
    assert ((b[37] ^ 86) + b[38]) & 255 == 171
    assert ((b[38] ^ 87) + b[39]) & 255 == 152
    assert ((b[39] ^ 88) + b[40]) & 255 == 145
    assert ((b[40] ^ 89) + b[41]) & 255 == 168
    assert ((b[41] ^ 90) + b[42]) & 255 == 162
    assert ((b[42] ^ 91) + b[43]) & 255 == 152
    assert ((b[43] ^ 92) + b[44]) & 255 == 177
    assert ((b[44] ^ 93) + b[45]) & 255 == 146
    assert ((b[45] ^ 94) + b[46]) & 255 == 166
    assert ((b[46] ^ 95) + b[47]) & 255 == 158
    assert ((b[47] ^ 96) + b[48]) & 255 == 139
    return b.startswith(b"SecurinetsENIT{") and b.endswith(b"}")

if __name__ == "__main__":
    print("accepted" if check(sys.argv[1]) else "rejected")
