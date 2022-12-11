**堆的性质** ：堆是一棵树，每一个结点都有一个键值 `key` ，且 **每个结点** 的键值都大于等于 / 小于等于其父亲的键值，称为小根堆 / 大根堆。由于小根堆和大根堆具有明显的对称性，若无说明，我们在下文讨论的都是小根堆。<br />**优先队列**（priority queue）是非常常用的一种数据结构。使用时，它需要支持的主要操作有：插入（入队），查询和删除最小值（出队）。由于小根堆的树根储存的即为整个堆中的最小键值，我们可以用堆来实现优先队列。

## 1 二叉堆 | Binary Heaps
首先我们探讨 **二叉堆** 。

### 1.1 结构
在未加说明的情况下，堆（heap）通常指二叉堆。二叉堆是一棵完全二叉树（complete binary tree），因此我们可以用一个一位数组储存一个二叉堆。显然，第 ![](https://cdn.nlark.com/yuque/__latex/865c0c0b4ab0e063e5caa3387c1a8741.svg#card=math&code=i&height=16&width=5) 个结点的左右儿子的下标分别是 ![](https://cdn.nlark.com/yuque/__latex/e5de2e95102b1ed31c3edbcd9701b6f0.svg#card=math&code=2i&height=16&width=14) 和 ![](https://cdn.nlark.com/yuque/__latex/a17022c3643548e48f666c66236fad49.svg#card=math&code=2i%2B1&height=16&width=43)。我们可以用一个数组、一个代表最大容量的整数和一个代表当前结点个数的整数表示一个二叉堆。

![image.png](./assets/1605938882879-6485a582-e29a-4c49-a75f-91b5736d4975.png)
一棵完全二叉树。上面的数字表示结点的序号而非键值

下面我们考虑（小根）二叉堆的一些基本操作。

### 1.2 插入操作
首先，为了满足完全二叉树的性质，插入一个新的元素后树的结构是唯一的。因此我们首先在下一个空闲位置处把新的元素放进去。但是，这个元素的插入可能会导致堆性质被破坏，这时我们就需要做一些调整。我们采用 **向上调整**（或 **上滤**，percolate up）：从插入的结点开始，如果它的权值小于父结点的值，我们将它们做交换，重复此过程直至不满足或者到根。这一操作的复杂度是 ![](https://cdn.nlark.com/yuque/__latex/2cb8094761b08b61fce3375da7042dfa.svg#card=math&code=O%28%5Clog%5C%20n%29%20&height=20&width=64) 的。

### 1.3 删除最小值操作
删除最小值，在小根堆里就是删除根节点。与插入操作相同，删除一个结点后树的结构仍然是唯一的，所以实际上我们需要给最后一个结点分配一个合理的位置。这时根结点的位置恰好被空了出来，因此我们首先将最后一个结点放在根结点的位置上。但是这也可能导致堆的性质被破坏，这时我们采用 **向下调整** （或 **下滤**，percolate down）：从插入的结点开始，如果它的权值大于任一子结点的权值，我们将它和较小的子结点交换，重复此过程直至不满足或者到底层。这一操作的复杂度也是![](https://cdn.nlark.com/yuque/__latex/2cb8094761b08b61fce3375da7042dfa.svg#card=math&code=O%28%5Clog%5C%20n%29%20&height=20&width=64) 的。

除了这些基本操作以外，我们可能还会涉及到一些其他常用操作：

### 1.4 建堆



## 2 左倾堆 | Leftist Heaps
左倾堆也称左偏树、左堆等等。

### 2.1 引入：堆的合并
如前所述，一般的二叉堆具有较好的平衡性。但是，如果我们希望两个二叉堆进行合并 (假设结点数分别为 M 和 N，其中 M <= N)，我们可以通过将较小的二叉堆逐个插入较大的堆，复杂度为![](https://cdn.nlark.com/yuque/__latex/94098d4b6716836287a1fc518e380f71.svg#card=math&code=O%28M%5Clog%20N%29&height=20&width=86)；或者直接将两个堆中的元素进行重新建堆，复杂度为 ![](https://cdn.nlark.com/yuque/__latex/034d4db04be85fef0334b6527626d63c.svg#card=math&code=O%28M%2BN%29&height=20&width=78)。可以看到，这两种合并操作都是较差的。其根本原因在于，合并两个二叉堆时维持其二叉堆的性质（即完全二叉树）是困难的；而且这两种合并方式并没有利用到这两个堆本身的堆性质；而堆性质在堆的合并中理应发挥一定作用。因此我们尝试找到一种堆的合并方式，能够利用原先两个堆的堆性质。

我们考虑这样一种合并方式，这种合并方式可以维持堆的 **堆性质** ，但是合并后它不一定仍是一个二叉堆，因为它不是一棵完全二叉树：<br />我们讨论小根堆。我们用 ![](https://cdn.nlark.com/yuque/__latex/65d3a8c6c0adfc7209899b58005ec6e4.svg#card=math&code=k_x&height=18&width=16) 表示一个小根堆根节点的键值。当我们将两个堆 x 和 y 合并时，不妨设 ![](https://cdn.nlark.com/yuque/__latex/0413fa512250e0df23dd5a9f684c9c9b.svg#card=math&code=k_x%20%5Cleq%20k_y%20&height=20&width=56)（如果不满足，交换即可），那么根据堆的性质， x 的根节点将成为合并后的新的根节点。那么我们可以用 x 的右子树（也是一个小根堆）和 y 进行合并，并将合并出来的堆作为 x 新的右子树。不断递归重复这一过程，直到 x （这里的 x 不是初始的 x，而是 x 或者 y 的某一个子树）为空时，返回 y。<br />我们分析这种算法的复杂度。我们用 ![](https://cdn.nlark.com/yuque/__latex/1bed63afcd0cd360bb1bf81f4cd66214.svg#card=math&code=h_x&height=18&width=18) 表示一棵树最右边那条链上的结点数。对于每一层递归，其 ![](https://cdn.nlark.com/yuque/__latex/15903ff6bd2fe64cf833af31bba4f1d2.svg#card=math&code=h_x%2Bh_y&height=20&width=56) 的值均比上一层小 1。因此该算法的复杂度为 ![](https://cdn.nlark.com/yuque/__latex/31315744f3cf1f0bbd4225a55161f9cb.svg#card=math&code=O%28h_x%2Bh_y%29%20&height=21&width=82)。但由于这种合并操作会破坏堆的平衡性，存在情况使得这样操作后的堆退化成一条向右的链，此后的合并、插入、删除等操作复杂度可能达到 ![](https://cdn.nlark.com/yuque/__latex/33697ce7dfa48ba80980d298c8089378.svg#card=math&code=O%28N%29&height=20&width=41)。而这种合并操作也很难满足二叉堆的要求，因此我们需要一种数据结构，使得其更容易在合并中维持性质，而且还具有一定的 **平衡性**（即使没有二叉堆那么强）。我们将这种可以支持较为高效的合并的操作的堆称为 **可并堆** 。下面介绍的左倾堆即为其中一种。


### 2.2 定义

#### 2.2.1 Null Path Length 
我们定义一棵二叉树中任一结点 X 的 **Null Path Length** ![](https://cdn.nlark.com/yuque/__latex/5c4ab7c292ac2be8f344f0dcf353577d.svg#card=math&code=%5Ctext%7BNpl%7D%28X%29&height=20&width=53) 为从 X 出发到最近的、只有 0 个或 1 个孩子的结点的路径长。特别地，我们定义 ![](https://cdn.nlark.com/yuque/__latex/52a7bf69bc8191c7d7686de021b66bd2.svg#card=math&code=%5Ctext%7BNpl%28Null%29%7D%20%3D%20-1&height=20&width=115)。<br />我们可以发现，一个结点的 Npl 即为其所有子结点（包括 NULL）中最小的 Npl + 1。

给定一棵二叉树根节点的 Npl，当且仅当对其中每个节点都有其左儿子和右儿子的 Npl 相等时，这个二叉树的节点数最少。此时这棵二叉树是一棵满二叉树，有 ![](https://cdn.nlark.com/yuque/__latex/dd1567971cc8513af854e877352f0557.svg#card=math&code=2%5E%7B%5Ctext%7BNpl%7D%2B1%7D-1&height=20&width=73) 个结点。<br />因此，对于一棵有 N 个结点的二叉树，其根节点的 Npl 不超过 ![](https://cdn.nlark.com/yuque/__latex/8932feaf07e4ed19a017c52006d1ce2e.svg#card=math&code=%5Clfloor%20%5Clog_2%28N%2B1%29%5Crfloor-1%20%3D%20O%28%5Clog%20N%29%20&height=20&width=218)。

注意：Npl 的定义及上述性质适用于所有二叉树。


#### 2.2.2 左倾堆
我们称一棵二叉树为左倾堆，如果它满足以下两条性质：

   - **堆性质**；
   - **左偏性质**：对于其中任一结点，其左儿子的 Npl 不小于右儿子的 Npl。

显然，一个左倾堆的任一子树也是左倾堆。

需要关注的是，左倾堆的 Npl 是 ![](https://cdn.nlark.com/yuque/__latex/70664169d1bc6295401283e5520056e1.svg#card=math&code=O%28%5Clog%20N%29&height=20&width=65) 的，但是其深度没有保证。例如，一条左斜的链也是一个左倾堆，其深度是 ![](https://cdn.nlark.com/yuque/__latex/33697ce7dfa48ba80980d298c8089378.svg#card=math&code=O%28N%29&height=20&width=41) 的，但其 Npl 为 0。<br />但是，我们在 2.1 中提出的合并方式的复杂度取决于堆最右边的那条链；而左倾堆由于其左偏性质，其 Npl 一定由最右边的那条链决定。也就是说，左倾堆维持的“平衡性”就是让它左重右轻；从而维持最右边链的链长在 ![](https://cdn.nlark.com/yuque/__latex/70664169d1bc6295401283e5520056e1.svg#card=math&code=O%28%5Clog%20N%29&height=20&width=65) 的水平。这就是左倾堆设计的意义所在。


### 2.3 操作

#### 2.3.1 合并操作
我们如同 2.1 中所说的那样进行合并。唯一不同的是，为了维护堆的左偏性质，我们在每一次合并后比较当前结点孩子的左右子树是否满足左偏要求；即：如果当前节点左儿子的 Npl 小于右儿子的 Npl，交换它们。每一次合并后应同时维护当前结点的 Npl 为右儿子的 Npl + 1。

我们分析这一操作的复杂度。如我们在 2.1 中分析的那样，合并操作的复杂度是![](https://cdn.nlark.com/yuque/__latex/31315744f3cf1f0bbd4225a55161f9cb.svg#card=math&code=O%28h_x%2Bh_y%29%20&height=21&width=82)。我们说过，由于左倾堆的左偏性质，其 Npl 由其右子树决定。而我们每一次合并都是对右子树的操作，在每一层递归中，![](https://cdn.nlark.com/yuque/__latex/15903ff6bd2fe64cf833af31bba4f1d2.svg#card=math&code=h_x%2Bh_y%20&height=20&width=56) 会 -1，也就是 ![](https://cdn.nlark.com/yuque/__latex/41b41c09a406c56f02ec0fafc4cd5cc8.svg#card=math&code=%5Ctext%7BNpl%7D%28x%29%2B%5Ctext%7BNpl%7D%28y%29%20&height=20&width=118) 也一定会 -1。因此该算法的复杂度为 ![](https://cdn.nlark.com/yuque/__latex/663ebbe52100bebff8fcb1c7ac49d85d.svg#card=math&code=O%28%5Ctext%7BNpl%7D%28x%29%2B%5Ctext%7BNpl%7D%28y%29%29&height=20&width=144)。结合 2.2.1 中对 Npl 的分析，我们得到算法复杂度为 ![](https://cdn.nlark.com/yuque/__latex/2782c514eb9960194520d599c03665ba.svg#card=math&code=O%28%5Clog%20N%2B%5Clog%20M%29%20%3D%20O%28%5Clog%20N%29&height=20&width=215)。


#### 2.3.2 其他操作
左斜堆的其他操作均基于合并操作。实际上，任何一个可并堆都可以基于合并操作完成如下操作：

   - 插入操作：视为与一个单结点的堆进行合并。
   - 删除最小值：合并左右子树。


### 2.4 References
以下是部分帮助我理解上述内容的关键文档：

   - 为什么要用 Leftist Heap：[https://www.luogu.com.cn/blog/hsfzLZH1/solution-p3377](https://www.luogu.com.cn/blog/hsfzLZH1/solution-p3377)
   - 复杂度分析：[https://oi-wiki.org/ds/leftist-tree](https://oi-wiki.org/ds/leftist-tree)


## 3 随机堆 | Randomized Heaps
随机堆解决的同样是 2.1 中提出的问题。其合并策略在于，每次随机决定使用左子树还是右子树进行合并。其他操作与 2.3.2 所示一致。

### 3.1 复杂度分析
复杂度分析参见 Ref。学完随机化再来补）

### 3.2 References

   - [https://cp-algorithms.com/data_structures/randomized_heap.html](https://cp-algorithms.com/data_structures/randomized_heap.html)


## 4 斜堆 | Skew Heaps
斜堆是左倾堆的一个变种，其合并思路与 2.1 中的一致。斜堆不统计 Npl，其维持一定平衡性的方法是：在合并的每一层递归中，一定交换左右子树。这一方法的直观原理是：每一次合并都会使得最右路径的长度增加，因此交换左右子树就更可能平衡这一增加带来的影响。<br />其他操作与 2.3.2 所示一致。

### 4.1 复杂度分析
Skew Heaps 进行合并的摊还复杂度为 ![](https://cdn.nlark.com/yuque/__latex/70664169d1bc6295401283e5520056e1.svg#card=math&code=O%28%5Clog%20N%29&height=20&width=65)。<br />emm 等学摊还分析的时候一并写吧qwq

### 4.2 References

   - 斜堆的直观意义：[https://zh.wikipedia.org/wiki/%E6%96%9C%E5%A0%86](https://zh.wikipedia.org/wiki/%E6%96%9C%E5%A0%86)
   - 复杂度分析：cyll 的课件

![_TBC.png](./assets/1606057224877-aa56f004-cca0-4d08-a94d-ba3302c09716.png)
