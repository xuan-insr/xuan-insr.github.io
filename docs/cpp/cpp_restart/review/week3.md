# Week 3 思考题

!!! abstract
    思考题旨在提出场景帮助大家了解一些比较零碎的知识。这些内容比较简单且没有那么重要，因此没有放在课程内容中。

## 本节内容一览

- 拷贝赋值运算符
    - 解决「非平凡拷贝」的问题
    - `Foo & Foo::operator=(const Foo &);`
    - 防止 self-assignment
    - `= default;`, `= delete`
    - 不可见时不能赋值
- 运算符重载
    - 让运算符适配自定义类型
    - 可以是成员或者全局
    - 友元
- 引用
    - 解决运算符重载按引用传参问题
    - 可以作为参数或者返回值
    - 类似于包装了的 `Foo * const`，但是不一定占内存
    - `const Foo &` 可以绑定临时对象
    - 重载解析
    - 类的引用成员和 const 成员的初始化
- I/O Stream
    - `cin`, `cout` 的使用
    - 对 `operator<<` 和 `operator>>` 的重载

## 思考题

### 1 `++` 和 `--` 的重载

`++` 和 `--` 既可以作为前缀，也可以作为后缀；在运算符重载时如何区分呢？

由于其他的单目运算符都是前缀，因此 C++ 规定 `Foo::operator++()` 和 `operator++(Foo)` 用来处理前缀的 `++`，而后缀的 `x++` 会调用 `x.operator++(0)` 或者 `operator++(x, 0)`，即作为后缀时，编译器通过让一个额外的参数 `0` 参与重载解析。即：

```c++
Foo operator++(Foo right);      /* prefix  */
Foo operator++(Foo left, int);  /* postfix */

class Bar {
    Bar operator++();       /* prefix  */
    Bar operator++(int);    /* postfix */
};
```

### 2 运算符重载的限制

为什么对 `=` (assignment), `()` (function call), `[]` (subscript), `->` (member access) 的重载必须是成员呢？

运算符重载是否有其他限制，例如能不能添加用户自定义的运算符，比如 `**` 呢？能不能更改运算符的操作数，或者给运算符增加默认参数呢？

请大家自行查阅资料回答上述问题。部分解答可以在 [运算符重载](../../5_class_2/#%E5%8F%8B%E5%85%83) 一节的「一些限制」块中找到。

### 3 矩阵的 `operator[]`

假如我们有这样的定义：

```c++
const int M = 100;
class Matrix {
    int data[M][M];
};
```

如果我们希望能够通过运算符重载方便地访问 `mat.data[x][y]`，就像对于 `Container` 类我们可以通过 `c[i]` 访问 `c.data[i]` 那样，应该怎么办呢？

请大家自行查阅资料回答上述问题。部分解答可以在 [引用作为返回值](../../5_class_2/#引用作为返回值) 一节的「关于自定义矩阵的 `operator[]`」块中找到。

### 4 Keyword arguments

Keyword arguments 或者 Named Parameter Idiom 是指根据参数的名字而非参数的位置来传参。这种机制在 C 和 C++ 中并不支持，它们只支持按位置传参。Python 之类的语言是允许这种传参方式的，即通过 `f(b = 1)` 之类的写法可以指定 `b` 的值是 `1`。

问题是：为什么 C++ 不支持这种语法？C++ 有没有方式能够实现这种语法的替代？

请大家自行查阅资料回答上述问题。部分解答可以在 [引用](../../5_class_2/#%E7%B1%BB%E7%9A%84%E5%BC%95%E7%94%A8%E6%88%90%E5%91%98%E5%92%8C-const-%E6%88%90%E5%91%98) 一节的「keyword arguments 的替代」块中找到。