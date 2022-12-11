![image.png](./assets/1650635466063-66a7a722-9e34-4435-a8b7-35124ca37f83.png)

## 写在前面
尝试阅读并且概括这本书！<br />每章和每节的梗概用 蓝绿底色 标明；没看懂的地方用 红色字体 标明。

### 进度

- 之前某天	0 ~ 1.3
- 22.04.22	1.3 ~ 3.1
- <br />

## 0 引言 | Preface
本章概括了全书的核心：写 semantic descriptions 从而更好地评估和设计编程语言。

本书希望让读者能够更深层次地理解编程语言。<br />这个世界上有很多种语言，而其中绝大多数都没能幸免于复杂化一些表达。<br />设计语言需要一些评估。我们更希望有一种形式化的方法去评估它，而不是将它实现之后再去评估。<br />高级语言很牛逼，比如好写和可移植性。<br />Java 这样的通用语言称为 HLLs, High-Level Languages；一些用于专门用途的语言称为 DSLs, Domain Specific。高级语言符合直觉，不需要考虑使用哪些存储之类的问题。<br />语言越抽象，compiler 越难写，同时更容易低效率。<br />有好多 HLL，也有很多乱七八糟的概念；但是这些概念深层次可能类似，而且可能有坑。<br />要评估一门语言，比写一个 compiler 更明智和有效的方法是写语义描述 semantic descriptions，这也正是本书的 topic。<br />Compiler / Interpreter 本身也提供了语义描述，但是并不适合用来评价和定义，因为实现的方式有很多种。写 semantic descriptions 优雅而合理，可以用来思考、记录、分析语言设计中的选择。我们会使用一种叫做 meta-language 的记号来帮助我们写 semantic descriptions。<br />本书考虑一系列 issue。<br />有助于让读者理解、设计语言。

## 1 Programming Languages and Their Description
本章介绍了一些基本内容，但是说实话没咋看懂。

### 1.1 Digital Computers and Programming Languages
本节阐述了本书考虑的内容：high-level languages for programming general-purpose computers.

本书 focus on 数字通用计算机。这种计算机由一个程序控制；Alan Turing 证明了其可行性。<br />不同机器支持不同功能 (ISA)，但是总能达到相同目的。<br />用低级语言编程乏味、易错。

### 1.2 The Importance of HLLs
本节阐述了高级语言的好处和一些可以支持的功能。

HLL 的好处：HLL 可以写的很大；错误易于检出和纠正；易于移植。生产力！<br />有很多 HLL，但是没有最好的；说明设计本身并不是容易的。例如功能 vs 抽象。<br />HLL 应当有数据结构化、常见的控制流、错误检测等支持。<br />如何抽象呢？要写多个语句的 asm 应当可以只用一句自然表达式实现；要有数组、结构体；list-processing (?)；垃圾回收；OOP；支持并发之类的。

### 1.3 Translators, etc.
本节指出程序需要翻译才能执行。

在 program 和 run 之间，需要 interpreter 和 / 或 compiler。<br />一些可能的优化，比如 loop 中不受影响的内容提到外面做一次计算，一些循环中的乘法可以用加法实现；这些优化会有对应 source code 的称为 source-to-source 优化。<br />也有些优化可以减少语句或者内存的使用。<br />优化应当遵守语义规则。<br />Translator 挺难写的。可以分部写。

### 1.4 Insights from Natural Languages
本节介绍了自然语言对语言学的分类并推广到编程语言；介绍了语法和语义的不同。

搞自然语言那边的 Charles Sanders Peirce 将语言学分类为 syntax, semantics, pragmatics（语法、语义、语用）。Heinz Zemanek 把这个应用到了 PL。

### 1.5 Approaches to Describing Semantics
本节阐述了描述语义的方法。

语义是语言使用者和实现者的桥梁。<br />一个 issue 是如何判断两个程序等价。<br />如何记录语义呢？

   - 翻译为同一种 known language，比如 machine code。但 machine code 的语义本身也不明确，而且不易处理。
   - Mathematical Semantics (i.e. Denotational Semantics) 数学语义 / 指称语义，将语义映射到易于处理的数学对象，优雅但复杂。
   - Operational Semantics 操作语义，核心是用一个 limited 的、易处理的 meta-language 来写一个抽象的解释器。(P9 最后一段没看懂) 一个方式是类似 mono-lingual dictionary 单语词典那样，将一种复杂的 feature 用同一种语言的更易懂的构造来解释。
   - Axiomatic Semantics 公理语义，用推理来做。

不同的语义描述可能适合不同任务；有时也可以共同使用，但是需要证明符合同一语义。<br />本书主体使用操作语义。

应该先搞 formal model 再写 compiler。11 章有一些 formal model。写出来 formal model 之后也有很多 检查对空指针解引用或者死锁的工具。<br />除了上述做语义描述的技术标准之外，还要考虑一些常用语言也可能存在的 semantic traps；formal semantic descriptions 也可以检测到这些。

