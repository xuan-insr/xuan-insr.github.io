# 7 模板

## 7.1 引入

在介绍 OOP 的章节中，我们讨论过一个链表的实现和使用，我们面临过这样的问题：

```c++ linenums="1"
#define elem Circle
#include "linkedlist.h"
#undef elem

#define elem Rectangle
#include "linkedlist.h"
#undef elem
```

<center>![](2023-02-06-21-40-36.png){width=500}</center>

我们当时的解决方案是，用一个 `Shape` 类作为它们的基类，然后 `using elem = Shape;` 即可。

不过，假如我们确实要维护两个不同类型的链表怎么办呢？比如需要分别维护一个 `int` 类型和 `double` 类型的链表，我们如何能够完成这一任务呢？

一种想法是，给这两个类型也找一个共同的基类——或者说，给所有类型找一个共同的基类；所有容器类（例如这里的 `linkedlist` 或者我们之前设计的 `Container`）都可以使用这个基类作为其 `elem`。这种组织方式叫做 **单根结构 (singly rooted hierarchy)**。很多面向对象的编程语言（如 Java）都使用单根结构，它们用一个叫做 `Object` 的类作为所有其他类的基类。不过，出于类型安全性和运行时效率的考量，C++ 并没有采用单根结构。我们会在继承相关章节中讨论单根结构的优劣。

那么，在 C++ 中，我们如何解决前面的问题呢？我们先考虑用 C 语言如何解决——毕竟如我们之前讨论的，在 C++ 的早期，C++ 的语法特性最终都要翻译到 C 来支持。作为一个简化，我们先看一个关于函数的例子：

```c++ title="abs.h"
TYPE abs(TYPE x) { return x > 0 ? x : -x; }
```

```c++ title="main.c"
#define TYPE int
#include "abs.h"
#undef TYPE

#define TYPE double
#include "abs.h"
#undef TYPE

int main() {
    int x = abs(-1);
    double y = abs(-1.0);
}
```

通过 `g++ main.c -E > main.i` 命令（`-E` 表示只完成预处理），我们得到下面的结果：

```c++ title="main.i"
# 0 "main.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "main.c"

# 1 "abs.h" 1
int abs(int x) { return x > 0 ? x : -x; }
# 3 "main.c" 2



# 1 "abs.h" 1
double abs(double x) { return x > 0 ? x : -x; }
# 7 "main.c" 2


int main() {
    int x = abs(-1);
    double y = abs(-1.0);
}
```

可以看到，和我们的预期一致，这里生成了 `abs` 两个版本的重载，分别对应 `int(int)` 和 `double(double)` 的版本。

而面对类的问题，这个事情变得更加不优雅起来——因为类不能「重载」，即不允许同名的类有两个不同的定义。我们必须在类名中也加入 `TYPE` 元素：

```c++ title="container.h"
#if defined(TYPE)
#define JOIN_(a, b) a ## b
#define JOIN(a, b) JOIN_(a, b)
#define NAME JOIN(Container_, TYPE)

class NAME {
    TYPE * val;
};

#undef JOIN_
#undef JOIN
#undef NAME
#endif
```

（关于上面这段代码为什么要写的这么麻烦，可以参考 [这个回答](https://stackoverflow.com/a/51161267/14430730)。基本原因是，如果我们写 `Container_TYPE`，那么 `#define TYPE int` 不会导致这个名字被替换为 `Container_int`，因为宏替换只替换完整的 token，而不会替换其中的一部分） 

```c++ title="main.c"
#define TYPE int
#include "container.h"
#undef TYPE

#define TYPE double
#include "container.h"
#undef TYPE

int main() {
    Container_int ci;
    Container_double cd;
}
```

预处理完成后，得到（删除了不重要的内容）：

```c++ title="main.i"
class Container_int {
    int * val;
};
class Container_double {
    double * val;
};

int main() {
    Container_int ci;
    Container_double cd;
}
```

这样，我们就实现了 `Container` 类用于两种或者多种不同类型的目标了。

但是，显然这样的写法是丑陋的，以及容易出错。回顾之前 BS 说过的，希望 C++ 能够「允许用语言本身表达所有重要的东西，而不是在注释里或者通过宏这类黑客手段」。那么，C++ 如何支持这种让一个函数或类适配多种不同类型的目标呢？

在 Release 3.0 中，C++ 受 Ada （一种编程语言）的启发加入了 **模板 (template)** 机制来解决这一问题。事实上，BS 反思说这么晚才引入模板机制是一个错误，因为模板远比 Release 2.0 中引入的多继承之类的特性重要。的确，模板将 **泛型编程 (generic programming)** 和 **模板元编程 (template metaprogramming)** 这两个编程范式引入了 C++，它在现在发挥着非常重要的作用。我们分别介绍这两种编程范式。

## 7.2 模板与泛型编程

泛型编程 (generic programming) 是一种编程范式，它是针对传统类和函数的一种抽象。其核心在于：在泛型的类或函数中使用到的类型是暂未指定的；它针对所有



模板元编程

---

定义放在类外还是类内

## ▲ auto & return type deduction

!!! note
    除了 DnE 等在首页提及的资料，以及文中附有链接的资料外，本文还参考了如下资料：

    - [[History of C++] Templates: from C-style macros to concepts](https://belaycpp.com/2021/10/01/history-of-c-templates-from-c-style-macros-to-concepts)
    - [Ceneric Programming | Wikipedia](https://en.wikipedia.org/wiki/Generic_programming)