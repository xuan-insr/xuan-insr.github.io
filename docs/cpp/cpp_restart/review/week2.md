# Week 2 思考题

!!! abstract
    思考题旨在提出场景帮助大家了解一些比较零碎的知识。这些内容比较简单且没有那么重要，因此没有放在课程内容中。

## 本周内容一览

- 类的定义
    - 定义引入新的类型
    - class-key 通常不必要
- 声明和定义
    - 定义是声明的一种    
- 类的成员
    - type alias
    - `this`
- 函数内联
- 构造函数
    - 建立起某种「保证」
    - 如何无参或有参地构造对象
    - `new`, `delete`, `new[]`, `delete[]`
    - implicitly-declared default constructor
    - `= default;`, `= delete`
    - member initializer lists
    - delegating constructor
    - default member initializer
- 函数默认参数和函数重载
    - 重载解析
    - 为什么 C++ 引入了 `nullptr`
- 析构函数
    - 用来回收资源
    - 为什么析构函数无法重载
- 构造和析构的时机和顺序
    - lifetime
    - storage duration
        - automatic
        - static
        - dynamic
    - 构造和析构的时机和顺序

## 思考题

!!! note
    在「思考题」部分，我们提出场景帮助大家了解一些比较零碎的知识。

    大家可以尝试通过搜索或者查阅 [cppreference](https://en.cppreference.com/w/) 来找到这些问题的答案。我们也会提供答案供参考。

### 1 Elaborated type specifiers

在 C 语言中，这样的定义是合法的：

```c
struct x { /* something */ };

int x;
```

这里的 `x` 不会引起歧义，因为 C 语言规定使用结构体的时候必须带上 `struct` 关键字。因此 `x` 就使用的是整型变量，而 `struct x` 使用的就是结构体。

但是，C++ 为了使得用户定义的类不是二等公民，允许用户不使用 `class-key` 即 `struct` 和 `class`。

**问题** ：在 C++ 中如何解决上面的歧义问题呢？

答案请参看 [4.1 类的定义](../../4_class_1/#41-%E7%B1%BB%E7%9A%84%E5%AE%9A%E4%B9%89) 中的「Note」块。

### 2 nested-name-specifier

课程中，我们看到了类的定义的形式：

![](2023-03-06-22-55-44.png)

**问题** ：这里的「nested-name-specifier」是什么呢？

答案请参看 [4.1 类的定义](../../4_class_1/#41-%E7%B1%BB%E7%9A%84%E5%AE%9A%E4%B9%89)。

### 3 name equivalence

假如有这样的定义：

```c++
struct X { int a; };
struct Y { int a; };
X a1;
Y a2;
int a3;
```

复习 C 语言中结构体的内存布局。我们可以得知，`a1`, `a2`, `a3` 的内存布局是一致的。

**问题** ：请问 `a1 = a2;` 或者 `a1 = a3;` 的赋值在 C/C++ 中是合法的吗？

答案请参看 [4.1 类的定义](../../4_class_1/#41-%E7%B1%BB%E7%9A%84%E5%AE%9A%E4%B9%89)。

### 4 Forward Declaration

请看下面的代码：

```c++ linenums="1"
struct Y {
    X* ptr;   // Error: unknown X
    X* foo();
};
struct X {
    Y* ptr;
    Y* bar();
};
```

在这段代码中，`Y` 和 `X` 分别有一个成员，是指向对方类型的指针。我们可以看到，第 2 行有一个编译错误，因为此时 `X` 是一个未知的名字。

**问题** ：请问这种情况在 C++ 中是否有解决方案呢？如果有，是什么呢？

答案请参看 [4.1 类的定义](../../4_class_1/#41-%E7%B1%BB%E7%9A%84%E5%AE%9A%E4%B9%89) 中的「Forward Declaration」块。

请注意理解「incomplete type」的含义以及相关限制。

### 5 Injected Class Name

我们在课程中提到，类的定义引入新的类型。那么，这个类型是从何处开始被引入的呢？是从定义结束后被引入的吗？

事实上并不是的，否则这段代码的第 2 行就会像前面那个问题的代码一样报出 unknown `Node` 的编译错误：

```c++ linenums="1"
struct Node {
    Node * next;
    // ...
};
```

**问题** ：C++ 中是如何给出相关规定的？结合上一个问题的答案考虑，下面的代码是合法的吗：

```c++
struct Node {
    Node next;
    // ...
};
```

答案请参看 [4.1 类的定义](../../4_class_1/#41-%E7%B1%BB%E7%9A%84%E5%AE%9A%E4%B9%89) 中的「Injected Class Name」块。

### 6 关于 `Foo f = Foo();`

**问题** ：`Foo f = Foo();` 的 `Foo()` 是调用构造函数的函数调用表达式吗？

作为一个提示，我们考虑这样一个事实：如果把一个函数的构造函数放在类外定义，我们需要写 `Foo::Foo` 作为标识符：

```c++
struct Foo { Foo(); };
Foo::Foo() { puts("ctor called"); }
```

那么，假如 `Foo()` 是函数调用表达式的话，为什么不需要写 `Foo::Foo()` 呢？

顺着这个思路，大家可以尝试写 `Foo f = Foo::Foo();`，看看会发生什么！

答案请参看 [4.3 构造函数](../../4_class_1/#43-构造函数) 中的「Foo() 是调用构造函数的函数调用表达式吗？」块。

### 7 关于 implicitly-declared default ctor & dtor

考虑这个问题：

```c++
struct Foo { Foo(int){} };
class Bar { Foo f; };
```

即，`Foo` 类型没有 default constructor（即可以无参调用的构造函数）；而 `Bar` 类型中有一个 `Foo` 类型的子对象 `f`。`Bar` 类型并没有提供构造函数。

根据我们所说，如果没有提供构造函数，则编译器自动生成一个 implicitly-declared default constructor；但是这里自动生成的构造函数并不能完成 `f` 的初始化。这种情况怎么办呢？

类似地，考虑以下几个场景：

`Foo` 的默认构造函数是有歧义的：

```c++
struct Foo { 
    Foo(){}
    Foo(int x = 1){}
};
class Bar { Foo f; };
```

`Foo` 的析构函数是 deleted 的：

```c++
struct Foo { ~Foo() = delete; };
class Bar { Foo f; };
```

`Foo` 的析构函数是 private 的：

```c++
class Foo { ~Foo() = default; };
class Bar { Foo f; };
```

或者，这个问题可以对称延伸到析构函数：

```c++
class Foo { ~Foo() = default; };
struct Bar { 
    Foo f; 
    Bar(){}
};
```

在这些时候，会发生什么事呢？

答案请看 [4.4 析构函数](../../4_class_1/#44-析构函数) 末尾的「defaulted ctor & dtor 被 delete 的情况」块。