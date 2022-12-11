---


## 0 开始之前
本文是自主学习的又一尝试（虽然，实际上大多数课程都是自学的）。该学习在大二春夏学期之前进行，主要目标是为了迎合我对课程安排的一些调换。<br />本文的学习围绕《现代编译原理  C 语言描述（修订版）》（_Modern Compiler Implementation in C_）展开，本文的目录结构也基本参考这一本书的内容。由于这本书中部分内容比较难以理解，同时参考了《编译原理》（_Compilers: Principles, Techniques and Tools_）以及 [CS143](https://web.stanford.edu/class/cs143/) 的相关资料。本文结构同时也受到 CS143 的影响。（上述书籍的选择完美地避开了教学班使用的课本）<br />若无特殊说明，本文的图片来源均为上述课本或课件资料。<br />在本文中，尤其是习题部分，绿色表示仍存问题，黄色表示很不确定或者未完成的内容，红色表示完全不会。
![image.png](./assets/1612540744502-fd3a1ab6-e83f-4932-a0c0-61ea415e63eb.png)

- 参与了朋辈辅学讲解计网，**录播** 在：[https://space.bilibili.com/18777618/channel/collectiondetail?sid=288316&ctype=0](https://space.bilibili.com/18777618/channel/collectiondetail?sid=288316&ctype=0)



### Course Info.
**Assessment** 

   - Final 40%
   - Mid-Term 15%
   - Quiz 10%
   - HW 10%
   - Proj 25%
      - HW Proj*2 30%
      - Final Proj 70%


### 目录
[CP Part.1 Lexical Analysis](https://www.yuque.com/xianyuxuan/coding/cp_1?view=doc_embed)
词法分析<br />[CP Part.2 Parsing (I)](https://www.yuque.com/xianyuxuan/coding/cp_2?view=doc_embed)
语法分析 - 上下文无关文法、自顶向下分析<br />[CP Part.2 Parsing (II)](https://www.yuque.com/xianyuxuan/coding/cp_3?view=doc_embed)
语法分析 - 自底向上分析、Yacc<br />[CP Part.3 Semantic Analysis](https://www.yuque.com/xianyuxuan/coding/cp_4?view=doc_embed)
语义分析<br />[CP Part.4 Runtime Environment](https://www.yuque.com/xianyuxuan/coding/cp_5?view=doc_embed)
运行时环境<br />[CP Part.5 Code Generation](https://www.yuque.com/xianyuxuan/coding/rp9cai?view=doc_embed)
代码生成


## 1 绪论 | Introduction
![image.png](./assets/1611949919610-c1c96f99-390b-4f8f-a7ec-3f718819044d.png)
