> 朋辈辅学录播：[编译原理速成(3) 语法分析(下) LL(1)与自底向上分析](https://www.bilibili.com/video/BV1j94y1d7eW)


此部分介绍 **自底向上分析 (Buttom-Up Parsing)** 以及 **Yacc** 的有关内容。


### 3.4 自底向上分析 | Bottom-Up Parsing
所谓 **自底向上分析 (Bottom-Up Parsing)**，就是从输入的 token 流一步步简化为 start symbol。Bottom-Up Parsing 相较 Top-Down Parsing 而言更加通用，而且并没有牺牲性能。Bottom-Up Parsing 的思路基于我们之前讨论过的 Top-Down Parsing 的相关思路。

同样的，我们首先讨论 Bottom-Up Parsing 的过程，稍后再讨论这些过程具体是怎么实现的，例如 parser 如何知道在什么情形下使用哪条 production。

我们看这样一个例子，其左边一列是输入的 token 流一步一步被 **规约 (reduce) **到 start symbol 的过程，其右边一列是每一步用到的 production。注意：自底向上分析使用 production 时是将 production 的 rhs 转换为 lhs：<br />![](./assets/1618581322665-4786f6cd-5978-4608-977e-0676666da18a.png)
从下往上查看分析过程，我们可以发现一个重要事实：**自底向上分析是最右分析的一个逆过程**。

更具体地研究这个过程。我们考虑我们发现的重要事实：如果某一次规约是 ![](https://cdn.nlark.com/yuque/__latex/2d80a1a92bf4a06f260d063af1d4a6e8.svg#card=math&code=%5Calpha%5Cbeta%5Comega%5Cto%5Calpha%20X%5Comega&height=18&id=t0wwj)，使用了 production ![](https://cdn.nlark.com/yuque/__latex/f0e4a687a57caa8c114bc81291d57032.svg#card=math&code=X%5Cto%5Cbeta&id=e0CVM)，那么由于这是最右分析逆过程的某一步，亦即 ![](https://cdn.nlark.com/yuque/__latex/ff7388d50f75c0f678f63aa7fdc5e034.svg#card=math&code=%5Calpha%20X%5Comega%5Cto%5Calpha%5Cbeta%5Comega&height=18&id=eT6cB) 是最右分析的某一步，因此 ![](https://cdn.nlark.com/yuque/__latex/260b57b4fdee8c5a001c09b555ccd28d.svg#card=math&code=%5Comega&id=KmTWj) 一定全部由 terminal 组成，这是分析过程中**已经完成了展开**的部分。那么对于这个逆过程来说，![](https://cdn.nlark.com/yuque/__latex/260b57b4fdee8c5a001c09b555ccd28d.svg#card=math&code=%5Comega&id=XVyTf) 则是**尚未被考虑**的部分。那么此时我们就可以将当前的 token 串分为两部分：![](https://cdn.nlark.com/yuque/__latex/9f85f0800fb34bdca35cd745ad8ad2e5.svg#card=math&code=%5Calpha%5Cbeta%20%7C%20%5Comega&id=Bz26X)，其中 | 左边的是已经被考虑过的部分，而 | 右边的是没有考虑过的部分。<br />我们进一步可以注意到：所有操作都会发生在 | 紧邻的左右两边。实际上，只会有 2 种操作产生：

1. **Reduce**，规约：将 | 左边的一些 token 用某条 production 转换为一个 Non-terminal；
2. **Shift**，移进：将 | 右移一位，即将下一个 terminal 纳入考虑。

因此，上面的例子实际上就是：<br />![](./assets/1618582403943-2cc175b0-e5b2-4f6a-b2ac-5a19b2b298c0.png)

我们容易想到，这个分析过程用栈很容易实现。我们将 | 左边的部分存在栈中，那么 reduce 操作就是将栈顶的若干个元素（对应某个 production 的 rhs，也有可能是 0 个）pop 出来，然后 push 相应 production 的 lhs；而 shift 操作就是读取输入 token 流中的一个 terminal 并将其 push 到栈顶。

在同一个状态下，parser 可能会有多种可选的操作，例如既可以 reduce 也可以 shift，这称为一个 shift-reduce conflict；有时还可能有多个可选的 reduce 方式，这称为一个 reduce-reduce conflict。这些冲突通常表明语法存在一定问题，当然也可以通过定义优先级的方式进行解决。我们将在后面讨论相应的解决方法。


#### Viable Prefix
![image.png](./assets/1649645253673-7e0f205b-b83b-477a-b5af-cc32592f22be.png)
![image.png](./assets/1649645266346-9136ce47-a39d-4413-990f-868d0fc70b1a.png)


### 3.5 LR(0) Parsing
[这篇博客](https://www.xiaoheidiannao.com/LR0-Analysis-Table-Construction-Algorithm.html) 是使我学明白 LR(0) 分析表构造的关键博客；[这篇博客](https://www.cnblogs.com/bryce1010/p/9387114.html) 是使我理解这张表怎么用的关键博客（3.5.3 中的伪代码也基于此处更改）；[这篇博客](http://leaver.me/2012/05/14/%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E5%AE%9E%E4%BE%8B%E7%9A%84lr%E5%88%86%E6%9E%90%E8%BF%87%E7%A8%8B/) 中有一个具体的示例演示这张表的用法。

LR(0) Parsing 是 Bottom-Up Parsing 的一种。LR(k) 表示 Left-to-Right Scan, Rightmost Derivation, Predict Based on _k_ Tokens of Lookahead。


#### 3.5.1 LR(0) Item
我们在 3.4 中提到，自底向上分析的过程就是不断地凑出一个 production 的 rhs，并让这些 rhs 位于 Parsing 栈的栈顶。因此假设下一次将会使用到的 production 为 ![](https://cdn.nlark.com/yuque/__latex/aea8e107dd5d9da00f7d1297e40cf00c.svg#card=math&code=X%5Cto%20%5Calpha%5Cbeta&id=PVOx5)，那么在使用这个 production 进行规约之前，栈顶可能包含了 ![](https://cdn.nlark.com/yuque/__latex/5ba804980e032532691163b835e222e1.svg#card=math&code=%5Ccdots%5Ccdots%2C%20%5Ccdots%5Calpha%5Ccdots%2C%20%5Ccdots%5Calpha%5Cbeta&id=zmsRr) 等情况，即我们凑出这个 production 的 rhs 的进度不同。对于这些情况，我们希望对其做出不一样的操作。<br />因此，对于每一个 production，我们用句点 . 来标识一种凑出其 rhs 的进度（right-hand-side position）。例如 ![](https://cdn.nlark.com/yuque/__latex/235bc924c6b170f86a77f481bb0ff571.svg#card=math&code=X%5Cto%5Calpha%5Cbeta&id=YfBTI) 的情况就会有：![](https://cdn.nlark.com/yuque/__latex/02f78e54abb6b62a8230c517d0c0c1c4.svg#card=math&code=X%5Cto%20.%5Calpha%5Cbeta%2C%20X%5Cto%20%5Calpha.%5Cbeta%2C%20X%5Cto%20%5Calpha%5Cbeta.&height=18&id=FPuzE) 三种。我们将这些情况称为 **LR(0) Item**。我们在后面将看到，我们的分析就是基于这些 Item 的。

我们举一个例子，贯穿后续小节的学习，直到成功完成分析。对于文法 `S'->S, S->(S)S | EPSILON` ，其 LR(0) Item 包括：`S'->.S`, `S'->S.`, `S->.(S)S`, `S->(.S)S`, `S->(S.)S`, `S->(S).S`, `S->(S)S.`, `S->.` 。


#### 3.5.2 LR(0) Parsing Table 的构造
我们会看到，LR(0) Item 之间会有一些转换关系。例如：

   - ![](https://cdn.nlark.com/yuque/__latex/8927e29078be86a405bea4b2a5588dcf.svg#card=math&code=X%5Cto.%5Calpha%5Cbeta&id=tysJb) 接收 ![](https://cdn.nlark.com/yuque/__latex/7b7f9dbfea05c83784f8b85149852f08.svg#card=math&code=%5Calpha&id=QilDM) 后就会变成 ![](https://cdn.nlark.com/yuque/__latex/8025976dad817ec664af99ac132ad6e1.svg#card=math&code=X%5Cto%20%5Calpha.%5Cbeta%20&height=18&id=koQsS)
   - 如果存在 production ![](https://cdn.nlark.com/yuque/__latex/362e42129ea4d8fe048cac472709f4b7.svg#card=math&code=X%5Cto%20%5Cgamma%20Y%5Comega%2C%20Y%5Cto%20%5Calpha%5Cbeta&height=19&id=ZPTkK)，那么 ![](https://cdn.nlark.com/yuque/__latex/07f03ddc4593bc75224167dcd473ac69.svg#card=math&code=X%5Cto%20%5Cgamma%20.Y%5Comega&id=BKCRc) 就可以转换到 ![](https://cdn.nlark.com/yuque/__latex/efeca4be5c8d19fc920eb281ac59beb0.svg#card=math&code=Y%5Cto%20.%5Calpha%5Cbeta&height=18&id=rpj8b)，因为要凑出 X，这时需要先凑出一个 Y。

根据上述转换关系，我们可以得到一个 LR(0) Items 的 NFA。之所以是 NFA，是因为上述第二条转换关系导致存在 ![](https://cdn.nlark.com/yuque/__latex/92e4da341fe8f4cd46192f21b6ff3aa7.svg#card=math&code=%5Cepsilon&id=MNJ0l) 转化。

那么，对于我们提出的例子，其 NFA 就是：
![](https://cdn.nlark.com/yuque/__graphviz/a00d8c0985d8df9507eefe2c941564cd.svg#lake_card_v2=eyJ0eXBlIjoiZ3JhcGh2aXoiLCJjb2RlIjoiZGlncmFwaCBHIHtcbiAgICBub2RlIFtzaGFwZSA9IHJlY3RhbmdsZV1cbiAgICAwIFtzdHlsZSA9IGludmlzXTtcbiAgICAxIFtsYWJlbCA9IFwiUyfihpIuU1wiXTtcbiAgICAyIFtsYWJlbCA9IFwiUyfihpJTLlwiXTtcbiAgICAzIFtsYWJlbCA9IFwiU-KGki4oUylTXCJdOyBcbiAgICA0IFtsYWJlbCA9IFwiU-KGkihTKVMuXCJdOyBcbiAgICA1IFtsYWJlbCA9IFwiU-KGkiguUylTXCJdOyBcbiAgICA2IFtsYWJlbCA9IFwiU-KGkihTLilTXCJdOyBcbiAgICA3IFtsYWJlbCA9IFwiU-KGkihTKS5TXCJdOyBcbiAgICA4IFtsYWJlbCA9IFwiU-KGki5cIl07XG4gICAgMC0-MTtcbiAgICAxLT4yIFtsYWJlbCA9IFwiU1wiXTtcbiAgICAxLT4zIFtsYWJlbCA9IFwiz7VcIl07XG4gICAgMS0-OCBbbGFiZWwgPSBcIs-1XCJdO1xuICAgIDMtPjUgW2xhYmVsID0gXCIoXCJdO1xuICAgIDUtPjMgW2xhYmVsID0gXCLPtVwiXTtcbiAgICA1LT44IFtsYWJlbCA9IFwiz7VcIl07XG4gICAgNS0-NiBbbGFiZWwgPSBcIlNcIl07XG4gICAgNi0-NyBbbGFiZWwgPSBcIilcIl07XG4gICAgNy0-NCBbbGFiZWwgPSBcIlNcIl07XG4gICAgNy0-MyBbbGFiZWwgPSBcIs-1XCJdO1xuICAgIDctPjggW2xhYmVsID0gXCLPtVwiXTtcbn0iLCJ1cmwiOiJodHRwczovL2Nkbi5ubGFyay5jb20veXVxdWUvX19ncmFwaHZpei9hMDBkOGMwOTg1ZDhkZjk1MDdlZWZlMmM5NDE1NjRjZC5zdmciLCJpZCI6IkJKSFZEIiwibWFyZ2luIjp7InRvcCI6dHJ1ZSwiYm90dG9tIjp0cnVlfSwiY2FyZCI6ImRpYWdyYW0ifQ==)
进一步地，我们将 NFA 转换为 DFA：
![](https://cdn.nlark.com/yuque/__graphviz/2c0c8c264a419eca5ca0f1d49971c021.svg#lake_card_v2=eyJ0eXBlIjoiZ3JhcGh2aXoiLCJjb2RlIjoiZGlncmFwaCBHIHtcbiAgICBub2RlIFtzaGFwZSA9IHJlY3RhbmdsZV1cbiAgICAwIFtzdHlsZSA9IGludmlzXTtcbiAgICAxIFtsYWJlbCA9IFwiUyfihpIuU1xcblPihpIuKFMpU1xcblPihpIuXCJdO1xuICAgIDMgW2xhYmVsID0gXCJT4oaSKC5TKVNcXG5T4oaSLihTKVNcXG5T4oaSLlwiXTsgXG4gICAgNCBbbGFiZWwgPSBcIlPihpIoUy4pU1wiXTsgXG4gICAgNSBbbGFiZWwgPSBcIlPihpIoUykuU1xcblPihpIuKFMpU1xcblPihpIuXCJdOyBcbiAgICA2IFtsYWJlbCA9IFwiU-KGkihTKVMuXCJdOyBcbiAgICAyIFtsYWJlbCA9IFwiUyfihpJTLlwiXTtcbiAgICAwLT4xO1xuICAgIFxuICAgIDEtPjMgW2xhYmVsID0gXCIoXCJdO1xuICAgIDMtPjMgW2xhYmVsID0gXCIoXCJdO1xuICAgIDUtPjMgW2xhYmVsID0gXCIoXCJdO1xuICAgIDMtPjQgW2xhYmVsID0gXCJTXCJdO1xuICAgIDQtPjUgW2xhYmVsID0gXCIpXCJdO1xuICAgIDUtPjYgW2xhYmVsID0gXCJTXCJdO1xuICAgIDEtPjIgW2xhYmVsID0gXCJTXCJdO1xufSIsInVybCI6Imh0dHBzOi8vY2RuLm5sYXJrLmNvbS95dXF1ZS9fX2dyYXBodml6LzJjMGM4YzI2NGE0MTllY2E1Y2EwZjFkNDk5NzFjMDIxLnN2ZyIsImlkIjoiWW4wTTkiLCJtYXJnaW4iOnsidG9wIjp0cnVlLCJib3R0b20iOnRydWV9LCJjYXJkIjoiZGlhZ3JhbSJ9)
我们可以据此构造出一个 LR(0) Parsing Table：

| **State** | **Input & Shift** |  |  | **Goto** |
| --- | --- | --- | --- | --- |
|  | **(** | **)** | **$** | **S** |
| **1** | s3/r3 | r3 | r3 | g2 |
| **2** | r1 | r1 | accept(r1) |  |
| **3** | s3/r3 | r3 | r3 | g4 |
| **4** |  | s5 |  |  |
| **5** | s3/r3 | r3 | r3 | g6 |
| **6** | r2 | r2 | r2 |  |

其中，s_k_ 表示将对应的 terminal 压栈，然后移到到状态 _k_；g_k_ 表示将对应的 non-terminal 压栈，然后移到状态 _k_；r_k_ 表示用第 _k_ 条 production 规约，这里 r1, r2, r3 分别为 `S'->S`, `S->(S)S`, `S->EPSILON`；accept 表示接受。<br />这个表的创建方式是：

   - 对于 DFA 中的每一个 ![](https://cdn.nlark.com/yuque/__latex/c3460d8ac5397e9fd7660930e1790bf7.svg#card=math&code=S_i%5Cstackrel%7Bt%7D%7B%5Clongrightarrow%7DS_j&height=30&id=HvvhZ)，我们令 `T[i, t] = sj`，其中 ![](https://cdn.nlark.com/yuque/__latex/804f14414dab2297b600211a82c39fa8.svg#card=math&code=S_i&id=hPVJa) 是状态 i，t 是一个 terminal；
   - 对于 DFA 中的每一个 ![](https://cdn.nlark.com/yuque/__latex/58ee528300edb79e03aa19341b19d783.svg#card=math&code=S_i%5Cstackrel%7BX%7D%7B%5Clongrightarrow%7DS_j&height=31&id=utahV)，我们令 `T[i, X] = gj`，其中 X 是一个 non-terminal；
   - 对于每一个可以规约（即句点在 rhs 最后）的 LR(0) item，对其所在状态 i 以及每一个 terminal t，令 `T[i, t] = rk`，其中 k 是 LR(0) item 对应的 production 的序号。

我们可以发现，我们建立的表中 `T[1, "("], T[3, "("], T[5, "("]` 这三项被标红，因为这些表项中有不止一个操作，这说明这里出现了冲突。这三项均为 shift-reduce conflict。这说明，这个文法并不是 LR(0) 文法。（由此可见 LR(0) 文法太弱，不是很有用。但是这会为后面的文法学习打下基础。）


#### 3.5.3 LR(0) Parsing Table 的使用
这里使用的 LR(0) Parsing Table 应当是一个没有冲突的表，即必须对 LR(0) Parsing Table 进行分析。<br />在使用 LR(0) Parsing Table 进行分析时，我们维护 2 个栈，分别存储当前分析的 token（就像 3.4 中我们讨论的那样）以及每个 token 对应的状态编号，我们称为 token 栈和状态栈。<br />shift 操作的实现是十分容易理解的：将当前 terminal 压入 token 栈，将 s_k_ 指示的状态 k 压入状态栈即可。但对于 reduce 操作（假设操作为 rj ，对应 production 为 A->β），那么我们需要首先将两个栈 pop 出 |β|（β 中 token 的个数）项，然后查看** pop 后 **栈顶的状态 S，查看 T[S, A] 的值即 g_k_，然后将 A 压入 token 栈，k 压入状态栈。<br />具体算法的伪代码如下：
```
置 ptr 指向输入串 w 的第一个符号
令 Si 为状态栈顶的状态
a 是 ptr 指向的符号，即当前输入符号
WHILE(1) BEGIN
  IF T[Si, a] = Sj THEN
    BEGIN
      PUSH (j, a)							// 将 j 压入状态栈，将 a 压入 token 栈
      ptr++
    END
  ELSE IF T[Si, a] = rj THEN	// rj 为 A->β
    BEGIN
      pop |β| times
      若当前栈顶状态为Sk
      push (T[Sk, A], A)			// 如果 T[Sk, A] 为空也应返回一个错误
    END
  ELSE IF T[Si, a] = accept THEN
    return 0
  ELSE 
    return -1
END
```
我们说这种分析法为 LR(_0_)，是因为我们 **_实际上 _**没有进行 look-ahead（虽然在上述的伪代码中我们实际上做了这件事）：所有的 reduce 操作实际上是与状态绑定的，而不是与 (状态, 输入) 对绑定的。因此我们在读取当前符号之前，就知道应该 reduce 还是应该 shift 了，而如果是 shift，则可以认为是读入当前符号以后再做判断，也就是说从理论上讲我们没有（或者说不必）做任何 look-ahead。


### 3.6 SLR(1) Parsing
SLR(1) 中的 S 表示 Simple。SLR(1) Parsing 在 LR(0) 的基础上通过简单的判断尝试解决冲突。

SLR(1) 在如 3.5.2 那样生成了 LR(0) DFA 后，计算每一个 non-terminal 的 Follow Set，并根据这两者创建 SLR(1) 分析表。<br />我们继续使用 3.5 小节的例子：`S'->S`, `S->(S)S`, `S->EPSILON`。那么，FOLLOW(S') = {$}，FOLLOW(S) = {')', $}。

我们构建 SLR(1) 分析表，与构建 LR(0) 分析表非常相似：

   - 对于 DFA 中的每一个 ![](https://cdn.nlark.com/yuque/__latex/c3460d8ac5397e9fd7660930e1790bf7.svg#card=math&code=S_i%5Cstackrel%7Bt%7D%7B%5Clongrightarrow%7DS_j&height=30&id=isFEK)，我们令 `T[i, t] = sj`，其中 ![](https://cdn.nlark.com/yuque/__latex/804f14414dab2297b600211a82c39fa8.svg#card=math&code=S_i&id=D5TVu) 是状态 i，t 是一个 terminal；
   - 对于 DFA 中的每一个 ![](https://cdn.nlark.com/yuque/__latex/58ee528300edb79e03aa19341b19d783.svg#card=math&code=S_i%5Cstackrel%7BX%7D%7B%5Clongrightarrow%7DS_j&height=31&id=vYtRF)，我们令 `T[i, X] = gj`，其中 X 是一个 non-terminal；
   - 对于每一个可以规约的 LR(0) item（假设是 `A->α.`），对其所在状态 i 以及每一个 terminal t，**如果 t ∈ FOLLOW(A)**，令 `T[i, t] = rk`，其中 k 是 LR(0) item 对应的 production 的序号。

也就是说，唯一的区别是，LR(0) 对可归约项所在状态的所有 terminal 进行 reduce，而 SLR(1) 只对那些下一个符号在对应 non-terminal 的 Follow Set 的情况进行 reduce。

对于我们的例子，我们可以构造如下的 SLR(1) Parsing Table。可以发现，我们已经消除了 conflict。

| **State** | **Input & Shift** |  |  | **Goto** |
| --- | --- | --- | --- | --- |
|  | **(** | **)** | **$** | **S** |
| **1** | s3 | r3 | r3 | g2 |
| **2** |  |  | accept(r1) |  |
| **3** | s3 | r3 | r3 | g4 |
| **4** |  | s5 |  |  |
| **5** | s3 | r3 | r3 | g6 |
| **6** | <br /> | r2 | r2 |  |


可以发现，与 LR(0) 不同的是，SLR(1) 的 reduce 不再只与状态有关，我们需要提前观看下一个符号从而判断进行什么样的 shift 或 reduce 操作。

如果这样构造出的 SLR(1) Parsing Table 没有含冲突的表项，那么称这个文法为 SLR(1) Grammar，否则不是。

SLR(1) Parsing Table 的使用方法与 3.5.3 完全一致，可以使用一样的伪代码。


### 3.7 LR(1) Parsing
LR(1) 在 SLR(1) 的基础上进行了进一步优化。

我们在 3.5.1 中定义了 LR(0) Item，LR(1) Item 与之相似但更加复杂。一个 LR(1) Item 除了有 production 和 rhs position（用句点表示）以外，还有一个 lookahead symbol。例如 ![](https://cdn.nlark.com/yuque/__latex/04b973292e957d28b75f78fda6d2cf7f.svg#card=math&code=A%5Cto%20%5Calpha.%5Cbeta%2C%5C%20t&id=YVgzX) 表示 ![](https://cdn.nlark.com/yuque/__latex/7b7f9dbfea05c83784f8b85149852f08.svg#card=math&code=%5Calpha&id=WqUJS) 在栈顶，而且未来的输入将会是 ![](https://cdn.nlark.com/yuque/__latex/f58b366dc703dff98777b36c5ea39699.svg#card=math&code=%5Cbeta%20t&id=xkA2G)。对 3.5 中提出的例子，根据 start symbol，这里有 LR(1) Item `S'->.S, $`。<br />LR(1) Item 在如下两种情况下存在转化：

   - ![](https://cdn.nlark.com/yuque/__latex/8927e29078be86a405bea4b2a5588dcf.svg#card=math&code=X%5Cto.%5Calpha%5Cbeta%2C%5C%20t&id=STgdB) 接收 ![](https://cdn.nlark.com/yuque/__latex/7b7f9dbfea05c83784f8b85149852f08.svg#card=math&code=%5Calpha&id=d75On) 后就会变成 ![](https://cdn.nlark.com/yuque/__latex/8025976dad817ec664af99ac132ad6e1.svg#card=math&code=X%5Cto%20%5Calpha.%5Cbeta%20%2C%20%5C%20t&height=18&id=JlOCz)；
   - 如果存在 production ![](https://cdn.nlark.com/yuque/__latex/362e42129ea4d8fe048cac472709f4b7.svg#card=math&code=X%5Cto%20%5Cgamma%20Y%5Comega%2C%20Y%5Cto%20%5Calpha%5Cbeta&height=2&id=euxVI)，那么对于每一个 ![](https://cdn.nlark.com/yuque/__latex/405f808f54fe5308aacb9c9b7b85405e.svg#card=math&code=t_i%5Cin%5Ctext%7BFirst%7D%28%5Comega%20t%29%20&id=b9T5z) (![](https://cdn.nlark.com/yuque/__latex/260b57b4fdee8c5a001c09b555ccd28d.svg#card=math&code=%5Comega&id=dOUKp) 可以为 ![](https://cdn.nlark.com/yuque/__latex/92e4da341fe8f4cd46192f21b6ff3aa7.svg#card=math&code=%5Cepsilon&id=CrUeg))，![](https://cdn.nlark.com/yuque/__latex/83680950f569a15aacc3ea403d2397dc.svg#card=math&code=X%5Cto%20%5Cgamma%20.Y%5Comega%2C%5C%20t&id=xn8mi) 可以经 ![](https://cdn.nlark.com/yuque/__latex/92e4da341fe8f4cd46192f21b6ff3aa7.svg#card=math&code=%5Cepsilon&id=w8vpR) 转换到 ![](https://cdn.nlark.com/yuque/__latex/4c1fd27cd0e34509dcc6909438f7b970.svg#card=math&code=Y%5Cto%20.%5Calpha%5Cbeta%2C%20%5C%20t_i&height=18&id=W9VMm)。

例如下面这个例子：
```
S'-> S
S -> aAd
S -> bBd
S -> aBe
S -> bAe
A -> c
B -> c
```
Start Symbol 有 LR(1) Item `S'->.S, $`，并可以通过此推出如下 State 1 中的 items。其余推导略同，下面是 LR(1) DFA：
![image.png](./assets/1619110489690-3dc51280-a2c1-46a9-a3cf-9fdc544bd4ae.png)
由此可以构造出 LR(1) Parsing Table，其方式是：

   - 对于 DFA 中的每一个 ![](https://cdn.nlark.com/yuque/__latex/c3460d8ac5397e9fd7660930e1790bf7.svg#card=math&code=S_i%5Cstackrel%7Bt%7D%7B%5Clongrightarrow%7DS_j&height=30&id=Fy8Fw)，我们令 `T[i, t] = sj`，其中 ![](https://cdn.nlark.com/yuque/__latex/804f14414dab2297b600211a82c39fa8.svg#card=math&code=S_i&id=OZBXB) 是状态 i，t 是一个 terminal；
   - 对于 DFA 中的每一个 ![](https://cdn.nlark.com/yuque/__latex/58ee528300edb79e03aa19341b19d783.svg#card=math&code=S_i%5Cstackrel%7BX%7D%7B%5Clongrightarrow%7DS_j&height=31&id=ZTYYw)，我们令 `T[i, X] = gj`，其中 X 是一个 non-terminal；
   - 对于每一个可以规约（即句点在 rhs 最后）的 LR(1) item，对其所在状态 i 以及每一个 lookahead symbol t，令 `T[i, t] = rk`，其中 k 是 LR(1) item 对应的 production 的序号。

如果以此法构造出的 Parsing Table 没有冲突项，则说明文法是 LR(1) 的，否则不是。


### 3.8 LALR(1) Parsing
可以看到，LR(1) 的状态有点太多了。在刚刚提出 LR(1) 的那个年代，如此大的空间需求还是不太现实的。因此，LR(1) 的简化版本 LALR(1) (Look-Ahead LR(1)) 被提出了。<br />对于每一个状态，我们将其包含的所有 LR(1) items 的第一个分量的集合成为这个状态的核心 (core)。例如，对于 3.7 最后例子中的状态图，其状态 5 和 6 的核心均为 ![](https://cdn.nlark.com/yuque/__latex/c7cc05f435d737a5bb7213a664008da6.svg#card=math&code=%5C%7BA%5Cto%20c.%2C%20B%5Cto%20c.%5C%7D&id=FPSoD)。我们将这样的具有相同核心的状态进行合并，通常能够减少许多状态。<br />但是，这有时（虽然很少）也可能引入 reduce-reduce conflict，例如 3.7 最后的例子的 LALR(1) DFA 是：
![](https://cdn.nlark.com/yuque/__graphviz/7f35b67da5519dc8edde547d58a2d007.svg#lake_card_v2=eyJ0eXBlIjoiZ3JhcGh2aXoiLCJjb2RlIjoiZGlncmFwaCBHIHtcbiAgICByYW5rZGlyID0gVEI7XG4gICAgbm9kZSBbc2hhcGUgPSByZWN0YW5nbGVdO1xuICAgIFxuICAgIDUgW2xhYmVsID0gXCItU3RhdGUgNSY2LVxcbkHihpJjLiwgZC9lXFxuQuKGkmMuLCBkL2VcIl07XG4gICAgMTAwIFtzdHlsZSA9IGludmlzXTtcbiAgICBcbiAgICAxIFtsYWJlbCA9IFwiLVN0YXRlIDEtXFxuUyfihpIuUywgJFxcblPihpIuYUFkLCAkXFxuU-KGki5hQmUsICRcXG5T4oaSLmJBZSwgJFxcblPihpIuYkJkLCAkXCJdOyBcbiAgICAyIFtsYWJlbCA9IFwiLVN0YXRlIDItXFxuUyfihpJTLiwgJFwiXTsgXG4gICAgMyBbbGFiZWwgPSBcIi1TdGF0ZSAzLVxcblPihpJhLkFkLCAkXFxuU-KGkmEuQmUsICRcXG5B4oaSLmMsIGRcXG5C4oaSLmMsIGVcIl07XG4gICAgNCBbbGFiZWwgPSBcIi1TdGF0ZSA0LVxcblPihpJiLkFlLCAkXFxuU-KGkmIuQmQsICRcXG5B4oaSLmMsIGVcXG5C4oaSLmMsIGRcIl07IFxuICAgIFxuICAgIDcgW2xhYmVsID0gXCItU3RhdGUgNy1cXG5T4oaSYUEuZCwgJFwiXTtcbiAgICA4IFtsYWJlbCA9IFwiLVN0YXRlIDgtXFxuU-KGkmFBZC4sICRcIl07XG4gICAgOSBbbGFiZWwgPSBcIi1TdGF0ZSA5LVxcblPihpJhQi5lLCAkXCJdOyBcbiAgICAxMFtsYWJlbCA9IFwiLVN0YXRlIDEwLVxcblPihpJhQmUuLCAkXCJdO1xuICAgIDExW2xhYmVsID0gXCItU3RhdGUgMTEtXFxuU-KGkmJBLmUsICRcIl07XG4gICAgMTJbbGFiZWwgPSBcIi1TdGF0ZSAxMi1cXG5T4oaSYkFlLiwgJFwiXTsgXG4gICAgMTNbbGFiZWwgPSBcIi1TdGF0ZSAxMy1cXG5T4oaSYkIuZCwgJFwiXTtcbiAgICAxNFtsYWJlbCA9IFwiLVN0YXRlIDE0LVxcblPihpJiQmQuLCAkXCJdOyBcbiAgICBcbiAgICAxMDAtPjE7XG4gICAgMS0-MltsYWJlbCA9IFwiU1wiXTtcbiAgICAxLT4zW2xhYmVsID0gXCJhXCJdO1xuICAgIDEtPjRbbGFiZWwgPSBcImJcIl07XG4gICAgMy0-NVtsYWJlbCA9IFwiY1wiXTtcbiAgICA0LT41W2xhYmVsID0gXCJjXCJdO1xuICAgIDQtPjExW2xhYmVsID0gXCJBXCJdO1xuICAgIDQtPjEzW2xhYmVsID0gXCJCXCJdO1xuICAgIDExLT4xMltsYWJlbCA9IFwiZVwiXTtcbiAgICAxMy0-MTRbbGFiZWwgPSBcImRcIl07XG4gICAgMy0-N1tsYWJlbCA9IFwiQVwiXTtcbiAgICAzLT45W2xhYmVsID0gXCJCXCJdO1xuICAgIDctPjhbbGFiZWwgPSBcImRcIl07XG4gICAgOS0-MTBbbGFiZWwgPSBcImVcIl07XG4gICAgXG4gICAge3JhbmsgPSBzYW1lOyAzLCAxLCA0O31cbiAgICB7cmFuayA9IHNhbWU7IDUsIDEwMDt9XG59IiwidXJsIjoiaHR0cHM6Ly9jZG4ubmxhcmsuY29tL3l1cXVlL19fZ3JhcGh2aXovN2YzNWI2N2RhNTUxOWRjOGVkZGU1NDdkNThhMmQwMDcuc3ZnIiwiaWQiOiJjZURNRSIsIm1hcmdpbiI6eyJ0b3AiOnRydWUsImJvdHRvbSI6dHJ1ZX0sImNhcmQiOiJkaWFncmFtIn0=)注意到合并后的状态 5&6，会存在 reduce-reduce conflict。这说明这个文法不是 LALR(1) 文法。<br />根据 DFA 可以构造 LALR(1) Parsing Table，其方法与 LR(1) 完全一致，在此不再赘述。同样地，如果构造出的 Parsing Table 没有冲突项，则说明文法是 LALR(1) 的，否则不是。

![image.png](./assets/1648826010075-7ea603c6-7f85-4c5e-b135-7e71302dcdcc.png)


### 3.9 Yacc：LALR(1) 语法分析器的生成器
我们在 [2.6 Lex：词法分析器的生成器](https://www.yuque.com/xianyuxuan/coding/ttn5z3#ka4lH) 中学习了 Lex 的使用。我们从本章的学习中发现词法分析器的生成同样是一个相当机械而复杂的过程。因此前人也设计了生成 Parser 的程序，这里我们用到的是 Yacc。<br />Yacc 需要和 Lex 结合使用，除非我们在其中自己编写 `yylex()` 函数。


### 习题

#### LR(0) & SLR(1)
> 5.8 Consider the following grammar

```
declaration → type var-list
type → int 
	 | float
var-list → identifier, var-list 
		 | identifier
```
> a. Rewrite it in a form more suitable for bottom-up parsing.
> b. Construct the LR(0) DFA for the rewritten grammar.
> c. Construct the SLR(1) parsing table for the rewritten grammar.


a. Add a start symbol and remove the right recursion:

```
S -> declaration
declaration -> type var-list
type -> int
type -> float
var-list -> var-list, identifier
var-list -> identifier
```

b. The LR(0) NFA is as follows:<br />![image-20210422104000199.png](./assets/1619094368439-1fa5e31f-7f06-465e-9b40-06cd770e1b5c.png)
We can simplify the NFA and get the requested DFA:
![](https://cdn.nlark.com/yuque/__graphviz/c1dfdf8e13d6dd17f7ffe518407f0522.svg#lake_card_v2=eyJ0eXBlIjoiZ3JhcGh2aXoiLCJjb2RlIjoiZGlncmFwaCBHIHtcbiAgICByYW5rZGlyID0gVEI7XG4gICAgbm9kZSBbc2hhcGUgPSByZWN0YW5nbGVdO1xuICAgIDEwMCBbc3R5bGUgPSBpbnZpc107XG4gICAgXG4gICAgMSBbbGFiZWwgPSBcIi1TdGF0ZSAxLVxcblPihpIuZGVjbGFyYXRpb25cXG5kZWNsYXJhdGlvbuKGki50eXBlIHZhci1saXN0XFxudHlwZeKGki5mbG9hdFxcbnR5cGXihpIuaW50XCJdOyBcbiAgICAzIFtsYWJlbCA9IFwiLVN0YXRlIDMtXFxudHlwZeKGkmludC5cIl07IFxuICAgIDIgW2xhYmVsID0gXCItU3RhdGUgMi1cXG5kZWNsYXJhdGlvbuKGknR5cGUudmFyLWxpc3RcXG52YXItbGlzdOKGki52YXItbGlzdCxpZGVudGlmaWVyXFxudmFyLWxpc3TihpIuaWRlbnRpZmllclwiXTsgXG4gICAgNCBbbGFiZWwgPSBcIi1TdGF0ZSA0LVxcbnR5cGXihpJmbG9hdC5cIl07IFxuICAgIDUgW2xhYmVsID0gXCItU3RhdGUgNS1cXG52YXItbGlzdOKGknZhci1saXN0LixpZGVudGlmaWVyXFxuZGVjbGFyYXRpb27ihpJ0eXBlIHZhci1saXN0LlwiXTtcbiAgICA2IFtsYWJlbCA9IFwiLVN0YXRlIDYtXFxudmFyLWxpc3TihpJpZGVudGlmaWVyLlwiXTsgXG4gICAgNyBbbGFiZWwgPSBcIi1TdGF0ZSA3LVxcbnZhci1saXN04oaSdmFyLWxpc3QsLmlkZW50aWZpZXJcIl07XG4gICAgOCBbbGFiZWwgPSBcIi1TdGF0ZSA4LVxcbnZhci1saXN04oaSdmFyLWxpc3QsaWRlbnRpZmllci5cIl07XG4gICAgOSBbbGFiZWwgPSBcIi1TdGF0ZSA5LVxcblPihpJkZWNsYXJhdGlvbi5cIl07IFxuICAgIFxuICAgIHtyYW5rPXNhbWU7IDEsIDk7fVxuICAgIHtyYW5rPXNhbWU7IDIsIDY7fVxuICAgIGFzc2lzMSBbc3R5bGUgPSBpbnZpc107XG4gICAgMy0-YXNzaXMxIFtzdHlsZSA9IGludmlzXTtcbiAgICB7cmFuaz1zYW1lOyBhc3NpczEsIDI7fVxuICAgIFxuICAgIFxuICAgIDEwMC0-MTtcbiAgICAxLT4yIFtsYWJlbCA9IFwidHlwZVwiXTtcbiAgICAxLT4zIFtsYWJlbCA9IFwiaW50XCJdO1xuICAgIDEtPjQgW2xhYmVsID0gXCJmbG9hdFwiXTtcbiAgICAxLT45IFtsYWJlbCA9IFwiZGVjbGFyYXRpb25cIl07XG4gICAgMi0-NSBbbGFiZWwgPSBcInZhci1saXN0XCJdO1xuICAgIDItPjYgW2xhYmVsID0gXCJpZGVudGlmaWVyXCJdO1xuICAgIDUtPjcgW2xhYmVsID0gXCIsXCJdO1xuICAgIDctPjggW2xhYmVsID0gXCJpZGVudGlmaWVyXCJdO1xufSIsInVybCI6Imh0dHBzOi8vY2RuLm5sYXJrLmNvbS95dXF1ZS9fX2dyYXBodml6L2MxZGZkZjhlMTNkNmRkMTdmN2ZmZTUxODQwN2YwNTIyLnN2ZyIsImlkIjoiSmxpUUciLCJtYXJnaW4iOnsidG9wIjp0cnVlLCJib3R0b20iOnRydWV9LCJjYXJkIjoiZGlhZ3JhbSJ9)
c. We can know that:

![](https://g.yuque.com/gr/latex?Follow(S)%20%3D%20%5C%7B%5C%24%5C%7D%5Csubseteq%20Follow(declaration)%5Csubseteq%20Follow(var%5Ctext-list)#card=math&code=Follow%28S%29%20%3D%20%5C%7B%5C%24%5C%7D%5Csubseteq%20Follow%28declaration%29%5Csubseteq%20Follow%28var%5Ctext-list%29&id=OK9tV)

![](https://g.yuque.com/gr/latex?First(var%5Ctext-list)%3D%5C%7Bidentifier%5C%7D%5Csubseteq%20Follow(type)#card=math&code=First%28var%5Ctext-list%29%3D%5C%7Bidentifier%5C%7D%5Csubseteq%20Follow%28type%29&id=u26ja)

![](https://g.yuque.com/gr/latex?%5C%7B'%2C'%5C%7D%5Csubseteq%20Follow(var%5Ctext-list)#card=math&code=%5C%7B%27%2C%27%5C%7D%5Csubseteq%20Follow%28var%5Ctext-list%29&id=YegF9)

Therefore, the follow set of each non-terminal is:

| non-terminal | S | declaration | var-list | type |
| --- | --- | --- | --- | --- |
| **follow set** | {$} | {$} | {',' , $} | {identifier} |


So we can construct the SLR(1) Parsing Table with the DFA and follow sets: ![20210422202137.png](./assets/1619094395187-be7e187e-58ca-443e-9c47-24cd897b777f.png)



感谢 lt 先生和 lhm 先生指出文档中的问题QWQ
