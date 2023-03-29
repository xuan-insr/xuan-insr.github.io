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

## ▲ 显式类型转换

阅读 DnE 14 章、Effective C++ 条款 27

cast operators (C++98) https://stackoverflow.com/questions/103512/why-use-static-castintx-instead-of-intx


讨论单根结构的优缺点