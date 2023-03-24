---
title: Week 3 - 类 (II) - 拷贝赋值、运算符重载与引用
verticalSeparator: ===
revealOptions:
  width: 1600
  height: 900
  margin: 0.04
  transition: 'fade'
  slideNumber: true
---

<!-- <link rel="stylesheet" href="custom_light.css">
<link rel="stylesheet" href="../custom_light.css"> -->
<link rel="stylesheet" href="custom.css">
<link rel="stylesheet" href="../custom.css">

# 探索 C++

<br>

## Week 3 - 类 (II) 拷贝赋值、运算符重载与引用

---

## 5.1 拷贝赋值运算符

===

在上一节中，我们创建了一个「容器」类：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
};
```

`c1 = c2;` 会发生什么？

===

`c1.val` 的值变得和 `c2.val` 一样了；也就是说，这两个容器现在指向同一块内存。

<br>

1. `c1` 原来的 `val` 也许指向了一块申请来的内存，但是它并没有被释放；
2. 这样的「赋值」实际上完成的是某种「共享」，而并非真正地建立一个副本。

===

```c++
class Container {
    elem* val;
    unsigned size = 0, capa;
    // ...
public:
    Container(unsigned capa) : val(new elem[capa]), capa(capa){}
    ~Container() { delete[] val; }

    void operator=(Container from) {
        delete[] val;
        val = new elem[from->capa];
        for (unsigned i = 0; i < from->size; i++) {
            val[i] = from->val[i];
        }
        size = from->size;
        capa = from->capa;
    }
};
```

===

在一个有运算符的表达式中，如果至少一个操作符是某个类的对象，则由重载解析查找对应的函数。

<br>

例如 `x = y;` 就会被视为 `x.operator=(y);` 进行查找。

===

```c++
void Container::operator=(Container from) {
    delete[] val;
    val = new elem[from->capa];
    for (unsigned i = 0; i < from->size; i++) {
        val[i] = from->val[i];
    }
    size = from->size;
    capa = from->capa;
}
```

`x = x;`

如果 `capa` 和 `from->capa` 的值相同

===

```c++ linenums="1"
class Container {
    elem* val;
    unsigned size = 0, capa;
public:
    // ...
    void operator=(Container from) {
        if (from->val != val) { // avoid self-assignment
            if (from->capa != capa) {
                delete[] val;
                val = new elem[from->capa];
            }
            for (unsigned i = 0; i < from->size; i++) {
                val[i] = from->val[i];
            }
            size = from->size;
            capa = from->capa;
        }
    }
};
```

===

`operator=` 同样可以有重载。例如：

```c++ linenums="1"
class Container {
    // ...
    void operator=(Container from);
    void operator=(elem * val) {
        this->val = val;
    }
};
```

如果有 `Container` 的实例 `c` 和一个 `elem *` 类型的 `ptr`，那么 

`c = ptr;`

是合法的，因为它实际上会被解释为 `c.operator=(ptr);`。

===

![](2023-03-18-20-48-30.png)

===

如果用户没有显示地给出 `operator=`，那么编译器会生成一个 public 的默认拷贝赋值运算符的定义；它完成的内容即为将各个成员变量拷贝一遍。

<br>

用户也可以将 `operator=` 设置为 `= default;` 或者 `= delete;`。

===

如果 `operator=` 在当前上下文不可见，那么 `a = b;` 这样的表达式非法：

```c++
class Foo { 
    void operator=(Foo){} // private operator=
    void foo() {
        Foo a, b;
        a = b;      // OK, private function available here
    }
};
struct Bar { 
    void operator=(Bar) = delete; // deleted operator=
    void foo() {
        Bar c, d;
        c = d;      // error: use of deleted function 
                    // 'void Bar::operator=(Bar)'
    }
};

void foo() {
    Foo a, b;
    a = b;      // error: 'void Foo::operator=(Foo)' 
                // is private within this context
    Bar c, d;
    c = d;      // error: use of deleted function 
                // 'void Bar::operator=(Bar)'
}
```

---

## A.4 运算符重载

---

## A.5 引用

---

## A.6 I/O Stream

---

## A.7 隐式类型转换

---

## 5.1 拷贝赋值运算符 (Cont.)

---

## Takeaway

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

===

## Takeaway

- 引用
  - 解决运算符重载按引用传参问题
  - 可以作为参数或者返回值
  - 类似于包装了的 `Foo * const`，但是不一定占内存
  - `const Foo &` 可以绑定临时对象
  - 重载解析
  - 类的引用成员和 const 成员的初始化

===

## Takeaway

- I/O Stream
  - `cin`, `cout` 的使用
  - 对 `operator<<` 和 `operator>>` 的重载
- 隐式类型转换
  - 标准转换
  - 用户定义的转换
    - 转换构造函数
    - 用户定义的转换函数