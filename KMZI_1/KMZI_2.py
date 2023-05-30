def cp_encrypt(plain_text, key):
    l0 = plain_text[:8]
    r0 = plain_text[8:]

    exp_permutation=[3,4,1,2,6,8,5,7,3,8,2,4]
    r0_exp=[r0[i-1] for i in exp_permutation]

    r0_exp_xor_key=[r0_exp[i]^key[i] for i in range(12)]
    #sbox=[
    #    [[4,6,1,3,5,7,2,5],[5,7,2,4,6,1,3,6]],
    #    [[3,5,7,2,4,6,1,7],[4,6,1,3,5,7,2,1]],
    #    [[1,3,2,1],[2,1,3,2],[3,2,1,3],[1,3,2,1]],
    #    ]

    sbox=[
    [[6,2,7,4,1,1,2,3],[5,1,2,5,3,4,1,6]],
    [[6,5,3,5,7,1,2,2],[5,1,6,4,6,3,4,7]],
    [[3,2,1,3],[2,1,3,2],[1,3,2,1],[3,2,1,3]],
    ]

    left0=r0_exp_xor_key[:4]
    middle0=r0_exp_xor_key[4:8]
    right0=r0_exp_xor_key[8:]

    row=left0[0]
    col=4*left0[1]+2*left0[2]+left0[3]
    out=sbox[0][row][col]
    out_l=[out//4,out%4//2,out%2]
    
    out_s=out_l

    row=middle0[0]
    col=4*middle0[1]+2*middle0[2]+middle0[3]
    out=sbox[1][row][col]
    out_l=[out//4,out%4//2,out%2]

    out_s=out_s+out_l

    row=2*right0[0]+right0[3]
    col=2*right0[1]+right0[2]
    out=sbox[2][row][col]
    out_l=[out//2,out%2]

    out_s=out_s+out_l
    end_permutation=[8,7,3,2,5,4,1,6]
    res=[out_s[i-1] for i in end_permutation]
    res=[res[i]^l0[i] for i in range(8)]
    return res+r0

def analiz_s1():
    sbox=[[6,2,7,4,1,1,2,3],[5,1,2,5,3,4,1,6]]
    tab=[
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
        ]
    for x in range(16):
        x_bit=[int(bit) for bit in bin(x)[2:]]
        x_bit=[0 for i in range(0, 4 - len(x_bit))] + x_bit
        row=x_bit[0]
        col=4*x_bit[1]+2*x_bit[2]+x_bit[3]
        out=sbox[row][col]
        for a in range(1,16):
            a_bit=[int(bit) for bit in bin(a)[2:]]
            a_bit=[0 for i in range(0, 4 - len(a_bit))] + a_bit
            res=[x_bit[i]&a_bit[i] for i in range(4)]
            u=0
            for g in res:
                u=u^g
            for b in range(1,8):
                b_bit=[int(bit) for bit in bin(b)[2:]]
                b_bit=[0 for i in range(0, 3 - len(b_bit))] + b_bit
                y_bit=[out//4,out%4//2,out%2]
                res=[y_bit[i]&b_bit[i] for i in range(3)]
                v=0
                for g in res:
                    v=v^g
                if u==v:
                    tab[a-1][b-1]+=1
    return tab

def analiz_s2():
    sbox=[[6,5,3,5,7,1,2,2],[5,1,6,4,6,3,4,7]]
    tab=[
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
        ]
    for x in range(16):
        x_bit=[int(bit) for bit in bin(x)[2:]]
        x_bit=[0 for i in range(0, 4 - len(x_bit))] + x_bit
        row=x_bit[0]
        col=4*x_bit[1]+2*x_bit[2]+x_bit[3]
        out=sbox[row][col]
        for a in range(1,16):
            a_bit=[int(bit) for bit in bin(a)[2:]]
            a_bit=[0 for i in range(0, 4 - len(a_bit))] + a_bit
            res=[x_bit[i]&a_bit[i] for i in range(4)]
            u=0
            for g in res:
                u=u^g
            for b in range(1,8):
                b_bit=[int(bit) for bit in bin(b)[2:]]
                b_bit=[0 for i in range(0, 3 - len(b_bit))] + b_bit
                y_bit=[out//4,out%4//2,out%2]
                res=[y_bit[i]&b_bit[i] for i in range(3)]
                v=0
                for g in res:
                    v=v^g
                if u==v:
                    tab[a-1][b-1]+=1
    return tab

def analiz_s3():
    sbox=[[3,2,1,3],[2,1,3,2],[1,3,2,1],[3,2,1,3]]
    tab=[
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        ]
    for x in range(16):
        x_bit=[int(bit) for bit in bin(x)[2:]]
        x_bit=[0 for i in range(0, 4 - len(x_bit))] + x_bit
        row=2*x_bit[0]+x_bit[3]
        col=2*x_bit[1]+x_bit[2]
        out=sbox[row][col]
        for a in range(1,16):
            a_bit=[int(bit) for bit in bin(a)[2:]]
            a_bit=[0 for i in range(0, 4 - len(a_bit))] + a_bit
            res=[x_bit[i]&a_bit[i] for i in range(4)]
            u=0
            for g in res:
                u=u^g
            for b in range(1,4):
                b_bit=[int(bit) for bit in bin(b)[2:]]
                b_bit=[0 for i in range(0, 2 - len(b_bit))] + b_bit
                y_bit=[out//2,out%2]
                res=[y_bit[i]&b_bit[i] for i in range(2)]
                v=0
                for g in res:
                    v=v^g
                if u==v:
                    tab[a-1][b-1]+=1
    return tab


ret_res=analiz_s1()
print("Analize block S1:")
print('\n'.join('\t'.join(map(str, row)) for row in ret_res))
print("\nAnalize block S2:")
ret_res=analiz_s2()
print('\n'.join('\t'.join(map(str, row)) for row in ret_res))
print("\nAnalize block S3:")
ret_res=analiz_s3()
print('\n'.join('\t'.join(map(str, row)) for row in ret_res))

#plain=[0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0]
#plain=[int(bit) for bit in input().split()]
#key=[1,0,1,0,1,0,1,0,1,0,1,0]
#res=cp_encrypt(plain,key)

#print(res)
#res=cp_encrypt(res,key)
#print(res)