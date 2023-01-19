# C++ 零散内容记录

!!! abstract
    看到的一些讨论、知识，或者需要学的一些内容。

## TODO

- [ ] 初始化
- [ ] value category
- [ ] 右值引用、移动语义
- [ ] placement new
- [ ] 模板
- [ ] POD
- [ ] 常量构造
- [ ] inline
- [ ] stream

## 关于 UB 和指针等的大讨论

<center>![](2023-01-16-23-55-30.png){width=800}</center>

- [原帖](https://loj.ac/d/3679)
- [我的尝试](https://godbolt.org/z/3Thssx941)
- [下面的作者给的例子](https://godbolt.org/z/TWrvcq)
- [Pointers Are Complicated, or: What's in a Byte?](https://www.ralfj.de/blog/2018/07/24/pointers-and-bytes.html) 本文还有后续
- ["What The Hardware Does" is not What Your Program Does: Uninitialized Memory](https://www.ralfj.de/blog/2019/07/14/uninit.html)
- [With Undefined Behavior, Anything is Possible](https://raphlinus.github.io/programming/rust/2018/08/17/undefined-behavior.html)
- [A Guide to Undefined Behavior in C and C++](https://blog.regehr.org/archives/213)
- 引文 [Taming Undefined Behavior in LLVM](https://www.cs.utah.edu/~regehr/papers/undef-pldi17.pdf)
- 引文 [Reconciling High-Level Optimizations and Low-Level Code in LLVM](https://sf.snu.ac.kr/publications/llvmtwin.pdf)

### 为什么要有 UB

<center>![](2023-01-16-23-45-33.png){width=800}</center>

Src: https://www.ralfj.de/blog/2018/07/24/pointers-and-bytes.html

