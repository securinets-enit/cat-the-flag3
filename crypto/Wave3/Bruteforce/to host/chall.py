#!/usr/bin/env -S python3 -u
flag = "brut3_f0rc3_1s_n0t_4ll0w3d_1n_s3curinets"
print("Don't even think to guess the flag , it is 33 characters long!")
user_input = input()
print(len(flag))
index = 0
for char in user_input:
    if char != flag[index]:
        print("Wrong flag!")
        exit()
    index += 1

print("Correct flag!")
print("flag is : SecurinetsENIT{" +user_input + "}")