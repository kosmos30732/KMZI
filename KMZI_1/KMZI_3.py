sbox=[
        [[4,6,1,3,5,7,2,5],[5,7,2,4,6,1,3,6]],
        [[3,5,7,2,4,6,1,7],[4,6,1,3,5,7,2,1]],
        [[1,3,2,1],[2,1,3,2],[3,2,1,3],[1,3,2,1]],
        ]

def cp_encrypt(plain_text, key):
    l0 = plain_text[:8]
    r0 = plain_text[8:]

    exp_permutation=[3,4,1,2,6,8,5,7,3,8,2,4]
    r0_exp=[r0[i-1] for i in exp_permutation]

    #print("r0_exp= ",r0_exp)

    r0_exp_xor_key=[r0_exp[i]^key[i] for i in range(12)]

    #sbox=[
    #[[6,2,7,4,1,1,2,3],[5,1,2,5,3,4,1,6]],
    #[[6,5,3,5,7,1,2,2],[5,1,6,4,6,3,4,7]],
    #[[3,2,1,3],[2,1,3,2],[1,3,2,1],[3,2,1,3]],
    #]

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
    return res+r0,r0_exp

perm=[7,4,3,6,5,8,2,1]
key=[1,0,1,0,1,0,1,0,1,0,1,0]
mask=[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]
dA=[1,1,1,1,1,1,1,1,1,1,1,1]
dC=[1,0,1,1,1,1,0,1]
matr=[]
for i in range(16):
    res=[]
    x = [int(bit) for bit in bin(i)[2:]]
    x = [0 for i in range(0, 4 - len(x))] + x
    row=x[0]
    col=4*x[1]+2*x[2]+x[3]
    out=sbox[0][row][col]
    out=[out//4,out%4//2,out%2]
    res.append(out)

    row=x[0]
    col=4*x[1]+2*x[2]+x[3]
    out=sbox[1][row][col]
    out=[out//4,out%4//2,out%2]
    res.append(out)

    row=2*x[0]+x[3]
    col=2*x[1]+x[2]
    out=sbox[2][row][col]
    out=[out//2,out%2]
    res.append(out)
    matr.append(res)

#print(matr[8][0])
chis=[15,30,105]
k1=[]
zero=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(16):
    x = [int(bit) for bit in bin(i)[2:]]
    x = [0 for i in range(0, 4 - len(x))] + x
    k1.append("".join(str(g) for g in x))

k1=dict(zip(k1,zero))
k2=k1.copy()
k3=k1.copy()

for i in range(150,200):
    x = [int(bit) for bit in bin(i)[2:]]
    x = [0 for i in range(0, 16 - len(x))] + x
    x1=[x[j]^mask[j] for j in range(16)]
    
    y,ex=cp_encrypt(x,key)
    y1,ex1=cp_encrypt(x1,key)
    
    sdC=[y[i-1] for i in perm]
    sdC1=[y1[i-1] for i in perm]

    res_ex=[ex[j]^ex1[j] for j in range(12)]
    res_sdC=[sdC[j]^sdC1[j] for j in range(8)]
    if res_ex==dA and res_sdC==dC:
        print("X=  {} E(X)=  {} S(E(X))=  {} Y=  {}\nX1= {} E(X1)= {} S(E(X1))= {} Y1= {}\n".format(
            "".join(str(g) for g in x),
            "".join(str(g) for g in ex),
            "".join(str(g) for g in sdC),
            "".join(str(g) for g in y),
            "".join(str(g) for g in x1),
            "".join(str(g) for g in ex1),
            "".join(str(g) for g in sdC1),
            "".join(str(g) for g in y1)
            ))
        in1=ex[:4]
        out1=sdC[:3]
        out1_str="".join(str(g) for g in out1)
        print("\nFor 1 S block\nFor pair above:\n {} + K1 give out {}".format(in1,out1))
        for j in range(16):
            if matr[j][0]==out1:
                xx= [int(bit) for bit in bin(j)[2:]]
                xx= [0 for jj in range(0, 4 - len(xx))] + xx
                
                res=[xx[k]^in1[k] for k in range(4)]
                
                res_str="".join(str(g) for g in res)
                print("in table {} and after XOR K1= {}".format(xx,res_str))
                k1[res_str]+=1
        in2=ex1[:4]
        out2=sdC1[:3]
        out2_str="".join(str(g) for g in out2)
        print("For pair above:\n {} + K1 give out {}".format(in2,out2))
        for j in range(16):
            if matr[j][0]==out2:
                xx= [int(bit) for bit in bin(j)[2:]]
                xx= [0 for ji in range(0, 4 - len(xx))] + xx
                res=[xx[k]^in2[k] for k in range(4)]
                
                res_str="".join(str(g) for g in res)
                print("in table {} and after XOR K1= {}".format(xx,res_str))
                k1[res_str]+=1

        in1=ex[4:8]
        out1=sdC[3:6]
        out1_str="".join(str(g) for g in out1)
        print("\nFor 2 S block\nFor pair above:\n {} + K2 give out {}".format(in1,out1))
        for j in range(16):
            if matr[j][1]==out1:
                xx= [int(bit) for bit in bin(j)[2:]]
                xx= [0 for jj in range(0, 4 - len(xx))] + xx
                res=[xx[k]^in1[k] for k in range(4)]
                
                res_str="".join(str(g) for g in res)
                print("in table {} and after XOR K2= {}".format(xx,res_str))
                k2[res_str]+=1
        in2=ex1[4:8]
        out2=sdC1[3:6]
        out2_str="".join(str(g) for g in out2)
        print("For pair above:\n {} + K2 give out {}".format(in2,out2))
        for j in range(16):
            if matr[j][1]==out2:
                xx= [int(bit) for bit in bin(j)[2:]]
                xx= [0 for ji in range(0, 4 - len(xx))] + xx
                res=[xx[k]^in2[k] for k in range(4)]
                
                res_str="".join(str(g) for g in res)
                print("in table {} and after XOR K2= {}".format(xx,res_str))
                k2[res_str]+=1
        
        in1=ex[8:]
        out1=sdC[6:]
        out1_str="".join(str(g) for g in out1)
        print("\nFor 3 S block\nFor pair above:\n {} + K3 give out {}".format(in1,out1))
        for j in range(16):
            if matr[j][2]==out1:
                xx= [int(bit) for bit in bin(j)[2:]]
                xx= [0 for jj in range(0, 4 - len(xx))] + xx
                res=[xx[k]^in1[k] for k in range(4)]
                
                res_str="".join(str(g) for g in res)
                print("in table {} and after XOR K3= {}".format(xx,res_str))
                k3[res_str]+=1
        in2=ex1[8:]
        out2=sdC1[6:]
        out2_str="".join(str(g) for g in out2)
        print("For pair above:\n {} + K3 give out {}".format(in2,out2))
        for j in range(16):
            if matr[j][2]==out2:
                xx= [int(bit) for bit in bin(j)[2:]]
                xx= [0 for ji in range(0, 4 - len(xx))] + xx
                res=[xx[k]^in2[k] for k in range(4)]
                
                res_str="".join(str(g) for g in res)
                print("in table {} and after XOR K3= {}".format(xx,res_str))
                k3[res_str]+=1

print("k1=",k1)
print("k2=",k2)
print("k3=",k3)



