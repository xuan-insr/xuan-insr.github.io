
### 抽象数据结构 | Abstract Data Type, ADT 
抽象数据结构就像面向对象里的接口（抽象类）。抽象数据结构首先是一种数据结构，因此它定义了对象的格式和允许的操作及其效果。但其 **抽象** 在于它操作的实现是没有在 ADT 中给出的。


### 表 ADT | The List ADT
Objects: ![](https://cdn.nlark.com/yuque/__latex/d017c33c65d93394b826f639d852b48e.svg#card=math&code=A_1%2C%20A_2%2C%20...%2C%20A_n&height=18&width=107)
Operations: Print, MakeEmpty, Insert, Delete, Find, FindKth

#### 实现

   1.  数组实现。插入和删除代价较高；表的大小需要事先已知，因此一般不用。
   2.  链表实现。[链接](https://www.yuque.com/xianyuxuan/coding/ayy290)

#### 应用

   - 多项式 ADT | Polynomial ADT
```c
typedef struct Node *PtrToNode;
struct Node  {
    int Coefficient;
    int Exponent;
    PtrToNode Next;
};
typedef PtrToNode Polynomial;

Polynomial Read(){
	/* Input should be sorted in decreasing order of exponents. */
	typedef PtrToNode ptr;
	ptr head = (ptr)malloc(sizeof(Node)), tail = NULL;
	head->Next = NULL, tail = head;
	
	int length;	scanf("%d", &length);
	while(length--){
		tail->Next = (PtrToNode)malloc(sizeof(Node));
		tail = tail->Next, tail->Next = NULL;
		scanf("%d%d", &tail->Coefficient, &tail->Exponent);
	}
	
	return head;
} 

void Print(Polynomial L){
	if(L == NULL){
		printf("\n");
		return;
	}
	
	Polynomial temp = L->Next;
	while(temp != NULL){
		printf("%d %d ", temp->Coefficient, temp->Exponent);
		temp = temp->Next;
	}
	printf("\n");
	return;
}
```

   - 多重表 | Multilists
   - 基数排序 | Radix Sort


### 栈 ADT | The Stack ADT
栈是一个后进先出（LIFO）表，限制了插入和删除只能在表的末端（成为栈顶，top）进行。典型的操作是 Push, Pop 和 Top（读取栈顶元素的值）。

#### 实现

   1. 链表实现。与链表实现线性表一样，栈通过一个头结点指示。当栈为空时，该节点指向 NULL。Push, Pop 和 Top 通过对链表前段进行插入、删除或读取实现。
   2. 数组实现。数组实现是显然的。
:::info
需要提示的是：在之前，我们用数组实现栈时通常习惯把栈顶指针指向栈顶元素的上面一个元素（即下次 push 的位置）；但是课程及课本的实现方式是确切指到栈顶元素（即刚刚 push 进去的东西）。因此在某些实现思路上存在偏差。这一偏差在作业 **6-2 Two Stacks In One Array** 中体现了出来。此记录。
:::

#### 应用

   - [后缀表达式 | Postfix Expression](https://www.yuque.com/xianyuxuan/coding/gl2s3b#MKeuv)

#### 一道有趣的作业 ： 7-1 Pop Sequence 
Given a stack which can keep _M_ numbers at most. Push _N_ numbers in the order of 1, 2, 3, ..., _N_ and pop randomly. You are supposed to tell if a given sequence of numbers is a possible pop sequence of the stack. For example, if _M_ is 5 and _N_ is 7, we can obtain 1, 2, 3, 4, 5, 6, 7 from the stack, but not 3, 2, 1, 7, 5, 6, 4.<br />**Input Specification:**<br />Each input file contains one test case. For each case, the first line contains 3 numbers (all no more than 1000): _M_ (the maximum capacity of the stack), _N_ (the length of push sequence), and _K_ (the number of pop sequences to be checked). Then _K_ lines follow, each contains a pop sequence of _N_ numbers. All the numbers in a line are separated by a space.<br />**Output Specification:**<br />For each pop sequence, print in one line "YES" if it is indeed a possible pop sequence of the stack, or "NO" if not.<br />**Sample Input:**
```
5 7 5
1 2 3 4 5 6 7
3 2 1 7 5 6 4
7 6 5 4 3 2 1
5 6 4 3 7 2 1
1 7 6 5 4 3 2
```
**Sample Output:**
```
YES
NO
NO
YES
NO
```
           大模拟可以简单地用 ![](https://cdn.nlark.com/yuque/__latex/7ba55e7c64a9405a0b39a1107e90ca94.svg#card=math&code=O%28n%29&height=20&width=36) 完成，优化的意义并不很大。但这里是否有更优的做法？


### 队列 ADT | The Queue ADT
队列是一个先进先出（FIFO）表。入队（Enqueue）在队尾（rear）插入一个元素，出队（Dequeue）则删除队头（front）的一个元素。<br />课本中只介绍了队列的数组实现，这种实现是显然的。同时，为了防止“假溢出”，课本介绍了循环队列的写法（并提出“它可能会使运行时间加倍”）。





![_EOF.png](./assets/1603246603191-fccc9713-2e61-4d7d-8d43-59a2d5e470a5.png)

