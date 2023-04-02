---
title: Week 5 - 模板 (I) - 基础知识与 STL 使用
verticalSeparator: ===
revealOptions:
  width: 1600
  height: 900
  margin: 0.04
  transition: 'fade'
  slideNumber: true
---

<link rel="stylesheet" href="custom_light.css">
<link rel="stylesheet" href="../custom_light.css">
<link rel="stylesheet" href="custom.css">
<link rel="stylesheet" href="../custom.css">

# 探索 C++

<br>

## Week 5 - 模板 (I) 基础知识与 STL 使用

---

## 后续一部分的内容安排

- 模板 (I): 核心目标是让大家能用 STL，针对此目标，引入并介绍必要的模板知识
- 模板 (II): 详细讨论 STL 的设计理念，理解泛型<!-- .element: class="fragment" -->
  - 到这里，预期大家能够具备只看 cppreference 就会用 STL 的能力<!-- .element: class="fragment" -->
- 右值引用与移动语义: 现代 C++ 的最后一座大山 (?)<!-- .element: class="fragment" -->
  - 到这里，预期大家能够具备只看 cppreference 就能看懂大多数内容的能力<!-- .element: class="fragment" -->
- 模板 (III): 关于模板的更多常见话题<!-- .element: class="fragment" -->
- 类 (IV): 继承、(运行时) 多态<!-- .element: class="fragment" -->
- 模板 (IV): 关于模板的高级话题<!-- .element: class="fragment" -->

---

## 7.1 模板

===

```c++
struct node {
    elem* val;
    struct node* next;
};
typedef struct node* linkedlist;

linkedlist create();
int size(linkedlist llist);
elem* get(linkedlist llist, int index);
void add(linkedlist llist, elem val);
// ...
```

===

```c++
struct node {
    elem* val;
    struct node* next;
};

struct linkedlist {
    struct node* llist;

    static linkedlist create();
    int size() const;
    elem* get(int index) const;
    void add(elem val);
    // ...
};
```

===

我们的需求实际上是：让我们的代码独立于具体的类型 (type-independently) 工作

我们写出一个适用于所有类型的数据结构（类）或者算法（函数）

在真正需要使用时，生成一个适用于所需要类型的实例

===

这种编程范式称为 **泛型编程 (generic programming)**

也就是说，在泛型的代码中，我们编写的并不是一个具体的类 / 函数，而是函数 / 类的一个族 (family)

或者说，我们定义了一种生成类 / 函数的模式。

===

```c++
#define elem Circle
#include "linkedlist.h"
#undef elem

#define elem Rectangle
#include "linkedlist.h"
#undef elem
```

![](2023-04-02-13-19-08.png)

===

我们当时的解决方案是，用一个 `Shape` 类作为它们的基类，然后 `using elem = Shape;` 即可

假如我们确实要维护两个不同类型的链表怎么办呢？比如需要分别维护一个 `int` 类型和 `double` 类型的链表

===

给这两个类型也找一个共同的基类——或者说，给所有类型找一个共同的基类；所有容器类（例如这里的 `linkedlist` 或者我们之前设计的 `Container`）都可以使用这个基类作为其 `elem`

这种组织方式叫做 **单根结构 (singly rooted hierarchy)**

很多面向对象的编程语言（如 Java）都使用单根结构

`Object`

C++ 并没有采用单根结构

===

`abs.h`

```c++
TYPE abs(TYPE x) { return x > 0 ? x : -x; }
```

`main.cpp`
```c++ title="main.cpp"
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

`g++ main.cpp -E > main.i`

===

`main.i`

```c++ title="main.i"
# 0 "main.cpp"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "main.cpp"

# 1 "abs.h" 1
int abs(int x) { return x > 0 ? x : -x; }
# 3 "main.cpp" 2



# 1 "abs.h" 1
double abs(double x) { return x > 0 ? x : -x; }
# 7 "main.cpp" 2


int main() {
    int x = abs(-1);
    double y = abs(-1.0);
}
```

===

```c++ title="main.cpp"
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

===

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

===

`Container_TYPE` ?

`#define a 1`

`int total = 1;` => `int tot1l = 1;` ?

===

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

===

希望 C++ 能够「允许用语言本身表达所有重要的东西，而不是在注释里或者通过宏这类黑客手段」

===

Release 3.0 中，C++ 受 Ada 的启发加入了 **模板 (template)** 机制来解决这一问题

模板将 **泛型编程 (generic programming)** 和 **模板元编程 (template metaprogramming)** 这两个编程范式引入了 C++，它们在现在发挥着非常重要的作用

---

## 7.2 模板和隐式实例化

---

## 7.3 STL 基本使用

---

## Takeaway