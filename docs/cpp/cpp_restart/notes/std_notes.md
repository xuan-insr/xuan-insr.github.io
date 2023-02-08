# C++ 语言标准阅读记录

!!! abstract
    本文记录阅读 [Standard for Programming Language C++](https://timsong-cpp.github.io/cppwp/n4868) 过程中的部分内容。
    
    !!! note
        这里阅读的 standard 版本并不是最新的版本；其对应的仓库在 https://github.com/timsong-cpp/cppwp。最新版本在 http://eel.is/c++draft。
    
    !!! warning
        这里的记录并不完整，当省略某一节或者某节的部分内容时也不一定会专门说明。

## 1 Scope

## 2 Normative references

## 3 Terms and definitions

这里定义了一些术语。例如 access, signature, undefined behavior, unspecified behavior 等。

**Undefined behavior** 定义为「behavior for which this document imposes no requirements」，其具体行为包括产生不可预测的情况（且不需要给出诊断信息）、终止编译或运行（但需要给出诊断信息）。^[defns.undefined](https://timsong-cpp.github.io/cppwp/n4868/defns.undefined)^

**Unspecified behavior** 定义为「在 well-formed 的程序结构和正确的数据中的、depends on implementation 的行为」。例如，`int x = f() + g();` 中 `f()` 和 `g()` 的运算顺序。^[defns.unspecified](https://timsong-cpp.github.io/cppwp/n4868/defns.unspecified)^

**Implementation-defined behavior** 定义为「在 well-formed 的程序结构和正确的数据中的、depends on implementation 且在对应 implementation 的文档中说明的行为」。^[defns.impl.defined](https://timsong-cpp.github.io/cppwp/n4868/defns.impl.defined)^

这里还定义了 **valid but unspecified state**，这个会在移动语义那里用到。

## 4 General principles

4.1 介绍了合规的实现应当满足的条件。

4.2 介绍了全文的结构。

4.3 介绍了全文中 syntax notation 的使用。

## 5 Lexical conventions

本节给出了 C++ 的词法。其中 5.1 和 5.2 介绍了 C++ 的编译过程。

## 6 Basics

### 6.1 Preamble

本节介绍了一些基本概念。

**Entity**。An entity is a value, object, reference, structured binding, function, enumerator, type, class member, bit-field, template, template specialization, namespace, or pack.

!!! note
    这里还没给出 object 的定义。

**Name**。一个 name 要么代表一个 entity，要么代表一个 label。如果一个 name 代表 entity，那么它由一个 declaration 引入。如果一个 name 代表 label，那么它由一个 goto statement 或者 labeled-statement 引入（后者的名字也是用来 goto 的）。

### 6.2 Declarations and definitions

这一节说明了哪些 declaration 同时也是 definition。注意，不存在不是 declaration 的 definition。

这一节也说明，在 definition 中，object 的类型不应当是 incomplete type 或者 abstract class，或者它们的数组。

这一节还提到了出现在 `extern "C" {}` (i.e. linkage-specification) 大括号中不影响 declaration 是否是 definition 的判断。

### 6.3 One-definition rule

No translation unit shall contain more than one definition of any variable, function, class type, enumeration type, template, default argument for a parameter (for a function in a given scope), or default template argument.



