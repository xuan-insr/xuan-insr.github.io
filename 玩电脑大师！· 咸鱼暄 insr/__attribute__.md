
可以通过 `__attribute__((A, B))`的方法定义多个 attribute。<br />`__attribute__((A)) void foo() {...}`, `void foo() __attribute__((A)) {...}`, `__attribute__((A)) void foo()`等都可以。

见到的`__attribute__`：

- `__attribute__((const))`
   - 标记函数的返回值不受传入参数以外的因素影响，且不会造成副作用。
   - 这个标记告诉 GCC，如果遇到对该函数的多次参数相同的访问，可以用第一次的返回结果代替后续的调用，无论这些调用之间存在什么代码。
- `__attribute__((hot))`
   - 标记这个函数是 hot spot。
   - 这个标记告诉 GCC，可以对这个函数进行更多的优化，同时可以将 hot spot 放到 text 段的临近位置，有助于 locality。
   - 当使用`-fprofile-use`来参考 profile feedback 时，hot functions 会被自动识别，该 attribute 失效。
- `__attribute__((cold))`
   - 标记这个函数很少会被运行。
   - 这个标记告诉 GCC，在优化这个函数时更多考虑空间而非速度。另外可以将 cold functions 放到 text 段的临近位置以提高其他函数的 locality。
   - 同时这个标记也告诉 GCC，包含对这个函数调用的分支可以被标记为 unlikely，从而帮助分支预测。
   - 当使用`-fprofile-use`来参考 profile feedback 时，hot functions 会被自动识别，该 attribute 失效。
- `__attribute__((always_inline))`
   - 告知 GCC 强制 inline 这个函数。
   - 如果无法 inline 会报错。注意，间接调用这个函数时不一定能够正常 inline 和报错。
- `__attribute___((noinline))`
   - 告知 GCC 不要 inline 这个函数。
   - 例如需要保留这个接口的情况下可以使用这个 attribute。
   - 又例如，如果这个函数是一个 cold function，而且其调用处在分支语句中，那么选择不 inline 可以缩短这段代码的长度，有助于 locality。



