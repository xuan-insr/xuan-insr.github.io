# 4 Statics | 静态语义

大多数编程语言（无论是编译型还是解释型）从代码到执行之间都可以分为两个阶段：**静态 (static)** 阶段和 **动态 (dynamic)** 阶段。静态阶段由 parsing（满足语法） 和 type checking（满足静态语义） 组成，以保证程序是 **well-formed** 的；动态阶段由 well-formed 程序的执行组成，如果能够正确运行，则程序是 **well-behaved** 的。

当且仅当 well-formed 的程序在执行时是 well-behaved 的，我们称这种编程语言是 **安全 (safe)** 的。