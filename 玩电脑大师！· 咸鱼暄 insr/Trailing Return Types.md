C++11 引入了 trailing return types，也就是把函数的返回值类型换了个位置。例如：<br />`auto foo(int a) -> int { return a + 1; }`<br />等价于<br />`int foo(int a) { return a + 1; }`

这种支持的好处在哪里呢？ 中有 2 个例子感动了我！

例如我们希望写一个`mul`函数，返回值类型根据传入值类型推断。我们就可以写这样一个东西：
```cpp
template<typename T, typename U>
auto mul(T t, U u) -> decltype(t * u) {
    return t * u;
}
```
其中`decltype(t * u)`就是`t * u`的类型。<br />（`decltype`参见 [https://www.yuque.com/xianyuxuan/coding/cpp_lang_type#V9Gzq](https://www.yuque.com/xianyuxuan/coding/cpp_lang_type#V9Gzq)）

如果没有 trailing return types，我们就需要写
```cpp
template<typename T, typename U>
decltype(t * u) mul(T t, U u) {
    return t * u;
}
```
但是编译器会报错！因为我们在`t`和`u`未定义的时候就使用了它们。

当然，C++14 开始又支持了 auto return type deduction，所以我们甚至可以直接写
```cpp
template<typename T, typename U>
auto mul(T t, U u) {
    return t * u;
}
```

那么另一个场景是这样的：<br />`Foo<int> (*(*foo())())() { return 0; }`<br />可以改写为<br />`auto foo() -> auto(*)() -> tmp<int>(*)() { return 0; }`<br />太美观了！
