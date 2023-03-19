# C++ 学习

我在高中阶段打 OI 的时候第一次接触了 C++；那时对 C++ 的掌握差不多就是 C + cin/cout + sort 了。大一下选了 oop，我把 _Thinking in C++_ 完整地读了一遍，对 C++（尤其是面向对象）有了基本的认识；在此后出于自己的爱好、工程的需要、面试的考察，以及和 27rabbit 等经营鱼肆时的学习，对 C++ 的认识开始深入起来。此时再去反思自己的 C++ 学习，感觉仍然有许多没有完全或者完整理解的地方，学习路径也存在一定问题。因此，我想要展开一次重新学习和整理。

虽然不记得这个概念是从哪里听来的了，但是我认为学习一门知识的重要节点是「自举」。放到 C++ 来说，如果我们了解到一个新的概念并希望学习它时，能比较容易地根据 [standard](https://timsong-cpp.github.io/cppwp/n4868/) 或者 [c++ reference](https://en.cppreference.com/w/) 理解它的各种信息，而不需要去搜索引擎搜索各种讲解，那么我们就算是完成了 C++ 学习的「自举」。

我认为这样的能力比较重要的原因是：首先这种能力说明了我们对于基础概念的理解是达到了基本水平的，同时看「一手」的资料效率也会高很多。我认为达到「自举」的水平并不太难，至少我认为在学校安排的课程时间内足以达到了。所以我也尝试证明一下这种认识——从自己体验和整理一遍开始！

### 内容安排

初步想的内容（划删除线的是可能延后的内容）：

（写好了的就打勾）

1. [x] C++ 诞生
1. [x] 编程范式
1. [x] 引入 oop（list & shape）
1. [ ] 类 (I): 定义、成员、构造、析构
    - 声明与定义
    - inline 函数
    - 函数默认参数与函数重载（不包含重载解析）
    - delegating constructors
    - 动态内存分配
2. [ ] 类 (II): 拷贝赋值
    - 运算符重载
    - 引用
    - I/O stream
    - brace initialization
    - 转换构造函数
    - user-defined conversion function
3. [ ] 类 (III): 拷贝构造、SMFs
    - copy elision
    - const
    - cast
    - bool
4. [ ] 类 (IV): const 和 static 成员
    - UB
        - signed integers are 2's complement (C++20)
    - 初始化
        - aggregate
6. [ ] 模板
    - string
    - alias template
    - constexpr (C++11); consteval, constinit (C++20)
7. [ ] STL
    - range-based for loop (C++11); init-statement in range-for (C++20)
    - lambda
    - auto & return type deduction & trailing return type
5. [ ] 类 (V): 继承与抽象类、访问控制
    - final, override
    - covariant return types
    - inherited constructors
6. [ ] 右值引用和移动语义
    - smart pointers
7. [ ] 类 (VI): 移动构造与移动赋值
8. [ ] namespace
9. [ ] exception

### Topics

（已经安排在上面的就打勾了）

- [x] 类 (1979, C with Classes)：类与成员、继承、private & public、友元、inline functions
- [x] default arguments, `operator =` overload (1979, C with Classes)
- [x] 类 (1985, Release 1.0)：虚函数、new & delete、`::`
- [x] 函数和运算符重载 (1985, Release 1.0)
- [ ] 重载解析
- [x] I/O stream (1985, Release 1.0; C++98)
- [x] string (1985, Release 1.0; C++98)
- [x] 类 (1989, Release 2.0)：多继承、抽象类、`const` 和 `static` 成员函数、每个类的 new & delete、protected
- [ ] 类 (1989, Release 2.0)：pointers to members
- [x] namespace (1990, ARM)
- [x] exception (1990, ARM)
- [x] 模板 (1990, ARM)
- [x] 类 (C++98)：mutable、covariant return types
- [ ] 类 (C++98)：RTTI
- [x] cast operators (C++98)
- [x] bool (C++98)
- [x] 模板 (C++98)：template instantiations、member templates
- [x] STL (C++98)：containers, iterators, algorithms, function objects (`std::function` C++11)
- [x] **初始化**：value initialization (C++03)、
list initialization (C++11)、brace-or-equal initializers (C++11)
- [ ] designated initialization (C++20)
- [x] 类 (C++11)：defaulted and deleted functions
- [x] 右值引用和移动语义 (C++11)
- [x] 类 (C++11)：move constructors and move assignment operators、delegating and inherited constructors
- [x] smart pointers (C++11)
- [x] lambda expressions (C++11); generic lambda (C++14); capture `*this` (C++17)
- [x] auto (C++11); return type deduction (C++14)
- [x] range-based for loop (C++11); init-statement in range-for (C++20)
- [x] type aliases (C++11)
- [x] alias template (C++11)
- [x] trailing return type (C++11)
- [ ] type traits (C++11)
- [x] constexpr (C++11); consteval, constinit (C++20)
- [x] 一些遗留问题 (C++11): final, override
- [x] nullptr (C++11)
- [ ] concurrency support (C++11), memory model (C++11), thread local storage (C++11)
- [ ] variable template (C++14)
- [ ] string_view (C++17)
- [ ] inline variables (C++17)
- [ ] structured bindings (C++17)
- [x] initializers for if and switch (C++17)
- [x] [Order of evaluation](https://en.cppreference.com/w/cpp/language/eval_order)
- [ ] `std::tuple`, `std::any`, `std::optional`, `std::variant` (C++17)
- [ ] Class template argument deduction (C++17)
- [ ] 3-way comparison (C++20)
- [x] signed integers are 2's complement (C++20)
- [ ] modules (C++20)
- [x] UB
- [ ] literals
- [ ] Explicit object parameter (C++23)
- [ ] placement new


*[ARM]: The Annotated C++ Reference Manual