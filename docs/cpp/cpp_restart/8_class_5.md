# 8 类 (V) - 继承与抽象类、访问控制

受控的是访问权而不是可见性：

```c++
int a;
class X {
    int a;
};
class XX : public X {
    void f() { a = 1; }     // which a?
};
```

派生类的拷贝赋值，参见 Effective C++ 条款 12

```c++
class Bar : public Foo {
  // ...

  void printStuff() override {  // help the compiler to check
    Foo::printStuff(); // calls base class' function
  }
};
```

## ▲ 显式类型转换

阅读 DnE 14 章、Effective C++ 条款 27

cast operators (C++98) https://stackoverflow.com/questions/103512/why-use-static-castintx-instead-of-intx

https://isocpp.org/wiki/faq/templates#nondependent-name-lookup-types

https://isocpp.org/wiki/faq/templates#nondependent-name-lookup-members

https://isocpp.org/wiki/faq/templates#nondependent-name-lookup-silent-bug

讨论单根结构的优缺点

CRTP，参考 https://youtu.be/eD-ceG-oByA?t=1455