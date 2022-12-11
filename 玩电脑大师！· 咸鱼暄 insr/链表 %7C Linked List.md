:::info
本文使用的主要编程语言是 C 语言。<br />阅读本文，需要掌握 [0 C/C++ 入门](https://www.yuque.com/xianyuxuan/coding/cpp-start) 的全部知识以及 [2.7.5 动态内存分配](https://www.yuque.com/xianyuxuan/coding/apd2_7#VsCZy) 的知识。如果没有掌握指针知识，可以阅读 [0 什么是链表](#1eKHn) 后直接阅读 [4 数组模拟链表](#cSHli)。<br />对于一些没有指针的编程语言，同样可以通过 [4 数组模拟链表](#cSHli) 的方式实现链表。
:::

---


### 0 什么是链表
链表和数组都可用于存储数据，其中链表通过指针来连接元素，而数组则是把所有元素按次序依次存储。<br />不同的存储结构令他们有了不同的优势：<br />链表可以方便地删除、插入数据，操作次数是 ![](https://cdn.nlark.com/yuque/__latex/5e079a28737d5dd019a3b8f6133ee55e.svg#card=math&code=O%281%29&height=20&width=34) 。但寻找读取数据的效率不如数组高，操作次数是 ![](https://cdn.nlark.com/yuque/__latex/7ba55e7c64a9405a0b39a1107e90ca94.svg#card=math&code=O%28n%29&height=20&width=36)。
![image.png](./assets/1585989925915-b6d38b49-25b4-4ddc-b375-d35e79762062.png)
图 1（图源: 《啊哈！算法》）<br />数组可以方便的寻找读取数据，在随机访问中操作次数是 ![](https://cdn.nlark.com/yuque/__latex/5e079a28737d5dd019a3b8f6133ee55e.svg#card=math&code=O%281%29&height=20&width=34) 。但删除、插入的操作次数却是却是 ![](https://cdn.nlark.com/yuque/__latex/7ba55e7c64a9405a0b39a1107e90ca94.svg#card=math&code=O%28n%29&height=20&width=36) 次。<br />另外，数组的大小必须在编译时确定，而链表的大小可以在内存时动态分配。


### 1 单向链表

#### 建立链表
图 1 中链表的每一个节点指向了下一个节点，这样的链表是单向链表。单项链表中每一个节点都包含了其数据以及指向下一个节点的指针。例如：
```cpp
struct Node{
    int value;
    struct Node *next;
};
```

每一个链表都需要有一个头结点指针，从头结点开始，我们可以遍历整个链表。链表没有元素时，头结点指针为空。即：`struct Node *head = NULL;` 。<br />为了方便我们在链表尾部增加节点，有时我们也会定义一个尾结点指针： `struct Node *tail = NULL;` 。


#### 增加节点
每当我们在链表尾部建立一个新的节点（值为 val）时，我们可以使用：
```cpp
if (head == NULL){
   tail = (struct Node *)malloc(sizeof(struct Node));
   head = tail;
} else{
   tail->next = (struct Node *)malloc(sizeof(struct Node));
   tail = tail->next;
}
tail->value = val;
tail->next = NULL;
```


#### 插入节点
如果我们需要在 p 和 p->next 之间插入一个节点（值为 val），我们可以使用：
```cpp
struct Node *node = (struct Node *)malloc(sizeof(struct Node));
node->value = val;
node->next = p->next;
p->next = node;
```


#### 删除节点
如果我们需要删除 p 之后的一个节点，我们可以使用：<br />`p->next = p->next->next;` <br />如果我们需要删除节点 p，我们可以使用（即用 p->next 覆盖 p 后删除 p->next）：
```cpp
p->value = p->next->value;
p->next = p->next->next;
```


#### 遍历链表
如果需要遍历整个链表，我们可以使用：
```cpp
for(struct node *p = head; p != NULL; p = p->next){
    /* do something */
}
```


### 2 双向链表


### 3 循环链表


### 4 数组模拟链表（链表的游标实现）


### 参考资料

- [链表 | OI Wiki](https://oi-wiki.org/ds/linked-list/)
- 《啊哈！算法》
