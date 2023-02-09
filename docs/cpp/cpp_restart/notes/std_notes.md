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

给出了 **potential evaluated** 的定义：一个 expression 或者 conversion 是 potential evaluated 的，除非它：是一个 **unevaluated operand** 或其 subexpression；或者是一个 initialization 中的 conversion 或 conversion sequence。定义了 **potential results** 的集合。

所谓 **unevaluated operand** 或者 **unevaluated context** ^[expr.context#1](https://timsong-cpp.github.io/cppwp/n4868/expr.context#1)^，是指类似于 `sizeof(foo())` 之类的使用中的 `foo()`。更具体的可以看这里：https://stackoverflow.com/a/35088909/14430730

**potential evaluated** 的 potential，是考虑到类似 `true ? expr1 : expr2` 中，`expr2` 虽然并不会实际被计算，但这里仍然认为它是 potential evaluated 的。

给出了一个函数 **named by** 一个 expression 或 conversion 的定义。

**potential evaluated** 和 **named by** 的定义是为了方便定义 **odr-used**，即 One-Definition Rule Used。这个定义的主要目的是：Every program shall contain exactly one definition of every non-inline function or variable that is odr-used in that program outside of a discarded statement; no diagnostic required. 大意就是说，这些东西必须得有个定义；除非它在 **discarded statement** 里。如果没有的话就是 UB，且编译器不需给出诊断信息。See Also: https://stackoverflow.com/questions/19630570/what-does-it-mean-to-odr-use-something

所谓 **discarded statement**，在 [[stmt.if#2](https://timsong-cpp.github.io/cppwp/n4868/stmt.if#2)] 定义，大意是 `if constexpr` 里没有走的那个分支。

基本上来说，如果一个 variable 或者 structured binding 在 potential evaluated expression 里出现了，那它就是 odr-used 的；如果一个函数 named by 某个 potential evaluated expression or conversion，那么它也是 odr-used 的；任何非 pure 的 virtual member function 是 odr-used 的；另外类的 non-placement (de)allocation 函数被 ctor / dtor 的定义 odr-used；类的 assignment operator function、ctor、dtor 在一定情况下也会 odr-used。

定义了 local entity 在 declarative region **odr-usable** 的条件；如果不满足但是在 declarative region 被 odr-used 了，那么程序是 ill-formed 的。

!!! danger ""
    看到 https://timsong-cpp.github.io/cppwp/n4868/basic#def.odr-11 了，但是我觉得我应该先看后面的。这里先放放。

