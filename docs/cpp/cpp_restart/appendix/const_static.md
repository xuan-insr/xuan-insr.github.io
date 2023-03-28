#### const 成员函数

我们之前看到了 `const` 成员函数：

```c++
class Complex {
    // ...
    string toString() const;
	// ...
};
```

声明为 `const` 的成员函数称为 `const` 成员函数，它保证不会修改 `*this` 的值；即调用这个成员函数的对象不会被更改。而如果没有 `const`，则没有这一保证。具体来说，声明为 `const` 的成员函数中，`this` 的类型是 `const Complex *`；而如果没有声明为 `const`，则 `this` 的类型是 `Complex *`。

如果没有这个保证，会出现什么问题呢？考虑这样的情形：

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

这种问题的原因很简单，我们要求 `b` 不能更改，但是函数 `toString()` 没有保证自己不会修改 `*this` 的值，因此调用这一函数是不安全的。

从语言实现的角度来说，我们取调用者 `b` 的指针，得到的是 `const Foo *`；但是 `toString()` 不是 `const` 成员函数，因此它的 `this` 是 `Foo *`；用 `const Foo *` 去初始化 `Foo *` 会丢失 cv-qualifier，这是 C++ 不允许的。因此这样的调用不合法。

显然，在 `const` 成员函数中，试图调用其他非 `const` 成员函数，或者更改成员变量都是不合法的：

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

