之前写过 [2.13 C/C++ 中的对齐](https://www.yuque.com/xianyuxuan/coding/gqfm4x?view=doc_embed)，这里来补充一下。

在 C++ 中，所有的 object type（[什么是 object type](https://www.yuque.com/xianyuxuan/coding/cpp_lang_type#DoX08)）都有一个属性叫做 alignment requirement。它是一个类型为`std::size_t`的，值总是 2 的幂次方的整数。这种类型的变量在内存中的地址必须是该值的整倍数。<br />对于 scalar types，其所占字节数是固定的，其 align 和其所占字节数相等。而对于 union、类（结构体），其 align 取其包含的所有成员的类型中 align 最大的。例如：
```cpp
struct A {
    long long i;
    char c;
};

struct B {};

struct C {
    A a;
    B b;
};

int main() {
    cout << sizeof(A) << " " << alignof(A) << endl;
    cout << sizeof(B) << " " << alignof(B) << endl;
    cout << sizeof(C) << " " << alignof(C) << endl;
    return 0;
}
```
 结果是：
```
16 8
1 1
24 8
```
	<br />这里也补充了 [2.13 C/C++ 中的对齐](https://www.yuque.com/xianyuxuan/coding/gqfm4x?view=doc_embed) 中未提到的情况：如果结构体的最后一个成员的字节数比该结构体的 align 小，也需要空出相应的字节。

C++11 开始，可以使用操作符 alignof(type-id) 获取一个 **类型** 的 align。

上述类型构成的数组的 align 和对应类型相等。

### alignas
C++11 开始，可以使用形如`struct alignas(16) B {};`或者`alignas(16) int c;`的方式给一个类型规定一个 **更强** 的 align。<br />注意，`alignas()`中的参数如果小于原来的 align，或者不为 2 的幂次方，则会报错或被忽略。

例如
```cpp
struct A {
    long long i;
    char c;
};

struct alignas(16) B {};

struct C {
    A a;
    B b;
};

int main() {
    cout << sizeof(A) << " " << alignof(A) << endl;
    cout << sizeof(B) << " " << alignof(B) << endl;
    cout << sizeof(C) << " " << alignof(C) << endl;

    alignas(16) int c;
    cout << typeid(c).name() << endl;
    cout << alignof(int) << endl;

    return 0;
}
```
	结果是
```
16 8
16 16
32 16
i
4
```
