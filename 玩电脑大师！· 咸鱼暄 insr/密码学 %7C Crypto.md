
## 考试内容
没怎么好好学，大概写一下考了什么吧qwq


### 选择题 2*10=20
比如 <br />AES 用多少位的密钥的时候用到了多少位还是什么的<br />还有 SHA-1 的位数<br />欧拉函数 ![](https://cdn.nlark.com/yuque/__latex/f857a781b75e8c85918e36a4589c15e2.svg#card=math&code=%5CPhi%28100%29&id=RM9X1) 的值<br />openssl 里哪个函数实现幂取模运算<br />openssl 里某个函数的某个参数是什么意思<br />三重 DES 是啥样的<br />之类的题


### 简答题 4*5=20
说明 MD5 的填充规则<br />说明 ECC 签名那什么的正确性<br />写 CFB 的一个函数，就像 DES 那次作业一样<br />写 DES 的查 sbox 过程的代码


### 计算题 10+10+20
给 Enigma 的各种细节，算两个输入的输出，写过程（10 分）<br />给表格，算 ECC 的一个过程，写过程（10 分）<br />写农夫算法的程序，并且用农夫算法手算一个，写过程（20 分）


### 证明题 2*10=20
证明 RSA<br />证明中国剩余定理<br />（没有考证明 Euler 准则和证明裴蜀定理）


## DES 算法
Ref：[The DES Algorithm Illustrated](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm)  _by J. Orlin Grabbe_


### Introduction
**DES (Data Encryption Standard)** 是一种 **block cipher**（块密码，或译为分组密码、分块密码等）。所谓 block cipher，就是将明文输入（二进制串）分成若干等长的 block；对于每个长度为 ![](https://g.yuque.com/gr/latex?n#card=math&code=n&id=GKnY1) 的 block ，使用一个长度为 ![](https://g.yuque.com/gr/latex?k#card=math&code=k&id=ATydY) 的密钥 ![](https://g.yuque.com/gr/latex?K#card=math&code=K&id=hxh1z) 加密后，生成长度也为 ![](https://g.yuque.com/gr/latex?n#card=math&code=n&id=UKKHm) 的密文输出 ![](https://g.yuque.com/gr/latex?C#card=math&code=C&id=uxrvr)。即，加密函数 ![](https://g.yuque.com/gr/latex?E_K(P)%3A%3DE(K%2CP)%3A%5C%7B0%2C1%5C%7D%5Ek%5Ctimes%5C%7B0%2C1%5C%7D%5En%5Cto%5C%7B0%2C1%5C%7D%5En#card=math&code=E_K%28P%29%3A%3DE%28K%2CP%29%3A%5C%7B0%2C1%5C%7D%5Ek%5Ctimes%5C%7B0%2C1%5C%7D%5En%5Cto%5C%7B0%2C1%5C%7D%5En&id=VR5Av)，解密函数 ![](https://g.yuque.com/gr/latex?D_K(C)%3A%3DD(K%2CC)%3A%3DE_K%5E%7B-1%7D(C)%3A%5C%7B0%2C1%5C%7D%5Ek%5Ctimes%5C%7B0%2C1%5C%7D%5En%5Cto%5C%7B0%2C1%5C%7D%5En#card=math&code=D_K%28C%29%3A%3DD%28K%2CC%29%3A%3DE_K%5E%7B-1%7D%28C%29%3A%5C%7B0%2C1%5C%7D%5Ek%5Ctimes%5C%7B0%2C1%5C%7D%5En%5Cto%5C%7B0%2C1%5C%7D%5En&id=saZvS) 。也就是说，加密函数 ![](https://g.yuque.com/gr/latex?E_K(P)#card=math&code=E_K%28P%29&id=jz4kv) 和解密函数 ![](https://g.yuque.com/gr/latex?D_K(C)#card=math&code=D_K%28C%29&id=c2tsq) 互为反函数， ![](https://g.yuque.com/gr/latex?E_K(P)%20%3D%20C%2CD_K(C)%3DP#card=math&code=E_K%28P%29%20%3D%20C%2CD_K%28C%29%3DP&id=IV3Nv)。

在 DES 算法中，每个 block 的大小是 64 bits；每个 key _看起来_ 是 64 bits，实际上只有 56 bits 有效，因为 every 8th key bit is ignored。

当明文输入的长度并非 64 bits 的整倍数时，我们需要将其进行补齐 (pad)。补齐的方法有很多，这并不属于 DES 算法关心的问题。


### An Example
我们引入一例，贯穿对 DES 的学习。我们设明文  0123456789ABCDEF，这是一个 16 进制数，其长度恰好为 64 bits，改写为二进制即为  0000 0001 0010 0011 0100 0101 0110 0111 。我们会将明文分为左右两个等长的部分，这里  0000 0001 0010 0011 0100 0101 0110 0111， 1000 1001 1010 1011 1100 1101 1110 1111。

我们设 16 进制数密钥  133457799BBCDFF1，亦即  00010011 00110100 01010111 01111001 10011011 10111100 11011111 11110001。注意，如我们之前所说，every 8th key bit is ignored。

下面是 DES 算法的具体流程：

### Step 1 - 构造 16 个 48-bits 的 subkey

#### 1.1 - 取 64-bits 密钥 ![](https://g.yuque.com/gr/latex?K#card=math&code=K&id=OOTxt) 的一个 56-bits 排列 ![](https://g.yuque.com/gr/latex?K%2B#card=math&code=K%2B&id=r3MNx)
首先，我们要用到一张表，小白老师叫它 `key_perm_table`，原文就叫它 `PC-1`。其值为：
```
            57   49    41   33    25    17    9
             1   58    50   42    34    26   18
            10    2    59   51    43    35   27
            19   11     3   60    52    44   36
            63   55    47   39    31    23   15
             7   62    54   46    38    30   22
            14    6    61   53    45    37   29
            21   13     5   28    20    12    4
```

可以看到，这张表总共有 56 个表项，对应的是 1~64 中除去了 every 8th bit 剩下的 56 个数。我们使用这张表得到密钥 ![](https://g.yuque.com/gr/latex?K#card=math&code=K&id=agQvj) 的一个新的排列 ![](https://g.yuque.com/gr/latex?K%2B#card=math&code=K%2B&id=swu9h)，其中 `K+[i] = K[key_perm_table[i]-1]`, ![](https://g.yuque.com/gr/latex?i%20%3D%200%2C%201%2C%20%5Cdots%2C%2055#card=math&code=i%20%3D%200%2C%201%2C%20%5Cdots%2C%2055&id=BkOBn)（这里 -1 也是因为下标从 0 开始）。例如这里 `key_perm_table[0] = 57`，则 ![](https://g.yuque.com/gr/latex?K%2B#card=math&code=K%2B&id=M4Gly) 的第 1 位（下标为 0）即为 `K[57-1] = 1`。

以此法，我们得到 ![](https://g.yuque.com/gr/latex?K%2B%3D#card=math&code=K%2B%3D&id=VfOdJ) 1111000 0110011 0010101 0101111 0101010 1011001 1001111 0001111。


#### 1.2 - 对 ![](https://g.yuque.com/gr/latex?K%2B#card=math&code=K%2B&id=bvQu6) 的左右部分进行 16 次循环左移
我们将 ![](https://g.yuque.com/gr/latex?K%2B#card=math&code=K%2B&id=Lvdv9) 均分为左右两个部分，这里 ![](https://g.yuque.com/gr/latex?C_0%20%3D#card=math&code=C_0%20%3D&id=l1WAJ) 1111000 0110011 0010101 0101111，![](https://g.yuque.com/gr/latex?D_0%20%3D#card=math&code=D_0%20%3D&id=IBl7c) 0101010 1011001 1001111 0001111。然后我们通过循环左移得到 ![](https://g.yuque.com/gr/latex?C_i%2C%20D_i%2C%20i%20%3D%201%2C%202%2C%20%5Cdots%2C%2016#card=math&code=C_i%2C%20D_i%2C%20i%20%3D%201%2C%202%2C%20%5Cdots%2C%2016&id=Khubp)，其中 ![](https://g.yuque.com/gr/latex?C_i%2C%20D_i#card=math&code=C_i%2C%20D_i&id=Ari2a) 分别是 ![](https://g.yuque.com/gr/latex?C_%7Bi-1%7D%2C%20D_%7Bi-1%7D#card=math&code=C_%7Bi-1%7D%2C%20D_%7Bi-1%7D&id=pg70z) 循环左移  位的结果，其中：
```
i		1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16
s_i		1	1	2	2	2	2	2	2	1	2	2	2	2	2	2	1
```

由此我们得到：<br /> = 1111000011001100101010101111<br />![](https://g.yuque.com/gr/latex?D_0#card=math&code=D_0&id=cQ5sO) = 0101010101100110011110001111<br />（例如，![](https://g.yuque.com/gr/latex?C_1%2C%20D_1#card=math&code=C_1%2C%20D_1&id=XCbLt) 分别由 ![](https://g.yuque.com/gr/latex?C_0%2C%20D_0#card=math&code=C_0%2C%20D_0&id=GMxrK) 循环左移 ![](https://g.yuque.com/gr/latex?s_1%20%3D%201#card=math&code=s_1%20%3D%201&id=zjK0Q) bit 得到）<br /> = 1110000110011001010101011111<br /> = 1010101011001100111100011110<br /> = 1100001100110010101010111111<br /> = 0101010110011001111000111101<br />（再如，![](https://g.yuque.com/gr/latex?C_3%2C%20D_3#card=math&code=C_3%2C%20D_3&id=F1krg) 分别由 ![](https://g.yuque.com/gr/latex?C_2%2C%20D_2#card=math&code=C_2%2C%20D_2&id=aiIKX) 循环左移 ![](https://g.yuque.com/gr/latex?s_3%20%3D%202#card=math&code=s_3%20%3D%202&id=rBAoJ) bits 得到）<br /> = 0000110011001010101011111111<br /> = 0101011001100111100011110101<br /> = 0011001100101010101111111100<br /> = 0101100110011110001111010101<br /> = 1100110010101010111111110000<br />![](https://g.yuque.com/gr/latex?D_5#card=math&code=D_5&id=kYa4C) = 0110011001111000111101010101<br />![](https://g.yuque.com/gr/latex?C_6#card=math&code=C_6&id=VpzyL) = 0011001010101011111111000011<br />![](https://g.yuque.com/gr/latex?D_6#card=math&code=D_6&id=SGLEi) = 1001100111100011110101010101<br />![](https://g.yuque.com/gr/latex?C_7#card=math&code=C_7&id=cI4jK) = 1100101010101111111100001100<br />![](https://g.yuque.com/gr/latex?D_7#card=math&code=D_7&id=K6bMc) = 0110011110001111010101010110<br />![](https://g.yuque.com/gr/latex?C_8#card=math&code=C_8&id=ekKdh) = 0010101010111111110000110011<br />![](https://g.yuque.com/gr/latex?D_8#card=math&code=D_8&id=tOny7) = 1001111000111101010101011001<br />![](https://g.yuque.com/gr/latex?C_9#card=math&code=C_9&id=NCyMb) = 0101010101111111100001100110<br />![](https://g.yuque.com/gr/latex?D_9#card=math&code=D_9&id=f7TXq) = 0011110001111010101010110011<br />![](https://g.yuque.com/gr/latex?C_%7B10%7D#card=math&code=C_%7B10%7D&id=QIJ2e) = 0101010111111110000110011001<br />![](https://g.yuque.com/gr/latex?D_%7B10%7D#card=math&code=D_%7B10%7D&id=kpIDz) = 1111000111101010101011001100<br /> = 0101011111111000011001100101<br />![](https://g.yuque.com/gr/latex?D_%7B11%7D#card=math&code=D_%7B11%7D&id=bPg64) = 1100011110101010101100110011<br /> = 0101111111100001100110010101<br />![](https://g.yuque.com/gr/latex?D_%7B12%7D#card=math&code=D_%7B12%7D&id=d64KV) = 0001111010101010110011001111<br />![](https://g.yuque.com/gr/latex?C_%7B13%7D#card=math&code=C_%7B13%7D&id=NEK4R) = 0111111110000110011001010101<br />![](https://g.yuque.com/gr/latex?D_%7B13%7D#card=math&code=D_%7B13%7D&id=uABUQ) = 0111101010101011001100111100<br />![](https://g.yuque.com/gr/latex?C_%7B14%7D#card=math&code=C_%7B14%7D&id=o95eA) = 1111111000011001100101010101<br />![](https://g.yuque.com/gr/latex?D_%7B14%7D#card=math&code=D_%7B14%7D&id=qCUQm) = 1110101010101100110011110001<br />![](https://g.yuque.com/gr/latex?C_%7B15%7D#card=math&code=C_%7B15%7D&id=c48sQ) = 1111100001100110010101010111<br />![](https://g.yuque.com/gr/latex?D_%7B15%7D#card=math&code=D_%7B15%7D&id=Z3vTf) = 1010101010110011001111000111<br />![](https://g.yuque.com/gr/latex?C_%7B16%7D#card=math&code=C_%7B16%7D&id=MQ9L0) = 1111000011001100101010101111<br />![](https://g.yuque.com/gr/latex?D_%7B16%7D#card=math&code=D_%7B16%7D&id=VkuID) = 0101010101100110011110001111


#### 1.3 - 从 16 次循环左移的结果选择出 subkey
然后，我们需要用到另一张表 `PC-2`，小白老师叫它 `key_56bit_to_48bit_table`：
```
                 14    17   11    24     1    5
                  3    28   15     6    21   10
                 23    19   12     4    26    8
                 16     7   27    20    13    2
                 41    52   31    37    47   55
                 30    40   51    45    33   48
                 44    49   39    56    34   53
                 46    42   50    36    29   32
```
这是一个 48 项的表，其中数字的范围为 1~56。我们利用与 PC-1 类似的查表方式 ，将 ![](https://g.yuque.com/gr/latex?C_iD_i#card=math&code=C_iD_i&id=OZqcD)（即这两个 28 bits 的数首尾相接）转换为我们的 subkey ：<br />![](https://g.yuque.com/gr/latex?K_%7B1%7D#card=math&code=K_%7B1%7D&id=yL0uV) = 000110 110000 001011 101111 111111 000111 000001 110010<br />![](https://g.yuque.com/gr/latex?K_%7B2%7D#card=math&code=K_%7B2%7D&id=oAulc) = 011110 011010 111011 011001 110110 111100 100111 100101<br />![](https://g.yuque.com/gr/latex?K_%7B3%7D#card=math&code=K_%7B3%7D&id=BrL4F) = 010101 011111 110010 001010 010000 101100 111110 011001<br />![](https://g.yuque.com/gr/latex?K_%7B4%7D#card=math&code=K_%7B4%7D&id=LpsNt) = 011100 101010 110111 010110 110110 110011 010100 011101<br />![](https://g.yuque.com/gr/latex?K_%7B5%7D#card=math&code=K_%7B5%7D&id=gtiRq) = 011111 001110 110000 000111 111010 110101 001110 101000<br />![](https://g.yuque.com/gr/latex?K_%7B6%7D#card=math&code=K_%7B6%7D&id=UTO0j) = 011000 111010 010100 111110 010100 000111 101100 101111<br />![](https://g.yuque.com/gr/latex?K_%7B7%7D#card=math&code=K_%7B7%7D&id=kixj9) = 111011 001000 010010 110111 111101 100001 100010 111100<br />![](https://g.yuque.com/gr/latex?K_%7B8%7D#card=math&code=K_%7B8%7D&id=WV1G1) = 111101 111000 101000 111010 110000 010011 101111 111011<br />![](https://g.yuque.com/gr/latex?K_%7B9%7D#card=math&code=K_%7B9%7D&id=YcOTr) = 111000 001101 101111 101011 111011 011110 011110 000001<br />![](https://g.yuque.com/gr/latex?K_%7B10%7D#card=math&code=K_%7B10%7D&id=cofEU) = 101100 011111 001101 000111 101110 100100 011001 001111<br />![](https://g.yuque.com/gr/latex?K_%7B11%7D#card=math&code=K_%7B11%7D&id=VmgK3) = 001000 010101 111111 010011 110111 101101 001110 000110<br />![](https://g.yuque.com/gr/latex?K_%7B12%7D#card=math&code=K_%7B12%7D&id=fmOcZ) = 011101 010111 000111 110101 100101 000110 011111 101001<br />![](https://g.yuque.com/gr/latex?K_%7B13%7D#card=math&code=K_%7B13%7D&id=FHOlT) = 100101 111100 010111 010001 111110 101011 101001 000001<br />![](https://g.yuque.com/gr/latex?K_%7B14%7D#card=math&code=K_%7B14%7D&id=EWPAA) = 010111 110100 001110 110111 111100 101110 011100 111010<br />![](https://g.yuque.com/gr/latex?K_%7B15%7D#card=math&code=K_%7B15%7D&id=nVaGS) = 101111 111001 000110 001101 001111 010011 111100 001010<br />![](https://g.yuque.com/gr/latex?K_%7B16%7D#card=math&code=K_%7B16%7D&id=ArTR7) = 110010 110011 110110 001011 000011 100001 011111 110101


### Step 2 - 将明文加密

#### 2.1 - 重排明文
我们首先用到一张表 `ip` (initial permutation) 重排明文 ![](https://g.yuque.com/gr/latex?M#card=math&code=M&id=uXyrW)：
```
            58    50   42    34    26   18    10    2
            60    52   44    36    28   20    12    4
            62    54   46    38    30   22    14    6
            64    56   48    40    32   24    16    8
            57    49   41    33    25   17     9    1
            59    51   43    35    27   19    11    3
            61    53   45    37    29   21    13    5
            63    55   47    39    31   23    15    7
```
查表的方式与 1.1 类似。

我们的例子中， 0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111，因此重排后得到 ![](https://g.yuque.com/gr/latex?IP%20%3D#card=math&code=IP%20%3D&id=vvNOn) 1100 1100 0000 0000 1100 1100 1111 1111 1111 0000 1010 1010 1111 0000 1010 1010。

我们再将  分为左右两部分，这里 ![](https://g.yuque.com/gr/latex?L_0%20%3D#card=math&code=L_0%20%3D&id=laVdN) 1100 1100 0000 0000 1100 1100 1111 1111，![](https://g.yuque.com/gr/latex?R_0%20%3D#card=math&code=R_0%20%3D&id=F2Xtv) 1111 0000 1010 1010 1111 0000 1010 1010。我们用这些参与后面的运算。


#### 2.2 - 定义一个函数 
我们定义一个函数 ![](https://g.yuque.com/gr/latex?f(R_i%2C%20K_%7Bi%2B1%7D)%3A%5C%7B0%2C1%5C%7D%5E%7B32%7D%5Ctimes%5C%7B0%2C1%5C%7D%5E%7B48%7D%5Cto%5C%7B0%2C1%5C%7D%5E%7B32%7D#card=math&code=f%28R_i%2C%20K_%7Bi%2B1%7D%29%3A%5C%7B0%2C1%5C%7D%5E%7B32%7D%5Ctimes%5C%7B0%2C1%5C%7D%5E%7B48%7D%5Cto%5C%7B0%2C1%5C%7D%5E%7B32%7D&id=rW0sS)，这个函数根据 32 位的 （我们在 2.1 中得到了 ，我们将在后面学习  等是从哪里来的）和一个 subkey ![](https://g.yuque.com/gr/latex?K_%7Bi%2B1%7D#card=math&code=K_%7Bi%2B1%7D&id=PyKSv) 计算出一个 32 位的结果 。


##### 2.2.1 - 扩展 
我们首先利用一个表 `E BIT-SELECTION TABLE` （小白老师称作 `plaintext_32bit_expanded_to_48bit_table`）将 32-bits 的  扩展到 48-bits 的 ![](https://g.yuque.com/gr/latex?E(R_i)#card=math&code=E%28R_i%29&id=axPTx)：
```
                 32     1    2     3     4    5
                  4     5    6     7     8    9
                  8     9   10    11    12   13
                 12    13   14    15    16   17
                 16    17   18    19    20   21
                 20    21   22    23    24   25
                 24    25   26    27    28   29
                 28    29   30    31    32    1
```
查表的方式与 1.1 类似。这是一个有 48 个表项的表，其中内容为 1~32，有重复。以此得到 ![](https://g.yuque.com/gr/latex?E(R_i)#card=math&code=E%28R_i%29&id=zLWb5)。

我们将 ![](https://g.yuque.com/gr/latex?K_%7Bi%2B1%7D#card=math&code=K_%7Bi%2B1%7D&id=nQlQQ) 和 ![](https://g.yuque.com/gr/latex?E(R_i)#card=math&code=E%28R_i%29&id=Azaac) 做按位异或，就得到了一个 48-bits 的结果，我们将这个结果分为 8 组，每组 6 bits，即 ![](https://g.yuque.com/gr/latex?K_%7Bi%2B1%7D%20%5Coplus%20E(R_i)%3DB_1B_2B_3B_4B_5B_6B_7B_8#card=math&code=K_%7Bi%2B1%7D%20%5Coplus%20E%28R_i%29%3DB_1B_2B_3B_4B_5B_6B_7B_8&id=gkDTy)。

我们的例子中，![](https://g.yuque.com/gr/latex?R_0%20%3D#card=math&code=R_0%20%3D&id=fhp4v) 1111 0000 1010 1010 1111 0000 1010 1010，计算出 ![](https://g.yuque.com/gr/latex?E(R_0)%20%3D#card=math&code=E%28R_0%29%20%3D&id=TimdC) 011110 100001 010101 010101 011110 100001 010101 010101，与 ![](https://g.yuque.com/gr/latex?K_1%20%3D#card=math&code=K_1%20%3D&id=DmuiH) 000110 110000 001011 101111 111111 000111 000001 110010 进行按位异或，得到 ![](https://g.yuque.com/gr/latex?K_%7B1%7D%20%5Coplus%20E(0)%20%3D#card=math&code=K_%7B1%7D%20%5Coplus%20E%280%29%20%3D&id=QgzFk) 011000 010001 011110 111010 100001 100110 010100 100111。


##### 2.2.2 - 对结果的每个分组查表
接下来，我们计算 ![](https://g.yuque.com/gr/latex?S_1(B_1)S_2(B_2)S_3(B_3)S_4(B_4)S_5(B_5)S_6(B_6)S_7(B_7)S_8(B_8)#card=math&code=S_1%28B_1%29S_2%28B_2%29S_3%28B_3%29S_4%28B_4%29S_5%28B_5%29S_6%28B_6%29S_7%28B_7%29S_8%28B_8%29&id=Q6Wgq)。其中，![](https://g.yuque.com/gr/latex?S_i(B_i)#card=math&code=S_i%28B_i%29&id=g03g9) 是根据下面第 ![](https://g.yuque.com/gr/latex?i#card=math&code=i&id=iYblw) 张表 ![](https://g.yuque.com/gr/latex?S_i#card=math&code=S_i&id=pv2sh) 查询  的结果；每个 ![](https://g.yuque.com/gr/latex?S_i#card=math&code=S_i&id=axTWJ) 都是一个 4 行 8 列的表（如下所示，这个 8 个表在小白那里叫 `sbox[i]`）， 是 2.2.1 节得到的 6-bits 二进制数。

查表方式是：

- 将  的首位和末位组成的 00~11 的值作为 ![](https://g.yuque.com/gr/latex?S_i#card=math&code=S_i&id=ilQ61) 中的行号
-  的中间 4 位组成的 0000~1111 的值作为 ![](https://g.yuque.com/gr/latex?S_i#card=math&code=S_i&id=W7aYF) 中的列号
- 定位出一个值。将这个 0~15 的值转为 0000~1111 的二进制，即为 ![](https://g.yuque.com/gr/latex?S_i(B_i)#card=math&code=S_i%28B_i%29&id=i5INA) 的值。

例如，我们在 2.2.1 中算出 ![](https://g.yuque.com/gr/latex?B_1%20%3D#card=math&code=B_1%20%3D&id=Yiywv)  011000，那么行号即为 00 = 0，列号为 1100 = 12，在  中查得对应数字为 5，因此 ![](https://g.yuque.com/gr/latex?S_1(B_1)%20%3D#card=math&code=S_1%28B_1%29%20%3D&id=a8552) 0101。

以此类推，计算出 ![](https://g.yuque.com/gr/latex?S_1(B_1)S_2(B_2)S_3(B_3)S_4(B_4)S_5(B_5)S_6(B_6)S_7(B_7)S_8(B_8)#card=math&code=S_1%28B_1%29S_2%28B_2%29S_3%28B_3%29S_4%28B_4%29S_5%28B_5%29S_6%28B_6%29S_7%28B_7%29S_8%28B_8%29&id=LX3mC) = 0101 1100 1000 0010 1011 0101 1001 0111。这是一个 32-bits 的结果。
```
                                  S1
 
     14  4  13  1   2 15  11  8   3 10   6 12   5  9   0  7
      0 15   7  4  14  2  13  1  10  6  12 11   9  5   3  8
      4  1  14  8  13  6   2 11  15 12   9  7   3 10   5  0
     15 12   8  2   4  9   1  7   5 11   3 14  10  0   6 13
                                  
                                  S2
 
     15  1   8 14   6 11   3  4   9  7   2 13  12  0   5 10
      3 13   4  7  15  2   8 14  12  0   1 10   6  9  11  5
      0 14   7 11  10  4  13  1   5  8  12  6   9  3   2 15
     13  8  10  1   3 15   4  2  11  6   7 12   0  5  14  9
                                  
                                  S3
 
     10  0   9 14   6  3  15  5   1 13  12  7  11  4   2  8
     13  7   0  9   3  4   6 10   2  8   5 14  12 11  15  1
     13  6   4  9   8 15   3  0  11  1   2 12   5 10  14  7
      1 10  13  0   6  9   8  7   4 15  14  3  11  5   2 12
                                  
                                  S4
 
      7 13  14  3   0  6   9 10   1  2   8  5  11 12   4 15
     13  8  11  5   6 15   0  3   4  7   2 12   1 10  14  9
     10  6   9  0  12 11   7 13  15  1   3 14   5  2   8  4
      3 15   0  6  10  1  13  8   9  4   5 11  12  7   2 14
                                 
                                 S5
 
      2 12   4  1   7 10  11  6   8  5   3 15  13  0  14  9
     14 11   2 12   4  7  13  1   5  0  15 10   3  9   8  6
      4  2   1 11  10 13   7  8  15  9  12  5   6  3   0 14
     11  8  12  7   1 14   2 13   6 15   0  9  10  4   5  3
                                 
                                 S6
 
     12  1  10 15   9  2   6  8   0 13   3  4  14  7   5 11
     10 15   4  2   7 12   9  5   6  1  13 14   0 11   3  8
      9 14  15  5   2  8  12  3   7  0   4 10   1 13  11  6
      4  3   2 12   9  5  15 10  11 14   1  7   6  0   8 13
                                 
                                 S7
 
      4 11   2 14  15  0   8 13   3 12   9  7   5 10   6  1
     13  0  11  7   4  9   1 10  14  3   5 12   2 15   8  6
      1  4  11 13  12  3   7 14  10 15   6  8   0  5   9  2
      6 11  13  8   1  4  10  7   9  5   0 15  14  2   3 12
                                 
                                 S8
 
     13  2   8  4   6 15  11  1  10  9   3 14   5  0  12  7
      1 15  13  8  10  3   7  4  12  5   6 11   0 14   9  2
      7 11   4  1   9 12  14  2   0  6  10 13  15  3   5  8
      2  1  14  7   4 10   8 13  15 12   9  0   3  5   6 11
```


##### 2.2.3 - 再查一次表，得到  的结果
我们对 ![](https://g.yuque.com/gr/latex?S_1(B_1)S_2(B_2)S_3(B_3)S_4(B_4)S_5(B_5)S_6(B_6)S_7(B_7)S_8(B_8)#card=math&code=S_1%28B_1%29S_2%28B_2%29S_3%28B_3%29S_4%28B_4%29S_5%28B_5%29S_6%28B_6%29S_7%28B_7%29S_8%28B_8%29&id=hr2nN) 的结果 ![](https://g.yuque.com/gr/latex?X#card=math&code=X&id=jE5L4) 再查一次表，这个表在小白那里叫 `sbox_perm_table`：
```
                         16   7  20  21
                         29  12  28  17
                          1  15  23  26
                          5  18  31  10
                          2   8  24  14
                         32  27   3   9
                         19  13  30   6
                         22  11   4  25
```
仍然是个线性的表，查表的方式与 1.1 类似。即，![](https://g.yuque.com/gr/latex?f(R_i%2C%20K_%7Bi%2B1%7D)#card=math&code=f%28R_i%2C%20K_%7Bi%2B1%7D%29&id=YQ9Ex) 的第 `i` 位即为 ![](https://g.yuque.com/gr/latex?X#card=math&code=X&id=KRXkC) 的第 `sbox_perm_table[i]` 位。

在我们的例子中，![](https://g.yuque.com/gr/latex?S_1(B_1)S_2(B_2)S_3(B_3)S_4(B_4)S_5(B_5)S_6(B_6)S_7(B_7)S_8(B_8)%20%3D#card=math&code=S_1%28B_1%29S_2%28B_2%29S_3%28B_3%29S_4%28B_4%29S_5%28B_5%29S_6%28B_6%29S_7%28B_7%29S_8%28B_8%29%20%3D&id=QmvTF) 0101 1100 1000 0010 1011 0101 1001 0111，因此 ![](https://g.yuque.com/gr/latex?f(R_i%2C%20K_%7Bi%2B1%7D)%20%3D#card=math&code=f%28R_i%2C%20K_%7Bi%2B1%7D%29%20%3D&id=kcKhh) 0010 0011 0100 1010 1010 1001 1011 1011。


#### 2.3 - 利用函数  ，做 16 次迭代
在 2.1 中，我们得到了  和 。在此基础上，我们对 ![](https://g.yuque.com/gr/latex?i%20%3D%201%2C%202%2C%20%5Cdots%2C%2016#card=math&code=i%20%3D%201%2C%202%2C%20%5Cdots%2C%2016&id=noPKh)，做如下计算：<br />![](https://g.yuque.com/gr/latex?%5Cbegin%7Barray%7D%5C%5C%0AL_i%20%3D%20R_%7Bi-1%7D%5C%5C%0AR_i%20%3D%20L_%7Bi-1%7D%20%5Coplus%20f(R_%7Bi-1%7D%2C%20K_i)%0A%5Cend%7Barray%7D%0A#card=math&code=%5Cbegin%7Barray%7D%5C%5C%0AL_i%20%3D%20R_%7Bi-1%7D%5C%5C%0AR_i%20%3D%20L_%7Bi-1%7D%20%5Coplus%20f%28R_%7Bi-1%7D%2C%20K_i%29%0A%5Cend%7Barray%7D%0A&id=O4DFQ)
在我们的例子中，我们最终计算得到 ![](https://g.yuque.com/gr/latex?L_%7B16%7D%20%3D#card=math&code=L_%7B16%7D%20%3D&id=JPYTP) 0100 0011 0100 0010 0011 0010 0011 0100，![](https://g.yuque.com/gr/latex?R_%7B16%7D%20%3D#card=math&code=R_%7B16%7D%20%3D&id=mJyxv) 0000 1010 0100 1100 1101 1001 1001 0101。


#### 2.4 - 组合 ![](https://g.yuque.com/gr/latex?R_%7B16%7DL_%7B16%7D#card=math&code=R_%7B16%7DL_%7B16%7D&id=YyvZ5)，再重排一次
注意，这里将 ![](https://g.yuque.com/gr/latex?R_%7B16%7D#card=math&code=R_%7B16%7D&id=noAcA) 放在了左边。求得 ![](https://g.yuque.com/gr/latex?R_%7B16%7DL_%7B16%7D#card=math&code=R_%7B16%7DL_%7B16%7D&id=A2Iyz) 后，查最后一次表！这个表在原文叫 IP-1，在小白那里叫 `fp`：
```
            40     8   48    16    56   24    64   32
            39     7   47    15    55   23    63   31
            38     6   46    14    54   22    62   30
            37     5   45    13    53   21    61   29
            36     4   44    12    52   20    60   28
            35     3   43    11    51   19    59   27
            34     2   42    10    50   18    58   26
            33     1   41     9    49   17    57   25
```
我们的例子中，![](https://g.yuque.com/gr/latex?R_%7B16%7DL_%7B16%7D#card=math&code=R_%7B16%7DL_%7B16%7D&id=GD9uO) = 00001010 01001100 11011001 10010101 01000011 01000010 00110010 00110100，因此最终得到的密文 ![](https://g.yuque.com/gr/latex?C#card=math&code=C&id=ZQE8V) = 10000101 11101000 00010011 01010100 00001111 00001010 10110100 00000101 = 85E813540F0AB405。


### Homework 2

#### T1 重写 DES 算法中的核心函数 f
函数的步骤已经在 2.2 小节中详细介绍了。下面是程序的详细注释，代码已经被删除。
```c
/* The leading 2 bits of each item in array "subkey" (8 bits)
 * are unused and are 0s. When calling this function, program
 * uses the array "kn" which is initialized in function
 * "des_set_key".
 *
 * [!] In this function, the most significant bit is considered
 * the first (0-th) bit.
 */
static long32 f(ulong32 r, unsigned char subkey[8])
{
	/* Step 1: seperate "r" into 4-char array "s" like:
	 *				+--+--+--+--+
	 *	ulong32 r	|s0|s1|s2|s3|
	 *				+--+--+--+--+
	 *				 ^  ^  ^  ^
	 *				 0  8  16 24
	 * Thus the j-th bit in s[i] is the i*8+j-th bit in "r".
	 */
    
	
	/* Step 2: expand r to 48 bits in array "plaintext".
	 * The storage schema is the same to "subkey".
	 */
	
	
	/* Step 3: plaintext[i] XOR subkey[i] for each i = 0, 1, ..., 7 */
	
	
	/* Step 4: calculate the output of each sbox and store in m[] like:
	 *	+-------------+-------------+---+
	 *	|    m [0]    |    m [1]    |...|
	 *	+-------------+-------------+---+
	 *	|S0(B0) S1(B1)|S2(B2) S3(B3)|...|
	 *	+-------------+-------------+---+
	 */
	
    
	/* Step 5: Do a permutation. */
	
    
	/* Step 6: Store t to rval and return. 
	 * The storage is the same to Step 1.
	 */
	
}
```


#### T2 改写 perm_init() 函数及 permute() 函数
这个问题主要考察对源代码中 2.1 和 2.4 步骤的实现，即根据 `ip` 和 `fp` 进行重排的方式。我们首先学习这个方式。<br />这里采用的方式不是直接查表，而是生成一个反向的表：即不是在生成重排结果的时候一位一位回去找，而是根据原来的值直接生成重排后的值。这样的好处是在输入内容比较多的时候查得会比较快。

回顾我们的 2.1 和 2.4 步骤，实际上都是根据一张表把一个 64-bit 的块重新排列一下。那么，这里的核心思想是：如果我们把这个 64-bit 的块分成 16 份，每份 4 个 bits，那么这 4 bits 的值一定与重排后某 4 个 bits 的值对应；因此，我们讨论这 4 个 bits 所有可能的取值 (0~15) 分别会使得重排后的 64 bits 中哪些 bits 为 1。进行重排时，我们按照 16 份 4-bits 依次查出每一份使得哪些 bits 为 1，将这些结果做 按位或 即得到结果。但是显然，这 4 bits 在块中的位置也会影响到它们对应的到底是哪 4 个 bits，我们将 64-bits 输入块按 4 bits 分组后，总共会有 64/4=16 个可能的位置。因此，我们讨论的实际上是，每个 4-bits 处在第 i 个位置上时，它的所有取值会使得哪些 bits 为 1。<br />即，我们得到一个函数 ：给出一个 4-bits 的值，以及它所在的位置（0~15，用 4 位二进制数表示），得到一个 64 bits 的结果，其中 1 的个数与给定的 4-bits 值的相等，这是因为它们实际上是对应的。使用时，我们计算  即得到重排后的结果。其中 ![](https://cdn.nlark.com/yuque/__latex/b99834bc19bbad24580b3adfa04fb947.svg#card=math&code=%7C&id=i3mQC) 表示位运算“或”，![](https://cdn.nlark.com/yuque/__latex/fed9fd1b2379c8128332ad074902d16b.svg#card=math&code=n%28i%29&id=Uu90b) 表示输入的 64-bits 块中的第  个 nibble（半字节，即 4-bit）。

原来 `perm_init` 的代码（备注已经删掉了，这些备注非常没用）：
```c
static void perm_init(char perm[16][16][8], char p[64])
{
   register int b, j, k;
   int i, m;

   memset(perm, 0, 16*16*8);
   for (i = 0; i < 16; i++) 
      for (j = 0; j < 16; j++) 
         for (k = 0; k < 64; k++) 
         {  
            b = p[k] - 1; 
            if ((b >> 2) != i) 
               continue;  
            if (!(j & nibblebit[b & 3]))
               continue;  
            
            m = k & 7;                                               
            perm[i][j][k>>3] |= bytebit[m]; 
         }
}
```
这个代码就很容易理解了。这个函数的输入 `char perm[16][16][8]` 其实就是我们要生成的那个反查表，其中第一个 16 表示 16 种位置，第二个 16 表示 16 种取值；第三个维度大小为 8，是因为每个 char 有 8 个字节，要保存 64-bits 的结果需要 8 个 char。另一个输入 `char p[64]` 就是 `ip` 和 `fp` 中的一个，这个函数会在这两个地方各被调用一次。<br />第 6 行清空。第 7 行 `i` 循环的是 16 个位置，第 8 行 `j` 循环的是 16 种取值，第 9 行 `k` 则是检查第 `k` 个 bit 会不会在 `i, j` 的情况下取值为 1：如果要取值为 1，那么首先它对应的位（第 11 行）必须在 `i` 的范围内（第 12 行），其次它对应的位必须为 1（第 14 行）。如果这两个条件都满足，那么 `perm[i][j]` 的第 `k` 位应该被置 1，亦即 `perm[i][j][k/8] |= 1 << (k % 8)`（第 17~18 行）。 

这个问题要我们做的是改为 `perm[8][256][8]`。也就是说，我们现在将它改成形如  的函数。即，我们将块分为 8-bits 的小份，这样每份的位置就只有 8 种， 但可能的取值有 256 种。总体思路与原来的函数大同小异。那看懂了这些的话好像也没啥区别）


#### T3 写一个函数 des_cfb_encrypt() 调用 DES 算法以 CFB 模式对明文进行加密
```c
void des_cfb_encrypt(
	unsigned char p[], int n, 		// 明文 p, n=strlen(p)
	unsigned char des_seed_iv[], 	// 初始向量的 seed
	unsigned char des_iv[], 		// 初始向量
	unsigned char des_seed_key[]) 	// des_key 的 seed
									// 上述三个东西都是 8 bytes
{
	/* Step 1: 根据 des_seed_iv 和 des_iv 算出 rc4 key k */
    /* Step 2: 根据 k 和 des_seed_key 算出 des_key */
	// des_iv = des_seed_iv ^ k，因此
	// k = des_iv ^ des_seed_iv
	// des_key = k ^ des_seed_key
    
	/* Step 3: 加密 */
}
```
