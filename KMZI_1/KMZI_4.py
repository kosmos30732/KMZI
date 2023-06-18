import random
import numpy as np

exp = [2, 0, 3, 1, 2, 0, 3, 1]
PERMUTATION = [1, 2, 3, 0]
BLOCK1 = {
    0: [2, 3, 1, 3],
    1: [1, 0, 0, 2],
    2: [3, 2, 3, 1],
    3: [1, 0, 2, 0]
}
BLOCK2 = {
    0: [0, 1, 2, 0],
    1: [1, 2, 1, 2],
    2: [3, 1, 2, 3],
    3: [0, 3, 3, 2]
}
MASK = '1010'


def permute(data, mapper):
    res = ''
    for i in mapper:
        res += data[i]
    return int(res, 2)


def F(right_part, key):
    right_part = permute(right_part, exp)
    right_xor_key = right_part ^ key
    right_xor_key = str(bin(right_xor_key)[2:]).rjust(8, '0')

    block1 = right_xor_key[:4]
    block1 = BLOCK1[int(block1[0] + block1[3], 2)][int(block1[1] + block1[2], 2)]
    block1 = str(bin(block1)[2:].rjust(2, '0'))

    block2 = right_xor_key[4:]
    block2 = BLOCK2[int(block2[0] + block2[3], 2)][int(block2[1] + block2[2], 2)]
    block2 = str(bin(block2)[2:].rjust(2, '0'))

    return permute(block1 + block2, PERMUTATION)


def encrypt(plaintext, key):
    plaintext = str(bin(plaintext)[2:]).rjust(8, '0')
    left_part = plaintext[:4]
    right_part = plaintext[4:]
    left_part2 = int(left_part, 2) ^ F(right_part, key)

    res = right_part + str(bin(left_part2)[2:].rjust(4, '0'))
    return res


def decrypt(ciphertext, key):
    ciphertext = str(bin(ciphertext)[2:]).rjust(8, '0')
    left_part = ciphertext[:4]
    right_part = ciphertext[4:]
    left_part2 = int(left_part, 2) ^ F(right_part, key)

    res = right_part + str(bin(left_part2)[2:].rjust(4, '0'))
    return res


def E(plaintext, key):
    for i in range(37):
        plaintext = int(encrypt(plaintext, key), 2)
    plaintext = str(bin(plaintext)[2:]).rjust(8, '0')
    return plaintext[4:] + plaintext[:4]

def find_sub_key(p, p1, e, e1):
    l_part = int(p[:4], 2)
    r_part = int(p[4:], 2)
    l_part1 = int(p1[:4], 2)
    r_part1 = int(p1[4:], 2)

    l_e = int(e[:4], 2)
    r_e = int(e[4:], 2)
    l_e1 = int(e1[:4], 2)
    r_e1 = int(e1[4:], 2)

    f1 = l_part ^ r_part1
    permutation = [3, 0, 1, 2]
    f1 = permute(str(bin(f1)[2:]).rjust(4, '0'), permutation)
    s1 = str(bin(f1)[2:].rjust(4, '0'))[:2]
    s2 = str(bin(f1)[2:].rjust(4, '0'))[2:]

    k1 = []
    k2 = []
    for i in range(len(BLOCK1)):
        for j in range(len(BLOCK1[i])):
            if BLOCK1[i][j] == int(s1, 2):
                i_tp = str(bin(i)[2:]).rjust(2, '0')
                j_tp = str(bin(j)[2:]).rjust(2, '0')
                # print(i_tp[0] + j_tp + i_tp[1])
                k1.append(int(i_tp[0] + j_tp + i_tp[1],2))
            if BLOCK2[i][j] == int(s2, 2):
                i_tp = str(bin(i)[2:]).rjust(2, '0')
                j_tp = str(bin(j)[2:]).rjust(2, '0')
                # print(i_tp[0] + j_tp + i_tp[1])
                k2.append(int(i_tp[0] + j_tp + i_tp[1],2))

    permutation = exp
    f1 = permute(str(bin(r_part)[2:]).rjust(4, '0'), permutation)
    s1 = int(str(bin(f1)[2:].rjust(8, '0'))[:4],2)
    s2 = int(str(bin(f1)[2:].rjust(8, '0'))[4:],2)
    kk1 = []
    kk2 = []
    for k in k1:
        kk1.append(str(bin(k ^ s1)[2:]).rjust(4, '0'))

    for k in k2:
        kk2.append(str(bin(k ^ s2)[2:]).rjust(4, '0'))

    f1 = l_e1 ^ r_e
    permutation = [3, 0, 1, 2]
    f1 = permute(str(bin(f1)[2:]).rjust(4, '0'), permutation)
    s1 = str(bin(f1)[2:].rjust(4, '0'))[:2]
    s2 = str(bin(f1)[2:].rjust(4, '0'))[2:]

    e1 = []
    e2 = []
    for i in range(len(BLOCK1)):
        for j in range(len(BLOCK1[i])):
            if BLOCK1[i][j] == int(s1, 2):
                i_tp = str(bin(i)[2:]).rjust(2, '0')
                j_tp = str(bin(j)[2:]).rjust(2, '0')
                # print(i_tp[0] + j_tp + i_tp[1])
                e1.append(int(i_tp[0] + j_tp + i_tp[1], 2))
            if BLOCK2[i][j] == int(s2, 2):
                i_tp = str(bin(i)[2:]).rjust(2, '0')
                j_tp = str(bin(j)[2:]).rjust(2, '0')
                # print(i_tp[0] + j_tp + i_tp[1])
                e2.append(int(i_tp[0] + j_tp + i_tp[1], 2))

    permutation = exp
    f1 = permute(str(bin(r_e1)[2:]).rjust(4, '0'), permutation)
    s1 = int(str(bin(f1)[2:].rjust(8, '0'))[:4], 2)
    s2 = int(str(bin(f1)[2:].rjust(8, '0'))[4:], 2)
    ee1 = []
    ee2 = []
    for k in e1:
        ee1.append(str(bin(k ^ s1)[2:]).rjust(4, '0'))

    for k in e2:
        ee2.append(str(bin(k ^ s2)[2:]).rjust(4, '0'))

    return kk1, kk2, ee1, ee2


key = 0b11000110

# generate slide pairs
try_key = []
for p in range(128, 256):
    e = E(p, key)
    p2 = encrypt(p, key)
    e2 = E(int(p2, 2), key)
    if str(bin(p)[2:]).rjust(8, '0')[4:] == p2[:4] == MASK:
        if e[:4] == e2[4:]:
            print(f"x = {str(bin(p)[2:]).rjust(8, '0')}, y = {e}, "
                    f"x* = {p2}, y* = {e2}")
            k1, k2, kk1, kk2 = find_sub_key(str(bin(p)[2:]).rjust(8, '0'), p2, e, e2)
            print(f"First two rounds = {k1}, k2 = {k2}")
            print(f"Last two rounds = {kk1}, k2 = {kk2}")
            print("")
            for k in k1:
                for kk in k2:
                    try_key.append(k+kk)
            for k in kk1:
                for kk in kk2:
                    try_key.append(k+kk)
keys = {}
for kk in try_key:
    keys[kk] = 1

for kk in try_key:
    keys[kk] += 1

for item, amount in keys.items():
    print("{} ({})".format(item, amount))
