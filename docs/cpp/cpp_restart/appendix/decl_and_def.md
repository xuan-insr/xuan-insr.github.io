声明将名字引入或重新引入到程序中。定义是声明的一种，指的是那些引入的名字对应的实体足以被使用的声明。

??? info "standard"
    [[basic.pre#5](https://timsong-cpp.github.io/cppwp/basic.pre#5)]: Every name is introduced by a declaration

    [[basic.def#2](https://timsong-cpp.github.io/cppwp/n4868/basic.def#2)]: Each entity declared by a declaration is also _defined_ by that declaration unless:

    - it declares a function without specifying the function's body
    - it contains the extern specifier or a linkage-specification (`extern "C" {}`) and neither an initializer nor a function-body,
    - it declares a non-inline static data member in a class definition
    - ...

声明「重新引入」的例子是：

```c++
extern int i;
extern int i;

int f(int);
int f(int x);
```

上面的例子是合法的。它们只是 `i` 和 `f` 的声明而非定义。

而下面的语句都是定义：

```c++
int a;                          // defines a
extern const int c = 1;         // defines c
int f(int x) { return x+a; }    // defines f and defines x
struct S { int a; int b; };     // defines S, S​::​a, and S​::​b
enum { up, down };              // defines up and down
S anS;                          // defines anS
```

??? note "例外"
    不过，也有一些不合法的情况，例如：

    ```c++
    int i;
    int i;
    ```

    这个例子会报 "redefinition of 'int i'" 错误。

    根据上面的讨论，这两个语句都属于定义。[[basic.scope.scope#5](https://timsong-cpp.github.io/cppwp/basic.scope.scope#5)] 规定 "The program is ill-formed if, in any scope, a name is bound to two declarations that potentially conflict and one precedes the other"。因此如果这两个 `i` 代表不同的 entity，则违反了这条规定；如果代表同一个 entity，则违反了 One-Definition Rule (ODR) [[basic.def.odr#1](https://timsong-cpp.github.io/cppwp/n4868/basic.def.odr#1)] "No translation unit shall contain more than one definition of any variable, function, class type..."。

    因此，下面的例子也是不合法的：

    ```c++
    extern int i = 1;
    extern int i = 2;
    ```

    因为这两个语句也都属于定义。

    另外：

    ```c++
    extern int i;
    extern char i;
    ```

    这个例子会报 "redeclaration of 'i' with a different type" 错误^[std_citation_needed](../std_citation_needed)^。
