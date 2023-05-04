# 6 类 (III) - 拷贝构造、SMFs

--8<-- "cpp/cpp_restart/toggle_visibility.md"

??? warning "本节使用的副本"
    本节引入的副本包括：

## 6.1 拷贝构造函数

上一节中，我们讨论了用于处理赋值的 `operator =`。不过，对于形如 `Matrix m = m1;` 的初始化，应当如何处理呢？

在 C with Classes 早期，这一问题的解决方案是，首先用无参的构造函数构造 `m`，然后再赋值；即等价于 `Matrix m; m = m1;`。不过，这种方式比较低效，因此后来的 C++ 引入了 **拷贝构造函数 (copy constructor)**。就像我们前面介绍的转换构造函数一样，拷贝构造函数是一种特殊的构造函数。具体而言，对于 class `T`，其构造函数中第一个参数类型为 `T&` 或者 `const T&`，且没有其他参数或者其他参数都有默认参数的那些构造函数称为拷贝构造函数^[class.copy.ctor#1](https://timsong-cpp.github.io/cppwp/n4868/class.copy.ctor#1)^。例如，`X::X(const X&)` 和 `X::X(X&, int = 1)` 都是拷贝构造函数。

与构造函数、析构函数、`operator =` 一样，拷贝构造函数也会在没有用户定义的版本时声明一个默认的拷贝构造函数[^implicit][^implicit_type]，同时也能够通过 `= default;` 和 `= delete;` 显式要求或避免编译器生成拷贝构造函数。

[^implicit]: 当该类有无法被拷贝（拷贝构造函数已删除、不可访问或有歧义）的非静态成员变量、基类，<span class="box box-yellow">TODO: 此处已知不完整</span>

[^implicit_type]: 如果该类的所有基类和类类型的非静态成员都有形如 `S::S(const S&)` 的拷贝构造函数，则默认声明的拷贝构造函数形如 `T::T(const T&)`；否则形如 `T::T(T&)`。

一个类中可以有多个拷贝构造函数，例如可以同时有 `T(T&) = default;` 和 `T(const T&) = default;`。

每当通过同一类型的另一个对象初始化当前对象时，拷贝构造函数会被调用（除非这个调用被省略，见后文），具体而言，发生在：

- 初始化，例如 `T t = t1;`, `T t(t1);`, `T t = T(t1);` 等
- 函数参数传递，例如 `f(t);`，其中 `f` 的签名是 `void t(T t)`
- 函数返回，例如函数 `T f()` 的返回语句 `return t;` [^ret_copy]

[^ret_copy]: 这种情况下，如果 `T` 有移动构造函数，则会调用移动构造函数。

需要注意的是，形如 `X::X(X)` 的构造函数是不合法的^[class.copy.ctor#5](https://timsong-cpp.github.io/cppwp/n4868/class.copy.ctor#5)^，因为按值传参的过程中本来就会调用拷贝构造函数。

### copy elision

我们考虑这样一个情形：

```c++
T f() {
    return T();
}

int main() {
    f();
}
```

如果按照我们之前的说法，这个函数在返回时构造一个 `T` 类型的临时对象，把它作为返回值；此时这个临时对象作为返回值会被用来初始化调用处的那个临时对象，然后被析构。随后该语句结束，临时对象被析构。也就是说，有两次构造（其中一次是拷贝构造）和两次析构发生。

容易理解，在上面的两种情况下，我们可以简易地达成一个优化，从而减省一次构造和一次析构。即，我们做的事情是在返回处构造、拷贝给调用处。但是，如果我们能够直接在调用处构造，就可以省略返回处的临时对象的构造和析构了。

即，`f();` 只会调用一次默认构造函数，而不会调用拷贝构造函数；如下图所示：

<center>![](2023-03-25-20-58-11.png)</center>

自 C++17 开始，在以下两种情况下，对拷贝的省略是强制的：

返回一个与返回值类型相同的临时值[^prvalue]：

[^prvalue]: prvalue

```c++
T f()
{
    return T();
}
 
f(); // only one call to default constructor of T

初始化表达式是相同类型的临时值：

```c++
T x = T(T(f())); // only one call to default constructor of T, to initialize x
```

也因此，在这种情形下，并不要求拷贝构造函数是可访问的：

<center>![](2023-03-25-20-58-55.png)</center>

在另外的一些情况下，也有可能有优化的空间，例如：

```c++
T f() {
    T tmp;
    // ...
    return tmp;
}

T t = f();
```

在这种情况下，有可能做的事情是：`tmp` 被拷贝给 `t`，然后 `tmp` 析构。但是，我们也容易看出，直接让 `t` 代替 `tmp` 活下去，就能够节省这次拷贝和析构。事实上，C++ 允许但不强制这种优化的发生，在一个函数返回一个非参数的局部变量时，在最初构造这一临时变量 `tmp` 时就可以直接构造到返回值 `t` 的位置，函数中对 `tmp` 的操作实际上都是对 `t` 的操作，然后省略返回时的拷贝和析构^[class.copy.elision#1.1](https://timsong-cpp.github.io/cppwp/n4868/class.copy.elision#1.1)^。这一优化称为 Named Return Value Optimization。

不过，即使这一优化发生，C++ 也仍然要求此处拷贝构造函数是可以访问的。

另外，由于这一优化是可选的，因此如果拷贝构造函数是有副作用（如输出、修改全局或成员变量等）的，那么在不同的编译环境下，运行的结果有可能有所不同。这是当前仅有的两种能影响可观察的副作用的优化形式之一^[copy_elision#Notes](https://en.cppreference.com/w/cpp/language/copy_elision#Notes)^。

## 6.2 Special Member Functions

我们之前学到的默认（可无参调用的）构造函数、拷贝构造函数、拷贝赋值运算符和析构函数被统称为 **Special Member Functions (SMF)**[^smf]^[special#1](https://timsong-cpp.github.io/cppwp/n4868/special#1)^。它们的共同特点是，如果没有用户显式声明的版本，编译器会生成默认的声明；如果需要使用，则编译器生成默认的定义。

[^smf]: 还有移动构造和移动赋值。

### Rule of Three

需要提示的是，如果一个类有用户声明的拷贝赋值运算符或者析构函数，那么不推荐使用隐式定义的拷贝构造函数；对应地，如果一个类有用户声明的拷贝构造函数或者析构函数，那么不推荐使用隐式定义的拷贝赋值函数。在 C++ 的未来版本中，这些隐式定义可能会被删除^[depr.impldec#1](https://timsong-cpp.github.io/cppwp/n4868/depr.impldec#1)^。

这一提示的依据来自于 **Rule of Three**，即如果用户需要自定义一个类的拷贝构造、拷贝赋值或者析构函数，那么基本上这三个都是必要的。这是因为，如我们之前的讨论，这三个函数的专门定义通常都是为了处理一些额外资源问题的；在这种需求存在时，任何一个函数缺失都有可能带来错误。例如：

```c++
class Msg {
    char * content;
    unsigned from, to;
public:
    Msg(const Msg &s) {
        content = new char[strlen(s.content) + 1];
        strcpy(content, s.content);
        from = s.from;
        to = s.to;
    }
    Msg & operator=(const Msg &s) {
        if (this == *s)     return *this;
        if (strlen(content) != strlen(s.content)) {
            delete[] content;
            content = new char[strlen(s.content) + 1];
        }
        strcpy(content, s.content);
        from = s.from;
        to = s.to();
    }
    ~Msg() {
        delete[] content;
    }
};
```

### Rule of Zero

不过，随着 C++ 的现代化，**Rule of Zero** 被提出。这一建议的核心是，应当遵循单一职责原则，即一个类要么只用来管理资源，要么就不应该有涉及资源管理的操作。例如上面的代码按照这种原则就应当改为：

```c++
class String {
    char * content;
public:
    String(const String &s) {
        content = new char[strlen(s.content) + 1];
        strcpy(content, s.content);
    }
    String & operator=(const String &s) {
        if (this == &s)     return *this;
        if (strlen(content) != strlen(s.content)) {
            delete[] content;
            content = new char[strlen(s.content) + 1];
        }
        strcpy(content, s.content);
        return *this;
    }
    ~String() {
        delete[] content;
    }
};

class Msg {
    String content;
    unsigned from, to;
};
```

在这里，我们用一个专门的类 `String` 用来处理资源；由于 `String` 类型有了所有需要的 special functions，因此在 `Msg` 类中，我们不需要做额外的操作了；编译器隐式生成的拷贝构造、拷贝赋值和析构函数会帮我们调用 `String` 类的这些函数。

而事实上，C++ 也帮我们写好了这样的类，就是我们之前看到的 `std::string`。因此，我们就可以简单地写成这样，而不需要写拷贝构造、拷贝赋值或者析构函数了：

```c++
class Msg {
    std::string content;
    unsigned from, to;
};
```

除了 `string` 代为管理字符串之外，我们之后还会看到代为管理动态内存的智能指针；文件读写也有 `fstream` 等替我们管理。因此，在绝大多数情况，我们并没有必要自己定义这三种函数。这就是 Rule of Zero 的含义。也就是说，C++11 改进了语言和标准库，提供了对动态分配对象生命周期管理的更好工具，在这种背景下 Rule of Zero 被提出，作为对之前 Rule of Three 的更新。

---

--8<-- "cpp/cpp_restart/toggle_visibility.md"