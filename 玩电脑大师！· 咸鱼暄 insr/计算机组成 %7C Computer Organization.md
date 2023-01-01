
<center>![image.png](../../../assets/1654452339796-a855e535-5361-4b3f-96bc-f084bb514e00.png){width=300}</center>


# 写在前面
	紫色背景的内容不重要

	橙色背景的内容是要学的补充说明内容

	蓝绿色背景的内容是例题

	品红色背景的内容是真题


## 进度！

- [ ] Ch 1 - Intro & Misc
- [x] Ch 2 - Instructions
- [x] _Ch 3 - Arith （没完全学完）_
- [ ] Ch 4 - Processor
- [x] Ch 5 - Cache
- [ ] Ch 6 - I/O
- [ ] 看题
- [ ] A4 纸

已经完成的：

- 5.10 Cache (partly)
- 5.23 Cache (done)
- 5.25 Instructions (2.1~2.3)
- 6.1 Instructions (done)
- 6.5 Arith 50%
- 6.6 Arith 100% _（没完全学完）_
- 6.8 Processor 35% (4.1~4.4)

计划：

- [ ] 6.9 Processor 100% (4.5~4.9)
- [ ] 6.10 I/O 100%		Lec Inst, Arith
- [ ] 6.11 Misc & A4	Lec Cache, I/O		[支部会，思想汇报]
- [ ] 6.12 做题			Lec Processor
- [ ] 6.13 查漏			Lec Exec			[回港]


# 1 Intro & Misc

