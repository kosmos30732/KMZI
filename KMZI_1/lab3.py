from TableIt import printTable
def build_table(pairs):
    pass


def main():
    BLOCK1 = {
        0: [6,2,7,4,1,1,2,3],
        1: [5,1,2,5,3,4,1,6]
        # 0: [4, 6, 1, 3, 5, 7, 2, 5],
        # 1: [5, 7, 2, 4, 6, 1, 3, 6]
    }
    BLOCK2 = {
        0: [6,5,3,5,7,1,2,2],
        1: [5,1,6,4,6,3,4,7]
    }
    BLOCK3 = {
        0: [3,2,1,3],
        1: [2,1,3,2],
        2: [1,3,2,1],
        3: [3,2,1,3]
        # 0: [1, 3, 2, 1],
        # 1: [2, 1, 3, 2],
        # 2: [3, 2, 1, 3],
        # 3: [1, 3, 2, 1]
    }

    # generate all delta_a
    delta_a = [i for i in range(1, 16)]

    # calculate all pairs to get delta_a
    # calculate delta_c
    pairs1 = {i: {j: 0 for j in range(0, 9)} for i in range(0, 16)}
    pairs2 = {i: {j: 0 for j in range(0, 9)} for i in range(0, 16)}
    pairs3 = {i: {j: 0 for j in range(0, 5)} for i in range(0, 16)}
    s_i = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    pairs1[0] = ["da/dc", 0, 1, 2, 3, 4, 5, 6, 7]
    pairs2[0] = ["da/dc", 0, 1, 2, 3, 4, 5, 6, 7]
    pairs3[0] = ["da/dc", 0, 1, 2, 3]

    for r in range(len(pairs1)):
        for c in range(len(pairs1[r])):
            if c == 0 and r > 0:
                pairs1[r][c] = s_i[r - 1]
                pairs2[r][c] = s_i[r - 1]

    for r in range(len(pairs3)):
        for c in range(len(pairs3[r])):
            if c == 0 and r > 0:
                pairs3[r][c] = s_i[r - 1]

    itter = 1

    for a in delta_a:
        # print(f"All pairs for {str(bin(a))[2:].rjust(4, '0')}")
        for i in range(16):
            for j in range(16):
                if i ^ j == a:
                    # print(f"{itter}: {str(bin(i))[2:].rjust(4, '0')} xor {str(bin(j))[2:].rjust(4, '0')}")
                    # print()
                    i_out = BLOCK1[int(str(bin(i))[2:].rjust(4, '0')[0], 2)][int(str(bin(i))[2:].rjust(4, '0')[1:], 2)]
                    j_out = BLOCK1[int(str(bin(j))[2:].rjust(4, '0')[0], 2)][int(str(bin(j))[2:].rjust(4, '0')[1:], 2)]
                    pairs1[a][(i_out ^ j_out) + 1] += 1

                    i_out = BLOCK2[int(str(bin(i))[2:].rjust(4, '0')[0], 2)][int(str(bin(i))[2:].rjust(4, '0')[1:], 2)]
                    j_out = BLOCK2[int(str(bin(j))[2:].rjust(4, '0')[0], 2)][int(str(bin(j))[2:].rjust(4, '0')[1:], 2)]
                    pairs2[a][(i_out ^ j_out) + 1] += 1

                    i_out = BLOCK3[int(str(bin(i))[2:].rjust(4, '0')[:2], 2)][int(str(bin(i))[2:].rjust(4, '0')[2:], 2)]
                    j_out = BLOCK3[int(str(bin(j))[2:].rjust(4, '0')[:2], 2)][int(str(bin(j))[2:].rjust(4, '0')[2:], 2)]
                    pairs3[a][(i_out ^ j_out) + 1] += 1

                    itter += 1
        itter = 1
        # print()


    printTable(pairs1, True)
    printTable(pairs2, True)
    printTable(pairs3, True)

    

    pass


if __name__ == "__main__":
    main()
