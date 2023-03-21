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