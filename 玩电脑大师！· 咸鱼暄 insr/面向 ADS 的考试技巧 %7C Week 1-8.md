刷一刷 ADS 的题，尝试解决一下考试。


### 1 平衡搜索树

#### AVL 树
balance factor BF( node ) = hL - hR 
![image.png](./assets/1620477098771-66372c0a-4069-4249-924c-f4a9b76246ff.png)
AVL 树结点数最小的情况是 ![](https://cdn.nlark.com/yuque/__latex/b558d4cd48147afe3a4ccc140d59ecd5.svg#card=math&code=F_N%20%3D%201%20%2B%20F_%7BN-1%7D%20%2B%20F_%7BN-2%7D&id=yYuub)
:::danger
![image.png](./assets/1625679034849-94497007-c47a-467b-b7f4-0af4a4019d16.png)
:::

:::success

- If the depth of an AVL tree is 6 (the depth of an empty tree is defined to be -1), then the minimum possible number of nodes in this tree is (33)
:::

:::success
![image.png](./assets/1620700331244-ae208962-4a43-4ca1-bba6-c71e51e95d4c.png)
:::

:::success
(F)	In an AVL tree, it is impossible to have the balance factor of every non-leaf node to be +1.
:::

:::success
![image.png](./assets/1625677991721-8b5fdf43-a74d-4bdb-b5ec-8e7ea2a6f262.png)
只有 I。AVL 删除就是 BST 删除然后调整；但是有可能到 O(log N)
:::


#### Splay 树
![image.png](./assets/1620477570147-c3eda8b8-baaf-487b-9278-4e5bcff3d354.png)
:::success
![image.png](./assets/1620701403420-d37b3856-1bc3-4ee0-a2e7-3810841b3883.png)
![image.png](./assets/1620701418436-7be75c5b-982e-40e5-b63b-9b1632476887.png)
:::

:::success
(T)	The result of inserting keys 1 to 2_k_−1 for any _k_>4 in order into an initially empty skew heap is always a full binary tree.<br />(T)	The right path of a skew heap can be arbitrarily long.<br />(T)	All of the Zig, Zig-zig, and Zig-zag rotations not only move the accessed node to the root, but also roughly half the depth of most nodes on the path. 
:::

:::warning
![image.png](./assets/1625678298296-13280a26-bc93-42fb-84c4-c8b74b961900.png)
![image.png](./assets/1625678452895-7ae0df20-904e-4abb-91eb-cd68656243bb.png)
（上图来自 cyll 微信群 wrh 学长）
:::


#### Red-Black 树
根始终为黑色。
![image.png](./assets/1625645757190-352c3048-a9dd-48bc-84f0-d74cbb4dbe11.png)
![image.png](./assets/1625643370585-4478e6a1-122c-42ca-a073-8a17d64b7bcb.png)
![image.png](./assets/1620702726330-3ffa25bc-dfc5-4752-80ec-914a61083b3f.png)
注意：bh 从 0 开始数，而且要数 NIL
![image.png](./assets/1620477983103-abdf53e2-2203-4a39-bee0-8b775becc3e8.png)
:::success
![image.png](./assets/1620702783861-10cf9998-70ca-4dfb-879d-4f94b98466ee.png)
![image.png](./assets/1620702818394-2f5bb043-8b45-44d5-b33e-2bd4bd239a82.png)
:::
:::success
(F)	In a red-black tree with 3 nodes, there must be a red node.<br />(T) 	In a red-black tree with 2 nodes, there must be a red node.<br />(T)	In a Red-Black tree, the path from the root to the farthest leaf is no more than twice as long as the path from the root to the nearest leaf.<br />(F)	When inserting a node into a red-black tree, we shall first insert the node as into an ordinary binary search tree, and then color the node black.

   - color it red.
:::
:::warning
(B)	In the red-black tree that results after successively inserting the keys 41; 38; 31; 12; 19; 8 into an initially empty red-black tree, which one of the following statements is FALSE?<br />A.	38 is the root<br />B.	19 and 41 are siblings, and they are both red<br />C.	12 and 31 are siblings, and they are both black<br />D.	8 is red
:::
:::warning
![image.png](./assets/1625646728126-a1b23d3e-8d12-4311-ac24-607c90141991.png)
:::


**Delete** 还没学，不想学了
![image.png](./assets/1625644275270-c966ad70-7213-4dfa-aec5-71aad76d09bf.png)


#### B+ 树
2-3 树就是允许一个结点里有 2~3 个值，插入第 4 个时分裂成 2+2，这视为给上一级也插入一个。<br />split it into 2 nodes with ![](https://cdn.nlark.com/yuque/__latex/7bcb3894c9bc9c7d19be7099a359aa55.svg#card=math&code=%5Clceil%20%5Cfrac%7BM%2B1%7D2%20%5Crceil&id=BWENt) and ![](https://cdn.nlark.com/yuque/__latex/80278b09a8f757c6db45a34c2c88b4a1.svg#card=math&code=%5Clfloor%20%5Cfrac%7BM%2B1%7D2%20%5Crfloor&id=Lpe5J) keys, respectively;
![image.png](./assets/1625645241739-98c84b7b-489e-405d-b8a8-a2e6d984de70.png)
插入一个最多需要 M 次操作，因为会将 M-1 个指针后移；进行分裂也需要 ![](https://cdn.nlark.com/yuque/__latex/bcd5c16ceda8a689e223d741f045f3ef.svg#card=math&code=O%28M%29&id=VfjdA) 的操作。最差情况下，需要从最下方一直分裂到根，而树的高度是 ![](https://cdn.nlark.com/yuque/__latex/e7e4a3a7f536a80e040abd74f8aab202.svg#card=math&code=O%28log_MN%29&id=eZ0q2)，因此插入一个节点的复杂度如图上红框所示。根据这个红框的内容，我们可以知道最优的 M 为 3 或者 4。
:::success
(T) In a B+ tree, leaves and nonleaf nodes have some key values in common.<br />(T) The time bound of the FIND operation in a B+ tree containing _N_ numbers is _O_(log_N_), no matter what the degree of the tree is.

- depth 有 log N / log M，每一层二分查找是 log M

(T)	The root of a B+ tree of order _m_ has at most _m_ subtrees.
:::
:::warning
(T)	A 2-3 tree with 3 nonleaf nodes must have 18 keys at most.

- 这里 key 就指叶子节点中的 key

(0)	A B+ tree of order 3 with 21 numbers has at least __ nodes of degree 2.
:::
:::success
![image.png](./assets/1625647511502-d3339f20-b033-4ff7-859d-8efbaaadb96c.png)
:::
:::warning
![image.png](./assets/1625648123263-05f1dca6-4ad2-48b3-ab48-c8f3ea0f1973.png)
:::
:::warning
(C)	Which of the following statements concerning a B+ tree of order _M_ is TRUE?<br />A.	the root always has between 2 and _M_ children<br />B.	not all leaves are at the same depth<br />C.	leaves and nonleaf nodes have some key values in common<br />D.	all nonleaf nodes have between ⌈_M_/2⌉ and _M_ children<br />**A: The root is either a leaf or has between 2 and M children.**<br />**D: All nonleaf nodes (except the root) have between **⌈**M/2**⌉** and M children.**
:::
<br />

### 2 各种优先队列
:::success
(T)	If we merge two heaps represented by complete binary trees, the time complexity is Θ(_N_) provided that the size of each heap is _N_.	（线性建堆）
:::


#### Leftist Heap
![image.png](./assets/1625655371254-cd4a0f65-7162-40a1-936c-7f7cd09a5ed5.png)
:::success
(T)	A leftist heap with the null path length of the root being _r_ must have at least 2_r_+1−1 nodes.<br />(F)	The NPL of each node in a heap is supposed to be calculated from top down.
:::

:::success
![image.png](./assets/1620699905227-f2c219ad-2b58-410c-874b-aac69b67e88f.png)
:::

:::success
![image.png](./assets/1620709082812-b39799e0-032d-48a7-9a68-e5bbf44bd24d.png)

:::

:::success
![image.png](./assets/1625656832129-f237396a-6798-4f41-8f9d-93b680524fb9.png)
:::

:::success
![image.png](./assets/1625656982082-c57e9b85-c35b-4bf8-bcd2-79cf225474e5.png)
:::


#### Skew Heap
![image.png](./assets/1625654843030-ee0ad90e-6991-4ffb-be3f-ebec4997ea6d.png)
:::warning
![image.png](./assets/1620708699938-92295b5b-73f4-466a-b81e-f0b198f585e6.png)
![image.png](./assets/1620708689165-d11e81ad-3146-41f1-85ea-b0b404fb499d.png)
上图中的红色标识是自然的：在合并的最后，14 与 25 进行合并，会导致 25 和 14 的右子树（NULL）合并，这样就会直接返回 25，并不会进入 25 进行进一步合并，因此 25 的子树不会交换位置。
:::

:::danger
**但是！如果并非只有左儿子，还是要换的，这非常的不自然！**（但是从摊还分析角度是自然的，因为需要保证将重结点转为轻结点；这也是符合 PPT 所给规律的），例如这个题：
![image.png](./assets/1625657146373-407b1d80-383d-4762-9104-80d07942d277.png)
![image.png](./assets/1625654795590-5649a48e-66ff-4994-ac05-8d3c608368cf.png)
:::

:::success
(F)	With the same operations, the resulting skew heap is always more balanced than the leftist heap.<br />(F)	With the same operations, the resulting leftist heap is always more balanced than the skew heap.<br />(T)	A skew heap is a heap data structure implemented as a binary tree. Skew heaps are advantageous because of their ability to merge more quickly than balanced binary heaps. The worst case time complexities for Merge, Insert, and DeleteMin are all _O_(_N_), while the amorited time complexities for Merge, Insert, and DeleteMin are all _O_(_logN_).
:::

:::success
(B)	Insert keys 1 to 15 in order into an initially empty skew heap. Which one of the following statements is FALSE?<br />A.	the resulting tree is a complete binary tree<br />B.	there are 6 leaf nodes<br />C.	6 is the left child of 2<br />D.	11 is the right child of 7
:::

> 摊还分析
> ![image.png](./assets/1625655703979-c6b8559f-b983-4e77-9954-2a28bc6d5d65.png)
> ![image.png](./assets/1625655711809-417c03a5-0682-4f7a-a384-f955ce36068f.png)



#### Binomial Queue
![image.png](./assets/1620699360918-83f0ece4-ab81-4683-a247-81926f628ef5.png)
![image.png](./assets/1625662318850-895285a1-7491-4d08-b237-7d46d9653e34.png)

:::success
(T)	Making _N_ insertions into an initally empty binomial queue takes _O_(_N_) time in the worst case.<br />(F)	To implement a binomial queue, the subtrees of a binomial tree are linked in increasing sizes.<br />(T)	To implement a binomial queue, left-child-next-sibling structure is used to represent each binomial tree.<br />(F)	For a binomial queue, delete-min takes a constant time on average.<br />(F)	For a binomial queue, merging takes a constant time on average.<br />(F)	Inserting a number into a binomial heap with 15 nodes costs less time than inserting a number into a binomial heap with 19 nodes.

- 1111 -> 10000 (4); 10011 -> 10100 (2)
:::
:::success
(B)	Which of the following binomial trees can represent a binomial queue of size 42?<br />A.	_B_0 _B_1 _B_2 _B_3 _B_4 _B_5<br />B.	_B_1 _B_3 _B_5<br />C.	_B_1 _B_5<br />D.	_B_2 _B_4

- 42 = 32 + 8 + 2 = 2^5 + 2^3 + 2^1

(-3)	The potential function _Q_ of a binomial queue is the number of the trees. After merging two binomial queues _H_1 with 22 nodes and _H_2 with 13 nodes，what is the potential change _Q_(_H_1+_H_2)−(_Q_(_H_1)+_Q_(_H_2)) ?

- 10110 + 01101 = 100011 (3 + 3 -> 3)
:::

:::warning
![image.png](./assets/1625670132935-22e67e05-0ff2-4a1b-86ee-9c48c88418c7.png)
只有可能是如下两种之一（注意 binomial queue 的保存方式）：
![image.png](./assets/1625670277582-0e997913-6af9-41ce-9798-3c40b1c0999f.png)
:::
:::success
(D)	For a binomial queue, __ takes a constant time on average.<br />A.	merging<br />B.	find-max<br />C.	delete-min<br />D.	insertion

- 其他三个都是 O(log N)；在空 binomial queue 上连续插入 N 个是 O(N) 的
:::
:::success
![image.png](./assets/1625670767438-d57cab97-f21a-4f63-91cc-be0c9d89d340.png)
1101 + 0111 = 10010，这里有 3 个 B2 (4, 13, 15, 18) (2, 11, 29, 55) (23, 24, 51, 65) 相加，因此会产生不同情况。<br />A B 必然对；<br />C 则 23 与 2 相加，此时 2 会继续与 12 相加，因此 12 确实是 2 的儿子<br />D 则 4 与 2 相加，此时 2 会继续与 12 相加，因此 2 的儿子是 11, 29, 4, 12，没有 23。
:::



### 3 摊还分析
核心思想：

   - 找到势能函数 ![](https://cdn.nlark.com/yuque/__latex/5b8f5adfb88f42d5b3ab1d4bfaef917f.svg#card=math&code=%5CPhi%28i%29&id=UdJxu)，记每种操作的 ![](https://cdn.nlark.com/yuque/__latex/96fafac0c054b9eb47d3f630ed02c289.svg#card=math&code=c_i&id=YLgNw) 是实际的时间花费
   - 使得各种操作的估计时间 ![](https://cdn.nlark.com/yuque/__latex/370797167404bf74ccf6612d48baf6aa.svg#card=math&code=%5Chat%20%7Bc_i%7D%20%3D%20c_i%20%2B%20%5CDelta%5CPhi&id=JEcOa) 都在一个不大于估计时间复杂度的级别
   - 由于![](https://cdn.nlark.com/yuque/__latex/971d176966bcbd4b8b1fe7ce210d3cc3.svg#card=math&code=%5CSigma_%7Bi%3D1%7D%5En%20%5Chat%7Bc_i%7D%20%3D%20%5CSigma_%7Bi%3D1%7D%5En%20c_i%20%2B%20%5CPhi%28n%29%20-%20%5CPhi%280%29%20%5Cgeq%20%5CSigma_%7Bi%3D1%7D%5En%20c_i%20%3D%20T%28n%29&id=zAV0F)
   - 则均摊时间 ![](https://cdn.nlark.com/yuque/__latex/4b565cf20dc6bda071a84d8ed360cf9f.svg#card=math&code=%5Cfrac%20%7BT%28n%29%7Dn%20%3D%20%5Cfrac%7B%5CSigma_%7Bi%3D1%7D%5En%20%5Chat%7Bc_i%7D%7D%20n&id=Zzt1d)
:::success
![image.png](./assets/1620698333029-2c481df0-8651-4e70-bde5-f6b54ccec817.png)
![B{E{S}69~X{KMNHI$H4O24M.png](./assets/1655972963141-c0274e5b-b189-4314-adff-c3f3230ae439.png)
则只有 D 选项中，三项操作的 ![](https://cdn.nlark.com/yuque/__latex/370797167404bf74ccf6612d48baf6aa.svg#card=math&code=%5Chat%20%7Bc_i%7D%20%3D%20c_i%20%2B%20%5CDelta%5CPhi&id=OGndJ) 分别为 +3, +1, 0。 因此均摊时间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/5e079a28737d5dd019a3b8f6133ee55e.svg#card=math&code=O%281%29&id=x9Lqj)。
:::


:::success
![image.png](./assets/1620700611945-29aa8196-6b8d-4b7b-a986-58516d1d990b.png)
:::

:::danger
(T)	In amortized analysis, a good potential function should always assume its minimum at the start of the sequence.<br />(F)	For one operation, if its average time bound is _O_(_logN_), then its amortized time bound must be _O_(_logN_).<br />(T)	For one operation, if its worst-case time bound is Θ(logN), then its amortized time bound must be O(logN). 
:::


### 4 倒排文件索引
![image.png](./assets/1625699198829-20257cf7-f9f8-4390-8088-d4264ab06bbf.png)
![image.png](./assets/1625699415484-34094f90-a3f4-49a0-927e-50ac5b42da9f.png)
维护 times 的作用：求几个 term 同时出现的 documents 时，从 times 小的 term 开始找。

Word Stemming：变成 stem / root 形式
![image.png](./assets/1625699659868-c926f3e7-9c9a-4a58-b1f1-f5422288505c.png)

using hashing, comparing to using search trees：faster for a single word but expensive for range search
![image.png](./assets/1625699786594-1429d281-eeb3-4e80-8e6b-7aa01c6c4ae1.png)

![image.png](./assets/1625700110408-0036d34c-df42-4b20-a543-99e2a474e3a1.png)

**Distributed indexing** - Term-partitioned insex / Document-partitioned index
![image.png](./assets/1620711712122-e4569de8-9f17-4b1c-8c81-3dd5bb058010.png)

**Dynamic indexing** - 用一个辅助 index 存储新文档，在合适的时机与 main index 合并；查询时从两边一起查
![image.png](./assets/1620711728012-d6594734-3de5-4f95-a2a4-32e407094623.png)

**Compression** - 两种思路：<br />1）压缩 term：将剩余 term 放在一个大字符串里，term 保存对应项在大字符串中的位置<br />2）压缩 posting list：存储每个 term 对应的文档编号与前一个对应文档的差而不是绝对的值
![image.png](./assets/1620711744016-c7fc0db1-194f-4bbe-92ed-8ec7e2bb9748.png)

**Thresholding **- 两种<br />1）Document - 给 documents 进行 rank，只返回前 x 个；不适用布尔查询，可能丢失部分相关文档<br />2）Query - 按照查询 term 频次由低到高进行查询；高于某个比例的不查询
![image.png](./assets/1620711794672-85972bab-8b9e-4027-8649-de4775fc6633.png)

**Measure**
![image.png](./assets/1625701009875-1eb8b928-a8a7-4ba7-a015-3b9ad2424126.png)
![image.png](./assets/1625701099702-b4e597ec-e857-4403-aa99-1aa0a7959d52.png)
![image.png](./assets/1620711814145-0bcb7612-c00b-4f60-b797-13ae71bb53c5.png)
:::warning
(C)	Two spam mail detection systems are tested on a dataset with 7981 ordinary mails and 2019 spam mails. System A detects 200 ordinary mails and 1800 spam mails, and system B detects 160 ordinary mails and 1500 spam mails. If our primary concern is to keep the important mails safe, which of the following is correct?<br />A.	Precision is our primary concern and system A is better.<br />B.	Recall is our primary concern and system B is better.<br />C.	Precision is our primary concern and system B is better.<br />D.	Recall is our primary concern and system A is better.
:::

:::danger
(T)	In data retrieval, the response time is more important than the relevance of the answer set.<br />(T)	When measuring the relevancy of the answer set, if the precision is low but the recall is high, it means that most of the relevant documents are retrieved, but too many irrelevant documents are returned as well.<br />(T)	When measuring the relevancy of the answer set, if the precision is high but the recall is low, it means that most of the relevant documents are missing, but most of the retrieved documents are relevant. <br />(F)	Word stemming is to eliminate the commonly used words from the original documents. <br />(T)	While accessing a term, hashing is faster than search trees.
:::

:::success
![image.png](./assets/1625677968942-5de3472c-a077-468d-9b24-ce101ff0217b.png)
![image.png](./assets/1625678615744-565bb886-dfc7-44d4-b92b-66117aa1932e.png)
:::
:::warning
(A)	Among the following groups of concepts, which group is not totally relevant to a search engine? (6分)

1. thresholding, dynamic programming, precision
2. word stemming, compression, recall
3. distributed index, hashing, inverted file index
4. stop words, posting list, dynamic indexing
:::


### 5 Backtracking
:::success
(F)	It is guaranteed that an exhaustive search can always find the solution in finite time.
:::
:::danger
(T)	In backtracking, if different solution spaces have different sizes, start testing from the partial solution with the smallest space size would have a better chance to reduce the time cost.<br />说明：<br />这里的 size of solution spaces 指的是在某种情况下可能的选择的个数，在搜索树里显示的就是子结点的个数。例如，我们认为下图中上面的情况的根节点比下面情况的根节点拥有更小的解空间；因此我们愿意使用上面这种情况，因为剪枝可以一下剪掉一大堆。
![image.png](./assets/1621865311203-6e1879a5-a935-41ed-b442-3b73ef47a790.png)
:::



##### 八皇后问题
:::success
(F)	In the 4-queens problem, (_x_1, _x_2, _x_3, _x_4) correspond to the 4 queens' column indices. During backtracking, (1, 4, 2, ?) will be checked before (2, 4, 1, ?), and none of them has any solution in their branches.<br />(T)	 In the 4-queens problem, (_x_1, _x_2, _x_3, _x_4) correspond to the 4 queens' column indices. During backtracking, (1, 3, 4, ?) will be checked before (1, 4, 2, ?), and none of them has any solution in their branches.  
:::


##### Turnpike Reconstruction Problem
（每次找剩下的最大距离，删除对应新增距离，没有对应的就回溯）


##### Tic-tac-toe
:::success
![image.png](./assets/1625672535955-5cfc9435-5299-49c5-a3fa-daa689c35d52.png)
答案是 0：两边都是 3。
![image.png](./assets/1625672526856-0781ee32-ec91-45ff-b352-85b404ecaf01.png)
:::


##### α-β 剪枝

α 剪枝是小中取大；β 是大中取小
![image.png](./assets/1625698237367-f6238f58-05e2-4ee0-bf11-f246b2abe9f6.png)
:::success
![image.png](./assets/1620710172908-7b5e1be9-99c0-4825-b12a-458013a9bffa.png)
记空白三个依次（层序）为 A B C。A 是 6, B, C 中的最大值，因此 15 如果被剪掉，说明即使 15<9，它也不影响 A 的值；即 B 已经必然不小于 C 的值了；而 C<=9，因此 B>=9，因此 x >= 9。
:::

:::success
![image.png](./assets/1625672336479-81928fac-5afa-4bdc-b2e8-09387f382c2e.png)
:::

:::warning
![image.png](./assets/1625677828135-386389d7-0524-4c4b-b54d-94b195ed860c.png)
:::


### 6 Divide & Conquer
:::danger
How many of the following sorting methods use(s) Divide and Conquer algorithm?

- Heap Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Selection Sort
- Shell Sort

(2)	Merge Sort：Divide 直接对半分，Merge 时耗时作比较；Quick Sort：Divide 耗时分成两部分，左边都比右边小，Merge 时直接合并。
:::

引例：对 y 也排序以后可以 ![](https://cdn.nlark.com/yuque/__latex/b8a262fbdf4ce5398d384195c6ed9851.svg#card=math&code=f%28N%29%3DO%28N%29&id=zq9K5)
![image.png](./assets/1620654388975-ee080390-1724-4b06-9a4f-d9e2d6b86674.png)
对应题目：
:::success
If devide-and-conquer strategy is used to find the closest pair of points in a plane, unless the points are sorted not only by their x coordinates but also by their y coordinates, it would be impossible to solve it in a time of O(NlogN), where N is the number of points.	**(T)**
:::


#### Master Theorem
![image.png](./assets/1620653626481-a026a616-dc44-4834-9e41-559094895c7e.png)
![image.png](./assets/1625707955723-ddd495ce-f50e-4688-a16f-801ee3ec8844.png)

:::success
(T)	For the recurrence equation _T_(_N_)=8_T_(_N_/2)+_N_3_logN_，we obtain _T_(_N_)=_O_(_N_3_logN_)acorrding to the Master Theorem.<br />(F)	![image.png](./assets/1625677588631-aaec61e7-f8d0-4d31-9da0-98f0e50d1bf4.png)
(F)	For the recurrence equation _T_(_N_)=_aT_(_N_/_b_)+_f_(_N_), if _af_(_N_/_b_)=_Kf_(_N_) for some constant _K_>1, then _T_(_N_)=Θ(_f_(_N_)).<br />(T)	![image.png](./assets/1625679135180-ba761f1e-a7d5-43cc-bbdd-85dac0ca91a0.png)
:::

:::warning
![image.png](./assets/1620710607275-0ac74852-dab9-44cd-be03-b18919cb7438.png)
:::

:::warning
![image.png](./assets/1620710615894-190877cf-8d1f-4204-bec3-64b75bfbe49f.png)
![](data:image/svg+xml;utf8,%3Csvg%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20width%3D%2245.844ex%22%20height%3D%223.176ex%22%20style%3D%22vertical-align%3A%20-0.838ex%3B%22%20viewBox%3D%220%20-1006.6%2019738.4%201367.4%22%20role%3D%22img%22%20focusable%3D%22false%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20aria-labelledby%3D%22MathJax-SVG-1-Title%22%3E%0A%3Ctitle%20id%3D%22MathJax-SVG-1-Title%22%3E%5Ctext%7BC.%20%7D3%26gt%3B2%5E1%2C%20O(N%5E%7B%5Clog_23%7D)%20%5Cquad%5Ctext%7BD.%20%7D3%3D3%5E1%2C%20O(N%5Clog%5E2N)%3C%2Ftitle%3E%0A%3Cdefs%20aria-hidden%3D%22true%22%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-43%22%20d%3D%22M56%20342Q56%20428%2089%20500T174%20615T283%20681T391%20705Q394%20705%20400%20705T408%20704Q499%20704%20569%20636L582%20624L612%20663Q639%20700%20643%20704Q644%20704%20647%20704T653%20705H657Q660%20705%20666%20699V419L660%20413H626Q620%20419%20619%20430Q610%20512%20571%20572T476%20651Q457%20658%20426%20658Q322%20658%20252%20588Q173%20509%20173%20342Q173%20221%20211%20151Q232%20111%20263%2084T328%2045T384%2029T428%2024Q517%2024%20571%2093T626%20244Q626%20251%20632%20257H660L666%20251V236Q661%20133%20590%2056T403%20-21Q262%20-21%20159%2083T56%20342Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-2E%22%20d%3D%22M78%2060Q78%2084%2095%20102T138%20120Q162%20120%20180%20104T199%2061Q199%2036%20182%2018T139%200T96%2017T78%2060Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-33%22%20d%3D%22M127%20463Q100%20463%2085%20480T69%20524Q69%20579%20117%20622T233%20665Q268%20665%20277%20664Q351%20652%20390%20611T430%20522Q430%20470%20396%20421T302%20350L299%20348Q299%20347%20308%20345T337%20336T375%20315Q457%20262%20457%20175Q457%2096%20395%2037T238%20-22Q158%20-22%20100%2021T42%20130Q42%20158%2060%20175T105%20193Q133%20193%20151%20175T169%20130Q169%20119%20166%20110T159%2094T148%2082T136%2074T126%2070T118%2067L114%2066Q165%2021%20238%2021Q293%2021%20321%2074Q338%20107%20338%20175V195Q338%20290%20274%20322Q259%20328%20213%20329L171%20330L168%20332Q166%20335%20166%20348Q166%20366%20174%20366Q202%20366%20232%20371Q266%20376%20294%20413T322%20525V533Q322%20590%20287%20612Q265%20626%20240%20626Q208%20626%20181%20615T143%20592T132%20580H135Q138%20579%20143%20578T153%20573T165%20566T175%20555T183%20540T186%20520Q186%20498%20172%20481T127%20463Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-3E%22%20d%3D%22M84%20520Q84%20528%2088%20533T96%20539L99%20540Q106%20540%20253%20471T544%20334L687%20265Q694%20260%20694%20250T687%20235Q685%20233%20395%2096L107%20-40H101Q83%20-38%2083%20-20Q83%20-19%2083%20-17Q82%20-10%2098%20-1Q117%209%20248%2071Q326%20108%20378%20132L626%20250L378%20368Q90%20504%2086%20509Q84%20513%2084%20520Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-32%22%20d%3D%22M109%20429Q82%20429%2066%20447T50%20491Q50%20562%20103%20614T235%20666Q326%20666%20387%20610T449%20465Q449%20422%20429%20383T381%20315T301%20241Q265%20210%20201%20149L142%2093L218%2092Q375%2092%20385%2097Q392%2099%20409%20186V189H449V186Q448%20183%20436%2095T421%203V0H50V19V31Q50%2038%2056%2046T86%2081Q115%20113%20136%20137Q145%20147%20170%20174T204%20211T233%20244T261%20278T284%20308T305%20340T320%20369T333%20401T340%20431T343%20464Q343%20527%20309%20573T212%20619Q179%20619%20154%20602T119%20569T109%20550Q109%20549%20114%20549Q132%20549%20151%20535T170%20489Q170%20464%20154%20447T109%20429Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-31%22%20d%3D%22M213%20578L200%20573Q186%20568%20160%20563T102%20556H83V602H102Q149%20604%20189%20617T245%20641T273%20663Q275%20666%20285%20666Q294%20666%20302%20660V361L303%2061Q310%2054%20315%2052T339%2048T401%2046H427V0H416Q395%203%20257%203Q121%203%20100%200H88V46H114Q136%2046%20152%2046T177%2047T193%2050T201%2052T207%2057T213%2061V578Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-2C%22%20d%3D%22M78%2035T78%2060T94%20103T137%20121Q165%20121%20187%2096T210%208Q210%20-27%20201%20-60T180%20-117T154%20-158T130%20-185T117%20-194Q113%20-194%20104%20-185T95%20-172Q95%20-168%20106%20-156T131%20-126T157%20-76T173%20-3V9L172%208Q170%207%20167%206T161%203T152%201T140%200Q113%200%2096%2017Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMATHI-4F%22%20d%3D%22M740%20435Q740%20320%20676%20213T511%2042T304%20-22Q207%20-22%20138%2035T51%20201Q50%20209%2050%20244Q50%20346%2098%20438T227%20601Q351%20704%20476%20704Q514%20704%20524%20703Q621%20689%20680%20617T740%20435ZM637%20476Q637%20565%20591%20615T476%20665Q396%20665%20322%20605Q242%20542%20200%20428T157%20216Q157%20126%20200%2073T314%2019Q404%2019%20485%2098T608%20313Q637%20408%20637%20476Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-28%22%20d%3D%22M94%20250Q94%20319%20104%20381T127%20488T164%20576T202%20643T244%20695T277%20729T302%20750H315H319Q333%20750%20333%20741Q333%20738%20316%20720T275%20667T226%20581T184%20443T167%20250T184%2058T225%20-81T274%20-167T316%20-220T333%20-241Q333%20-250%20318%20-250H315H302L274%20-226Q180%20-141%20137%20-14T94%20250Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMATHI-4E%22%20d%3D%22M234%20637Q231%20637%20226%20637Q201%20637%20196%20638T191%20649Q191%20676%20202%20682Q204%20683%20299%20683Q376%20683%20387%20683T401%20677Q612%20181%20616%20168L670%20381Q723%20592%20723%20606Q723%20633%20659%20637Q635%20637%20635%20648Q635%20650%20637%20660Q641%20676%20643%20679T653%20683Q656%20683%20684%20682T767%20680Q817%20680%20843%20681T873%20682Q888%20682%20888%20672Q888%20650%20880%20642Q878%20637%20858%20637Q787%20633%20769%20597L620%207Q618%200%20599%200Q585%200%20582%202Q579%205%20453%20305L326%20604L261%20344Q196%2088%20196%2079Q201%2046%20268%2046H278Q284%2041%20284%2038T282%2019Q278%206%20272%200H259Q228%202%20151%202Q123%202%20100%202T63%202T46%201Q31%201%2031%2010Q31%2014%2034%2026T39%2040Q41%2046%2062%2046Q130%2049%20150%2085Q154%2091%20221%20362L289%20634Q287%20635%20234%20637Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-6C%22%20d%3D%22M42%2046H56Q95%2046%20103%2060V68Q103%2077%20103%2091T103%20124T104%20167T104%20217T104%20272T104%20329Q104%20366%20104%20407T104%20482T104%20542T103%20586T103%20603Q100%20622%2089%20628T44%20637H26V660Q26%20683%2028%20683L38%20684Q48%20685%2067%20686T104%20688Q121%20689%20141%20690T171%20693T182%20694H185V379Q185%2062%20186%2060Q190%2052%20198%2049Q219%2046%20247%2046H263V0H255L232%201Q209%202%20183%202T145%203T107%203T57%201L34%200H26V46H42Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-6F%22%20d%3D%22M28%20214Q28%20309%2093%20378T250%20448Q340%20448%20405%20380T471%20215Q471%20120%20407%2055T250%20-10Q153%20-10%2091%2057T28%20214ZM250%2030Q372%2030%20372%20193V225V250Q372%20272%20371%20288T364%20326T348%20362T317%20390T268%20410Q263%20411%20252%20411Q222%20411%20195%20399Q152%20377%20139%20338T126%20246V226Q126%20130%20145%2091Q177%2030%20250%2030Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-67%22%20d%3D%22M329%20409Q373%20453%20429%20453Q459%20453%20472%20434T485%20396Q485%20382%20476%20371T449%20360Q416%20360%20412%20390Q410%20404%20415%20411Q415%20412%20416%20414V415Q388%20412%20363%20393Q355%20388%20355%20386Q355%20385%20359%20381T368%20369T379%20351T388%20325T392%20292Q392%20230%20343%20187T222%20143Q172%20143%20123%20171Q112%20153%20112%20133Q112%2098%20138%2081Q147%2075%20155%2075T227%2073Q311%2072%20335%2067Q396%2058%20431%2026Q470%20-13%20470%20-72Q470%20-139%20392%20-175Q332%20-206%20250%20-206Q167%20-206%20107%20-175Q29%20-140%2029%20-75Q29%20-39%2050%20-15T92%2018L103%2024Q67%2055%2067%20108Q67%20155%2096%20193Q52%20237%2052%20292Q52%20355%20102%20398T223%20442Q274%20442%20318%20416L329%20409ZM299%20343Q294%20371%20273%20387T221%20404Q192%20404%20171%20388T145%20343Q142%20326%20142%20292Q142%20248%20149%20227T179%20192Q196%20182%20222%20182Q244%20182%20260%20189T283%20207T294%20227T299%20242Q302%20258%20302%20292T299%20343ZM403%20-75Q403%20-50%20389%20-34T348%20-11T299%20-2T245%200H218Q151%200%20138%20-6Q118%20-15%20107%20-34T95%20-74Q95%20-84%20101%20-97T122%20-127T170%20-155T250%20-167Q319%20-167%20361%20-139T403%20-75Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-29%22%20d%3D%22M60%20749L64%20750Q69%20750%2074%20750H86L114%20726Q208%20641%20251%20514T294%20250Q294%20182%20284%20119T261%2012T224%20-76T186%20-143T145%20-194T113%20-227T90%20-246Q87%20-249%2086%20-250H74Q66%20-250%2063%20-250T58%20-247T55%20-238Q56%20-237%2066%20-225Q221%20-64%20221%20250T66%20725Q56%20737%2055%20738Q55%20746%2060%20749Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-44%22%20d%3D%22M130%20622Q123%20629%20119%20631T103%20634T60%20637H27V683H228Q399%20682%20419%20682T461%20676Q504%20667%20546%20641T626%20573T685%20470T708%20336Q708%20210%20634%20116T442%203Q429%201%20228%200H27V46H60Q102%2047%20111%2049T130%2061V622ZM593%20338Q593%20439%20571%20501T493%20602Q439%20637%20355%20637H322H294Q238%20637%20234%20628Q231%20624%20231%20344Q231%2062%20232%2059Q233%2049%20248%2048T339%2046H350Q456%2046%20515%2095Q561%20133%20577%20191T593%20338Z%22%3E%3C%2Fpath%3E%0A%3Cpath%20stroke-width%3D%221%22%20id%3D%22E1-MJMAIN-3D%22%20d%3D%22M56%20347Q56%20360%2070%20367H707Q722%20359%20722%20347Q722%20336%20708%20328L390%20327H72Q56%20332%2056%20347ZM56%20153Q56%20168%2072%20173H708Q722%20163%20722%20153Q722%20140%20707%20133H70Q56%20140%2056%20153Z%22%3E%3C%2Fpath%3E%0A%3C%2Fdefs%3E%0A%3Cg%20stroke%3D%22currentColor%22%20fill%3D%22currentColor%22%20stroke-width%3D%220%22%20transform%3D%22matrix(1%200%200%20-1%200%200)%22%20aria-hidden%3D%22true%22%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-43%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-2E%22%20x%3D%22722%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-33%22%20x%3D%221251%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-3E%22%20x%3D%222029%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3Cg%20transform%3D%22translate(3085%2C0)%22%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-32%22%20x%3D%220%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-31%22%20x%3D%22707%22%20y%3D%22583%22%3E%3C%2Fuse%3E%0A%3C%2Fg%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-2C%22%20x%3D%224039%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMATHI-4F%22%20x%3D%224485%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-28%22%20x%3D%225248%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3Cg%20transform%3D%22translate(5638%2C0)%22%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMATHI-4E%22%20x%3D%220%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3Cg%20transform%3D%22translate(914%2C412)%22%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-6C%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-6F%22%20x%3D%22278%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-67%22%20x%3D%22779%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.574)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-32%22%20x%3D%221576%22%20y%3D%22-305%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-33%22%20x%3D%222021%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3C%2Fg%3E%0A%3C%2Fg%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-29%22%20x%3D%228435%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3Cg%20transform%3D%22translate(9825%2C0)%22%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-44%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-2E%22%20x%3D%22764%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3C%2Fg%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-33%22%20x%3D%2211118%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-3D%22%20x%3D%2211896%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3Cg%20transform%3D%22translate(12952%2C0)%22%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-33%22%20x%3D%220%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-31%22%20x%3D%22707%22%20y%3D%22583%22%3E%3C%2Fuse%3E%0A%3C%2Fg%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-2C%22%20x%3D%2213906%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMATHI-4F%22%20x%3D%2214352%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-28%22%20x%3D%2215115%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMATHI-4E%22%20x%3D%2215505%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3Cg%20transform%3D%22translate(16560%2C0)%22%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-6C%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-6F%22%20x%3D%22278%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-67%22%20x%3D%22779%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20transform%3D%22scale(0.707)%22%20xlink%3Ahref%3D%22%23E1-MJMAIN-32%22%20x%3D%221809%22%20y%3D%22598%22%3E%3C%2Fuse%3E%0A%3C%2Fg%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMATHI-4E%22%20x%3D%2218460%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%20%3Cuse%20xlink%3Ahref%3D%22%23E1-MJMAIN-29%22%20x%3D%2219348%22%20y%3D%220%22%3E%3C%2Fuse%3E%0A%3C%2Fg%3E%0A%3C%2Fsvg%3E#card=math&code=%5Ctext%7BC.%20%7D3%3E2%5E1%2C%20O%28N%5E%7B%5Clog_23%7D%29%20%5Cquad%5Ctext%7BD.%20%7D3%3D3%5E1%2C%20O%28N%5Clog%5E2N%29&id=FCOMB)
:::

:::warning
(C)	3-way-mergesort : Suppose instead of dividing in two halves at each step of the mergesort, we divide into three one thirds, sort each part, and finally combine all of them using a three-way-merge. What is the overall time complexity of this algorithm ? (5分)
_A.	O_(_n_(log2_n_))
B.	O(_n_2log_n_)
_C.	O_(_n_log_n_)
_D.	O_(_n_)
:::

:::warning
(A)	![image.png](./assets/1625678970245-e90fea95-4071-4a0b-81e4-6fa77f9755f9.png)
:::

:::warning
![image.png](./assets/1625679204144-39b5ee9b-e504-4a57-bbc4-2330e11763f5.png)\
:::

:::warning
![image.png](./assets/1625679243931-a427d374-60f7-4263-a2c1-43da0dbc92a7.png)
:::

:::warning
![image.png](./assets/1625702866501-b2293be6-5b55-4452-acce-a9a844ee9cc8.png)
:::

### 7 DP
Quiz 考到了上课的几个引例<br />HW 考到了简单的状态转移方程的构造 以及合理的循环顺序
:::warning
(T)	To solve a problem by dynamic programming instead of recursions, the key approach is to store the results of computations for the subproblems so that we only have to compute each different subproblem once. Those solutions can be stored in an array or a hash table.<br />(F)	The root of an optimal binary search tree always contains the key with the highest search probability.
:::

:::warning
(D)	Which one of the following problems can be best solved by dynamic programming?<br />A.	Closest pair of points problem<br />B.	Quicksort<br />C.	Mergesort<br />D.	Longest common subsequence problem
:::

:::danger
![image.png](./assets/1625678261798-dc9ded81-f674-4635-bc10-de07fe70af0b.png)
![image.png](./assets/1625679412543-ca841b0e-fb0d-40bf-bfcf-ff8a66c35ad1.png)
![image.png](./assets/1625679473075-7ee5b878-1e19-4ac3-a253-1450356f0d13.png)
:::

:::warning
![image.png](./assets/1625679436908-58318aea-07ab-4f71-a128-605c1f561b9e.png)
:::

:::success
![image.png](./assets/1625679457258-86fa2d2c-938c-4a6d-a6fa-fb8bb0af4b45.png)
:::

:::warning
![image.png](./assets/1625679493048-ba2f4f78-1bc5-4442-ab81-eed4d8721189.png)
:::
