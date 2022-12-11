**Assessment:**<br />Labs        30%<br />Project        15%<br />Quiz        25%<br />Final        30%

![image.png](./assets/1603956870364-db787ea4-bbac-498d-acf4-2657597fbfa4.png)

# 1 数字系统与信息 | Digital Systems and Information
在计算机系统概论相关章节 [Bits, Data Types and Operations | ICS](https://www.yuque.com/xianyuxuan/coding/ez9cdg#jiVzt) 中学习过的内容在此部分省略。

**Information Representation.**<br />**Number Systems [binary, octal and hexadecimal].**<br />**Arithmetic Operations.**<br />**Base Conversion.**

**Binary-Coded Decimal.** BCD 码。计算时满十进一，即到达 1010 以上时减去 1010 并进 1。
![image.png](./assets/1603956820595-938b3e7d-fb6f-451c-8ca4-c4afbf07cfb8.png)

**Unicode.** UTF-8 is a variable-length encoding. 
![image.png](./assets/1606058118393-f7e9d41c-5430-49c2-8145-b3b651a6d7d2.png)

**Parity Bit.** A parity bit is the extra bit included to make the total number of 1s in the resulting code word either even or odd. <br />奇校验（Odd Parity）：加上校验位后，1 的个数为奇数个；偶校验（Even Parity）类似。
![image.png](./assets/1606058272495-d13d651b-8c4d-4708-9677-f77d5bf24ef8.png)

**Gray Code.** 格雷码在每次计数（二进制值向下一个二进制值变化）时，需要翻转的位数始终恰为 1。<br />Let Binary code be ![](https://cdn.nlark.com/yuque/__latex/5a8d220733b1569d2e3c6d9a2295be98.svg#card=math&code=b_3b_2b_1b_0&height=18&id=jhlnk) . Then the Gray code can be obtained as follows:<br />![](https://cdn.nlark.com/yuque/__latex/69f6896d730fee89a0713dbd63991ff0.svg#card=math&code=g_3%20%3D%20b_3%2C%5Cquad%20g_i%20%3D%20b_%7Bi%2B1%7D%20%5Coplus%20b_i%5C%20%28i%20%3D%200%2C%201%2C%202%29%20&height=20&id=BTMJ2)
![image.png](./assets/1606058775721-a000baa1-8c19-4f33-84ff-c138fa91c194.png)


# 2 组合逻辑电路 | Combinational Logic Circuits
在计算机系统概论相关章节 [Digital Logic Structures | ICS](https://www.yuque.com/xianyuxuan/coding/ez9cdg#NxCuV) 中以及信息安全原理与数学基础相关章节 [数理逻辑 | 信安数学基础](https://www.yuque.com/xianyuxuan/coding/sfs9gg) 学习过的内容在此部分省略。

## 2.1 二值逻辑与逻辑门 | Binary Logic and Gates

**Gate Circuits and Boolean Equations.**
![image.png](./assets/1606062344314-dc84881d-59a0-4422-ad08-a7df04261841.png)
**Gate Delay.** Each gate has a very important property called gate delay, the length of time it takes for an input change to result in the corresponding output change. Depending on the technology used to implement the gate, the length of time may depend on which of the inputs are changing. <br />Denoted by ![](https://cdn.nlark.com/yuque/__latex/a89a26316951efdf3666f1f74d92b594.svg#card=math&code=t_&height=16&id=iuDR8):
![image.png](./assets/1606062531775-fa03a457-6159-490e-a402-cd6940fd99fe.png)
**Universial Gate.** A gate type that alone can be used to implement all possible Boolean functions is called a universal gate and is said to be "functionally complete." The NAND gate is a universial gate.（参见 [Peirce 记号 | 信安数学](https://www.yuque.com/xianyuxuan/coding/sfs9gg#V7Jk5)）


## 2.2 布尔代数 | Boolean Algebra

**Boolean Algebra.** 处理二进制变量和逻辑运算的代数方法。

**Literal.** 我们称布尔函数项中的每一个变量或变量的补数为 **文字（literal）**。

**布尔代数的基本性质：** 
![image.png](./assets/1606701302362-31ec53f3-94cd-4711-a2f9-f7efed2eaef5.png)
优先级：括号 > NOT > AND > OR。

**Dual.** 一个布尔表达式的 **对偶（dual）**可以通过 1) 交换 AND 和 OR 运算；2) 交换常量 0 和 1 来得到。注意：对偶并不对变量作取反。例如，上表中右边一列均为左边一列的对偶式。<br />另请注意：对偶不改变运算顺序。例如 ![](https://cdn.nlark.com/yuque/__latex/3aebe1d7ead919fbbb5c46519fea4c5f.svg#card=math&code=AB%2BAC%2BBC&height=16&id=dBjVL)的对偶式为 ![](https://cdn.nlark.com/yuque/__latex/1075727422f748f9518dd739cc2cecc9.svg#card=math&code=%28A%2BB%29%28A%2BC%29%28B%2BC%29&height=20&id=yvPSd)。<br />一个布尔表达式及其对偶式 **并不一定** 等价。如果等价，我们称其是 **self-dual** 的。<br />但是，如果我们将一个 **等式** 两边同时取对偶，那么等式仍然是成立的。我们称这种性质为布尔代数的 **对偶原则（duality principle）**。

**一些常用的化简性质：**<br />![](https://cdn.nlark.com/yuque/__latex/05e7418072b8a2d84c975cd48b952b1e.svg#card=math&code=X%2BXY%20%3D%20X%281%2BY%29%20%3D%20X%5Ccdot1%3DX&height=20&id=L4xKc)
![](https://cdn.nlark.com/yuque/__latex/918464a51e5e44f3950e0bc8714d97f7.svg#card=math&code=XY%2BX%5Coverline%20Y%20%3D%20X%28Y%2B%5Coverline%20Y%29%20%3D%20X%5Ccdot%201%20%3D%20X&height=25&id=IKnJa)
![](https://cdn.nlark.com/yuque/__latex/8f8e094ea8710e03258660d73ee8bee3.svg#card=math&code=X%2B%5Coverline%20XY%20%3D%20%28X%2B%5Coverline%20X%29%28X%2BY%29%20%3D%201%5Ccdot%28X%2BY%29%3DX%2BY&height=25&id=fGKt6)（应用分配率 15）<br />![](https://cdn.nlark.com/yuque/__latex/5483a36cbf6da1202a25c40a5ee72a6a.svg#card=math&code=XY%2B%5Coverline%20XZ%2BYZ%3DXY%2B%5Coverline%20XZ%2BXYZ%2B%5Coverline%20XYZ%3DXY%281%2BZ%29%2B%5Coverline%20XZ%281%2BY%29%20%3D%20XY%2B%5Coverline%20XZ&height=25&id=hF3UF)
（称为 **一致律定理, consensus theorem**，说明第三项是冗余项）<br />又根据对偶原则，有：<br />![](https://cdn.nlark.com/yuque/__latex/9a3de1e58f77af06457af5a29fe1edf9.svg#card=math&code=X%28X%2BY%29%3DX&height=20&id=N1UIv)
![](https://cdn.nlark.com/yuque/__latex/2f95c3640f34e98567fc3df151df9fa2.svg#card=math&code=%28X%2BY%29%28X%2B%5Coverline%20Y%29%20%3D%20X&height=25&id=beo9G)
![](https://cdn.nlark.com/yuque/__latex/a2a4be22003ce06454c5fde60c08fda8.svg#card=math&code=X%28%5Coverline%20X%2BY%29%20%3D%20XY&height=25&id=mNF7l)
![](https://cdn.nlark.com/yuque/__latex/c2d0ba04285a90d4eab56811115ed029.svg#card=math&code=%28X%2BY%29%28%5Coverline%20X%2BZ%29%28Y%2BZ%29%3D%28X%2BY%29%28%5Coverline%20X%2BZ%29&height=25&id=n5Mnv)

**Complementing Functions.** 函数 ![](https://cdn.nlark.com/yuque/__latex/800618943025315f869e4e1f09471012.svg#card=math&code=F&height=16&id=nOgd1) 的反函数记为 ![](https://cdn.nlark.com/yuque/__latex/43c712f7eaeee6f3f498a2148cc136da.svg#card=math&code=%5Coverline%20F&height=21&id=j5Wb0)，取反即为对整个函数作 NOT。如图：
![image.png](./assets/1606703696429-6c2370a7-97c4-4385-8923-6a2f4774984b.png)
有一种等价的方法：1) 将 AND 和 OR 相互交换；2) 对每一个常量和变量取反。亦即，先求函数的对偶式，然后对每个文字取反：
![image.png](./assets/1606703896990-5437db0f-b60c-4dcd-8ff0-bec71e949678.png)

**Substitution rules.** 将一个等式中的某个变量的所有出现都代换为逻辑函数 F，等式仍然成立。


## 2.3 范式 | Standard Forms
**Product term.** 单个文字或若干文字的 AND 称为 **乘积项**（同“合取字句”。注：此处“同”指与 [范式 | 信安数学基础](https://www.yuque.com/xianyuxuan/coding/sfs9gg#bwkws) 中含义相同但命名不同的概念，下同）。<br />**Sum term.** 单个文字或若干文字的 OR 称为 **求和项**（同“析取字句”）。<br />**Min term.** 所有变量都以原变量或反变量的形式出现且只出现一次的 **乘积项 **称为 **最小项** 。<br />对于 n 个变量，一共有 ![](https://cdn.nlark.com/yuque/__latex/d1db0d9c696a8c056e7117dbbb4ef6db.svg#card=math&code=2%5E&height=16&id=yo1S6) 个不同的最小项；因此对每个最小项我们可以得到其唯一的序号 ![](https://cdn.nlark.com/yuque/__latex/865c0c0b4ab0e063e5caa3387c1a8741.svg#card=math&code=i&height=16&id=uhgfe)，我们用 ![](https://cdn.nlark.com/yuque/__latex/342e772474b691ac87dac30aeef596c0.svg#card=math&code=m_i&height=14&id=KdndQ) 来表示这个最小项。例如：
![image.png](./assets/1606706062205-4c8d3ed3-eaab-4f9f-a802-e0181c99c423.png)
**Max term. **所有变量都以原变量或反变量的形式出现且只出现一次的 **求和项 **称为 **最大项** 。 我们用 ![](https://cdn.nlark.com/yuque/__latex/cf02c22fc164faf4976cae168d7d73bd.svg#card=math&code=%20M_i&height=18&id=ceQRT) 表示最大项。如：
![image.png](./assets/1606706080343-4fac8746-5512-4101-a71a-32de96495482.png)
可见，![](https://cdn.nlark.com/yuque/__latex/9f7a07958410e025cc04134d838a2cc6.svg#card=math&code=M_i%20%3D%20%5Coverline%20%7Bm_i%7D%2C%5Cquad%20m_i%20%3D%20%5Coverline%20%7BM_i%7D&height=24&id=g7LD6)。

**Sum of minterm, SOM.** 一个布尔函数可以由真值表中所有使函数取值为 1 的最小项的和来表示，这种表达式称为 **最小项之和**（同“主析取范式”）。例如，下面一个函数 F 表示为 SOM 为：
![image.png](./assets/1606706400501-a4bc7300-9090-40cd-bfac-9d3a415a149f.png)
进一步，可以简写为：
![image.png](./assets/1606706460127-bb252218-c961-4704-956b-b986ce35c7eb.png)
[这里](https://www.yuque.com/xianyuxuan/coding/sfs9gg#JTlmy) 证明了 SOM 的存在和唯一性。

**Product of maxterm, POM.** 最大项之积（同“主合取范式”）的定义是类似的。看下面一个例子：<br />研究 F 的反函数：
![image.png](./assets/1606706679444-46753a50-9e9b-424d-8675-0351b808525a.png)
对其取反，有：
![image.png](./assets/1606706711056-0318bb2f-25cf-4a20-bdc1-0893e538c220.png)
进一步可以简写为：
![image.png](./assets/1606706726646-759dd8ee-4e53-4e03-98fe-7ee7e79225e4.png)

**Sum of products, SOP.** 乘积项之和，同“析取范式”。<br />**Product of sums, POS.** 求和项之积，同“合取范式”。<br />SOP 和 POS 可以用 AND/OR 两级电路结构实现。
![image.png](./assets/1606707266219-1b0e00a2-583e-40d8-89b8-47a79e194698.png)


## 2.4 电路化简 | Circuit Optimization

### 2.4.1 成本标准 | Cost Criteria
**Literal cost.**<br />**Gate-input cost.**  


### 2.4.2 两级电路优化 | Two-Level Optimization

#### 2.4.2.1 卡诺图 | Karnaugh Map
**2 variable maps.** <br />**3 variable maps.** <br />**4 variable maps.** <br />**Don't-cares in K-maps.** <br />**POS optimization.** 


#### 2.4.2.2 卡诺图的化简 | Map Manipulation
**Implicants.** <br />**Prime implicants.** <br />**Essencial Prime Implicants.** <br />**Selection Rule.** 


### 2.4.3 多级电路优化 | Multi-Level Optimization


## 2.5 更多的门 | Other Gate Types
**NAND gate.** <br />**NOR gate.** <br />**XOR gate.** <br />**XNOR gate.** <br />**Odd & Even Functions.** <br />**Parity Generator & Checkers.** <br />**Buffers.** 


# 

# 4 时序电路 | Sequential Circuit

## 4.1 


# 6 寄存器与寄存器传输 | Registers and Register Transfers


