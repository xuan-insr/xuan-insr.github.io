# 4 类 (I) - 定义、成员、构造、析构

!!! warning
    从本节开始，我们在部分内容会尝试直接使用 standard 的相应内容讲解[^std_version]。由于会涉及到一些尚未讨论的内容，因此这些内容我们会通过脚注的方式给出。初学者可以忽略这些脚注。

    因此，从本节开始，类似本节这样有比较大量的参考资料标注和脚注的文章，会提供下面的按钮来帮助提高阅读质量（文末也会有一份）：

    --8<-- "cpp/cpp_restart/toggle_visibility.md"

## 4.1 类的定义

我们在上一节已经看到了类的定义的一些具体例子，例如：

```c++ linenums="1"
class Textbox : public Shape {
public:
    char* text;
    int penwidth;

    void do_draw() {
        int old_penwidth = get_penwidth();
        set_penwidth(penwidth);
        // 画出文本框和文本内容
        set_penwidth(old_penwidth);
    }
}
```

在 C++ 中，每个类的定义 (class definition) 引入一个新的类型^[class.name#1](https://timsong-cpp.github.io/cppwp/n4868/class.name#1)^。因此，有了上面的定义，我们就可以用它来声明一个变量，如 `Textbox tb;` 声明并定义^[basic.def#2](https://timsong-cpp.github.io/cppwp/n4868/basic.def#2)^了一个类型为 `Textbox`，名为 `tb` 的变量。

!!! note
    在 C++ 中，用类来定义变量时，不必像 C 语言那样带有 `struct` 关键字。即，如果有 `class Foo` 或者 `struct Bar` 的定义，那么 `Foo x;`, `class Foo x;`, `Bar b;`, `struct Bar b;` 都是合法的声明语句。这是因为，从 C with Classes 设计之初就希望让用户定义的类型不是二等公民，而是能被与内置类型一样的方式使用。

    ??? tips "Elaborated type specifiers"
        带有 `struct` 或者 `class` 关键字的类型名 (如 `class Foo`) 叫做 Elaborated type specifiers^[dcl.type.elab](https://timsong-cpp.github.io/cppwp/n4868/dcl.type.elab)^。
        
        在 C 语言中，类似 `struct x {}; int x;` 是符合语法的：虽然这会使得名字 `x` 既表示一个结构体，又表示一个变量；但在 C 语言中这不会引起歧义，因为当 `x` 表示结构体时必须带上 `struct` 关键字。不过在 C++ 中，直接使用 `x` 就只能引用到变量 `x` 了，因为此时 `int x;` 的 `x` hides `struct x {};` 的 `x`^[basic.scope.hiding](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.hiding)^。
        
        但是为了兼容 C，C++ 并没有禁止上述写法，而是规定可以通过 Elaborated type specifiers 显式地来使用结构体 `x`，即使用 `struct x`^[basic.lookup.elab#1](https://timsong-cpp.github.io/cppwp/n4868/basic.lookup.elab#1),[class.name#2](https://timsong-cpp.github.io/cppwp/n4868/class.name#2)^；对 `class` 也一样。

        Elaborated type specifiers 还在 forward declaration 以及 enum 中有用途。


具体来说，类的定义具有如下形式[^class-specifier]^[class.pre#1,2](https://timsong-cpp.github.io/cppwp/n4868/class.pre#1)^：

<center>![](2023-02-09-20-19-03.png){width=600}</center>

1. 这里的 opt 指明某个元素是可选的。例如，class-specifier: class-head { member-specification~opt~ } 说明 class-specifier 中可以没有 member-specification，例如 `class Foo {}` 或者 `class A : public B {}` 之类的。
2. 这里的 class-name 是一个 identifier[^class-name]，例如上面的 `Foo` 和 `A`。
3. 这里的 class-key 决定了类是否是一个 union，以及默认情况下成员是 public 的还是 private 的。union 一次最多保存一个数据成员的值。也就是说，在 C++ 中，struct, class, union 都是类。但是在本节的后续讨论中，我们暂时只讨论 struct 和 class。
4. 这里的 attribute-specifier-seq 和 class-virt-specifier 现在暂时不用管。
5. 这里的 base-clause 定义为 `base-clause : base-specifier-list`，是用来处理派生类的。例如 1 中的 `: public B`。
6. 这里的 nested-name-specifier 是 `::` 或者 `Foo::` 之类的东西，其意义可以看下面的例子[^refer_to_same][^nonzero_size]：  
```C++ linenums="1" title="https://godbolt.org/z/shjxaKhxc"
class Inner { };

class Outer {
public:
    class Inner { int x; };
    Outer::Inner i;
    Inner i2;
    ::Inner i3;     // global Inner
    struct A;       // declares struct Outer::A
};

struct Outer::A {}; // defines struct Outer::A

int main() {
    Outer o;
    Inner i4;
    Outer::Inner i5;
    printf("%d %d %d %d %d", sizeof o.i, sizeof o.i2, sizeof o.i3, sizeof i4, sizeof i5);
    // Possible output: 4 4 1 1 4
    return 0;
}
```
在 C++ 中，类的定义会引入新的作用域，其范围是 member-specification 等^[basic.scope.class#1](https://timsong-cpp.github.io/cppwp/basic.scope.class#1)^[^class-scope]。因此这里的 `Outer::Inner` 和外面的 `Inner` 可以同时存在[^redeclaration]。  
这里第 7 行访问到 `Outer::Inner` 是因为 Name Hiding^[basic.scope.hiding](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.hiding)^，即我们熟悉的作用域屏蔽[^name_hiding]。

C 和 C++ 都是按名等价 (name equivalence) 而非按结构等价 (structural equivalence) 的[^structural]，例如^[class.name#1](https://timsong-cpp.github.io/cppwp/n4868/class.name#1)^：

<center>![](2023-02-09-22-36-23.png){width=600}</center>

[^std_version]: 本文所参考的 standard 版本是 N4868 (October 2020 pre-virtual-plenary working draft/C++20 plus editorial changes)，这并不是最新的版本。参考该版本的主要考量是防止可能的更新导致链接失效。
[^class-specifier]: class-specifier 在这里用到：[dcl.type.general#1](https://timsong-cpp.github.io/cppwp/n4868/dcl.type.general#1)
[^class-name]: class-name 还可能是一个 simple-template-id，即模板特化。
[^refer_to_same]: 如果将代码中 L7 提到 L5 之前，GCC 会出现报错。这是因为：[basic.scope.class#2](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.class#2): A name N used in a class S shall refer to the same declaration in its context and when re-evaluated in the completed scope of S. No diagnostic is required for a violation of this rule.
[^nonzero_size]: 关于输出中的 1：[class.pre#6](https://timsong-cpp.github.io/cppwp/n4868/class.pre#6): Complete objects of class type have nonzero size. Base class subobjects and members declared with the no_­unique_­address attribute are not so constrained. 
[^structural]: 但 layout capability rules 允许了 low-level 的强转。
[^noexcept-specifier]: 还有 noexcept-specifier
[^scope]: 注意，作用域定义为「the largest part of the program in which that name is valid, that is, in which that name may be used as an **unqualified name** to refer to the same entity^[basic.scope.declarative#1](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.declarative#1)^.」
[^redeclaration]: 见问题： [Which subclause of C++ standard prohibits redeclaration / redefinition in a same block?](https://stackoverflow.com/questions/75402077/which-subclause-of-c-standard-prohibits-redeclaration-redefinition-in-a-same)，已经解决。
[^class-scope]: 在 N4868 里，这里解释为：当一个名字在类内被定义后，类内的剩余部分^[basic.scope.pdecl#6](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.pdecl#6)^及该类的成员函数的函数体、default argument 以及 default member initializer（后两者会在后面讲解）[^noexcept-specifier]^[class.mem.general#6](https://timsong-cpp.github.io/cppwp/n4868/class.mem.general#6)^成为其作用域[^scope]^[basic.scope.class#1](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.class#1)^。在最新版（写本文时，为 2023-01-02）中，scope 的定义发生了较大更改。
[^name_hiding]: 在最新版本里，name hiding 一节也没有了。可以在 [basic.scope.pdecl#2](https://timsong-cpp.github.io/cppwp/basic.scope.pdecl#2) 找到相关描述。

??? tips "Forward Declaration"
    如果当前作用域没有名为 `identifier` 的类，那么形如 `class-key attr identifier ;` 的声明是一个 forward declaration^[class.name#2](https://timsong-cpp.github.io/cppwp/n4868/class.name#2)^。
    
    例如 `class Foo;`，它声明了一个叫 `Foo` 的类；但直到这个类被定义之前，它的类型是不完整的^[basic.types.general#5](https://timsong-cpp.github.io/cppwp/n4868/basic.types.general#5)^。

    不完整的类型有一些限制，但是也有一些可以完成的操作。例如不完整的类型不能用来定义变量（包括成员变量）、作为函数声明或定义的参数或者返回值类型等；但是可以定义指向它的指针。

    例如，常见的用途是，两个类可能会互相使用。这时就可以写出类似下面这样的代码：

    ```c++ linenums="1"
    struct X;
    struct Y {
        X* ptr;
        // X mem; // Error: field has incomplete type 'X'
        X* foo();
    };
    struct X {
        Y* ptr;
        Y* bar();
    };
    ```

    这时第 1 行是必须的，否则第 3 行的 `X` 就是一个未知的类型。

??? tips "Injected Class Name"
    C++ 规定，A class-name is inserted into the scope in which it is declared immediately after the class-name is seen. The class-name is also inserted into the scope of the class itself; this is known as the injected-class-name^[class.pre#2](https://timsong-cpp.github.io/cppwp/n4868/class.pre#2)^。这就是 `struct Node { Node* next; };` 能够使用 `Node` 的原因。

    但是，考虑内存布局容易理解，class `C` 内部不能有 non-static data member of type `C`。

## ▲ 声明与定义

--8<-- "cpp/cpp_restart/appendix/decl_and_def.md"

## 4.2 类的成员

member-specification 说明了类的成员。其结构如下^[class.mem.general](https://timsong-cpp.github.io/cppwp/n4868/class.mem.general)^：

<center>![](2023-02-11-15-49-10.png){width=400}</center>

其中 member-declaration 是成员的声明，而 access-specifier 是 `private`, `public`, `protected` 之一（前面两个我们讨论过了，第三个我们会在后文讨论）。成员可以包括成员变量、成员函数，也可以（嵌套的）类、枚举等，如本文前面代码中的 `Outer::Inner`，还可以包括声明类型的别名（如 `typedef` 和 `using`）等[^class_member]。

!!! note "Type alias"
    C++11 引入了 `using` 来声明类型别名，它的用途和 `typedef` 类似，如 `typedef struct arraylist_* arraylist;` 可以写成 `using arraylist = struct arraylist_ *;`。

    类型别名的声明也可以是类的成员，其作用域是类的作用域，同样受 access-specifier 的影响。例如：

    ```c++ linenums="1"
    struct Foo {
        using elem = int;
        elem x;     // OK, x has type int
        elem add(elem v) { x += v; return x; }
    private:
        using type = char;
        type c;     // OK, c has type char
    };

    // elem y;      // Error: unknown type name 'elem'
    Foo::elem z;    // OK, z has type int
    // Foo::type c; // Error: 'type' is a private member of 'Foo'   
    ```

    `using` 被引入是为了支持模板。我们在讲到模板的时候再来讨论这些问题。

类的成员函数可以在类内直接给出定义，也可以在类内只声明，在类外给出定义；这不影响成员函数的 access-specifier：

```C++
class Foo {
    int x = 0;
    void foo(int v) { x += v; }
    void bar(int v);
};

void Foo::bar(int v) { x += v; }

int main() {
    Foo f;
    f.bar(1);  // Error: 'bar' is a private member of 'Foo'
}
```

[^class_member]: 还能有 using-declarations, static_assert declarations, member template declarations, deduction guides (C++17), Using-enum-declarations (C++20)

## ▲ inline 函数

--8<-- "cpp/cpp_restart/appendix/inline_functions.md"

## 4.4 构造函数

构造函数 (constructor) 是一种特殊的成员函数，用于初始化该类的对象。

用 BS 的话说，构造函数的意义之一是「使程序员能够建立起某种保证，其他成员函数都能依赖这个保证」。例如：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
public:
    Container() {
        val = nullptr;
    }
    // ...
}
```

在上面的程序中，第 5 行的 `Container()` 是构造函数。它和其他成员函数的区别是，它不写返回值类型，而且它的名字是类的名字。

第 6 行的 `val = nullptr;` 就是前面提到的「保证」，即 `val` 的值要么是 `nullptr`，要么是其他成员函数赋的值，而不会是个随机的值。

!!! note "nullptr"
    `nullptr` 是 C++11 引入的一个关键字，用来表示空指针。这与 C 中的 `NULL` 不同，虽然后者在 C++ 中也能使用。我们在稍后介绍 `nullptr` 为什么会被引入。

## ▲ 函数默认参数与函数重载

由构造函数默认参数和重载引入本节。

!!! note "nullptr"
    TODO

## 4.6 析构函数


--8<-- "cpp/cpp_restart/toggle_visibility.md"

*[BS]: Bjarne Stroustrup
*[SMFs]: Special Member Functions