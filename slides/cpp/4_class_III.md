---
title: Week 4 - 类 (III) - 隐式类型转换、拷贝构造、
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

---

## A.6 `const` 和 `static`

===

#### const 成员函数

我们之前看到了 `const` 成员函数：

```c++
class Complex {
    // ...
    string toString() const;
	// ...
};
```

===

声明为 `const` 的成员函数中，`this` 的类型是 `const Complex *`；而如果没有声明为 `const`，则 `this` 的类型是 `Complex *`

===

如果没有这个保证，会出现什么问题呢？

```c++
struct Foo {
    string toString();
};

void bar(Foo & a, const Foo & b) {
    a.toString();   // OK
    b.toString();   // Error: 'this' argument to member function 'toString' 
                    // has type 'const Foo', but function is not marked const
}
```

我们要求 `b` 不能更改，但是函数 `toString()` 没有保证自己不会修改 `*this` 的值

用 `const Foo *` 去初始化 `Foo *` 会丢失 cv-qualifier

===

在 `const` 成员函数中，试图调用其他非 `const` 成员函数，或者更改成员变量都是不合法的：

```c++
struct Foo {
    int a;
    void foo();
    void bar() const {
        a++;    // cannot assign to non-static data member 
                // within const member function
        foo();  // 'this' argument to member function 'foo' has type 
                // 'const Foo', but function is not marked const
    }
};
```

===

`const int Foo::foo();`

===

是 `const` 和非 `const` 的两个同名成员函数实际上是合法的重载，因为它们其实说明了 `this` 的类型是 `T*` 还是 `const T*`：

```c++
struct Foo {
    void foo() { cout << 1 << endl; }
    void foo() const { cout << 2 << endl; }
};

int main() {
    Foo f;
    const Foo cf;
    f.foo();    // #1 called, as Foo* fits Foo* best
    cf.foo();   // #2 called, as const Foo* can only fit const Foo*
}
```

===

```c++
class Container {
    elem * data;
    // ...
public:
          elem & operator[](unsigned index)       { return data[index]; }
    const elem & operator[](unsigned index) const { return data[index]; }
    // ...
}
```

===

#### mutable

===

#### static 成员变量

```c++
int tot = 0;
struct User {
    int id;
    User() : id(tot++) {}
};
```

===

```c++
struct User {
    static int tot;
    int id;
    User() : id(tot++) {}
};
int User::tot = 0;
```

===

`static` 成员不被绑定到类的实例中，也就是上面 `User` 类的每个实例里仍然只有 `id` 而没有 `tot`

由于它是类的成员，因此访问它的时候需要用 `User::tot`

不过，语法仍然允许用一个类的实例访问 `static` 成员，例如 `user.tot`。静态成员也受 access specifier 的影响。

===

需要提示的是，之前我们讨论的 default member initializer 和 member initializer list 是针对 non-static 成员变量的，它们对于 static 成员变量不适用：

![](2023-03-26-16-19-45.png)

===

也就是说，在类中的 static 成员变量 **只是声明**。我们必须在类外给出其定义，才能让编译器知道在哪里构造这些成员：

```c++
class Foo {
    static int a;
    static int b;
};

int Foo::a = 1;
int Foo::b;
```

===

作为一个例外，如果一个 `const` `static` 成员变量是整数类型，则可以在类内给出它的 default member initializer:

```c++
struct Foo {
    const static int i = 1; // OK
};

int main() {
    cout << Foo::i << endl;
}
```

===

另外，自 C++17 起，`static` 成员变量可以声明为 `inline`；它可以在类定义中定义，并且可以指定初始化器：

```c++
struct Foo {
    inline static int i = 1; // OK since C++17
}
```

===

#### static 成员函数

`static` 函数的动机和 `static` 变量一致，都是「属于类，但不需要和具体对象相关」的需求

在这两种情形下，类被简单地当做一种作用域来使用

===

由于 `static` 成员函数不与任何对象关联，因此它在调用时没有 `this` 指针。例如：

![](2023-03-26-16-21-45.png)

我们可以使用 `User::getTot()` 来调用这个函数，当然也允许通过一个具体的对象调用这个函数

===

`static` 成员函数不能设为 `const`。原因很简单：`static` 说明函数没有 `this`，而 `const` 说明函数的 `this` 是 `const X *`，这两个说明是互相矛盾的。

---