`int a[M] = {1}` 要花多久？<br />C语言课上老师告诉我们，对数组的某个元素进行初始化后，其后变量都将置为0。那么这是如何实现的呢？又要花多长时间呢？我对此进行了粗略的测试。

```cpp
#include<bits/stdc++.h>
#define M 500000

using namespace std;

clock_t begin = clock();

/*-1-*///int a[M] = {1};

int main(){
    /*-2-*///int a[M] = {1};
	/*-3-*///int a[M]; memset(a, 0, sizeof(int) * M);
	/*-4-*///int a[M]; for(int i = 0; i < M; i++)	a[i] = 0;
    
	clock_t end = clock();
	cout<<(double) (end - begin) / CLOCKS_PER_SEC<<endl;
	return 0;
} 
```

上述代码中，1~4 是测试的四个情况，其中 2~4 这三种情况在我的机器上运行的平均用时约为 0.04, 0.04, 0.08（均进行了 10 次测试），而 1 的用时为 0，即使M扩大了 10 倍，1 的用时仍为 0。

因此我猜测：

- `int a[M] = {1};` 中对未给出初值的部分赋值为 0 的实现方式与 memset 类似；
- 全局变量所在的内存本来就没有垃圾数据，不需要赋值为 0。

**20.12.9 Update:** <br />今天在 Stack Overflow 上问了这个问题（是第一次在上面问问题 很害怕），大概明白了：

- 首先，将未给出初值的部分赋值为 0 **确实是 C 和 C++ 标准中的要求** 。
   - [https://en.cppreference.com/w/c/language/array_initialization](https://en.cppreference.com/w/c/language/array_initialization)
   - [http://eel.is/c++draft/dcl.init.aggr](http://eel.is/c++draft/dcl.init.aggr)

- 其次， **编译器有义务，但可以选择任何方式来实现这一要求** 。因此之前的猜测“实现方式与 memset 类似”不是正确的。实际上，我们在 [https://godbolt.org/](https://godbolt.org/) 上查看编译 `int a[100] = {1}` 的结果如下：

**x86-64 gcc 10.2**:
```
		leaq    -400(%rbp), %rdx
    movl    $0, %eax
    movl    $50, %ecx
    movq    %rdx, %rdi
    rep stosq
    movl    $1, -400(%rbp)
    movl    $0, %eax
```
即，循环 `stosq` (store string to quad-word，存储 `eax` [在第 2 行赋值为 0] 到 四字 [4*4 字节，等同于 2 个 int]) 50 次（ `rep` ，循环字符串操作 `ecx` [在第 2 行赋值为 50] 次），然后把 `a[0]` 赋值为 `1` 。

**x86-64 clang 11.0.0**:
```
		leaq    -400(%rbp), %rcx
    movq    %rcx, %rdi
    movl    %eax, %esi
    movl    $400, %edx                      # imm = 0x190
    movl    %eax, -404(%rbp)                # 4-byte Spill
    callq   memset
    movl    $1, -400(%rbp)
    movl    -404(%rbp), %eax                # 4-byte Reload
```
可见，clang 编译出的结果就是直接调用了 `memset` 。memset 是按字节设置成 0 的，所以这里的立即数是 400。

这也说明了不同编译器的确会选择不同的方式实现这一要求。这种方式与 `memset` 的方式类似（都是内存复制），因此时间上也差不多。

另外我收到了这样的评论：
> you measured the time without optimizations turned on. Measuring times without optimiztations is close to meaningless, because in a release build runtimes can be completely different.


实际上开了优化以后函数就被优化得只剩 `ret` 了）不过确实需要重新学习一下时间测量的手段，发在另外的文章中。

![_EOF.png](./assets/1607504605924-b35a9f0d-0b2d-4680-8888-38245d3f990d.png)
