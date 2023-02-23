# 标准引用待补充

!!! abstract
    我尽可能保证文章的各种重要叙述有标准原文支撑，但为了兼顾效率，一些没有容易地找到来源的论断会暂时被放在此处表示等待补充。

    欢迎感兴趣的读者帮我找找QWQ！

- 4.1 <span class="box box-green">SOLVED</span> 重定义 `int i; int i;` 错误。见 [这个问题](https://stackoverflow.com/questions/75402077/which-subclause-of-c-standard-prohibits-redeclaration-redefinition-in-a-same)。
- 4.3 If an inline function or variable (since C++17) with external linkage is defined differently in different translation units, the behavior is undefined. 来源：[inline - cppreference](https://en.cppreference.com/w/cpp/language/inline#Notes)

- A.1 两个 extern 声明同一个变量，但类型不同是错误。