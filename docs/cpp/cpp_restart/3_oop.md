# 3 面向对象程序设计 | Object-Oriented Programming

在上一节中，我们讨论了编程范式和抽象的相关内容。而我们要介绍的 OOP 也是一种编程范式；它在结构化程序设计的基础上做了进一步的抽象。

我们来考虑这样一个情景。假如我们和队友一起做大程，想要做一个绘图板。在这个工程中，会有一些地方要使用到线性表 (list)。我们知道，线性表是一种抽象数据结构 (ADT, Abstract Data Type)；它能够有序地存放若干数据，数据是可以有重的；它支持的操作可能包括创建表、获取大小、插入元素、删除元素、访问元素等。

??? info "如果不知道什么是线性表或者抽象数据结构"
    **抽象数据结构** 是数据类型的一种抽象模型。
    
    我们知道，数组和链表都可以实现有序地存放若干可重数据的功能，它们支持的操作也类似，唯一的区别是其内部实现和这些操作的复杂度不同。但是，有时使用者或者系统的设计者并不需要关心具体的实现，而只需要知道这个类型能够提供哪些功能就可以了。这其实就和我们上一节提到的「抽象」的含义一致。

    也就是说，数组和链表都是具体的数据结构，但它们提供的功能是一致的。因此，我们将它们抽象为同一种 ADT，即线性表。

线性表的常见实现方式包括数组 (array list) 和链表 (linked list)，我们和队友分别实现一种。我们可能会分别写出这样的代码：

（下面的 `elem` 是线性表元素的类型，例如 `typedef Shape elem`。）

链表的版本 (可以玩一下 https://godbolt.org/z/GYWjsKhbM)：

```c linenums="1"
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

数组的版本（可以玩一下 https://godbolt.org/z/39G916Yq5）：

```c linenums="1"
#define MAX_SIZE 1024

struct _arraylist {
    elem* val[MAX_SIZE];
    int size;
};
typedef struct _arraylist* arraylist;

arraylist create();
int size(arraylist alist);
elem* get(arraylist alist, int index);
void add(arraylist alist, elem val);
// ...
```

它们单独使用都没什么问题。但是，当我们把这两份代码 include 到一起时就发生了错误！因为 C 语言并不允许同名函数有不同类型的版本：

<center>![](2023-02-04-22-28-48.png){width=600}</center>

*[ADT]: Abstract Data Type，抽象数据类型