- **Moore's Law**: Integrated circuit resources double every 18-24 months.
- KB = 103 B, KiB = 210 B
- K M G T P E Z Y
- **Response Time / Execution Time**	从程序开始到结束的时间
- **Throughput / Bandwidth**	单位时间内完成的任务数量
- **Performance**		可以定义为 
<center>![](https://cdn.nlark.com/yuque/__latex/519c3451d4ff7e5defa5f0d852b26fa4.svg#card=math&code=%5Cfrac%7B1%7D%7B%5Ctext%7BResponse%20Time%7D%7D&id=ZrBYh){width=300}</center>

- **Amdahl Law **
<center>![](https://cdn.nlark.com/yuque/__latex/96ca9002856d7756660b7ed2b5cd6648.svg#card=math&code=T_%7B%5Ctext%7Bimproved%7D%7D%20%3D%20%5Cfrac%7BT_%7B%5Ctext%7Baffected%7D%7D%7D%7B%5Ctext%7BImprovement%20Factor%7D%7D%2BT_%5Ctext%7Bunaffected%7D&id=vm5Wl){width=300}</center>

- ……不是很想学了 再说吧


# 2 Instructions
:::success
本章部分内容建立在掌握至少一门汇编语言的基础上，例如修读过计算机系统概论或汇编语言等课程。
:::
我们讨论过，计算机的 performance 受 **inst#, clock cycle time 和 clock cycles per inst (CPI)** 决定。给定一个程序，需要使用的 inst# 受编译器和 inst set architecture 决定。本章介绍 RISC-V 的 ISA。

## 2.1 寄存器，寻址方式
**寄存器**	RISC-V architecture 提供 32 个数据寄存器，分别命名为`x0`~`x31`，每个寄存器的大小是`64`位。在 RISC-V architecture 中，一个 **word** 为 32 位，一个 **doubleword** 为 64 位。这些寄存器中的一部分有专门的用途，我们稍后对其进行讨论。

RISC-V architecture 也提供一系列浮点数寄存器`f0`~`f31`，这不是我们讨论的重点。

**寻址**		RISC-V architecture 的地址是 64 位的，地址为字节地址，因此总共可以寻址
<center>![](https://cdn.nlark.com/yuque/__latex/716ae4ac9b8718291cfcfcaf3b993026.svg#card=math&code=2%5E%7B64%7D&id=s6u9l)个字节，即![](https://cdn.nlark.com/yuque/__latex/6da2a02c9623c82e9ec092b83489fb2b.svg#card=math&code=2%5E%7B61%7D&id=ENdf7)个 dword (doubleword, 下同){width=300}</center>
。

在一些 architecture 中，word 的起始地址必须是 word 大小的整倍数，dword 也一样，这种要求称为 **alignment restriction**。RISC-V 允许不对齐的寻址，但是效率会低。

RISC-V 使用 **little endian** 小端编址。也就是说，当我们从 0x1000 这个地址读出一个 dword 时，我们读到的实际上是 0x1000~0x1007 这 8 个字节，并将 0x1000 存入寄存器地位，0x1007 存入高位。

RISC-V 支持 PC relative 寻址、立即数寻址 (`lui`)、间接寻址 (`jalr`)、基址寻址 (`8(sp)`)：

<center>![image.png](../../../assets/1654055499913-f3fd752f-06b7-43e4-a06f-3640e66481ed.png){width=300}</center>


**补码 2's complement**	
<center>![](https://cdn.nlark.com/yuque/__latex/2215ae4ad672c6271e34c7645f35f70b.svg#card=math&code=x%20%2B%20%5Cbar%20x%20%3D%20111%5Cdots111_2%20%3D%20-1&id=kkLTx)，因此![](https://cdn.nlark.com/yuque/__latex/5509d710878235b8ef48acdd007f4ad0.svg#card=math&code=-x%20%3D%20%5Cbar%20x%20%2B%201&id=V7Urh)。前导 0 表示正数，前导 1 表示负数。[See also](https://www.yuque.com/xianyuxuan/coding/sca003#VqE99){width=300}</center>

因此在将不足 64 位的数据载入寄存器时，如果数据是无符号数，只需要使用 0 将寄存器的其他部分填充 (**zero extension**)；而如果是符号数，则需要用最高位即符号位填充剩余部分，称为符号扩展 (**sign extension**)。

即，在指令中的`lw`, `lh`, `lb`使用 sign extension，而`lwu`, `lhu`, `lbu`使用 zero extension。

	【18 - 19 Final】
	
<center>![image.png](../../../assets/1655019006306-bf6087f9-5461-4b02-be9a-8b6b410c9f89.png){width=300}</center>

	答案：-0x52F00000, -0x0FFFFCDF



## 2.2 指令，指令格式
课本上介绍的 RISC-V 指令（`lr.d`, `sc.d`被省略了）列表如下：


<center>![Q1@]9V[K[%EY}0U95C$BKN9.png](../../../assets/1654864713202-23520b16-be27-484e-8f08-39aa863679ba.png){width=300}</center>

RISC-V 的跳转指令的 offset 是基于当前指令的地址的偏移；这不同于其他一些汇编是基于下一条指令的偏移的。即如果是跳转语句`PC`就不 +4 了，而是直接 +offset。

`lw`, `lwu`等操作都会清零高位。

RISC-V 指令格式如下：


<center>![BL)RAQGFHU[QI(3H`~05U$Y.png](../../../assets/1653461947307-ab399754-6565-46f5-8554-641c7def91a4.png){width=300}</center>

其中`I`型指令有两个条目；这是因为立即数移位操作`slli`,`srli`,`srai`并不可能对一个 64 位寄存器进行大于 63 位的移位操作，因此 12 位 imm 中只有后 6 位能实际被用到，因此前面 6 位被用来作为一个额外的操作码字段，如上图中第二个`I`条目那样。其他`I`型指令适用第一个`I`条目。

另外，为什么`SB`和`UJ`不存立即数（也就是偏移）的最低位呢？因为，偏移的最后一位一定是 0，即地址一定是 2 字节对齐的，因此没有必要保存。
	**既然每个指令都是 4 字节对齐的，为什么不是最后两位都省略，而是只省略一位呢？**
	实际上，是存在指令长为 2 字节的 extension 的，只不过我们没学
<center>![)]UX{S0[~_]}[W%2I(CMEAY.png](../../../assets/1654679588063-ac5bf562-8b30-4151-918c-d95cb93b7888.png){width=300}</center>
：
	
<center>![image.png](../../../assets/1654679475579-ff3afec9-a463-41e1-a7ad-a2ec86b35e51.png){width=300}</center>

	
<center>![image.png](../../../assets/1654679542585-af36dd13-2f74-4126-8b67-90392a0f1f8a.png){width=300}</center>




## 2.3 伪指令及其实现

<center>![image.png](../../../assets/1653470001735-c9b5f2b8-f4c6-48ca-beec-7987bea5d71f.png){width=300}</center>

[*] `j imm`也可以用`beq x0, x0, imm`实现，但是此法的`imm`的位数会较短，所以不采用。

## 2.4 分支和循环
略


## 2.5 过程调用和栈
RISC-V 约定：

   - `x5`-`x7`以及`x28`-`x31`是 temp reg，如果需要的话 caller 保存；也就是说，不保证在经过过程调用之后这些寄存器的值不变。
   - `x8`-`x9`和`x18`-`x27`是 saved reg，callee 需要保证调用前后这些寄存器的值不变；也就是说，如果 callee 要用到这些寄存器，必须保存一份，返回前恢复。
   - `x10`-`x17`是 8 个参数寄存器，函数调用的前 8 个参数会放在这些寄存器中；如果参数超过 8 个的话就需要放到栈上（放在`fp`上方，`fp + 8`是第 9 个参数，`fp + 16`的第 10 个，以此类推）。同时，过程的结果也会放到这些寄存器中（当然，对于 C 语言这种只能有一个返回值的语言，可能只会用到`x10`）。
   - `x1`用来保存返回地址，所以也叫`ra`。因此，伪指令`ret`其实就是`jalr x0, 0(x1)`。
   - 栈指针是`x2`，也叫`sp`；始终指向**栈顶元素**。栈从高地址向低地址增长。
      - `addi sp, sp, -24`, `sd x5, 16(sp)`, `sd x6, 8(sp)`, `sd x20, 0(sp)`可以实现将 x5, x6, x20 压栈。
   - 一些 RISC-V 编译器保留寄存器`x3`用来指向静态变量区，称为 global pointer `gp`。
   - 一些 RISC-V 编译器使用`x8`指向 activation record 的第一个 dword，方便访问局部变量；因此`x8`也称为 frame pointer `fp`。在进入函数时，用`sp`将`fp`初始化。
      - `fp`的方便性在于在整个过程中对局部变量的所有引用相对于`fp`的偏移都是固定的，但是对`sp`不一定。当然，如果过程中没有什么栈的变化或者根本没有局部变量，那就没有必要用`fp`了。

至此，我们将所有寄存器及其用途总结如下：


<center>![YTQMX_[2%~{%R3(K)F4H{67.png](../../../assets/1654054605190-66992a62-3995-4285-8002-c28a0a8e9073.png){width=300}</center>

其中“preserved on call”的意思是，是否保证调用前后这些寄存器的值不变。


<center>![image.png](../../../assets/1654866071308-dc8851c8-a41c-404f-830d-3aae477775df.png){width=300}</center>



## 2.6 其他话题

- 检查 index out of bounds：如果`x20 = i, x11 = size`，那么`bgeu x20, x11, IndexOutOfBounds`，即 `x20 >= x11 || x20 < 0`
- 大立即数
   - `lui`将 20 位常数加载到目标寄存器的 31 到 12 位；然后用`addi`填充后面 12 位，就可以实现加载一个大立即数了。
   - 但是，如果后 12 位的首位是 1，在`addi`的时候就会因为`sign ext`额外加上`0xFFFFF000`。因此，我们只需要将`lui`的 imm 增加 1，这样`lui`加载后实际上就是增加了`0x00001000`，和`0xFFFFF000`相加后就可以抵消影响了。
- ASCII，是 8 位的，可以用`lbu`
- Unicode，是 16 位的，可以用`lhu`
- 尾递归 tail call / tail recursion，可以转成循环。


## 2.7 练习

### 写代码


### 译码


# 3 Arithmetic

## 3.1 一个基本的 ALU
**世界上不存在减法**。众所周知，减法就是加上相反数。所以这个世界上不存在减法。

**Overflow**。硬件规模是有限的，因此运算结果超过这个限制时，就会发生溢出。对于有符号加法，当正数和正数相加得到负数，或者负数和负数相加得到正数时，就可以判定溢出。对于无符号加法，如果结果小于二者中任意一个，也可以判定溢出。

**ALU, Arithmetic Logic Unit**，算术逻辑单元，执行一些算术运算或者逻辑运算。


### 3.1.1 1-bit ALU
	（下面这部分内容在课本附录 A.5 开始的地方）

在数字逻辑设计这门课程中，我们学过 AND, OR, XOR 这些 gates，以及 inverter 和 mux 这些东西，我们尝试用这些东西攒一个 ALU 出来。在这一节中，我们希望 ALU 具有加法、减法、与运算、或运算和比较的能力。

我们先考虑 1 bit ALU 的构造。我们学习过 1 bit Full Adder 的构造：

<center>![image.png](../../../assets/1654415057128-ba0032a0-c3b5-49a4-8a7a-43abcb692357.png){width=300}</center>

上左图是全加器的具体构造，右图是我们将其进行封装后的表示方式。

我们结合一个 mux，就可以构造一个支持与、或以及加法运算的 1 bit ALU：

<center>![image.png](../../../assets/1654415145349-fd034b21-25ff-4a16-95f1-a0d964750b9b.png){width=300}</center>

其中`Operation`是用来指明 mux 采取哪个结果的信号，值为 00 01 10 分别对应与、或、加法运算。


### 3.1.2 加上减法和 NOR！
减法运算怎么办呢？众所周知，由于补码有 
<center>![](https://cdn.nlark.com/yuque/__latex/333729f98b3736002e2b12934b4b9a8c.svg#card=math&code=x%20%2B%20%5Cbar%20x%20%3D%2011%5Cdots11_2%20%3D%20-1&id=nivrD)，因此![](https://cdn.nlark.com/yuque/__latex/5509d710878235b8ef48acdd007f4ad0.svg#card=math&code=-x%20%3D%20%5Cbar%20x%20%2B%201&id=XFKTk)，所以![](https://cdn.nlark.com/yuque/__latex/15e09e887b06975fc03aaac24d90fd54.svg#card=math&code=a%20-%20b%20%3D%20a%20%2B%20%28-b%29%20%3D%20a%20%2B%20%5Cbar%20b%20%2B%201&id=DmUvk){width=300}</center>
。据此我们可以构造这样的结构：

<center>![image.png](../../../assets/1654415317462-1a651623-9b94-4957-9f1d-e7c18a33af84.png){width=300}</center>

其中`Binvert`用来指明是否需要将结果取反；在计算减法时，我们将`Binvert`设为`1`，然后将`CarryIn`也设为`1`，`Operation`设为`2`，这样我们的结果就是
<center>![](https://cdn.nlark.com/yuque/__latex/8ab092144360d37dee44378116c6a260.svg#card=math&code=a%20%2B%20%5Cbar%20b%20%2B%201&id=eCF8C){width=300}</center>
。

`NOR`运算：`a NOR b = NOT(a OR b) = (NOT a) AND (NOT b)`，因此`NOR`运算可以这样实现：

<center>![image.png](../../../assets/1654416483714-328ce497-05f0-4a7c-bb5d-5dd9bb6f585e.png){width=300}</center>

上右图是我们目前的 1 bit ALU 的抽象结构。


### 3.1.3 串联得到 64-bit ALU！
有了 1 bit 的 ALU，我们就可以构造出 RISC-V 所需的 64 bits 的 ALU 了：

<center>![image.png](../../../assets/1654416886066-2c770d92-fb4b-4c67-9e8a-9c1dd508276e.png){width=300}</center>

可以看到，对于 64 位的加法、减法、AND, OR, NOR 运算，这样的 64 位 ALU 都可以完成。

同时也可以注意到，这里面除了我们熟悉的内容外，还多了`Less`, `Set`和`Overflow`这些位。它们是用来干什么的呢？

首先`Overflow`是容易理解的，它用来表示加法或减法有没有出现溢出的现象；显然这个判断只需要在 ALU63，即 Most Significant Bit 才需要进行。容易证明，如果
<center>![](https://cdn.nlark.com/yuque/__latex/7ecd9ba47c51075dfc7f458cf512df1c.svg#card=math&code=C_%7Bin%7D%5Coplus%20C_%7Bout%7D%20%3D%201&id=NRiFC){width=300}</center>
，那么存在溢出；因此 ALU63 只需要添加一个额外的 XOR 门即可完成这一判断。

`Less`和`Set`共同使用，是为了实现`slt rd, rs1, rs2`这个操作的。这个操作的含义是，如果`rs1 < rs2`，那么将`rd`置为`1`，否则置为`0`。如何进行这一判断呢？很简单，如果`rs1 - rs2`的结果为负，也就是说如果`rs1 - rs2`结果的最高位是`1`，那么就说明`rs1 < rs2`。所以等价地，对于`slt`这个操作，我们只需要将 ALU63 中加法器的结果赋值给`Result0`，即运算结果的 Least Significant Bit，而将其他位的结果`Result1`~`Result63`都设成 0，就可以完成`slt`操作了。

所以可以看到，上图中，除了 ALU0 的`Less`来自 ALU63 的`Set`外，其他 ALU 的`Less`都是`0`。

结合上述讨论，上图中 ALU0 ~ ALU62 的结构如下左图所示，ALU63 的结构如下右图所示：

<center>![image.png](../../../assets/1654430550957-7cc66c76-4fce-415a-bcc7-a43c0eac8bc1.png){width=300}</center>

（注：右图中的 Overflow Detection 被复杂化了，实际上可以通过`CarryIn`和`CarryOut`的异或完成的。）

可以看到，`Operation`增加了`3`的取值，这个取值表示进行`slt`操作。


### 3.1.4 一点优化！
之前我们也讨论过，如果做减法或者`slt`的话，需要将`Binvert`和 ALU0 的`CarryIn`设成`1`，如果是加法的话这两个信号都是`0`；其他运算用不到这两个信号。因此这两个信号始终取值相等，我们可以将这两个信号合并为一个，称之为`Bnegate`。

另外，我们也有`beq`，`bne`这样的操作，结合 Common case fast 的设计思想，我们将判断结果是否为 0 的功能也直接加到 ALU 里。

结合上述两个思路，我们形成了最终的 64-bit ALU！

<center>![image.png](../../../assets/1654431118686-b635a01f-1dbd-41b0-89a3-bddec064c1dc.png){width=300}</center>

对于这样的一个 ALU，我们需要 4 bits 的 control lines，分别是`Ainvert`, `Bnegate`和`Operation`(2 bits)。ALU 的符号和 control lines 的含义如下：

<center>![image.png](../../../assets/1654432159980-cad11a29-2d85-414a-964b-113491b93193.png){width=300}</center>



### 3.1.5 更快的加法
上面的 64 位加法的实现方式是通过 1 位加法器串联实现的，这种方式势必需要等待前一个加法器算出结果后才能算后一个的。这种多位加法器的实现称为行波加法器 **Ripple Carry Adder, RCA**。显然，这种实现方式比较慢。

那么，如何加速呢？


#### 3.1.5.1 Carry Lookahead Adder, CLA
课本指出，RCA 缓慢的重要原因是后一个 adder 需要等前一个 adder 的 carry 结果；但我们不妨讨论出现 carry 的可能。第一种可能是，如果
<center>![](https://cdn.nlark.com/yuque/__latex/26fdbf8e53cb0e48da5f4ddd4aaf5a5c.svg#card=math&code=a&id=sKaO3)和![](https://cdn.nlark.com/yuque/__latex/d29c2e5f4926e5b0e9a95305650f6e54.svg#card=math&code=b&id=nuYZV)都是 1，那么一定会**生成**一个 carry；另一种可能是，如果![](https://cdn.nlark.com/yuque/__latex/26fdbf8e53cb0e48da5f4ddd4aaf5a5c.svg#card=math&code=a&id=G6cIw)和![](https://cdn.nlark.com/yuque/__latex/d29c2e5f4926e5b0e9a95305650f6e54.svg#card=math&code=b&id=AlPpY){width=300}</center>
中有且仅有一个是 1，那么如果传入的 carry 是 1，则这里也会 carry，即 carry 被**传播**了。

也就是说，
<center>![](https://cdn.nlark.com/yuque/__latex/1402279c3b56627a3ef176f0fe4df21e.svg#card=math&code=c_%7Bout%7D%20%3D%20a%5Ccdot%20b%20%2B%20%28a%20%2B%20b%29%5Ccdot%20c_%7Bin%7D&id=ZlZt8)。我们记 **generate**![](https://cdn.nlark.com/yuque/__latex/1d8b390da49888d520c54c974dd8117d.svg#card=math&code=g%20%3D%20a%20%5Ccdot%20b&id=hl9yE)，**propagate**![](https://cdn.nlark.com/yuque/__latex/dcc3c7b79458e2418791da868f01d0aa.svg#card=math&code=p%20%3D%20a%20%2B%20b&id=yTBHR)，则有 ![](https://cdn.nlark.com/yuque/__latex/0ca12dd0ce8cb82fc0b65e5499ed6cc2.svg#card=math&code=c_%7Bout%7D%20%3D%20g%20%2B%20p%5Ccdot%20c_%7Bin%7D&id=rFmU0){width=300}</center>
。所以，我们可以这样构造一个全加器：

<center>![image.png](../../../assets/1654448385307-b26150c1-a6fb-4e18-b237-e1a4ddf9ead3.png){width=300}</center>

所以，我们可以推导出如下关系：

<center>![image.png](../../../assets/1654448174404-88b6a7da-5012-41b6-95ce-5a58f0e1fe68.png){width=300}</center>

利用这个关系，我们可以构造这样一个四位加法器：

<center>![image.png](../../../assets/1654448839751-163b42fd-a4f6-4667-a1ba-c021ec0e70c3.png){width=300}</center>

上面的 PFA, Partial Fully Adder，就是前面我们构造的新全加器的一部分。可以看到，通过这样的方式，我们可以加速加法的运算；但是注意到越到高位，门的 fan-in 就越大，但是这不是可以一直增加的。所以对于更多位数的加法器，我们将上面这样构成的 4-bit CLA 再通过类似的方式串起来！

<center>![image.png](../../../assets/1654450398290-9368b91c-4f00-4f53-8777-dc7147a6d99e.png){width=300}</center>


#### 3.1.5.2 Carry Skip Adder (马德先生没讲)

#### 3.1.5.3 Carry Select Adder, CSA
这个思路其实比较简单，就是把输入 carry 为 0 或者 1 的情况都算一遍，然后根据实际的情况从中选出正确的那种就好了：

<center>![image.png](../../../assets/1654450514491-a6a750b1-fc9b-4d11-982a-b19cbbf6f1a0.png){width=300}</center>


<center>![image.png](../../../assets/1654450525296-c94b0e6d-acad-4a81-952a-70fe8c461e32.png){width=300}</center>


## 3.2 乘法 暂时不想学了，听说考的不多
下面这样的硬件结构可以实现无符号乘法：

<center>![image.png](../../../assets/1654531121258-e497919c-c487-4f1f-8310-4e0b537a9dbd.png){width=300}</center>




## 3.3 除法 暂时不想学了，听说考的不多


## 3.4 浮点运算

### 3.4.1 IEEE 754 浮点表示
我们将小数点左边只有 1 位数字的表示数的方法称为 **科学记数法, scientific notation**，而如果小数点左边的数字不是 0，我们称这个数的表示是一个 **规格化数, normalized number**。科学记数法能用来表示十进制数，当然也能用来表示二进制数。

IEEE 754 规定了一种浮点数标准：我们将浮点数表示为
<center>![](https://cdn.nlark.com/yuque/__latex/e96775115fd0a18b9f7a8712ba58d164.svg#card=math&code=%28-1%29%5ES%20%5Ctimes%20F%5Ctimes%202%5EE&id=xBN8J)的形式，这里的![](https://cdn.nlark.com/yuque/__latex/17708400872717c1340d839667052458.svg#card=math&code=F%5Ctimes%202%5EE&id=fooMJ)是一个规格化数，而![](https://cdn.nlark.com/yuque/__latex/c4c3660263be91c48b92d8621cd95271.svg#card=math&code=%28-1%29%5ES&id=GSKiU)用来表示符号位：![](https://cdn.nlark.com/yuque/__latex/55fc237afbe535f7d8434985b848a6a7.svg#card=math&code=S&id=TQPBn)为 0 说明该浮点数为整数，为 1 则为负数；![](https://cdn.nlark.com/yuque/__latex/7aaf2781990aa336d909f7ebd32e2f69.svg#card=math&code=F&id=JuieP)和![](https://cdn.nlark.com/yuque/__latex/321138a59e6eab0c97c21f05282a80a6.svg#card=math&code=E&id=mcfpf)也用若干 bits 表示，分别表示尾数和指数，我们稍后讨论。也就是说，我们将其表示为![](https://cdn.nlark.com/yuque/__latex/8c1a336f9f76cb0c115e1dcb8c095b1c.svg#card=math&code=1.xxxxx_2%20%5Ctimes%202%5E%7Byyyy%7D&id=VBoQr){width=300}</center>
的形式（为什么小数点左边是 1 呢？因为二进制只有 0 和 1，而规格化要求小数点左边不能为 0）。我们通过科学记数法调整了小数点的位置使其满足规格化的要求，因此我们称这种数的表示方法为 **浮点, floating point**。

小数点的英文是 decimal point，但是我们这种表示方法不再是 decimal 的了，因此我们起个新名字：**二进制小数点, binary point**。

IEEE 754 规定了两种精度的浮点数格式，分别是 single precision 和 double precision（分别对应 C 语言中的`float`和`double`），RISC-V 这两种都支持：

<center>![image.png](../../../assets/1654451689188-30db0d4d-73e6-478a-b01e-dd90b16c68ca.png){width=300}</center>


<center>![image.png](../../../assets/1654451723799-f579acc1-0bdb-4e18-9804-ac94ad9d1d55.png){width=300}</center>

可以看到，fraction 的位数越多，浮点数的精度就越高；而 exponent 的位数越多，浮点数能保存的范围就越大。

那么对于
<center>![](https://cdn.nlark.com/yuque/__latex/e96775115fd0a18b9f7a8712ba58d164.svg#card=math&code=%28-1%29%5ES%20%5Ctimes%20F%5Ctimes%202%5EE&id=KACFq)，![](https://cdn.nlark.com/yuque/__latex/55fc237afbe535f7d8434985b848a6a7.svg#card=math&code=S&id=libXo)的二进制表示方法是显然的，仅需要一个 bit 就好了。那么![](https://cdn.nlark.com/yuque/__latex/7aaf2781990aa336d909f7ebd32e2f69.svg#card=math&code=F&id=Z5LOl)和![](https://cdn.nlark.com/yuque/__latex/321138a59e6eab0c97c21f05282a80a6.svg#card=math&code=E&id=SLRI9)怎么表示呢？如我们之前所说，![](https://cdn.nlark.com/yuque/__latex/7aaf2781990aa336d909f7ebd32e2f69.svg#card=math&code=F&id=dEKZw)就是![](https://cdn.nlark.com/yuque/__latex/9bed0c4398ad2ffcc2855ad8cd3baff0.svg#card=math&code=1.xxxx_2&id=CbaXT)的形式，这个 1 是固定的，因此![](https://cdn.nlark.com/yuque/__latex/7aaf2781990aa336d909f7ebd32e2f69.svg#card=math&code=F&id=ATUTa)只需要保存![](https://cdn.nlark.com/yuque/__latex/4d201d774b486b47180686e239bfe4b4.svg#card=math&code=xxxx_2&id=Pmwg3)的部分就可以了！那么![](https://cdn.nlark.com/yuque/__latex/321138a59e6eab0c97c21f05282a80a6.svg#card=math&code=E&id=n8UIB)怎么办呢？注意到这个指数可能是正整数、负整数或 0，因此我们使用一个偏移，对单精度浮点数偏移 127，双精度浮点数偏移 1023（刚好是表示范围的一半！），也就是说我们保存的`exponent`其实是![](https://cdn.nlark.com/yuque/__latex/0bb448c020f1170d9589ebd3fa1b2783.svg#card=math&code=E%20%2B%20bias&id=kk3tx){width=300}</center>
的二进制。也就是说，对于这样的一个表示，其值是：


<center>![](https://cdn.nlark.com/yuque/__latex/802c0e3ba472b6c857f3747887de03a9.svg#card=math&code=%28-1%29%5ES%5Ccdot%20%281%20%2B%20%5Ctext%7Bfraction%7D%29%20%5Ccdot%202%20%5E%20%7B%5Ctext%7Bexponent%7D%20-%20%5Ctext%7Bbias%7D%7D&id=hNC4O){width=300}</center>

课本给出了一个例子：

<center>![image.png](../../../assets/1654452276501-8091ba6c-3817-41b9-9bc0-592dff9a9432.png){width=300}</center>

聪明的小朋友可能会问，0 应该怎么保存呢？毕竟 0 没有前导 1。对于这样的特殊情形，IEEE 754 有特别规定，用特殊的值保存它们：

<center>![image.png](../../../assets/1654452874205-52d98ec3-52b4-499b-b318-548fdd6ea083.png){width=300}</center>

在上表中：

   - 第 1 条表示 0；
   - 第 2 条表示非规格化数，这种数主要是为了用来表示一些很小的数，它的取值为
<center>![](https://cdn.nlark.com/yuque/__latex/9fc7936bcdfafd41801dd3e8c2cf24ce.svg#card=math&code=%28-1%29%5ES%5Ccdot%20%28%5Cmathbf%7B0%7D%20%2B%20%5Ctext%7Bfraction%7D%29%20%5Ccdot%202%20%5E%20%7B-%20%5Ctext%7Bbias%7D%7D&id=T1lAe){width=300}</center>
；但是并非所有机器都支持这种表示，有的机器会直接抛出一个 exception。我们不考虑非规格数的存在；
   - 第 3 条表示正常的浮点数；
   - 第 4 条表示无穷大或者无穷小，出现在 exponent overflow 或者浮点数运算中非 0 数除以 0 的情况；
   - 第 5 条表示非数，出现在 0/0, inf / inf, inf - inf, inf * 0 的情况

（如果数字过大不能表示，即 overflow，则结果置为 inf；如果数字过小不能表示，即 underflow，则结果置为 0。）

这两种表示法的范围和精度分别是多少呢？

   - 范围
      - 能表示值的**绝对值**的范围是 
<center>![](https://cdn.nlark.com/yuque/__latex/2f7e79dd8afb5db140cc396938456e74.svg#card=math&code=1.0_2%20%5Ctimes%202%5E%7B1-%5Ctext%7Bbias%7D%7D%20%5Csim%201.11%5Cdots%2011_2%20%5Ctimes%202%5E%7B11%5Cdots%2011_2-1-%5Ctext%7Bbias%7D%7D&id=u0hG4)，即![](https://cdn.nlark.com/yuque/__latex/a4227c2d0a2c6cc0883d191efe29e07f.svg#card=math&code=1%5Ctimes%202%5E%7B1%20-%20%5Ctext%7Bbias%7D%7D%5Csim%282%20-%202%5E%5Ctext%7BFra%23%7D%29%5Ctimes%202%5E%7B%282%5E%5Ctext%7BExp%23%7D%20-%201%29%20-%201%20-%20%5Ctext%7Bbias%7D%7D&id=TSoal){width=300}</center>
，其中`Fra#`和`Exp#`分别表示 fraction 和 exponent 的位数；
      - 单精度浮点数：
<center>![](https://cdn.nlark.com/yuque/__latex/f802837485f043773b055786d052ba2f.svg#card=math&code=%5Cpm%201%5Ctimes%202%5E%7B-126%7D%5Csim%20%5Cpm%282%20-%202%5E%7B23%7D%29%20%5Ctimes%202%5E%7B127%7D&id=DRjk6){width=300}</center>

      - 双精度浮点数：
<center>![](https://cdn.nlark.com/yuque/__latex/e5ff7cb2d4bc629501540d50ef9e0049.svg#card=math&code=%5Cpm%201%5Ctimes%202%5E%7B-1022%7D%5Csim%20%5Cpm%282%20-%202%5E%7B52%7D%29%20%5Ctimes%202%5E%7B1023%7D&id=fPwNC){width=300}</center>

   - 精度
      - 
<center>![](https://cdn.nlark.com/yuque/__latex/371586ae207a130ea344984ff3a6cb9d.svg#card=math&code=2%5E%20%5Ctext%7B-Fra%23%7D&id=r9vbq){width=300}</center>

      - 单精度浮点数：
<center>![](https://cdn.nlark.com/yuque/__latex/585cd29ce96cf4f755fa4b42d881ed00.svg#card=math&code=2%5E%7B-23%7D&id=ynk1b){width=300}</center>

      - 双精度浮点数：
<center>![](https://cdn.nlark.com/yuque/__latex/55af0b8bfc476c77483ffa24a4e2f885.svg#card=math&code=2%5E%7B-52%7D&id=YQNVn){width=300}</center>


可以试一下 -32.6，结果可以自己在  里面找~
	【18 - 19 Final】
	
<center>![image.png](../../../assets/1655018545639-c1ced675-3229-464b-94c1-5c684361738b.png){width=300}</center>

	答案：+inf, 0xBF800000



### 3.4.2 浮点加法
以
<center>![](https://g.yuque.com/gr/latex?1.000_2%5Ctimes2%5E%7B-1%7D-1.110_2%5Ctimes2%5E%7B-2%7D#card=math&code=1.000_2%5Ctimes2%5E%7B-1%7D-1.110_2%5Ctimes2%5E%7B-2%7D&id=YTIcR){width=300}</center>
为例， 浮点数的加减法分为以下几步：

1.  指数对齐，将小指数对齐到大指数：
<center>![](https://g.yuque.com/gr/latex?-1.110_2%5Ctimes2%5E%7B-2%7D%20%3D%20-0.111%5Ctimes2%5E%7B-1%7D#card=math&code=-1.110_2%5Ctimes2%5E%7B-2%7D%20%3D%20-0.111%5Ctimes2%5E%7B-1%7D&id=lzH5T){width=300}</center>
 
2.  Fraction 部分相加减：
<center>![](https://g.yuque.com/gr/latex?1.000-0.111%3D0.001#card=math&code=1.000-0.111%3D0.001&id=ttxCP){width=300}</center>
 
3.  将结果规格化：
<center>![](https://g.yuque.com/gr/latex?0.001%5Ctimes2%5E%7B-1%7D%3D1.000%5Ctimes2%5E%7B-4%7D#card=math&code=0.001%5Ctimes2%5E%7B-1%7D%3D1.000%5Ctimes2%5E%7B-4%7D&id=ceOVp){width=300}</center>
 ；同时需要检查是否出现 overflow 或者 underflow，如果出现则触发 Exception
4.  将 Fraction 部分舍入到正确位数；舍入结果可能还需要规格化，此时回到步骤 3 继续运行


<center>![image.png](../../../assets/1654493922562-098d36c8-cd64-4671-ac6b-a83f882e095a.png){width=300}</center>


### 3.4.3 浮点乘法
分别处理符号位、exponent 和 fraction：

- Exponent 相加并**减去 bias**，因为 bias 加了 2 次
- Fraction 部分相乘，并将其规格化；此时同样要考虑 overflow 和 underflow；然后舍入，如果还需要规格化则重复执行
- 根据两个操作数的符号决定结果的符号


<center>![image.png](../../../assets/1654494125594-7445f47b-e6a7-4288-a370-b2a8cd0c746d.png){width=300}</center>



### 3.4.4 精确算术
IEEE 754 规定了一些额外的舍入控制，用来保证舍入的精确性。

**Round modes**


<center>![VO3$J2GEZ3YX(}3F0_)NWHW.png](../../../assets/1654504454500-4ae127de-3333-4b4e-8b88-e44f5d83f7ed.png){width=300}</center>

Round to nearest even 只对 0.5 有效，别的都和四舍五入一样

一般的浮点数后面还会有 2 bits，分别称为 guard 和 round，其主要目的是让计算结果的舍入更加的精确： 

<center>![image.png](../../../assets/1654504509244-6c97c446-da50-48cb-b778-7217e04fa622.png){width=300}</center>

事实上加法只需要用到 guard，但是对于乘法，如果存在前导 0，需要将结果左移，这时候 round bit 就成了有效位，能避免精度的损失。

另外还有一个位叫 sticky bit，其定义是：只要 round 右边有非零位，就将 sticky 置 1，这一点可以用在加法的右移中，可以记住是否有 1 被移出，从而能够实现 "round to nearest even"。


# 4 Processor
我们讨论过，计算机的 performance 受 **inst#, clock cycle time 和 clock cycles per inst (CPI)** 决定。Clock cycle time 和 CPI 受 processor 的实现方式影响。本章介绍 RISC-V 的 processor 一种实现。


## 4.1 Datapath

### 4.1.1 Overview

<center>![image.png](../../../assets/1654671143448-cfbcadc6-ce0c-4723-bc9e-5c880f31fdac.png){width=300}</center>

上图展示了一个 RISC-V 核心指令的实现（并不完整），包括`ld`, `sd`, `add`, `sub`, `and`, `or`, `beq`。我们简单进行分析。

   - PC 寄存器存储当前运行到的指令的地址。**PC** 寄存器连到 **Instruction memory** 中，读出的结果就是当前要运行的指令。这个指令被 **Control** 解析产生相应的信号。我们在 4.1.6 小节中具体说明它的实现。


### 4.1.2 R 型指令

   - `add`, `sub`, `and`, `or`这几个 R 型指令总共需要访问 3 个寄存器，如下图所示：


<center>![image.png](../../../assets/1654672203572-171714de-bbd9-4da7-b2d6-024c1dd0b2f0.png){width=300}</center>


      - ① 处取出指令，`[6:0]`被送到 Control 产生对应的控制信号，我们稍后可以看到；`[19:15]`, `[24:20]`, `[11:7]`分别对应`rs1`,`rs2`,`rd`，被连入 Registers 这个结构，对应地`Read data 1`和`Read data 2`两处的值即变为`rs1`,`rs2`的值；
      - ② 处 MUX 在`ALUSrc = 0`的信号作用下选择`Read data 2`作为 ALU 的输入与`Read data 1`进行运算，具体的运算由`ALU control`提供的信号指明（我们在 **4.1.3 小节** 讨论这个话题）。运算结果在`ALU result`中。
      - ③ 处 MUX 在`MemtoReg = 0`的信号作用下选择`ALU result`作为写回 Register 的值，连到 ④ 处；在 ⑤ 处`RegWrite = 1`信号控制下，该值写入到`rd`寄存器中。

这就是 R 型指令的运行过程。执行完指令后 PC 会 +4，我们在 **4.1.4 小节** 讨论这一操作的实现。
	有聪明的小朋友可能会问，为什么需要`RegWrite`这个控制信号呢？非常简单，因为`Write register`和`Write data`这两条线始终是连着的，Reg files 需要知道什么时候需要写入寄存器，因此只有当`RegWrite = 1`时才会被对应地写入。
	聪明的小朋友可能又会问了，为什么`PC`寄存器也要写入，但是不需要控制信号呢？非常简单，因为`PC`在**每个**时钟周期都会被写入，所以只需要在时钟的**每个**上升沿或者下降沿触发就好了（我们采取的设计是下降沿触发，我们在 **4.2.3 小节** 再讨论为什么这样设计），不需要额外的控制信号了。



### 4.1.3 ALU Control
在 3.1 节中，我们设计的 ALU 需要这样的控制结构：

<center>![image.png](../../../assets/1654674035822-c566a50e-cde7-4244-880a-21bcc3b31699.png){width=300}</center>

我们列一下需要使用 ALU 的指令的表格（我们在）：

<center>![image.png](../../../assets/1654674059843-56287529-b9a6-4441-9933-2879581bf8f3.png){width=300}</center>

我们根据这个表列出真值表：

<center>![image.png](../../../assets/1654674304680-f7f2359b-bd75-47d9-b19c-d53550653ed9.png){width=300}</center>

其中可以发现，标为绿色的列的取值要么是 0 要么是无关的，因此它们并不影响结果。

根据这个真值表构造门电路，就可以构造出 ALU control 单元了。如图中所示，该单元依赖 Control 单元给出的`ALUOp`信号以及`I[30, 14:2]`：

<center>![image.png](../../../assets/1654674211472-df83a1c1-1776-4a5a-a662-cf7c81edfead.png){width=300}</center>

	ALU control 模块可以这样实现：
	
<center>![image.png](../../../assets/1654680132424-1501096b-1795-4e84-aa15-31b81cdbe7bd.png){width=300}</center>

	需要理解的是，我们并不是根据机器码来构造电路的，而是相反：电路的设计参考了很多方面的问题，机器码应当主要迎合电路使其设计更加方便。



### 4.1.4 跳转指令与 Imm Gen 模块

   - 在一条指令运行完后，如果不发生跳转，PC + 4，否则 PC 跳转到 PC + offset 的位置去。这个过程是如何完成的呢？看下图：


<center>![image.png](../../../assets/1654671880110-a3a3e4f1-ba35-4a91-810e-895996d1025c.png){width=300}</center>


      - ① 中有两个加法器，一个的结果是 PC + 4，另一个是 PC + offset，其中 offset 是来自当前 instruction 的；这两个加法器通过 MUX 送给 PC
      - MUX 的控制信号来自 ②，② 是一个与门，即当且仅当两个输入信号都为真时才会输出 1，从而在上述 MUX 中选择跳转。② 的两个输入分别来自：
         - ⑤ 这个 ALU 的 Zero 信号，这是第 3 章中我们设计的可以用来实现`beq`的结构；我们讨论过实现`beq`其实就是计算`rs1 - rs2`判断其是否为 0，所以这里根据 Zero 是否为 0 就能判断两个寄存器是否相等
         - ④ 处 Control 给出的`Branch`信号，即如果这个语句是跳转语句，那么对应的信号会置为 1

也就是说，当且仅当语句确实是`beq`而且`Zero`信号的值确实为 1 时才会进行跳转。

      - 再来看看当进行跳转的时候，③ 处的 offset 来自哪里。我们可以看到，实际上这个 offset 来自于`I[31:0]`，也就是整个指令；它被传给 **Imm Gen 模块**，将指令中的立即数符号扩展到 64 位；然后在 ③ 处左移 1 位（请回顾，因为 RISC-V 指令总是 2 字节对齐 [我们学的都是 4 字节对齐]，所以我们没有保存偏移的最低一位）再与 PC 相加。
	**Imm Gen 模块**
	这个模块识别`load`类指令、`store`类指令和`branch`类指令的立即数模式并将其 **符号扩展** 到 64 位，根据`I[5:6]`的不同取值区分这三种情况，构造一个 3:1 MUX 选择实际的立即数，将其传给后面的使用。



### 4.1.5 Load 指令和 Store 指令
懒得写了，可以自己理解一下。

用文化人的话来说，Load 指令和 Store 指令的数据通路操作留作习题。


### 4.1.6 Control
看完上述若干小节，control 单元的设计也非常显然了。我们很容易给出如下真值表：

<center>![image.png](../../../assets/1654681433205-5ed6293c-b44b-49c5-90de-ae0d3d93cac7.png){width=300}</center>

后面就是连电路的工作了。
	连出来长这样：
	
<center>![image.png](../../../assets/1654681479004-e8c104d3-390b-4210-a4ee-1495f73f9970.png){width=300}</center>




### 4.1.7 Why a Single-Cycle Implementation is not Used Today
单周期的实现是指，一个指令的所有工作都在一个时钟周期内完成，也就是 CPI = 1。那么，一个时钟周期的长度就要足够最长的那个指令完成运行。但是，例如`load`类的指令要经过 inst mem, reg file, ALU, data mem, reg file 这么多的步骤，这会使得时钟周期变得很长，导致整体性能变得很差。单周期的实现违反了 **common case fast** 这一设计原则。

因此，我们引入一种新的实现技术，叫 **流水线 (Pipeline)**。


## 4.2 Pipeline

### 4.2.1 Intro
在小学奥数中我们就学过，并行能够提高整体的效率，例如这个洗衣服的例子：

<center>![image.png](../../../assets/1654740094086-8364d8a3-4cec-4e6f-837e-fa717447c1db.png){width=300}</center>

对于单个工作，流水线技术并没有缩短其运行时间；但是由于多个工作可以并行地执行，流水线技术可以更好地压榨资源，使得它们被同时而不是轮流使用，在工作比较多的时候可以增加整体的 **吞吐率 throughput**，从而减少了完成整个任务的时间。

在本例中，由于流水线开始和结束的时候并没有完全充满，因此吞吐率不及原来的 4 倍；但是当工作数足够多的时候，吞吐率就几乎是原来的 4 倍了。

回到 RISC-V 中来，一个指令通常包含 5 个阶段：

1. **IF, Inst Fetch**，从内存中获取指令
2. **ID, Inst Decode**，读取寄存器、指令译码
3. **EX, Execute**，计算操作结果和/或地址
4. **MEM, Memory**，内存存取（如果需要的话）
5. **WB, Write Back**，将结果写回寄存器（如果需要的话）

各阶段会用到的组件如下图所示（这个图还有很多问题，我们后面慢慢讨论~），可以看到这些部分是可以并行执行的（比如 Reg File 可以一边读一边写）：

<center>![image.png](../../../assets/1654741944095-f2787d5f-e997-4ada-afda-38ef9bc5057e.png){width=300}</center>

也就是说，我们本来是在一个周期中完成一个指令，而现在是在一个周期中完成一个阶段。所以，每个时钟周期的长度也需要足够任何一个阶段完成执行。

RISC-V 也有很多流水线友好的设计，例如：

   - 所有 RISC-V 的指令长度相同，这可以方便`IF`和`ID`的工作
   - RISC-V 的指令格式比较少，而且源寄存器、目标寄存器的位置相同
   - 只在 load 或 store 指令中操作 data memory 而不会将存取的结果做进一步运算，这样就可以将`MEM`放在比较后面的位置；如果还能对结果做运算则还需要一个额外的阶段，流水线较长是不好的


### 4.2.2 Datapath
但是，聪明的小朋友也可以看出一些问题！比如，前一个指令在`ID`阶段的时候，会使用到其在`IF`阶段读出的指令的内容；但与此同时后一个指令已经运行到`IF`阶段并读出了新的指令，那么前一个指令就没的用了！这个现象在很多地方普遍存在，包括 Control 信号的传递，因此我们实际上会在每两个 stage 之间用一些寄存器保存这些内容：

<center>![image.png](../../../assets/1655061248536-62d39071-e009-424a-ab6f-4bddbdbe144f.png){width=300}</center>

可以看到，上面这个图除了加了一些竖条条以外和之前没有流水线的时候几乎没什么差别。这些竖条条就是 pipeline registers，例如`IF/ID`就是`IF`和`ID`阶段之间的一些寄存器。
	聪明的小朋友可能会回忆起我们在 **4.1.2 小节** 中提到的，由于 PC 每个时钟周期都会被写入，所以不需要像 Reg files 和 Data mem 那样需要额外的控制信号`RegWrite`和`MemWrite`来控制写入，只需要在每个下降沿写入就好。Pipeline registers 也是这样，它们每个时钟周期都会被写入一次，所以也不需要额外的信号，也是在每个下降沿写入就好。
	我们之前并没有讨论为什么要在下降沿写入，本节下一个橙色框框就会说明啦！


我们关注 datapath 中两个从右往左传东西的情况！一个是`WB`阶段写回数据，一个是`MEM`阶段判断是否发生跳转。分别关注对应增加的 datapath：

<center>![image.png](../../../assets/1654757278833-5e408879-9e7d-4e6d-80f0-0ff4a20f7c35.png){width=300}</center>

对于`WB`来说，我们写会时需要记录写到哪个 register 中，这个信息是`ID`阶段从 Instruction 中`[11:7]`的位置取出的，但是直到`WB`阶段才被用到，因此这个信息被存到了`ID/EX`，下一个周期存到了`EX/MEM`，下一个周期存到了`MEM/WB`，然后下一个周期被使用。

`MEM`判断是否发生跳转的逻辑类似，略。


### 4.2.3 Data Hazards
但是，聪明的小朋友仍然可以看出一些问题！考虑这样的指令序列：

<center>![image.png](../../../assets/1654795731132-5ba12d3f-c143-43d5-9114-3c22725c4abf.png){width=300}</center>

用简化的数据通路查看一下各指令各 stage 的执行时间：

<center>![image.png](../../../assets/1654795975014-57ed0190-026f-4d9d-84eb-8a3f6fa3d26d.png){width=300}</center>

我们简单介绍一下这张图。最上面是横轴，也就是时间轴，CC 代表 Clock Cycle；下面的 10, -20 这种数据是`x2`寄存器的值；接下来的每一行都是一个语句的执行过程，`IM`就是 inst mem，对应`IF`stage；`Reg`就是 reg file，对应`ID`stage；长得像 ALU 的就是 ALU，对应`EX`stage；`DM`就是 data mem，对应`MEM`stage；最后面的`Reg`也是 reg file，对应`WB`stage。每个 stage 占用一个时钟周期。

图中深色（灰色、蓝色）的部分就是对应指令会使用到的组件，其中 mem 和 reg file 用左半边为深色表示 **写入**，右半边为深色表示 **读取**。我们稍后解释这样表示的原因。

可以看到，当第一条语句`sub x2, x1, x3`运行到第 5 个时钟周期时，计算结果才被写回`x2`（如绿色框框所示），但是在第 3 个周期时第二条语句`and x12, x2, x5`就运行到`ID`阶段，需要用到`x2`的值（如橙色框框所示）。如果这时候不加处理，第二条语句读到的值就是错误的！这一问题同时会发生在第 3 条指令那里，它在第 4 个时钟周期需要用到`x2`的值，但是这时候`x2`的值仍未被更新。

也就是说，由于指令所需的数据依赖于前面一条尚未完成的指令，因此指令不能在预期的时钟周期内执行，这种情况我们称之为 **data hazard**。
	在第 5 个时钟周期内，关于 Reg files 我们需要完成 2 件事：`sub x2, x1, x3`的`WB`阶段将`x2`的新值写入 Reg files，以及`add x14, x2, x2`的`ID`阶段将`x2`的值读出来并且存到`ID/EX`寄存器中。这两个事情有没有可能正确执行呢？答案是有的！
	众所周知，时钟信号有上升沿和下降沿，我们既可以规定一个时钟周期由一个上升沿开始到另一个上升沿结束，也可以规定一个时钟周期从一个下降沿开始到另一个下降沿结束：
	
<center>![image.png](../../../assets/1654798942770-f1bffcc8-2e09-4472-92a3-19d5438c106c.png){width=300}</center>

	在课本的设计中，我们采取前者，也就是一个时钟周期就是相邻两次上升沿之间的时间段。
	而寄存器的写入可以由上升沿触发，也可以由下降沿触发。如果我们规定 Reg files 中的寄存器在上升沿触发写入，也就是在前半个周期中完成写入 Reg files 寄存器的工作；而规定 Pipeline registers 在下降沿触发写入，也就是在后半个周期完成写入工作，那么，在第 5 个时钟周期的上半，`x2`的新值被写入；下半读出`x2`并写入`ID/EX`的值就是`x2`的新值了。所以说，这样的设计使得这种情况下不会出现 data hazard。
	
	这也就能解释为什么`PC`要在下降沿写入了，看 datapath 的这一部分：
	
<center>![image.png](../../../assets/1654800274740-6ee9e8eb-af7d-4d26-874f-ce82ba6bee7e.png){width=300}</center>

	如果`PC`在上升沿写入，也就是在上升沿更新到下一条指令的位置，那么在下降沿要将当前指令写入`IF/ID`的时候，从 inst mem 中读出的指令已经是下一条而不是当前指令了！所以我们必须让`PC`在下降沿写入，这样才能读取到正确的指令。
	
	**也就是说，Reg files 的写入均发生在上半周期，也就是上升沿；而 Pipeline registers 和**`**PC**`**的写入均发生在下半周期，也就是下降沿。**
	这也是图例中 reg file 用左半边为深色表示写入，右半边为深色表示读取的原因：写入发生在上半个周期，而使用读取的结果发生在下半个周期。


那么，如何解决 data hazard 呢？回顾刚刚的那张图：

<center>![image.png](../../../assets/1654795975014-57ed0190-026f-4d9d-84eb-8a3f6fa3d26d.png){width=300}</center>

我们注意到，虽然`sub x2, x1, x3`在第 5 个时钟周期的`WB`阶段才将结果写回，但是在第 3 个时钟周期的`EX`阶段其实就算出来了！所以我们可以增加额外的硬件结构，使得 ALU 的输入不仅可以来源于寄存器中读出来的、放在`ID/EX`中的值，还可以来源于`EX/MEM`中或者`MEM/WB`中的值，它们分别对应前一条和再前一条指令的 ALU 的计算结果。如下图所示： 

<center>![image.png](../../../assets/1654861103791-a16d1edb-9e66-46ed-849a-c292bba99b03.png){width=300}</center>

在第 3 个时钟周期，第一条指令的结果被算出并保存在`EX/MEM`

学不完了，暂时不详细写了，大意就是 `X = 1, 2 =	if (MEM.Rd != x0 && EX.RsX == MEM.Rd) ForwardX = 10; else if (WB.Rd != x0 && EX.RsX == WB.Rd) ForwardX = 01; else ForwardX = 00;`：

<center>![image.png](../../../assets/1655054499226-ac885ac8-6b68-4191-ad18-776f62a0b762.png){width=300}</center>


但是遇到 load 指令不得不 stall：

<center>![image.png](../../../assets/1655054689394-a8283431-11f7-49fa-8bd4-96d9fbae73a5.png){width=300}</center>


<center>![image.png](../../../assets/1655054716560-ae2d14e7-454d-45d2-857c-4aa1b93107be.png){width=300}</center>

在 ID 阶段可以判定 hazard：`if (EX.MemRead && EX.Rd == ID.RsX) Hazard();`

如何 stall 呢？两个任务：让当前指令不要产生效果 (清空`RegWrite`和`MemWrite`)、让后面的语句不要受到影响 (保留`PC`和`IF/ID`一周期不改)：

<center>![image.png](../../../assets/1655054837667-510c675d-617c-4ce5-bab1-7ff5bc4ade30.png){width=300}</center>



### 4.2.4 Control Hazards / Branch Hazards


	【例题】下面一段代码在不考虑解决 hazard 的情况下的运行结果是什么？假设所有寄存器初始值为 0，Mem(1) = 0x99, Mem(8) = 0xaa, Mem(9) = 0xbb。
	
<center>![{E948E6BF-5169-F815-4D0F-041670E8B363}.png](../../../assets/1654444304614-a4aa93e1-af21-4393-be24-c942fc624e0c.png){width=300}</center>

	我们可以模拟每条指令各阶段的执行情况：
	
<center>![GWYC$Z9(5Y{EUQG$Z2QA2W6.png](../../../assets/1654444145762-06b778ee-17cb-409d-a9c8-88e0a9329674.png){width=300}</center>

	从中我们也可以总结出规律（这和流水线的具体设计有关！），即：
	   - 某条指令 (例如 #10)`WB`阶段做的寄存器更改，其之后第三条指令 (#13) 的`ID`阶段才能读出新的值；
	   - 某条指令 (例如 #10)`MEM`阶段产生`PCSrc = 1`的信号，此时其之后第三条指令 (#13) 正在运行`IF`阶段，它运行结束后才会将`PC`置为实际上要跳转的指令，因此如果要跳转的话，#11, #12, #13 这三条语句是额外运行的；如果不用跳转就什么事都没有了；
	   - 不存在其他影响结果的情况了！
	
	利用这些规律，我们可以简化我们的解题方式：
	
	Reg: 到哪一次执行的 ID 阶段开始，读出的 Reg 值会是该值
	PC: 到哪一次执行 **之后**，PC 的值会被改为该值
	
<center>![PH3G}NGLYL@KV}D[S8{_%$2.png](../../../assets/1654444212530-325281ab-e86e-4ce4-a4a2-dbd4f451ba04.png){width=300}</center>




### 4.2.5 Structural Hazard


## 4.3 Exceptions
Exception 和 Interrupt 在很多地方是不作区分的，但是我们做一个简单的区分：

<center>![image.png](../../../assets/1654930011877-7a77a135-36e1-4ccc-8822-49a704cc0d95.png){width=300}</center>

当 exception 发生时，在 **Supervisor Exception Program Counter, SEPC** 这个寄存器中保存发生 exception 的指令地址，然后将控制权交给操作系统。操作系统还必须知道发生 exception 的原因，RISC-V 中使用的方法是在 **Supervisor Exception Cause Register, SCAUSE** 这个寄存器中记录 exception 的原因。可以选择的另一种方法是 **vectored interrupt**，


# 5 Cache

## 5.1 Memory Hierarchy Introduction
众所周知，指令和数据都需要在 memory 里才能访问。而访问 memory 比较慢。

关注到程序对 memory 的访问有如下特点：

   - **Temporal locality**, 时间局部性，即近期访问的项目很有可能会在短时间内再次被访问。例如循环中的指令、induction variables (循环中用来计数的变量) 等
   - **Spatial locality**, 空间局部性，即近期访问项目附近的项目也有可能会在短时间内再次被访问。例如连续的指令执行，或者数组变量等

因此，结构化的 memory 被设计出来。近期访问到的内存单元和它附近的内容被复制一份放在离 CPU 更近、访问更快，但也更小的 **cache **中，从而利用上述局部性加速访问。


<center>![image.png](../../../assets/1652692160527-7606f530-5481-4d42-8ed2-c4df690c9bf4.png){width=300}</center>


我们称复制的单位是 **block **或者 **line**，它通常是 2 的若干次方个 word 那么大（一个 word 是 4 Byte）。

如果我们希望访问的内存单元 (即，它所在的 block) 恰好在 cache 中（之前某一次被搬上来了），我们称之为一次 **hit**，这时我们只需要从中读出来就可以了。判断是否 hit，以及读出来的时间称为 **hit time**。

如果并不存在，称为一次 **miss**。当 cache miss 时，我们需要先将内容所在的 block 从 memory 拿到 cache，然后再将内容读到处理器；这个过程花的时间成为 **miss penalty**。

对应的有 hit / miss rate (也称 ratio) 的概念，不再赘述。


## 5.2 The basics of Cache
下面我们来具体考虑 cache 怎么实现。主要需要讨论的问题是：如何知道一个 block 是否在 cache 里？以及如果知道它在的话，如何找到它？


### 5.3.1 Direct Mapped Cache

<center>![image.png](../../../assets/1652692837568-a910a2a5-d2ff-4251-8dfb-447508ca670c.png){width=300}</center>

如上图所示，内存有 32 个 block，其编号 (block address) 分别为 00000 到 11111；cache 有 8 个 block。Direct mapped cache 这种方式直接按 block address 的后 3 位确定它应该放在 cache 的哪个 block 里。

即，图上灰色的 block 的编号末 3 位都是 001，所以就应该放在 cache 中编号为 001 的灰色 block 里；橙色同理。

为什么是三位呢？很简单，因为 cache 有 8 个 block 的话，其对应的就是 3 位二进制数。我们把这个决定映射关系的末几位称为 **index**。同理，如果 cache 有 64 个 block 的话，index 就是 6 位。Cache 的 block 数始终是 2 的幂次方。

那么我们如何确定放在 cache 中编号为 001 的位置的 block 究竟是 00001，还是 01001，还是其他的哪个 block 呢？我们可以通过在 cache 中额外存放这个 block 的 block address 来知道这个问题。

当然，实际上我们只需要存放这个 block address 的前若干位，因为后面的几位已经通过 index 来确定了。例如图上的例子中，10001 存在 index 为 001 的 cache block 中，只需要额外存开头的 10 即可。我们把用来判定某个 cache block 中到底存的是哪个 memory block 的这几位称为 **tag**。

下一个问题是，如何确定 cache 中的这个 block 是否有效呢？也就是说，任何时候这个 block 中总有一个值，但是假设这个值是启动的时候自带的，那么访问它就会发生错误，因为它实际上并不是对应的 memory block 的值。因此，我们引入一个 **valid bit** 来表示这个 block 是否有效；初始值为 0 表示无效，当有一次将 memory 的一个 block 拿进来之后就将其置为 1。

也就是说，cache hit 当且仅当 valid bit 是 1 而且 tag 是一致的。

我们在内存中的地址都是以字节为单位的，而上面我们讨论的 block address 都是以 block 为单位的，这两者之间有什么样的关系呢？非常简单，由于一个 block 总是 2 的若干次方个 word 那么大， 而每个 word 是 4 Byte，因此每个 block 的 byte 数也是 2 的若干次方。因此，我们只需要去掉 byte address 的后几位，就可以获得它的 block address 了。这样相邻的 2 的若干次方个 byte 就会聚合成一个 block 了，因为它们的 byte address 的前若干位，即 block address，是相同的。

也就是说，我们将 byte address 分为 2 个部分：block address 和 byte offset，即所在 block 的编号以及在 block 中的偏移量 (in byte)；而 block address 又分为了两个部分，即 tag 和 index。即：

<center>![image.png](../../../assets/1652751935229-d2221dfa-a158-4842-9cb6-7bcb51479bec.png){width=300}</center>

而在 cache 中，我们存储以下信息：

<center>![image.png](../../../assets/1652752079856-f08cb589-5068-4524-90b6-23c7a3f1b7df.png){width=300}</center>

即，每个 cache block 有一个 index，当出现一次 miss 后从内存中拿所需内存覆盖到对应的 index 条目上的 data 字段，将 tag 设为 block address 的前几位，将 valid bit 设为 1。

	【例 5.1 Direct Mapped Cache 的填充和替换】
	下面是一个具体的例子：
	
<center>![image.png](../../../assets/1652752776370-d0133a42-a292-4d62-b055-001d5d601a10.png){width=300}</center>



	【例 5.2 Direct Mapped Cache 的位数计算和连线方式】
	又例如，对于一个 64 位地址的机器，cache 的大小为 1024 个 block，一个 block 有 1 个 word，即 4 个 byte，那么 index 的位数就是 
<center>![](https://cdn.nlark.com/yuque/__latex/9e055dd0da22be9da3f64f9c1bd824de.svg#card=math&code=%5Clog_21024%20%3D%2010&id=RBCy2)，byte offset 的位数就是 ![](https://cdn.nlark.com/yuque/__latex/bc7b0dd0635fc1689b53f2b5699db296.svg#card=math&code=%5Clog_24%20%3D%202&id=LnZHm)，因此 tag 的位数就是 ![](https://cdn.nlark.com/yuque/__latex/e35622a5edf06b4ad5edc63974574b2b.svg#card=math&code=64%20-%2010%20-%202%20%3D%2052&id=d1SA6){width=300}</center>
；另外一个 block 的大小是 4 个 byte，即 32 位，因此一个 cache 的条目的位数就是 valid bit 1 位 + tag 52 位 + word 32 位 = 85 位。
	（index 并不需要在这里被计算，因为 index 之于 cache 就像 address 之于 main memory 一样，是直接用来访问的）
	亦即：
	
<center>![image.png](../../../assets/1652752904223-cd18cbdd-7d9b-45f6-9dfc-4543a5951094.png){width=300}</center>

	
	当然，如我们之前所说，一个 block 有可能包含多个 word，而每次实际上只会访问出一个 word。因此这时我们还需要在 block 中选择对应的 word，这时候我们就可以将 byte offset 进一步细分成表示 block 中某个 word 的 **block offset**（为什么不叫 word offset 呢？），以及表示 word 中某个 byte 的 **byte offset**：
	
<center>![image.png](../../../assets/1652765206172-56e8e84c-5e9c-41d4-ae02-6a0dfca2399c.png){width=300}</center>

	即，对这个图中的情形，地址是 32 位的，一个 block 有 16 个 word，有 256 个 cache entry。因此 byte offset 的位数是 
<center>![](https://cdn.nlark.com/yuque/__latex/bc7b0dd0635fc1689b53f2b5699db296.svg#card=math&code=%5Clog_24%20%3D%202&id=gycRb)，block offset 的位数是 ![](https://cdn.nlark.com/yuque/__latex/aafdf86095953918721470286d9222c1.svg#card=math&code=%5Clog_2%2016%20%3D%204&id=cgays)，index 的位数是 ![](https://cdn.nlark.com/yuque/__latex/be92705c19c0a298c366c67b77fdbb5e.svg#card=math&code=%5Clog_2256%20%3D%208&id=fpQUG)，tag 的位数是 ![](https://cdn.nlark.com/yuque/__latex/15aa6b2210cd5a14338126f3770e7807.svg#card=math&code=32%20-%208%20-%204%20-%202%20%3D%2018&id=lj8NJ){width=300}</center>
，一个 cache entry 的长度是 valid bit 1 位 + tag 18 位 + data 16 word * 4 byte/word * 8 bit/byte = 531 位。



	【例 5.3 Direct Mapped Cache 的位数计算】
	再例如：
	
<center>![image.png](../../../assets/1652753397820-7f30a36f-aab7-41b1-bbbf-89c151253a49.png){width=300}</center>




### 5.3.2 Handling Cache Hits & Misses
显然，读和写的时候发生 cache miss 的处理方式是不一样的；另外读也有读数据和读指令之分（指令 cache 和数据 cache 通常是分离的）。我们分别对其进行讨论：

- **Read**
   - **Hit**
      - 直接从 cache 里读就好了
   - **Miss**
      - **Data cache miss**
         - 从 memory 里把对应的 block 拿到 cache，然后读取对应的内容。
      - **Instruction cache miss**
         - 暂停 CPU 运行，从 memory 里把对应的 block 拿到 cache，从第一个 step 开始重新运行当前这条指令。
- **Write**
   - **Hit**
      - 有两种可以选的方式：
      - **write-through**，即每次写数据时，既写在 cache，也写在 main memory。这样的好处是 cache 和 main memory 总是一致的，但是这样很慢。
         - 一个改进是引入一个 **write buffer**，即当需要写 main memory 的时候不是立即去写，而是加入到这个队列中，找机会写进去；此时 CPU 就可以继续运行了。当然，当 write buffer 满了的时候，也需要暂停处理器来做写入 main memory 的工作，直到 buffer 中有空闲的 entry。因此，如果 main memory 的写入速率低于 CPU 产生写操作的速率，多大的缓冲都无济于事。
      - **write-back**，只将修改的内容写在 cache 里，等到这个 block 要被覆盖掉的时候将其写回内存。这种情况需要一个额外的 **dirty bit** 来记录这个 cache block 是否被更改过，从而直到被覆盖前是否需要被写回内存。由于对同一个 block 通常会有多次写入，因此这种方式消耗的总带宽是更小的。
   - **Miss**
      - 同样有两种方式：
      - **write allocate**，即像 read miss 一样先把 block 拿到 cache 里再写入。
      - **write around **(or** no write allocate**)，考虑到既然本来就要去一次 main memory，不如直接在里面写了，就不再拿到 cache 里了。
      - write-back 只能使用 write allocate；一般来说，write-through 使用 write around，其原因是明显的。


### 5.3.3 其他定位方式
在 5.3.1 中，我们讨论了最简单的映射方式，即直接映射：对于任一给定的 block address，有且仅有一个 cache block 可供它存放。实际上，还有一些其他的映射方式。

**Fully associative**，简单来说就是 block can go anywhere in cache。这种方式的好处是可以降低 miss rate，坏处是每次需要跟所有 block 比较是否 hit：

<center>![image.png](../../../assets/1652756194622-6e4626af-f977-45b0-86dc-7cbfcef52bfd.png){width=300}</center>

这种情况下，我们需要额外讨论替换时采用什么样的策略；即：替换哪一块。通常有三种策略：

   - **Random replacement**，随机挑选一个幸运 block 覆盖掉（需要一个随机数生成器）
   - **LRU, Least Recently Used**，选择上一次使用时间距离现在最远的那个 block 覆盖掉（需要一些额外的位用来记录信息，具体实现没有讲）
   - **FIFO, First In First Out**，选择进入时间最早的 block 覆盖掉（同样需要一些额外的位记录信息，同样没讲具体实现）

介于 direct mapping 和 fully associative 之间的是 set associative，即每个 block 仍然会根据其 address 确定其可以存放的 cache block，但是可以放的地方并不是一个，而是一组。即：

<center>![image.png](../../../assets/1652756607490-1017df1c-5566-4e2a-a28b-116f0e333638.png){width=300}</center>

最右边是一个 2-way set-associative 的例子，每个地址对应 cache 中的一组，在这里一组有两个 cache block。因此在访问时也需要分别比较这两个 block 是否 hit。在替换时也需要决定替换哪一块，也可以使用前述的三个策略中的一个实现。

相似地，一个 4-way set-associative 的访问中判断 hit 和获取 data 的连线如下：

<center>![image.png](../../../assets/1652757530348-328003df-17fe-47b0-826f-7c7f283d4811.png){width=300}</center>


所以，事实上，direct mapping 和 fully associative 其实都是 set associative 的特例：direct mapping 其实就是 1-way set associative，而 fully associative 就是 n-way set associative，其中 n 是 cache block 的个数；我们称一组的大小为 **associativity**，那么这两种方法的 associativity 就分别是 1 和 n。

显然，在查看所需 block 是否在 cache 中时，需要访问的 cache block 个数就等于 associativity，即：

<center>![image.png](../../../assets/1652757375415-3eaa40f0-fcf9-4005-a401-8892a22d6867.png){width=300}</center>


	【例 5.4 Set associative 的位数计算】
	已知 Cache size is 4K Block, Block size is 4 words, Physical address is 32bits，求 direct-mapped, 2-way associative, 4-way associative, fully associative 时 tag 和 index 的位数。
	
	即求 associativity 为 1, 2, 4 和 4096 时 tag 和 index 的位数。
	
	我们知道，在 direct-mapped 中 index 是用来确定 memory block 放在哪个 cache block 中的，那么在 set-associative 中，index 就是用来确定放在哪个 set 中的。因此，index 的位数就对应着 set 的个数，即：
	
<center>![](https://cdn.nlark.com/yuque/__latex/f43ec0e2ab99f08d92a0d80967e86fc3.svg#card=math&code=%5Ctext%7Bindex%7D_%5C%23%20%3D%20%5Clog_2%28%5Ctext%7Bset%7D_%5C%23%29%20%3D%20%5Clog_2%5Cfrac%7B%5Ctext%7Bcache%20block%7D_%5C%23%7D%7B%5Ctext%7Bassociativity%7D%7D&id=PSRyl){width=300}</center>

	因此 associativity 为 1, 2, 4, 4096 时，index 的位数分别是 12, 11, 10, 0。
	
	由于 block size 为 4 words，即 16 Bytes，因此 byte offset 需要 4 位（或者，具体地说，block offset 2 位，byte offset 2 位）。所以剩下的都是 tag 了，因此 tag 的位数分别是 16, 17, 18, 28。



	【18 - 19 Final】
	
<center>![image.png](../../../assets/1655057793599-cf6a859a-8c2d-4ebc-8e7a-97569ae0fa53.png){width=300}</center>

	
<center>![image.png](../../../assets/1655057800314-657b2aba-4f32-41f4-829a-507806fc4afd.png){width=300}</center>

	答案：
	
<center>![image.png](../../../assets/1655057824454-acd8b498-375e-461d-9c9e-1225e8dae46b.png){width=300}</center>



## 5.3 Measuring Cache Performance
再说吧


## 5.4 Virtual Machines
先不学了


## 5.5 Virtual Memory

### 5.5.1 虚拟内存技术
计组把 main memory 描述为 secondary storage (即 disk) 的 "cache"。或者，反过来说，我们把那些在 main memory 里放不下的内容存到 disk 里（这样更能符合我们熟悉的“可执行文件必须加载到内存才能运行”的一贯认知）。这种技术称为 **virtual memory**。

虚拟内存技术可以让多个程序之间高效、安全地共享内存，同时允许单个程序使用超过内存容量的内存（正如虽然 CPU 取数据时是从 cache 中取的，但是它能访问到的数据的数目比 cache 的容量要大）。在远古时期，很多程序因为需要使用过大的内存而无法被运行；但现在由于虚拟内存技术的广泛使用，这些程序都不成问题了。

如下图所示，实际上的 main memory（我们称之为 **物理内存, physical memory**）中的地址称为 **物理地址, physical addresses**；而我们给每一个程序内部使用到的内存另外编一套地址，称为 **虚拟地址, virtual addresses**；虚拟内存技术负责了这两个地址之间的转换 (**address translation**，我们稍后再讨论转换的方式)：


<center>![image.png](../../../assets/1653214940649-4eef3e3d-058d-4c77-b2e5-82a20bf1ed46.png){width=300}</center>

从这张图中我们也可以很容易地看出“虚拟内存技术可以允许单个程序访问超过物理内存大小限制的内存”的原因，即有一些内存可以被临时地存放在磁盘上，到被访问的时候再被放到 physical memory 中，就像 cache 做的那样。

从这张图中，我们还可以注意到 physical memory 的存放并没有分组的概念，即用 cache 的术语来说，main memory 是 fully-associative 的。

虚拟存储的技术和 cache 的原理是一样的，但是一些术语的名字并不相同。对应于 cache 中的 block / line，虚拟存储的内存单元称为 **page**，当我们要访问的 page 不在主存中而是在磁盘里，也就是 miss，我们称之为一次 **page fault**。
	（以下内容并不重要：）
	在一些地方，virtual page 称为 page，physical page 称为 **帧, frame**；我们的课本并未采用这种称呼。但无论如何，在看到单独出现的 _page_ 时，应当参考上下文判断它是 virtual 还是 physical。
	在一些地方，virtual address 也被称为 logical address。



### 5.5.2 如何完成映射呢
首先我们要考虑的一个问题就是，一个 page 应该有多大。我们知道，访问磁盘相比于访问内存是非常慢的（相差大约十万倍），这个主要时延来自于磁盘转到正确的位置上的时间花费；所以我们希望一次读进来多一点从而来分摊这个访问时间。典型的 page 大小从 4KiB ~ 64KiB 不等。

下面我们考虑映射关系。我们不妨假设一个 page 的大小是 4KiB，那么其页内的偏移 **page offset** 就需要 12 位来表示；那么物理地址中除去后 12 位以外前面的部分就表征着它是属于哪一页的，我们称之为 **physical page number**。
	（以下内容并不重要：）
	如我们之前所说，memory 作为 disk 的 "cache" 是 fully-associative 的，因此 physical page number 其实就是 cache 中的 "tag"，而 page offset 就是 cache 中的 "byte offset"，fully-associative 的 cache 并没有 index 这一字段。


<center>![image.png](../../../assets/1653273502100-3bc83b47-f1e3-45c6-93a2-d96a1b080554.png){width=300}</center>

为什么要使用 fully-associative 的存储方式呢？我们在 cache 中讨论过，这种方式的好处是失效率低，坏处是查询难度大。但是我们也讨论到了，page fault 的开销是非常大的，因此比较低的 page fault 的概率相对于额外的查询来说是非常划算的。

同样，由于读写磁盘是非常慢的，write through 的策略并不合适，因此在 virtual memory 的技术中，我们采取 write back 的方式。

而 virtual address 的形式与之类似，由若干位 page number 和若干位 page offset 组成。

我们之前提到，我们有一种方式可以找到 virtual page 对应的 physical page，因此当我们要访问一个虚拟地址时，将其 virtual page number 通过这种 translation 转换为 physical page number（这种 translation 也会负责 page fault 的处理并给出正确的转换），而 page offset 表示的是在一页内的偏移，保持不变即可。这样我们就获得了这个 virtual address 对应的 physical address，也就是它在实际的 main memory 中存储的位置。如下图所示：

<center>![image.png](../../../assets/1653274122638-cbffd0c2-1397-4a3a-83a8-67c57004505b.png){width=300}</center>

同时也可以看出，virtual page number 的位数比 physical 的多；这也是显然的，因为我们引入虚拟内存的一个重要原因就是为了使用比 main memory 更大的内存。
	（以下内容并不重要：）
	如果我们把 translation 看成一个函数（事实上，我们之后可以看到，这种 translation 确实符合函数的定义），那么事实上 virtual page number 到 physical page number 的转换是 direct mapped 的，因为我们从一个 virtual page number 可以确切地找到**一个** physical page number，而不是在一组中再去寻找。因此，virtual page number 实际上对应了 cache 中的 "index"，tag 并不需要。
	所以说，我们认为 virtual address 之于 physical address 是 direct mapped 的，virtual page number 对应 cache 中的 index，page offset 对应 byte offset；而 physical address 之于 secondary storage 是 fully associative 的，physical page number 对应 cache 中的 tag，page offset 对应 byte offset。
	
	（但是实际上，我个人并不认同把 virtual memory 和 cache 类比起来。）



### 5.5.3 页表
我们下面讨论这种 translation 的具体方案。之前也提到，fully-associative 的一个重要问题就是如何去定位某一项；这里我们引入 **page table** 这种结构，它被存放在 main memory 中，每个程序（实际上是进程，但是写课本的人好像现在并不想引入这个概念）都有一个自己的 page table；同时硬件上有一个 **page table register** 保存当前进程这个页表的地址。

使用页表时，我们根据 virtual page number 找到对应 **page table entry, PTE** 在 page table 中的偏移，然后与 page table register 相加得到对应 entry 的 physical address，从中读取对应的 entry。其实就是说，page table 就是一个数组，`page_table[i]`表示第`i`个 virtual page 对应的 physical page number。

如下图所示，每个 entry 中包含了一个 valid bit 和 physical page number。如果 valid bit = 1，那么转换完成；否则触发了 page fault，handle 之后再进行转换。

<center>![image.png](../../../assets/1653274939462-abfe7f29-a821-469c-b76c-df2efb82a791.png){width=300}</center>

Page fault 会引发一个 exception，由操作系统接管控制，处理完之后再将控制交还给进程。操作系统要做的事情是在 secondary storage 中找到这一 page，将其放到 main memory 里（可能需要与当前主存中的某个 page 交换），然后更新 page table。

操作系统在创建进程时在 disk (或者 flash memory) 上创建一个虚拟地址空间那么大的空间，以便上述的交换；这个空间称为 **交换区, swap space**。下面的问题是操作系统如何在 swap space 中找到需要的 page。

我们可以看到，如果 page table entry 的 valid bit 为 0，那么后面的 physical page number 是没有用到的。我们可以利用这个字段存储对应 page 被交换到了 disk 的哪个位置；或者另外开辟一个索引结构，在其中记录每个 virtual page number 对应的 disk 位置。作为前者的一个例子，请看下图：

<center>![image.png](../../../assets/1653277209068-e7036fd9-6841-400e-96e2-d2f97013a4ba.png){width=300}</center>

操作系统还会跟踪哪些进程和虚拟地址正在使用哪个物理页，因为操作系统需要让交换引发后续 page fault 的次数尽可能少。操作系统会使用我们之前提到的 **LRU, Least Recently Used** 的策略处理交换。

LRU 的代价有点太大了，毕竟如果使用 LRU 的话需要遍历整个 main memory。因此，很多操作系统引入了 **reference bit** (或者称为 **use bit**) 来近似地实现 LRU。当一个 page 被访问时这个 bit 被置为 1；操作系统定期将 reference bit 清零。因此，在需要交换时，只需要找一个 reference bit 为 0 的就可以说明它在这段时间内没有被访问过。

如我们之前所说，virtual memory 使用 write back 的策略，因此还需要一个 dirty bit。


### 5.5.4 用多级页表解决页表过大的问题
我们不妨关注一下 page table 有多大。在我们之前的例子中，virtual address 有 48 bit，每个 page 的大小为 4KiB，所以 page table entry 的数目是 
<center>![](https://cdn.nlark.com/yuque/__latex/239411fdaac0b5f23072926c85b10bc0.svg#card=math&code=%5Cfrac%7B2%5E%7B48%7D%20%5Ctext%7B%20B%7D%7D%7B4%5Ctext%7B%20KiB%7D%7D%20%3D%20%5Cfrac%7B2%5E%7B48%7D%7D%7B4%5Ctimes%202%5E%7B10%7D%7D%20%3D%202%5E%7B36%7D&id=AJjfF)；而 RISC-V 每个表项有 8 Byte，所以 page table 的总大小来到了 ![](https://cdn.nlark.com/yuque/__latex/1656f79bbbe1cb3d8d19a4295215ea02.svg#card=math&code=2%5E%7B39%7D%5Ctext%7B%20B%7D%20%3D%200.5%20%5Ctext%7BTiB%7D&id=a7NM2){width=300}</center>
，这是极其不合理的；尤其是每个进程都有一个 page table 的前提下。

我们可以通过多级页表的方式解决这个问题。

如我们之前所述，页表是一个数组， `page_table[i]` 中存储的是 page number 为 i 的 page 所对应的 frame number。考虑我们的逻辑地址结构：

<center>![image.png](../../../assets/1607247135113-1998902c-c1c0-4d78-8d21-99766857be7e.png){width=300}</center>

这样的逻辑地址结构需要一个存储 2p 个元素的 page table，即需要这么大的连续内存，这是非常大的消耗。我们考虑将 p 再分为 p1 和 p2 ：

<center>![image.png](../../../assets/1608315590109-e84d3ab8-0a2d-4e6a-becd-d10f57d45f2f.png){width=300}</center>


<center>![image.png](../../../assets/1608315596044-0e1ba30c-ca5d-4f3a-ae2f-f792f992a1b1.png){width=300}</center>


我们使用一个两级页表， `outer_page_table[i]` 中存储的是 p1 为 i 的 inner page table，即`inner_page_table[i][]` 的基地址；而 `inner_page_table[i][j]` 中存储的就是 p1 为 i，p2 为 j 的 page 对应的 frame number，即 page number 为 p1p2 （没有分割时的 p）对应的 frame number。

这里，我们称 p1 为 **page directory number** ，p2 为 **page table number**，d 为 **page offset**。

<center>![image.png](../../../assets/1608316895578-0d32183b-93b0-44a1-805d-c96b47b0f3b0.png){width=300}</center>

考虑这样做的好处：hierarchical paging 其实就是对页表的分页（page the page table）。因此，它避免了 page table 必须处在连续内存的问题，这一问题在 _p_ 比较大时尤其严重。

另外，这样做在一般情况下可以节省空间。我们之前提到，页表不一定会全部使用；并且由于逻辑地址是连续的，因此用到的页表项也是连续的，都排在页表的头部。因此如果我们采用了二级页表，那么许多排在后面的 inner page table 将完全为空；此时我们可以直接不给这些 inner page table 分配空间，即我们只分配最大的 p1 那么多个 inner page table。这样我们可以节省很多空间。即使在最差的情况下，所有页表都被使用了，我们的页表所用的总条目数也只有 
<center>![](https://cdn.nlark.com/yuque/__latex/ed85ab3a4b1becb0009d61b35decf435.svg#card=math&code=2%5E%7Bp_1%7D%2B2%5E%7Bp_1%7D%5Ccdot%202%5E%7Bp_2%7D%20%3D%202%5E%7Bp_1%7D%20%2B%202%5E%7Bp_1%20%2B%20p_2%7D&height=18&id=W5OIH) 个，只比单级页表结构多了 ![](https://cdn.nlark.com/yuque/__latex/72cacc86da1cd1a47d75cca11c6539aa.svg#card=math&code=2%5E%7Bp_1%7D&height=16&id=tEUO2){width=300}</center>
，是完全可以接受的。

类似地，我们可以设计更多级的页表。例如，64 位的逻辑地址空间使用二级页表就是不够的，否则它的页表就会长成这样：

<center>![image.png](../../../assets/1608317288073-c745144b-ee16-43e2-b38b-56b32797856b.png){width=300}</center>


这样 outer page 就会超级大。我们可以 page the outer page：

<center>![image.png](../../../assets/1608360619753-f1b1e4b2-e278-40ba-ab7d-47133aa06989.png){width=300}</center>

这样，我们就建立了一个三级页表。

实际上，我们不必使用全部的 64 位，即我们不需要一个 64 位那么巨大的 virtual address space。AMD-64 支持 48-bit 的虚拟地址，ARM64 支持 39-bit 和 48-bit 的虚拟地址空间：

<center>![image.png](../../../assets/1608360842899-bab5d705-9051-4802-a36e-514d9977a7c5.png){width=300}</center>



### 5.5.5 使用 TLB 加快地址转换
我们之前提到，使用页表时，我们根据 virtual page number 找到对应 page table entry 在 page table 中的偏移，然后与 page table register 相加得到对应 entry 的 physical address，从中读取对应的 entry。但是这种方法的效率存在问题。要访问 virtual address 对应的 physical address，我们首先要根据 page table register 和 page number 来找到页表在内存的位置，并在其中得到 page 对应的 frame number，这需要一次内存访问；然后我们根据 frame number 和 page offset 算出真实的 physical address，并访问对应的字节内容。即，访问一个字节需要两次内存访问，这会加倍原本的内存访问的时间，这是难以接受的。

这个问题的解决方法用到一个专用的高速查找硬件 cache，这里称它为 **translation look-aside buffer (TLB)**。它实际上就是 page table 的专用 cache（它真的是 cache；page table 并不是 cache，只是像 cache），其 associativity 的设计可以根据实际情况决定。

下图是一个 fully-associative 的 TLB 的例子；由于是 fully-associative，并不需要 index：

<center>![image.png](../../../assets/1653281003134-b3440528-694f-4c30-8289-c05f06bde0a3.png){width=300}</center>

当 TLB miss 的时候，处理器去 page table 查找对应的项；如果发现对应项是 valid 的，那么就把他拿到 TLB 里（此时被替换掉的 TLB entry 的 dirty bit 如果是 1，也要写会 page table）；否则就会触发一个 page fault，然后在做上述的事。

<center>![image.png](../../../assets/1653281383373-c6779ed4-1765-4bd5-9be9-f57c2e5ebd3c.png){width=300}</center>



### 5.5.6 Memory Protection
暂时不想学QWQ


## 5.6 The Three Cs | 对 cache miss 的归类 存疑

- Compulsory misses / Cold-start misses：对一个块第一次访问时引发的 miss
- Capacity misses：在 fully-associative cache 中，某个块虽然访问过，但是由于容量不够被换出去了，再访问时就 miss 了
- Conflict misses / Collision misses：在 set-associative 或 direct-mapped cache 中，某个块虽然访问过，但是由于这个组里的容量不够被换出去了，再访问时就 miss 了


## 5.7 Using FSM to Control a Simple Cache
FSM，Finite State Machine，有限状态自动机；其实就是根据当前状态和输入转换状态的东西。这里根据当前的状态以及发生的事件转换状态，并给出一些控制信号的输出：

<center>![image.png](../../../assets/1653286348338-6817d850-727d-4644-b0ee-b4b0e3f90861.png){width=300}</center>


<center>![image.png](../../../assets/1653286361901-d528850a-0cfa-42d6-81ec-67f2455d231d.png){width=300}</center>



# 6 I/O


# Reference


## 历年卷
[https://www.cc98.org/topic/5114223](https://www.cc98.org/topic/5114223)
[https://www.cc98.org/topic/5118209](https://www.cc98.org/topic/5118209)


### 小考点

- Intro & Misc
- Instructions
   - machine code
   - addressing method
   - floating point inst
- Arithmetic
   - 1's complement, 2's complement
   - sign extensions
   - floating point calc steps
   - what is underflow
   - IEEE 754 
- Processor
- Cache
   - write-through, etc.
- Virtual Memory
   - TLB
   - usage of dirty bit
- I/O
   - SCSI Bus, etc.
   - memory-mapped I/O system


### 大题

- 给 C 写汇编 [19(14)]
- Cache 算位数 [19(12)]


<center>![image.png](../../../assets/1655054029001-a6ad0f7a-ded6-44f9-8ab3-d51797baf14c.png){width=300}</center>
 D