做语义描述的难点是适当程度的抽象。3~9 章都会有例子介绍这些。

### 1.6 A Meta-Language
本节介绍了一点 Meta-Language。

我们用 object language 来指代我们要分析的语言；我们用 meta-language 来描述它。<br />meta-language 是一种 formal language，它应当能够描述很多种语言，而且要小，而且要容易推理表达式。<br />我们使用 VDM, Vienna Development Method 的一个子集。<br />这里我们首先介绍集合相关的符号；用集合是因为集合可以表明顺序对其并没有影响。

![image.png](./assets/1650638782424-3413b8bb-8647-4283-9d49-f21cda92987a.png)
![image.png](./assets/1650638862614-d98e0c3d-292f-479c-8e18-34695d3af79b.png)
下面这种东西表示横线上面的等价于横线下面的：
![image.png](./assets/1650639351889-ab967748-93f9-4d01-bca7-9632c4830a3a.png)

### 1.7 Further Material

#### 1.7.1 Further Reading

#### 1.7.2 Classes of Languages
本书主要聊命令式语言。逻辑式和函数式差不太多。

#### 1.7.3 Logic of Partial Functions
（没太看懂）<br />有一些情况下，一些值并不能取到有效值；例如 `5/0` 这样的未定义的值。<br />下图中 `*` 就表示那种没有办法表示为 truth value 的值。
![image.png](./assets/1650639117838-d297f7dd-1dce-4435-abbc-67320fe2360c.png)

## 2 Delimiting a Language
本章介绍了具体语法和抽象语法的描述。

本书主要做语义的描述和设计，但是我们首先需要区分 syntax 和 semantic 的分界。<br />对于给定的程序，我们有必要在讨论其语义之前先检查它是不是语法所允许的。Concrete syntax 用到一些额外的 marks，而 abstract syntax 则不需要额外的 symbol。

### 2.1 Concrete Syntax
本节主要讲了 BNF 和 EBNF，略。

### 2.2 Abstract Syntax
本节介绍了 VDM sequence notation，并给出了抽象语法的一个示例。

