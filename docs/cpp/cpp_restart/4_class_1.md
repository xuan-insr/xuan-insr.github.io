# 4 类 (I) - 定义、成员、构造、析构

!!! warning
    从本节开始，我们在部分内容会尝试直接使用 standard 的相应内容讲解[^std_version]。由于会涉及到一些尚未讨论的内容，因此这些内容我们会通过脚注的方式给出。初学者可以忽略这些脚注。

    因此，从本节开始，类似本节这样有比较大量的参考资料标注和脚注的文章，会提供下面的按钮来帮助提高阅读质量（文末也会有一份）：

    --8<-- "cpp/cpp_restart/toggle_visibility.md"

!!! warning "本节使用的副本"
    自本节开始，我们会在讲解类相关的内容时，引入一些 C++ 语法说明。这些说明有的是阐明容易混淆的概念，有的是介绍 C++ 相对于 C 的新语法。这些章节用 ▲ 表示。它们仍然是文章的重要部分，但由于本身话题相对独立，因此单独在导航目录中的「A 附录」一节中展示；正文里的是插件引入的副本，因此本文的字数统计并不包含这些副本。

    本节引入的副本包括：

    - [声明与定义](../appendix/decl_and_def)
    - [inline 函数](../appendix/inline_functions)
    - [函数默认参数与函数重载](../appendix/func_overload)

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

另外，和全局函数一样，类的成员函数也可以只有声明没有定义，只要这个函数没有被使用：

```c++
void f();   // OK if f() is never called;
            // if called, link error may occur
struct Foo {
    void bar();     // ditto
}
```

### `this` 指针

我们之前介绍过，C++ 早期会被编译成 C 语言，然后再编译成汇编。那么问题来了！例如上面代码中的 `Foo::bar` 函数，如何编译成 C 中的函数呢？这一问题的难点是：这个函数里访问了调用这个函数的对象 (不妨称之为 calling object) 的成员变量 `x`；那么这个函数如何知道 calling object 在哪里，从而访问它的成员变量呢？

答案是，每个成员函数[^this]都会被视为有一个 implicit object parameter，它即是 calling object。而在成员函数的函数体中，`this` 表达式的值即是 implicit object parameter 即 calling object 的地址。

在成员函数的函数体中，访问任何成员时都会被自动添加 `this->`，例如 `void Foo::bar(int v) { x += v; }` 中的 `x += v;` 实际是 `this->x += v;`。

下图中，汇编第 17~19 行将参数 `ff` 放到了第一个参数的位置，20 行调用 `f()`，事实上就是将这个对象的地址隐式传入其中了。

<center>![](2023-03-04-02-13-48.png){width=300}</center>