???+ note "mutable"
    和之前的讨论一样，`const` 的设计是为了检查偶然的错误，但是不是为了给程序员增加不必要束缚。程序员在需要的时候，可以 **明确地** 要求做一些突破类型系统的事情；这些内容有时是有用的[^const_cast]。例如：

    [^const_cast]: 在 C++ 中，提倡明确使用 `const_cast` 来完成这一任务。Scott Meyers 在 Effective C++ 的条款 03 中提到了一种「适用」cast away `const` 的情况，这个情况也可以在 [这个回答](https://stackoverflow.com/a/2673585/14430730) 中找到。不过我们也可以发现，这种写法是有争议的；C++ Core Guidelines 的 [ES.50: Don't cast away `const`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-casts-const) 一节中有所讨论，建议的处理方案是使用模板和返回值类型推导。

    ```c++
    struct Foo {
        int a;
        void foo() const {
            ((Foo *)this)->a = 2;
        }
    };
    ```

    在这里，程序员显式地要求将 `this` 转换到 `Foo *`，去掉了 cv-qualifier；然后更改了 `a` 这个参数。这种事情是 C++ 允许的，但是有可能出错——如果 `*this` 被存放在只读的存储器里，这句话实际上没办法工作。

    但是事情并非总是如此。如果程序员明知调用的对象不可能存放在只读存储器中，那么他这么做是没有问题的。例如，调用的对象是一个 non-const 的对象，虽然它的地址在调用这个函数时确实被赋值给了 `const Foo *`，但是它指向的那个对象确实不是 `const` 对象，所以这种赋值是能够完成的。当然，如果调用的对象是一个 const 对象，那么这样的行为是 UB^[dcl.type.cv#4](https://timsong-cpp.github.io/cppwp/n4868/dcl.type.cv#4)^。

    但是，上面这种编程方式有点太极限了，它不适合绝大多数的人。然而，让对象的一部分是可变的这种需求仍然是比较普遍的。为了满足这种需求，C++ 引入了一个关键字 `mutable`；用 `mutable` 声明的类成员，即使包含它的对象是 `const` 的也能够修改：

    ```c++
    struct Foo {
        mutable int a;
        void foo() const {
            a = 2;  // OK
        }
    }
    ```

    显然，`mutable` 成员不应声明为 `const` 的。

注意，`const int Foo::foo();` 不是 `const` 成员函数，它是个返回值类型为 `const int` 的 non-const 成员函数。

值得说明的是，是 `const` 和非 `const` 的两个同名成员函数实际上是合法的重载，因为它们其实说明了 `this` 的类型是 `T*` 还是 `const T*`：

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

#### static 成员变量

我们考虑这样一个情形：

```c++
int tot = 0;
struct User {
    int id;
    User() : id(tot++) {}
};
```

即，我们有一个全局变量 `tot` 用来表示当前的 `id` 分配到第几号了；当构建一个新的 `User` 实例时，用 `tot` 当前值来初始化其 `id`，然后 `tot++`。

显然这个 `tot` 逻辑上属于 `User` 这个类的一部分；但是我们不能把它当做一个普通的成员变量，因为这样的话每个对象都会有它的一个副本，而不是共用一个 `tot`。但是，放成全局变量的话又损失了封装性。怎么办呢？

C++ 规定，在类定义中，用 `static` 声明没有绑定到类的实例中的成员；例如：

```c++
struct User {
    static int tot;
    int id;
    User() : id(tot++) {}
};
int User::tot = 0;
```

这个 `tot` 虽然从全局移到了类内，但是它仍然具有 static 的生命周期。它的生命周期仍然从它的定义 `int User::tot = 0;` 开始，到程序结束为止。由于它是类的成员，因此访问它的时候需要用 `User::tot`。

如我们刚才所说，`static` 成员不被绑定到类的实例中，也就是上面 `User` 类的每个实例里仍然只有 `id` 而没有 `tot`。不过，语法仍然允许用一个类的实例访问 `static` 成员，例如 `user.tot`[^static_call]。静态成员也受 access specifier 的影响。

[^static_call]: 如果有一个 `User & foo();`，那么 `foo().tot` 虽然用的是 `User::tot`，但是 `foo()` 仍会被调用。

需要提示的是，之前我们讨论的 default member initializer 和 member initializer list 是针对 non-static 成员变量的，它们对于 static 成员变量不适用：

<center>![](2023-03-26-15-15-19.png)</center>

也就是说，在类中的 static 成员变量 **只是声明** ^[class.static.data#3](https://timsong-cpp.github.io/cppwp/n4868/class.static.data#3)^。也就是说，我们必须在类外给出其定义，才能让编译器知道在哪里构造这些成员：

```c++
class Foo {
    static int a;
    static int b;
};

int Foo::a = 1;
int Foo::b;
```

这一要求的动机是，我们通常会把类的定义放到头文件中，而头文件通常会被多个翻译单元（多个源文件）包含；如果 `static` 成员变量在类中定义，这样多个翻译单元就会有多个这个静态变量的定义，因此链接就会出错。

注意，根据我们之前的讨论，`int Foo::b;` 也是定义。与 C 语言中我们学到的内容相同，它会被初始化为 0。一旦定义了静态成员，即使没有该类的成员被创建，它也存在。

作为一个例外，如果一个 `const` `static` 成员变量是整数类型，则可以在类内给出它的 default member initializer^[class.static.data#4](https://timsong-cpp.github.io/cppwp/n4868/class.static.data#4)^:

```c++
struct Foo {
    const static int i = 1; // OK
};

int main() {
    cout << Foo::i << endl;
}
```

另外，自 C++17 起，`static` 成员变量可以声明为 `inline`；它可以在类定义中定义，并且可以指定初始化器：

```c++
struct Foo {
    inline static int i = 1; // OK since C++17
}
```

在这种情况下，C++ 要求程序员保证各个编译单元内的这个变量的初始值是同一个，因为链接器在这种情况下会把多个定义合并为一个定义。我们会在后面的章节中详细讨论 `inline` 相关的问题。

`static` 成员变量不应是 `mutable` 的。

#### static 成员函数

`static` 函数的动机和 `static` 变量一致，都是「属于类，但不需要和具体对象相关」的需求；在这两种情形下，类被简单地当做一种作用域来使用。

由于 `static` 成员函数不与任何对象关联，因此它在调用时没有 `this` 指针。例如：

```c++
class User {
    inline static int tot = 0;
    int id;
public:
    // ...
    static int getTot() { return tot; }
}
```

我们可以使用 `User::getTot()` 来调用这个函数，当然也允许通过一个具体的对象调用这个函数；但是调用时不会有 `this` 指针。可以看到，下图中调用 non-static 成员函数 `get()` 的时候传入了 `ff` 即调用者地址，而调用 `getTot()` 时并没有：

![](2023-03-26-16-08-41.png)

`static` 成员函数不能设为 `const`。原因很简单：`static` 说明函数没有 `this`，而 `const` 说明函数的 `this` 是 `const X *`，这两个说明是互相矛盾的。