# member initializer lists

member initializer lists 包含在构造函数的定义中。形式见 [class#base.init-1](https://timsong-cpp.github.io/cppwp/n4868/class#base.init-1)

## delegating constructor

member initializer list 可以将构造委托给同一类型的另一个构造函数，做出这一委托的构造函数称为 delegating constructor；如果这样的话，member initializer list 应当只包含这一个项目。目标构造函数由重载解析选取，其运行结束后，delegating constructor 的函数体被执行^[class.base.init#6](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#6)^。

```c++
struct C {
    C( int ) { }                  // #1: non-delegating constructor
    C(): C(42) { }                // #2: delegates to #1
    C( char c ) : C(42.0) { }     // #3: ill-formed due to recursion with #4
    C( double d ) : C('a') { }    // #4: ill-formed due to recursion with #3
};
```

## non-delegating constructor

下面讨论排除 delegating constructor 的情况。此种情况中，member initializer list 指定基类和非静态成员的 initializer。

如果一个非静态成员变量没有被 member initializer list 指定，则如果它有 default member initializer，则按照其描述初始化，否则 default-initialize。例外是，如果该成员变量是 union，且 member initializer list 指定了 union 中另一个 member，则无论它有没有 default member initializer 都不会被初始化。^[class.base.init#9](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#9)^

如果一个非静态成员变量同时被 member initializer list 指定且有 default member initializer，按前者执行，后者被忽略。

member initializer list 的顺序不影响基类和成员构造和析构的顺序。构造顺序描述如下：^[class.base.init#13](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#13)^

1. 首先，对象确切所属的类型 (most derived class, See [intro.object#6](https://timsong-cpp.github.io/cppwp/n4868/intro.object#6) and [What does the "most derived object" mean](https://stackoverflow.com/questions/12241637/what-does-the-most-derived-object-mean)) 的所有 virtual base classes 按 `base-specifier-list` 中的顺序深度优先地初始化；
2. 其次，所有 direct base classes 按 `base-specifier-list` 中的顺序初始化；
3. 再其次，所有非静态成员变量按其在 class definition 中定义的顺序初始化。

??? note "use data members in member initializer list"
    因此，下面的代码^[class.base.init#15](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#15)^是合理的，因为 `r` 在引用 `a`、`j` 在使用 `this->i` 时，对应的成员已经被正确构造：

    ```c++
    class X {
        int a;
        int b;
        int i;
        int j;
    public:
        const int& r;
        X(int i): r(a), b(i), i(i), j(this->i) { }
    };
    ```

??? note "use member functions in member initializer list"
    在上述第 2 步完成之前使用成员函数是 UB^[class.base.init#16](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#16)^：

    ```c++
    class A {
    public:
        A(int);
    };

    class B : public A {
        int j;
    public:
        int f();
        B() : A(f()),     // undefined behavior: calls member function but base A not yet initialized
        j(f()) { }        // well-defined: bases are all initialized
    };

    class C {
    public:
        C(int);
    };

    class D : public B, C {
        int i;
    public:
        D() : C(f()),     // undefined behavior: calls member function but base C not yet initialized
        i(f()) { }        // well-defined: bases are all initialized
    };
    ```

在上述初始化完成后，构造函数的函数体被执行。

在析构函数的函数体执行完后，基类和成员按与上述相反的顺序析构。

!!! warning "已知不完整"
    本文省略了 member initializer list 相关的一些 ill-formed 的情况。

    本文省略了 pack expansion 的情况 ([class.base.init#18](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#18))。