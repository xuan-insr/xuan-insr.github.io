# 编译原理

!!! danger ""
    我的笔记所追求的目标是有逻辑、通畅地总结知识；因此如果您在阅读过程中在任何地方发现了不容易读懂的部分，请务必在评论区或者通过其它方式告知我QWQ！非常感谢！


!!! tips
    参与了朋辈辅学讲解编译原理，**录播** 在 [这里](https://space.bilibili.com/18777618/channel/collectiondetail?sid=288316&ctype=0)


## 0 开始之前
本文是自主学习的又一尝试（虽然，实际上大多数课程都是自学的）。该学习在大二春夏学期之前进行，主要目标是为了迎合我对课程安排的一些调换。

本文的学习围绕《现代编译原理  C 语言描述（修订版）》（_Modern Compiler Implementation in C_）展开，本文的目录结构也基本参考这一本书的内容。由于这本书中部分内容比较难以理解，同时参考了《编译原理》（_Compilers: Principles, Techniques and Tools_）以及 [CS143](https://web.stanford.edu/class/cs143/) 的相关资料。本文结构同时也受到 CS143 的影响。（上述书籍的选择完美地避开了教学班使用的课本）

若无特殊说明，本文的图片来源均为上述课本或课件资料。

在本文中，尤其是习题部分：

!!! success ""
    绿色表示仍存问题
    
!!! warning ""
    黄色表示很不确定或者未完成的内容
    
!!! danger ""
    红色表示完全不会

<center>![image.png](../../assets/1612540744502-fd3a1ab6-e83f-4932-a0c0-61ea415e63eb.png){width=300}</center>

### 历年卷等相关资源

（很多来自 [求是潮课程攻略共享计划](https://github.com/QSCTech/zju-icicles/tree/master/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86) ，但是我为了方便把部分的题目和答案分开了）

- [2021wqMidterm.pdf](./res/2021wqMidterm.pdf)
- [2021wqQuiz1.pdf](./res/2021wqQuiz1.pdf)
- [2021wqQuiz2.pdf](./res/2021wqQuiz2.pdf)
- [CP MidTerm 1 A (2018).pdf](./res/CP MidTerm 1 A (2018).pdf)
- [CP MidTerm 1 Q (2018).pdf](./res/CP MidTerm 1 Q (2018).pdf)
- [CP MidTerm 2 A (unknown).pdf](./res/CP MidTerm 2 A (unknown).pdf)
- [CP MidTerm 2 Q (unknown).pdf](./res/CP MidTerm 2 Q (unknown).pdf)
- [CP MidTerm 3 A (2017B).pdf](./res/CP MidTerm 3 A (2017B).pdf)
- [CP MidTerm 3 Q (2017B).pdf](./res/CP MidTerm 3 Q (2017B).pdf)
- [CP MidTerm 4 A (2017A).pdf](./res/CP MidTerm 4 A (2017A).pdf)
- [CP MidTerm 4 Q (2017A).pdf](./res/CP MidTerm 4 Q (2017A).pdf)
- [CP MidTerm 5 (2021).pdf](./res/CP MidTerm 5 (2021).pdf)
- https://www.cc98.org/topic/5115473
- https://www.cc98.org/topic/4932042

### Assessment

   - Final 40%
   - Mid-Term 15%
   - Quiz 10%
   - HW 10%
   - Proj 25%
      - HW Proj*2 30%
      - Final Proj 70%


## 1 绪论 | Introduction

<center>![image.png](../../assets/1611949919610-c1c96f99-390b-4f8f-a7ec-3f718819044d.png)</center>

