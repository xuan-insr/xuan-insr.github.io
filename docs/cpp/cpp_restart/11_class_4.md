# 8 类 (V) - 继承与抽象类、访问控制

类的布局绝大多数是 implementation-defined 或者 unspecified 的；为数不多被指定了的是，具有相同 access control 的成员会按顺序分配，但每个成员后仍然有可能有实现决定的填充。^[class.mem.general#19](https://timsong-cpp.github.io/cppwp/n4868/class.mem.general#19)^



虽然 C++ 标准并未规定虚函数的具体实现，但几乎所有的 C++ 编译器都通过虚表 (virtual table) 来

虚拟函数调用 (virtual function call) 的主要性能开销事实上是对流水线预测的破坏；其内存访问和跳转本身并没有很显著的额外开销。虚拟函数调用的成本主要应当与函数本身的时长相比较。

可以通过 `final` 声明类不能被继承，或者成员函数不能被 override

派生类可以 override 非 virtual 成员函数，但通常不要这么做：https://isocpp.org/wiki/faq/strange-inheritance#redefining-nonvirtuals

通常的编译器实现会将 vtable 放在定义了第一个非 inline virtual 函数被定义的编译单元

![](assets/2023-06-01-14-51-02.png)

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