我们考虑更多的 VDM 标记，这次是关于 sequences（即 lists）的一些新记号：
![image.png](./assets/1650639747719-1f91ef8f-8d38-4829-83ed-50408e5d4040.png)
我们尝试用 VDM 来表示一个函数，例如检查一个列表里是否有重复元素。<br />根据 VDM 的标准写法，我们首先应该给出函数签名：![](https://cdn.nlark.com/yuque/__latex/edf184394e6a8cbfc7f2651de62dea69.svg#card=math&code=uniquel%3A%20X%5E%2A%20%5Cto%20%5Cmathbb%7BB%7D&id=B4IHg)，即表示从类型 ![](https://cdn.nlark.com/yuque/__latex/94e79ad0c1aabeafef9e2fc4af6adf66.svg#card=math&code=X&id=AXQGN)的有限 sequence 到 boolean 的一个 function。<br />下面给出函数描述：<br />![](https://cdn.nlark.com/yuque/__latex/d9d077b587c3029f24cc470aa9d6924f.svg#card=math&code=uniquel%28s%29%20%5Ctriangleq%20%5Cforall%20i%2C%20j%20%5Cin%20%5Ctext%7Binds%20%7D%20s%20%5Ccdot%20i%20%5Cneq%20j%20%5CRightarrow%20s%28i%29%20%5Cneq%20s%28j%29&id=XNZo3)
注：![](https://cdn.nlark.com/yuque/__latex/e48856bc610e3120970a7aed65c63597.svg#card=math&code=%5Ctriangleq&id=N4ilM)在书中其实是 ![](https://cdn.nlark.com/yuque/__latex/9f9a1c23e54731ecf90ee304d8bd198e.svg#card=math&code=%5Cunderline%5Ctriangle&id=NfAHq)，但是打出来不好看。<br />当然也可以描述成：<br />![](https://cdn.nlark.com/yuque/__latex/6fb20c4e10f637dded99bbd5e1ab8013.svg#card=math&code=uniquel%28s%29%20%5Ctriangleq%20%5Ctext%7Blen%20%7D%20s%20%3D%20%5Ctext%7Bcard%20elems%20%7Ds&id=aGZ3f)
这种产生 boolean 结果的函数也称为 predicates (谓词)。

很多编程语言也有 record / struct，可以表示为
![image.png](./assets/1650641034835-4fbc5a3b-2cb4-47b9-a8ed-d31bd76b0013.png)
这种东西有默认的构造函数，即：<br />![](https://cdn.nlark.com/yuque/__latex/d964ad5107e483f123798d56fb493e61.svg#card=math&code=mk%5Ctext-Example%20%3A%20X%5Ctimes%20Y%5Cto%20Example&id=hPB28)
因此 ![](https://cdn.nlark.com/yuque/__latex/0d7d5a4c4431e4c068060b7c7d91d6c7.svg#card=math&code=Example&id=VRugp)类的所有 object 的集合就可以表示为：<br />![](https://cdn.nlark.com/yuque/__latex/dc0a5ca74daca7d8f5b9bea6f5759e20.svg#card=math&code=Example%20%3D%20%5C%7Bmk%5Ctext-Example%28x%2C%20y%29%5C%20%7C%5C%20x%5Cin%20X%20%5Cland%20y%20%5Cin%20Y%5C%7D&id=rNEnL)

我们可以用 selectors 来访问 struct 的元素，例如 ![](https://cdn.nlark.com/yuque/__latex/e215f3d3c86ca3f99c3bb9ea2b06d286.svg#card=math&code=e.field%5Ctext-1&id=Iw9HX)。

我们可以用 ![](https://cdn.nlark.com/yuque/__latex/0180f724eb1525596664758a7bbd6440.svg#card=math&code=%7C&id=GX9MJ)来表示 union。

下面我们就可以给出抽象语法描述的一个例子：
![image.png](./assets/1650641317883-17cb9b4c-1b9e-4bb7-bd24-b9eb4df91a22.png)

举一个例子来应用：
![image.png](./assets/1650641382392-6197b570-ec9a-4a6b-ba82-d8456bf941eb.png)


### 2.3 Further Material
不看了

## 3 Operational Semantics

### 3.1 Operational Semantics
又来新 notation 了！这次是关于 map 的：
![image.png](./assets/1650641511715-cd255940-eb35-415d-8185-6c775f993e86.png)
![](https://cdn.nlark.com/yuque/__latex/7c012b3d3356f1e65ee18c1233e5f04b.svg#card=math&code=D%5Cstackrel%7Bm%7D%7B%5Clongrightarrow%7DR&id=k5012)表示从 domain 集合![](https://cdn.nlark.com/yuque/__latex/558270b7f0a90c3c286b860273d106a0.svg#card=math&code=D&id=ymFyg)到 range 集合![](https://cdn.nlark.com/yuque/__latex/dd1caa3f2e1582dab2cf9bfdb21b7556.svg#card=math&code=R&id=GbNL6)的一个 map![](https://cdn.nlark.com/yuque/__latex/4760e2f007e23d820825ba241c47ce3b.svg#card=math&code=m&id=tP2Cs)。<br />如果![](https://cdn.nlark.com/yuque/__latex/56c1b0cb7a48ccf9520b0adb3c8cb2e8.svg#card=math&code=d&id=YLG9r)不存在，那么![](https://cdn.nlark.com/yuque/__latex/98f3e06c327be6ec7cc3bb5e0930d1bb.svg#card=math&code=m%28d%29&id=F6lfh)的结果是 undefined。

容易理解，sequence 是一种特殊类型的 map，例如 ![](https://cdn.nlark.com/yuque/__latex/409b63e1130820a0e6621e9db867b191.svg#card=math&code=T%5E%2A&id=eAo8V)可以被认为是![](https://cdn.nlark.com/yuque/__latex/cc182376a50303dca72f9f32c0052590.svg#card=math&code=%5Cmathbb%7BN%7D%5Cstackrel%7Bm%7D%7B%5Clongrightarrow%7DT&id=tBqLn)。

程序中的 map，例如符号表，会有很多不同的状态，我们将这些状态的集合，即这些 map 的集合记为![](https://cdn.nlark.com/yuque/__latex/a99c3dabbb2eeee45801b2b7d343cc65.svg#card=math&code=%5CSigma&id=ESOJq)，用![](https://cdn.nlark.com/yuque/__latex/788df1ba344b3092def7590d1be6b4d4.svg#card=math&code=%5Csigma&id=yyQO6)表示其中的实例，例如![](https://cdn.nlark.com/yuque/__latex/a76ebbe99d5ff0965f9efb9c0fee82d9.svg#card=math&code=%5C%7Bi%5Cmapsto2%2C%20j%5Cmapsto3%5C%7D&id=c06uU)。

这样我们就可以定义出函数 ![](https://cdn.nlark.com/yuque/__latex/b8ca9fffa5f79d393c7d797508b58d0c.svg#card=math&code=eval&id=yJdCL)：
![image.png](./assets/1650642006046-11355357-9472-4701-8b3c-eccd8fc916c6.png)
因此 ![](https://cdn.nlark.com/yuque/__latex/b4db8bb4f362dfea374b7df4e04dd85f.svg#card=math&code=eval%28mk%5Ctext-BinArithExpr%281%2C%20%5Ctext%7BP%7D%5Cfootnotesize%20%5Ctext%7BLUS%7D%5Cnormalsize%20%2C%20i%29%2C%20%5C%7Bi%5Cmapsto2%2C%20j%5Cmapsto3%5C%7D%29%20%3D%203&id=kukhN)

我们可以进一步用 cases 代替 if 判断：
![image.png](./assets/1650642355939-abc13870-48e9-4c1f-8080-fb2bcd5d1b35.png)
这样做的副作用之一是不再需要使用 selector。

（本节未完）
