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


## 1 Intro & Misc

- **Moore's Law**: Integrated circuit resources double every 18-24 months.
- KB = 103 B, KiB = 210 B
- K M G T P E Z Y
- **Response Time / Execution Time**	从程序开始到结束的时间
- **Throughput / Bandwidth**	单位时间内完成的任务数量
- **Performance**	可以定义为 $\cfrac{1}{\text{Response Time}}$
- **Amdahl Law**   $T_{\text{improved}} = \cfrac{T_{\text{affected}}}{\text{Improvement Factor}}+T_\text{unaffected}$
- ……不是很想学了 再说吧

