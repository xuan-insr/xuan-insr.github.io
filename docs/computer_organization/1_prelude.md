# 写在前面

!!! danger ""
    我的笔记所追求的目标是有逻辑、通畅地总结知识；因此如果您在阅读过程中在任何地方发现了不容易读懂的部分，请务必在评论区或者通过其它方式告知我QWQ！非常感谢！

这是计算机组成课程的学习记录。

使用的课本是 _Computer Organization and Design - The Hardware / Software Interface (RISC-V Edition)_：

<center>![image.png](../../../assets/1654452339796-a855e535-5361-4b3f-96bc-f084bb514e00.png){width=300}</center>

!!! warning "说明"
    我自认为在 **3 Arithmetic**, **4 Processor**, **5 Cache** 三章中的整理和讲解是非常详细的，如果这些部分存在看不懂的地方，请务必联系我。

    但是，计组课程本身在 **2 Instructions** 的部分讲解了很多关于汇编程序的知识；但是我之前在汇编语言和计算机系统概论等课程中已经学习过了这些知识，因此在本章中只整理了 RISC-V 的指令集和一些约定，省略了关于函数调用、递归的一些内容。

    同时，由于时间原因，**1 Overview** 和 **6 I/O** 两章的内容不完整。暂时没有补全计划。

!!! summary "课程速览"
    - Chapter1: Computer Abstraction and Technology
    - **Chapter 2: Instructions: Language of  the Computer**
    - **Chapter 3: Arithmetic for Computers**
    - **Chapter 4:The Processor：Datapath and Control**
    - **Chapter 5:Large and Fast:  Exploiting Memory Hierarchy**
    - Chapter 6: Parallel processor from client to Cloud (选讲，非考试内容)
    - Appendix: Storage, Networks, and Other Peripherals (Ch8 of Version 3,了解概念)

    > 加粗为核心内容。


## 1 Intro & Misc

- **Moore's Law**: Integrated circuit resources double every 18-24 months.
- KB = 103 B, KiB = 210 B
- K M G T P E Z Y
- **Response Time / Execution Time**	从程序开始到结束的时间
- **Throughput / Bandwidth**	单位时间内完成的任务数量
- **Performance**	可以定义为 $\cfrac{1}{\text{Response Time}}$
- **Amdahl Law**   $T_{\text{improved}} = \cfrac{T_{\text{affected}}}{\text{Improvement Factor}}+T_\text{unaffected}$ [🔗 Wiki](https://zh.wikipedia.org/wiki/%E9%98%BF%E5%A7%86%E8%BE%BE%E5%B0%94%E5%AE%9A%E5%BE%8B)

- ~~……不是很想学了 再说吧~~ 那我帮你学

- Eight Great Ideas
    - Design for Moore’s Law （设计紧跟摩尔定律）
    - Use Abstraction to Simplify Design (采用抽象简化设计)
    - Make the Common Case Fast (加速大概率事件)
    - Performance via Parallelism (通过并行提高性能)
    - Performance via Pipelining (通过流水线提高性能)
        - 换句话说就是，每个流程同时进行，只不过每一个流程工作的对象是时间上相邻的若干产品；
        - 相比于等一个产品完全生产完再开始下一个产品的生产，会快很多；
        - 希望每一个流程的时间是相对均匀的；
    - Performance via Prediction (通过预测提高性能)
        - 例如先当作 `if()` 条件成立，执行完内部内容，如果后来发现确实成立，那么直接 apply，否则就再重新正常做；
        - 这么做就好在，预测成功了就加速了，预测失败了纠正的成本也不高； 
    - Hierarchy of Memories (存储器层次)
        - Disk / Tape -> Main Memory(DRAM) -> L2-Cache(SRAM) -> L1-Cache -> Registers
    - Dependability via Redundancy (通过冗余提高可靠性)
        - “备胎”；