[^this]: implicit object parameter 的实际用途是重载解析，无论是否 static 都会被视为有这个成员，见 [这个回答](https://stackoverflow.com/a/72534617/14430730)。但是 static 成员函数没有 `this`。只有构造函数没有 implicit object parameter。

自 C++23 开始，`this` 关键字有了新的含义。我们将在后面的章节讨论。

??? note "成员函数不能重新声明"
    如果写了这样的代码：

    ```c++
    class Foo {
        void foo();
        void foo();
    }
    ```

    gcc 12.2 会给出这样的报错：`'void Foo::foo()' cannot be overloaded with 'void Foo::foo()'`

    这会让人比较疑惑，因为这两个明明都只是声明。错误的原因其实是，标准规定，类的成员函数不应被重新声明，除非这个重新声明是出现在类定义之外的成员函数定义[^redecl]^[class.mfct#2](https://timsong-cpp.github.io/cppwp/n4868/class.mfct#2)^。

    [^redecl]: 或者成员函数模板的显式特化。
    
    clang 16.0.0 给出的报错就合理许多：`error: class member cannot be redeclared`

## ▲ inline 函数

--8<-- "cpp/cpp_restart/appendix/inline_functions.md"

## 4.3 构造函数

构造函数 (constructor) 是一种特殊的成员函数，用于初始化该类的对象。构造函数 constructor 也时常被简写为 ctor 或者 c'tor 等。

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
};
```

在上面的程序中，第 5 行的 `Container()` 是构造函数。它和其他成员函数的区别是，它不写返回值类型，而且它直接使用类的名字。（构造函数并没有名字^[class.ctor.general#2](https://timsong-cpp.github.io/cppwp/n4868/class.ctor.general#2)^。）

第 6 行的 `val = nullptr;` 就是前面提到的「保证」，即 `val` 的值要么是 `nullptr`，要么是其他成员函数赋的值，而不会是个随机的值。

!!! note "nullptr"
    `nullptr` 是 C++11 引入的一个关键字，用来表示空指针。这与 C 中的 `NULL` 不同，虽然后者在 C++ 中也能使用。我们在稍后介绍 `nullptr` 为什么会被引入。

这样，就可以使用 `Container c = Container();` 构造一个对象了[^copy_ctor]。

`Container();` 会返回一个构造出的无名对象。不严谨地说，上面的语句将名字 `c` 绑定到了对应的无名对象上。为了代码更加简洁紧凑，C++ 允许更加简洁的写法：`Container c;`。

[^copy_ctor]: 部分对 C++ 有基础了解的读者可能会认为，用这里返回的临时对象来构造 `c1` 或者 `c2` 时有可能调用拷贝构造函数。这在早期 C++ 中是有可能的，但是自 C++17 强制 copy elision 之后拷贝构造函数的调用不会发生，即`Container()` 得到的是一个 prvalue，用这个 prvalue 去构造 `f` 时会出现 copy elision。事实上，在 C++17 之前，如果抑制 RVO，`Container f = Container();` 可能会触发一次构造和一次拷贝构造：https://godbolt.org/z/W55qWddM7 。因此，这里的构造必定等价于 `Container c1;` 和 `Container c2(64);`。我们会在讨论拷贝构造时讨论这个问题。

因此，当我们在用 `Container c;` 定义一个对象时，就会调用构造函数。例如：

<center>![](2023-02-24-00-02-54.png){width=700}</center>

也就是说，由于定义一个对象时需要用到构造函数，因此如果要用的构造函数是 `private` 的，对象就无法被构造：

<center>![](2023-03-04-01-35-48.png)</center>

???+ note "Foo() 是调用构造函数的函数调用表达式吗？"
    不是！看下面的代码：

    ```c++
    Foo f = Foo();
    Foo f2 = Foo::Foo();
    ```

    第二行会有报错：

    <center>![](2023-03-03-12-30-33.png)</center>

    即，我们不能直接调用构造函数，这是因为 **构造函数并没有名字，因此永远无法被用名字找到**^[class.ctor.general#2](https://timsong-cpp.github.io/cppwp/n4868/class.ctor.general#2)^。`Foo();` 的写法并不是对构造函数的调用，而是一个 "function-style cast"。

    这是什么东西呢？我们知道 C 语言中的类型转换 (cast) 表达式形如 `(int)3.2`（称为 C-style cast），而 C++ 引入了形如 `int(3.2)` 的 function-style cast。`int(3.2)` 将 3.2 显式地转换为了一个临时的 `int` 对象；类似地，`Foo()` 也（什么都不用地）显式地转换出了一个临时的 `Foo` 对象。虽然这个转换本身会使用到构造函数，但是这个表达式本身不是在调用构造函数。

    这个东西的重要用途之一也是模板。我们会在后面的章节中再次讨论。

像普通的函数一样，构造函数可以是有参数的。例如，下面的构造函数允许用户传递一个初始大小，然后直接开一个对应大小的空间：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
public:
    Container(unsigned size) {
        val = (elem*)malloc(sizeof(elem) * size);
        // ...
    }
    // ...
};
```

这样，就可以使用 `Container c2 = Container(64);` 构造一个自定义大小的容器了。

同样地，C++ 允许更加简洁的写法：`Container c2(64);`。即，如果无参地构造，则不需要写出括号；如果有参构造，则将参数写在括号中。

也就是说，在 C++ 中，声明变量时的 **初始化器 (initializer)** 除了类似 `int a = 4;` 的 `= initializer-clause` 之外，还有类似 `int a(4);` 的 `( expression-list )`^[dcl.init.general#1](https://timsong-cpp.github.io/cppwp/n4868/dcl.init.general#1)^。[^initializer][^equal-initializer]

[^initializer]: 还有 braced-init-list。我们在后面讨论。
[^equal-initializer]: 关于类使用 `Foo f = expr;` 形式的初始化的行为，我们在讨论完拷贝构造函数和转换构造函数之后再讨论。

???+ notes "无参构造时为什么不用括号呢？"
    这个问题被称为 **most vexing parse**。如果它加了括号，变成了 `Container c1();`，会被理解成什么呢？

    我们来看这个东西：`int func();`，这显然是一个函数声明；而 `Container c1();` 的语法结构与其完全相同，因此这样的表述是有歧义的。

    因此，C++ 规定无参构造时不用带括号（准确地说，声明语句中要么没有 initializer，如果有 initalizer 且是括号的形式的话则括号里不能为空^[dcl.init.general#1](https://timsong-cpp.github.io/cppwp/n4868/dcl.init.general#1)^）。

    C++11 引入的 **brace initialization**（也被称为 **uniform initialization**）一定程度上解决了这个问题。我们在后面的章节讨论这个机制。

### 动态内存分配

我们之前提到，构造函数存在的意义是给该类的每个对象提供一定的「保证」，而 C++ 通过确保每个对象都执行过构造函数来提供这一保证。但是，我们在 C 中知道通过 `malloc` 动态分配内存的方式；那么如果我们写 `Container *p = (Container *)malloc(sizeof(Container));` 会发生什么呢？

事实上，这确实分配了 `sizeof(Container)` 那么大的空间，但是确实也没有调用构造函数。因此，C++ 引入了新的用于创建动态对象的操作符 `new` 以及对应的用来回收的 `delete`。

`new` 表达式可以用来创建对象或者数组：`int * p1 = new int; int * pa = new int[n];`。

如果是类的对象，则构造函数会被调用：

<center>![](2023-03-05-16-37-46.png)</center>

`new` 表达式也可以包含初始化器，但是只能是 `( something )` 或者 `{ something }` 的形式，不能是 `= something` 的形式：

<center>![](2023-03-05-16-41-09.png)</center>

`new` 表达式干的事情是申请内存 + 调用构造函数，返回一个指针；而 `delete` 表达式干的事情是调用析构函数 + 释放内存。`new` 表达式是 **唯一** 的用来创建动态生命周期对象的方式（因为 `malloc` 只是开辟内存，并不创建对象。对象是「a region of storage with **associated semantics**」）。

`delete` 会调用类对象的析构函数：

<center>![](2023-03-05-16-43-29.png)</center>

如上面例子所示，如果 `p` 在 `new` 的时候创建的是单个对象，则应该用 `delete p;` 的形式 (single-object delete expression) 回收；如果 `p` 在 `new` 的时候创建的是数组，则应该用 `delete[] p;` (array delete expression) 的形式回收，否则是未定义行为 (UB, undefined behavior)^[expr.delete#2](https://timsong-cpp.github.io/cppwp/n4868/expr.delete#2)^；这种情况下任何情况都有可能发生，包括但不限于（不需要诊断信息的）编译错误、运行时错误，或产生意料之外的运行结果等。我们会在后面的章节中具体讨论未定义行为。

关于 `new` 和 `delete`，我们还有一些话题没有讨论，例如 `operator new` 等以及 placement new。我们会在后面的章节中讨论相关问题。

## ▲ 函数默认参数与函数重载

--8<-- "cpp/cpp_restart/appendix/func_overload.md"

## 4.3 构造函数 (Cont.)

关于构造函数，我们还有几个问题可以讨论！

### implicitly-declared default constructor

我们称一个能够无参调用的构造函数是 default constructor。即，它不接收任何参数，或者所有参数都有默认值。

有一个问题是，我们在讲构造函数之前的代码里都没有写构造函数，但是它们也能正常编译运行！C++ 也希望在没有必要的理由时不与 C 发生不兼容，而 C 中的 struct 也没有写构造函数，但是它们也能被运行。这是怎么回事呢？

事实上，对于一个类，如果用户没有提供任何构造函数，则编译器会自动为这个类创建一个 public 的 implicitly-declared default constructor，它被定义为 defaulted。Defaulted 的构造函数不接收任何参数，也什么都不做。如果有任何用户提供的构造函数[^default_ctor]，则 defaulted default constructor 被定义为 deleted 的。deleted 的函数不能被调用。

[^default_ctor]: 如果有未指明初始化方式的引用成员、const 成员，或者 default ctor 被删除或不可访问的成员或基类等情况下，implicitly-declared default constructor 也是 deleted 的。

不过，如果用户提供了构造函数，他仍然可以用 `ClassName() = default;` 来引入 defaulted 的构造函数。

用户还可以通过 `ClassName() = delete;` 显式地将 default constructor 设置成 deleted 的。

### member initializer lists

!!! success "总结"
    如果您并非初学者，[这里](../summaries/member_init_lists/) 有关于该话题更详尽的总结。

一个问题是这样的：假如我们希望根据构造函数的一些参数来初始化一些成员，我们固然可以这样写：

```c++ linenums="1"
class User {
    int id, age, failTimes;
    char* password;
public:
    User(int id, int age, char* pw) {
        this->id = id;
        this->age = age;
        failTimes = 0;
        password = copyStr(pw); // assume that `copyStr` gets a string and allocate some space and copy it
    }
    // ...
};
```

但是这样很累！于是 C++ 允许这样的写法：

```c++ linenums="1"
class User {
    int id, age, failTimes;
    char* password;
public:
    User(int id, int age, char* pw) : id(id), age(age), failTimes(0), password(copyStr(pw)) {}
    // ...
};
```

构造函数定义中形如 `: member(expr), member(expr)` 的东西叫做 member initializer lists^[class#base.init-1](https://timsong-cpp.github.io/cppwp/n4868/class#base.init-1)^，用来指明成员变量的初始化器 (initializer)。这些初始化会在构造函数的函数体执行之前完成。

在一些情况下，member initializer lists 是必要的。例如：

```c++ linenums="1"
class Point {
    int x, y;
public:
    Point(int x, int y) : x(x), y(y) {}
};

class Circle {
    Point c;
    int r;
public:
    Circle(int cx, int cy, int r) : c(cx, cy), r(r) {}
};
```

C++ 规定，在构造函数的函数体执行之前，所有参数要么按照 member initializer lists 的描述初始化，要么以默认方式初始化^[class.base.init#13](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#13)^。而对于类的对象，「默认方式初始化」意味着使用 default constructor 构造。然而，`Point` 类并没有 default constructor，因此如果 member initializer lists 没有指明 `Point` 类的初始化方式，就会出现编译错误：

<center>![](2023-03-04-03-11-28.png)</center>

在后面的章节中，我们还会看到更多 member initializer lists 是必要的的情况。

???+ note "补充"

    如果构造函数的声明和定义分离，则 member initializer lists 应当出现在构造函数的定义中。

    member initializer list 的顺序不影响成员被初始化的顺序，它们按照在类定义中的顺序初始化。例如：

    <center>![](2023-03-04-03-20-24.png)</center>

#### delegating constructor

member initializer list 可以将构造委托给同一类型的另一个构造函数，做出这一委托的构造函数称为 delegating constructor；如果这样的话，member initializer list 应当只包含这一个项目。目标构造函数由重载解析选取，其运行结束后，delegating constructor 的函数体被执行^[class.base.init#6](https://timsong-cpp.github.io/cppwp/n4868/class.base.init#6)^。一个构造函数不能直接或间接地被委托给自己。

```c++
struct C {
    C( int ) { }                  // #1: non-delegating constructor
    C(): C(42) { }                // #2: delegates to #1
    C( char c ) : C(42.0) { }     // #3: ill-formed due to recursion with #4
    C( double d ) : C('a') { }    // #4: ill-formed due to recursion with #3
};
```

<center>![](2023-03-04-03-15-43.png)</center>

可见，被委托的目标构造函数运行完输出 `ctor1 called` 后，委托构造函数运行，输出 `ctor2 called`。

### default member initializer

假设我们有若干个构造函数：

```c++ linenums="1"
class User {
    int id, age, failTimes;
    char* password;
public:
    User(int id, int age, char* pw) : id(id), age(age), failTimes(0), password(copyStr(pw)) {}
    User(int id, int age) : id(id), age(age), failTimes(0), password(nullptr) {}
    User(int id) : id(id), age(-1), failTimes(0), password(nullptr) {}
    // ...
};
```

可以看到，我们也许想要给构造时没有提供的参数赋一个初值；如果在构造函数或者 member initializer list 中写初始值，则所有构造函数都要写一份，这是比较累的！于是，C++11 引入了 default member initializer 解决这个问题！

```c++ linenums="1"
class User {
    int id, age = -1, failTimes = 0;
    char* password = nullptr;
public:
    User(int id, int age, char* pw) : id(id), age(age), password(copyStr(pw)) {}
    User(int id, int age) : id(id), age(age) {}
    User(int id) : id(id) {}
    // ...
};
```

如果一个成员变量同时被 member initializer list 指定且有 default member initializer，按前者执行，后者被忽略。

default member initializer 只允许 `brace-or-equal-initializer` 即 `= something` 或者 `{ something }`，而不允许用括号的形式^[class.mem.general#nt:member-declarator](https://timsong-cpp.github.io/cppwp/n4868/class.mem.general#nt:member-declarator)^。`{ something }` 是我们之前提到的 brace initialization (uniform initialization)，我们在后面的章节具体讨论。

也就是说，含 default member initializer 的成员可以形如 `Foo f = Foo(...);`，但不能形如 `Foo f(...);`：

```c++ linenums="1"
class Point {
    int x, y;
public:
    Point(int x, int y) : x(x), y(y) {}
};

class Circle {
    // Point c(0, 0);       // error
    Point c = Point(0, 0);  // OK
    int r;
public:
    Circle(int cx, int cy, int r) : c(cx, cy), r(r) {}
};
```

## 4.4 析构函数

我们考虑这样一个问题：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
public:
    Container(unsigned size) {
        val = (elem*)malloc(sizeof(elem) * size);
        // ...
    }
    // ...
};
```

`Container` 的每个对象都会 `malloc` 一块内存。众所周知，`malloc` 出来的空间需要我们在不用的时候手动 `free` 来回收。那么什么时候完成这个回收呢？最好的选择显然是当对象的生命周期结束的时候。生命周期结束意味着这个对象再也无法被访问，因此它的成员自然也无法被访问；在这个时候我们将它所拥有的资源（即指针成员变量指向的 `malloc` 出来的内存）释放，既不会太早（因为后面不会再有使用了），也不会太晚（因为此时仍然能知道那些资源的地址）。

因此，C++ 引入了 **析构函数 (destructors)** 来解决这个问题；析构函数在每个对象的生命周期结束的时候被调用，大多数情况被用来释放对象在运行过程中可能获取的资源，例如释放申请的内存、关闭打开的文件等。我们稍后讨论各种变量的生命周期。析构函数形如 `~class-name()`，其中 `~` 也被用作取反运算符，这里来表示「与构造相反」的含义，即析构。一个例子是：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
public:
    Container(unsigned size) {
        val = (elem*)malloc(sizeof(elem) * size);
        // ...
    }
    ~Container() {
        free(val);
    }
};
```

9~11 行是析构函数。这里，析构函数将 `val` 指向的内存释放。

析构函数的参数列表永远是空的。显然，析构函数是无法重载的。

析构函数和构造函数一样，如果某个类没有 user-declared destructor，编译器会自动生成一个 public 的 implicitly-declared destructor，定义为 defaulted。因此，当类的成员中没有什么需要释放的资源时，我们就不需要写析构函数了[^rule_of_zero]。

[^rule_of_zero]: [The rule of three / five / zero](https://en.cppreference.com/w/cpp/language/rule_of_three) 一些讨论中涵盖了什么时候需要析构函数。我们会在后面的章节中具体讨论相关问题。

析构函数 destructor 也经常被简写为 dtor 或 d'tor 等。

当然，自 C++11 起，我们仍然可以通过 `= default;` 或者 `= delete;` 来生成默认的析构函数，或者删除 implicitly-declared destructor。例如：

```c++
class Foo{
private:
    ~Foo() = default;
};
```

这里我们告知编译器在 `private` 范围内显式生成了默认的构造函数。

```c++
struct Foo {
    ~Foo() = delete;
};
```

这里我们将 implicitly-declared destructor 标记为 deleted。

如果 `Foo` 的析构函数是 deleted 的，或者在当前位置不可访问 (如当前在类外，但是析构函数是 private 的)，那么类似 `Foo f;` 的全局变量、局部变量或者成员变量定义是非法的[^private_or_deleted_dtor]。但是，这种情况下，可以通过 `new` 来创建一个动态的对象，因为这样创建的对象并不隐式地在同一个作用域内调用析构函数。

[^private_or_deleted_dtor]: 我们会在后面的章节讨论将析构函数设成 private 或者 delete 的场景。[这篇文章](https://www.rangakrish.com/index.php/2020/03/04/deleted-destructor-in-c/) 给出了一些解释。

与构造函数不同，析构函数是可以手动调用的。我们在后面讨论 placement new 的章节讨论这个问题[^call_dtor]。

[^call_dtor]: https://stackoverflow.com/a/10082335/14430730 是一个很好的例子，讨论容器中对 placement new 和手动调用析构函数的用途。

??? note "defaulted ctor & dtor 被 delete 的情况"
    考虑这个问题：
 
    ```c++
    struct Foo { Foo(int){} };
    class Bar { Foo f; };
    ```

    即，`Foo` 类型没有 default constructor（即可以无参调用的构造函数）；而 `Bar` 类型中有一个 `Foo` 类型的子对象 `f`。`Bar` 类型并没有提供构造函数。

    根据我们所说，如果没有提供构造函数，则编译器自动生成一个 implicitly-declared default constructor；但是这里自动生成的构造函数并不能完成 `f` 的初始化。这种情况怎么办呢？

    类似地，考虑以下几个场景：

    `Foo` 的默认构造函数是有歧义的：

    ```c++
    struct Foo { 
        Foo(){}
        Foo(int x = 1){}
    };
    class Bar { Foo f; };
    ```

    `Foo` 的析构函数是 deleted 的：

    ```c++
    struct Foo { ~Foo() = delete; };
    class Bar { Foo f; };
    ```

    `Foo` 的析构函数是 private 的：

    ```c++
    class Foo { ~Foo() = default; };
    class Bar { Foo f; };
    ```

    或者，这个问题可以对称延伸到析构函数：

    ```c++
    class Foo { ~Foo() = default; };
    struct Bar { 
        Foo f; 
        Bar(){}
    };
    ```

    C++ 规定，当以下任一情况发生时，其 defaulted 的 default constructor 被定义为 deleted 的^[class.default.ctor#2](https://timsong-cpp.github.io/cppwp/n4868/class.default.ctor#2)^：

    - 某个没有 default member initializer 的 subobject 没有 default constructor
    - 对某个 subobject 的对应 constructor 的重载解析得到歧义，或者解析出的函数是被删除或在此处不可访问的
    - 某个 subobject 的 destructor 是被删除或者在此处不可访问的
    - （其他情况略）

    同时，如果某个 subobject 的 destructor 是被删除或者在此处不可访问的，其 defaulted 的 dtor 被定义为 deleted 的^[class.dtor#7](https://timsong-cpp.github.io/cppwp/n4868/class.dtor#7)^。

## 4.5 构造和析构的时机和顺序

对于一个类对象，它的 **生命周期 (lifetime)** 自它的初始化（构造）完成开始，到它的析构函数调用被启动为止。

任何一个对象都会占据一部分存储；这部分存储的最小生命周期称为这个对象的 **storage duration**。对象的 lifetime 等于或被包含于其 storage duration。

!!! note
    这里说「最小生命周期」，是因为对象被析构后，对应的存储虽然可以被立刻回收，但也不一定立刻被回收。但「最小」提供的是一种保证。

在 C++11 之前，任何一个对象的 storage duration 都是如下一种[^thread_storage_duration]：

- **automatic** storage duration: 没有被定义为 `static`[^auto] 的局部对象。[^auto_opt]
- **static** storage duration: non-local 对象，或者被定义为 `static` 的局部对象或者类成员对象。我们会在后面的章节讨论 `static` 成员对象。
- **dynamic** storage duration: `new` 出来的对象。

[^thread_storage_duration]: 自 C++11 开始，还有 thread storage duration，这里暂略。下面的讨论中也一样。
[^auto]: 还有 `extern` 和 `thread_local`。[basic.stc.auto#1](https://timsong-cpp.github.io/cppwp/n4868/basic.stc.auto#1)
[^auto_opt]: [basic.stc.auto#3](https://timsong-cpp.github.io/cppwp/n4868/basic.stc.auto#3) If a variable with automatic storage duration has initialization or a destructor with side effects, an implementation shall not destroy it before the end of its block nor eliminate it as an optimization, even if it appears to be unused, except that a class object or its copy/move may be eliminated as specified in [class.copy.elision].

子对象 (subobject，如成员变量) 的 storage duration 是它所在的对象的 storage duration。

在下面的情况下，构造函数会被调用：

- 对于全局对象，在 `main()` 函数运行之前，或者在同一个编译单元[^trans_units]内定义的任一函数或对象被使用之前。在同一个编译单元内，它们的构造函数按照声明的顺序初始化[^static_init]。
- 对于 static local variables，在第一次运行到它的声明的时候[^static_local]。
- 对于 automatic storage duration 的对象，在其声明被运行时。
- 对于 dynamic storage duration 的对象，在其用 `new` 表达式创建时。

[^trans_units]: 简单地说，一个编译单元是一个源代码文件完成编译预处理的结果。

[^static_init]: 在这里，我们没有讨论跨编译单元的初始化顺序问题。这一问题有时比较重要，

[^static_local]: 这是线程安全的。这会带来额外的运行时开销，参见 [Does a function local static variable automatically incur a branch?](https://stackoverflow.com/questions/23829389/does-a-function-local-static-variable-automatically-incur-a-branch)。

在下面的情况下，析构函数会被调用：

- 对于 static storage duration 的对象，在程序结束时，按照与构造相反的顺序。
- 对于 automatic storage duration 的对象，在所在的 block 退出时，按照与构造相反的顺序。
- 对于 dynamic storage duration 的对象，在 `delete` 表达式中。
- 对于临时对象，当其生命周期结束时。我们会在后面的章节讨论临时对象及其生命周期。

数组元素的析构函数调用顺序与其构造顺序相反。

![](2023-03-05-19-26-59.png)

类的成员的析构函数调用顺序也与其构造顺序相反。类的成员的构造顺序依照它们在类定义中声明出现的顺序，而与 member initializer list 中的顺序无关。这样设计的原因是，不同的构造函数的 member initializer list 中成员顺序可能不同；如果依照 member initializer list 的顺序构造，那么析构时就很难保证和构造顺序相反。

作为一个练习，请说明下面的代码的输出：

```c++ linenums="1"
class Count{
    int s = 0;
public:
    ~Count();

    Count(int s) { this->s = s; }
    int getS(){
        return s;
    }
    void sPlus(){
        s++;
    }
};

Count::~Count() { cout << this->s << " ";}

Count count5(555);
static Count count6(666);
Count count7(777);

void f(){
    static Count count9(999);
}

int main() {
    Count *count1 = new Count(111);
    Count *count2 = new Count(222);

    Count count3(333);
    Count count4(444);

    f();

    static Count count8(888);

    delete(count1);

    for(int i = 1; i <= 5; i++)
        for(Count c(1); c.getS() <= i; c.sPlus());

    return 0;
}
```

答案是 `111 2 3 4 5 6 444 333 888 999 777 666 555 `。

## 4.6 小结

- 类的定义
    - 定义引入新的类型
    - class-key 通常不必要
- 声明和定义
    - 定义是声明的一种
- 类的成员
    - type alias
    - `this`
- 函数内联
- 构造函数
    - 建立起某种「保证」
    - 如何无参或有参地构造对象
    - `new`, `delete`, `new[]`, `delete[]`
    - implicitly-declared default constructor
    - `= default;`, `= delete`
    - member initializer lists
    - delegating constructor
    - default member initializer
- 函数默认参数和函数重载
    - 重载解析
    - 为什么 C++ 引入了 `nullptr`
- 析构函数
    - 用来回收资源
    - 为什么析构函数无法重载
- 构造和析构的时机和顺序
    - lifetime
    - storage duration
        - automatic
        - static
        - dynamic
    - 构造和析构的时机和顺序

---

--8<-- "cpp/cpp_restart/toggle_visibility.md"

*[BS]: Bjarne Stroustrup
*[SMFs]: Special Member Functions
