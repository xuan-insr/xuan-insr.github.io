## 预备知识检测

**Direction**：请**尝试回答**下面问题，并且对每个小题目**陈述您对该题目的掌握程度**（未掌握 | 经尝试或查阅资料后理解 | 之前已经理解）。

**如果您想要尝试运行其中代码以得到结果，请务必在进行充分思考后再与输出结果进行比对验证**。


### Question 1 - 输入和输出，函数，指针初步

请看下面代码片段：

```c
int main() {
	int a, b;
	scanf("%d%d", &a, &b);
	return 0;
}
```
请尝试思考回答：

**问题 3.1.1** 第 3 行中，为什么 `scanf` 函数中要使用 `&a` 而不是 `a` ？

**问题 3.1.2** 如果定义字符数组 `char c[10];`，用 `scanf("%s", _-1-_)` 读入一个字符串时， `_-1-_` 处应该使用 `&c` 还是 `c` ，为什么？


### Question 2 - 变量及其运算数组、结构体，指针初步

请看下面代码片段：

```c
struct node {
	char C1, C2, C3;
	short S1;
	int I1;
}*b;

int main() {
	char array[12];
	for (int i = 11; i >= 0; i--)
		array[11 - i] = i;
	
	b = (struct node *)array;
	printf("%d %d %d %d %d", b->C1, b->C2, b->C3, b->S1, b->I1);
	
	return 0;
}
```
请尝试思考回答：

**问题 3.2.1** 第 10 行后，`array` 数组的值如何？

**问题 3.2.2** 程序的输出如何？`sizeof(struct node)` 的值是多少？

请注意：`S1` 和 `I1` 的输出结果以及 `sizeof(struct node)` 的值不属于现阶段需要掌握的知识；如果您对结果感到迷惑，可以不必浪费时间研究这个问题。


### Question 3 - 数组，函数，指针初步

若有声明 `struct node { int a, b, c; };`

**问题 3.3.1** `sizeof(int*)` 的值是多少？`sizeof(double*)` 的值呢？`sizeof(struct node *)` 的值呢？为什么？

**问题 3.3.2** 如果定义数组 `int arrI[5];`：

- `arrI` 和 `arrI + 1` 分别表示什么？
- `(unsigned long long)(arrI + 1) - (unsigned long long)arrI` 的值是多少？

类似地，如果定义数组 `char arrC[5];` 和 `struct node arrN[5];`, 那么 `(unsigned long long)(arrC + 1) - (unsigned long long)arrC` 和`(unsigned long long)(arrN + 1) - (unsigned long long)arrN` 的值分别是多少？为什么？

**问题 3.3.3** 结合前面两个问题思考，指针包含了哪些信息？这些信息分别以什么形式呈现？

**问题 3.3.4** 结合前面问题的思考，请回答：我们试图将数组 `int a[10]` 作为函数的传入参数时，参数列表中应当写 `int *a` 或者 `int a[]`。那么如果我希望将数组 `int a[10][10]` 作为传入参数时，参数列表可以写 `int **a` 或者 `int a[][]` 吗？为什么？
