# 4 类 (I)

!!! warning
    从本节开始，我们在部分内容会尝试直接使用 standard 的相应内容讲解。由于会涉及到一些尚未讨论的内容，因此这些内容我们会通过脚注的方式给出。初学者可以忽略这些脚注。

    因此，从本节开始，类似本节这样有比较大量的参考资料标注和脚注的文章，会提供下面的按钮来帮助提高阅读质量（文末也会有一份）：

    --8<-- "cpp/cpp_restart/toggle_visibility.md"

在 C++ 中，每个类的定义 (class definition) 引入一个新的类型^[class.name#1](https://timsong-cpp.github.io/cppwp/n4868/class.name#1)^。

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

具体来说，类的定义具有如下形式[^1]^[class.pre#1,2](https://timsong-cpp.github.io/cppwp/n4868/class.pre#1)^：

<center>![](2023-02-09-20-19-03.png){width=600}</center>

1. 这里的 opt 指明某个元素是可选的。例如，class-specifier: class-head { member-specification~opt~ } 说明 class-specifier 中可以没有 member-specification，例如 `class Foo {}` 或者 `class A : public B {}` 之类的。
2. 这里的 class-name 是一个 identifier[^2]，例如上面的 `Foo` 和 `A`。
3. 这里的 class-key 决定了类是否是一个 union，以及默认情况下成员是 public 的还是 private 的。union 一次最多保存一个数据成员的值。也就是说，在 C++ 中，struct, class, union 都是类。
4. 这里的 attribute-specifier-seq 和 class-virt-specifier 现在暂时不用管。
5. 这里的 base-clause 定义为 `base-clause : base-specifier-list`，是用来处理派生类的。例如 1 中的 `: public B`。
6. 这里的 nested-name-specifier 是 `::` 或者 `Foo::` 之类的东西，其意义可以看下面的例子[^3][^4]：  
```C++ linenums="1" title="https://godbolt.org/z/shjxaKhxc"
class Inner { };

class Outer {
public:
    class Inner { int x; };
    Outer::Inner i;
    Inner i2;
    ::Inner i3;     // global Inner
    struct A;
};

struct Outer::A {};

int main() {
    Outer o;
    Inner i4;
    Outer::Inner i5;
    printf("%d %d %d %d %d", sizeof o.i, sizeof o.i2, sizeof o.i3, sizeof i4, sizeof i5);
    // Possible output: 4 4 1 1 4
    return 0;
}
```
在 C++ 中，类的定义会引入新的作用域，其范围是 member-specification 等^[basic.scope.class#1](https://timsong-cpp.github.io/cppwp/basic.scope.class#1)^[^9]。因此这里的 `Outer::Inner` 和外面的 `Inner` 可以同时存在[^8]。  
这里第 7 行访问到 `Outer::Inner` 是因为 Name Hiding^[basic.scope.hiding](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.hiding)^，即我们熟悉的作用域屏蔽[^10]。

C 和 C++ 都是按名等价 (name equivalence) 而非按结构等价 (structural equivalence) 的[^5]，例如^[class.name#1](https://timsong-cpp.github.io/cppwp/n4868/class.name#1)^：

<center>![](2023-02-09-22-36-23.png){width=600}</center>


[^1]: class-specifier 在这里用到：[dcl.type.general#1](https://timsong-cpp.github.io/cppwp/n4868/dcl.type.general#1)
[^2]: class-name 还可能是一个 simple-template-id，即模板特化。
[^3]: 如果将代码中 L7 提到 L5 之前，GCC 会出现报错。这是因为：[basic.scope.class#2](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.class#2): A name N used in a class S shall refer to the same declaration in its context and when re-evaluated in the completed scope of S. No diagnostic is required for a violation of this rule.
[^4]: 关于输出中的 1：[class.pre#6](https://timsong-cpp.github.io/cppwp/n4868/class.pre#6): Complete objects of class type have nonzero size. Base class subobjects and members declared with the no_­unique_­address attribute are not so constrained. 
[^5]: 但 layout capability rules 允许了 low-level 的强转。
[^6]: 还有 noexcept-specifier
[^7]: 注意，作用域定义为「the largest part of the program in which that name is valid, that is, in which that name may be used as an **unqualified name** to refer to the same entity^[basic.scope.declarative#1](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.declarative#1)^.」
[^8]: 见问题： [Which subclause of C++ standard prohibits redeclaration / redefinition in a same block?](https://stackoverflow.com/questions/75402077/which-subclause-of-c-standard-prohibits-redeclaration-redefinition-in-a-same)，已经解决，看起来像是直到 C++20 的时候还没改好的东西。
[^9]: 在 N4868 里，这里解释为：当一个名字在类内被定义后，类内的剩余部分^[basic.scope.pdecl#6](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.pdecl#6)^及该类的成员函数的函数体、default argument 以及 default member initializer（后两者会在后面讲解）[^6]^[class.mem.general#6](https://timsong-cpp.github.io/cppwp/n4868/class.mem.general#6)^成为其作用域[^7]^[basic.scope.class#1](https://timsong-cpp.github.io/cppwp/n4868/basic.scope.class#1)^。在最新版（写本文时，为 2023-01-02）中，scope 的定义发生了较大更改。
[^10]: 在最新版本里，name hiding 一节也没有了。可以在 [basic.scope.pdecl#2](https://timsong-cpp.github.io/cppwp/basic.scope.pdecl#2) 找到相关描述。


--8<-- "cpp/cpp_restart/toggle_visibility.md"