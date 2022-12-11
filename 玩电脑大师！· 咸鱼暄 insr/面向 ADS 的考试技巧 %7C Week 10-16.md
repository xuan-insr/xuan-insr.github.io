期中考的太差了）需要好好学一学了

### 10 Greedy
一个最优化问题 (Optimization Problem) 包含若干约束条件 (constraints)，满足约束条件的解称为可行解 (feasible solutions)；在可行解中，使得最优化函数 (optimization function) 有最佳取值的解称为最优解 (optimal solution)。

贪心算法是在问题的每个阶段，选取在一定标准 (greedy criterion) 意义下最优的决定。这个决定不会在后面解决子问题时被修改，因此这个决定应能保证可行性。贪心算法不保证取得最优解，除非问题的部分最优等同于整体最优。

贪心算法实际上将问题分为两部分：做一次选择，然后解决子问题。因此证明贪心算法的思路就是：

- 首先证明 greedy choice 的正确性，即证明总存在一个 optimal solution，它当前做的选择与贪心选择相同。可以考虑的方法是将 optimal solution 转化为一个贪心选择，或者证明贪心选择此时不差于某一个最优解。
- 其次证明，子问题的一个最优解与当前贪心选择结合后的解是原问题的一个最优解。

一个贪心算法之下总有一个更麻烦的 DP 算法。


#### 10.0 题目
:::success

- Greedy algorithm works only if the local optimum is equal to the global optimum. (T)
- In a greedy algorithm, a decision made in one stage is not changed in a later stage. (T)
:::

:::danger

- To prove the correctness of a greedy algorithm, we must prove that an optimal solution to the original problem always makes the greedy choice, so that the greedy choice is always safe. (F) 
   - 解释：optimal solution 不一定要用 greedy choice 得到
:::
 

#### 10.1 Activity Selection Problem
其实就是这个题  [P1803 凌乱的yyy / 线段覆盖 - 洛谷](https://www.luogu.com.cn/problem/P1803)

一个正确的贪心思路是不断选取没有冲突而且最先结束的事件。这种选择方法的直观原理是：选择最先结束的时间，可以在选取活动次数 +1 的意义下剩下最多的时间。

另一种思路与此对称，即不断选取最后开始的事件。下面给出证明：

我们记 ![](https://g.yuque.com/gr/latex?T_%7Bi%2Cj%7D#card=math&code=T_%7Bi%2Cj%7D&id=V2orY) 为对给定活动集合 ![](https://g.yuque.com/gr/latex?S#card=math&code=S&id=qJQhQ)，在时间段 ![](https://g.yuque.com/gr/latex?%5Bi%2C%20j)#card=math&code=%5Bi%2C%20j%29&id=PH6Bq) 中可以取到的最大事件个数。那么全局问题就是 ![](https://g.yuque.com/gr/latex?T_%7B0%2C%20%5Cinf%7D#card=math&code=T_%7B0%2C%20%5Cinf%7D&id=yHsQB)。<br />显然，当 ![](https://g.yuque.com/gr/latex?j%20%5Cgeq%20j'#card=math&code=j%20%5Cgeq%20j%27&id=lvTSA) 时，![](https://g.yuque.com/gr/latex?T_%7Bi%2C%20j%7D%20%5Cgeq%20T_%7Bi%2C%20j'%7D#card=math&code=T_%7Bi%2C%20j%7D%20%5Cgeq%20T_%7Bi%2C%20j%27%7D&id=aaOk7)。

当我们进行过 0 至若干次选择之后，问题为求出 ![](https://g.yuque.com/gr/latex?T_%7B0%2C%20j%7D#card=math&code=T_%7B0%2C%20j%7D&id=apIBe)，此时问题集合为 ![](https://g.yuque.com/gr/latex?S_j%20%3D%20%5C%7Ba_i%7Ca_i%5Cin%20S%2C%20%20a_i.f%20%5Cleq%20j%5C%7D#card=math&code=S_j%20%3D%20%5C%7Ba_i%7Ca_i%5Cin%20S%2C%20%20a_i.f%20%5Cleq%20j%5C%7D&id=R8Swy)。<br />记一个最优解的活动集合为 ![](https://g.yuque.com/gr/latex?I#card=math&code=I&id=x2gZY)，其中开始时间最晚的活动为 ![](https://g.yuque.com/gr/latex?a_n#card=math&code=a_n&id=b4lmr)，开始时间为 ![](https://g.yuque.com/gr/latex?s_n#card=math&code=s_n&id=om22M)。记 ![](https://g.yuque.com/gr/latex?S_j#card=math&code=S_j&id=oq9HO) 中开始最晚的活动为 ![](https://g.yuque.com/gr/latex?a_m#card=math&code=a_m&id=Hld25)，开始时间为 ![](https://g.yuque.com/gr/latex?s_m#card=math&code=s_m&id=qcqeH)，则有 ![](https://g.yuque.com/gr/latex?s_n%5Cleq%20s_m#card=math&code=s_n%5Cleq%20s_m&id=S95Rk)。

那么，如果 ![](https://g.yuque.com/gr/latex?a_n%20%5Cneq%20a_m#card=math&code=a_n%20%5Cneq%20a_m&id=cZRJ4)，![](https://g.yuque.com/gr/latex?I'%20%3D%20I%20-%20%7Ba_n%7D%20%2B%20%7Ba_m%7D#card=math&code=I%27%20%3D%20I%20-%20%7Ba_n%7D%20%2B%20%7Ba_m%7D&id=S2DGs) 一定也是一个最优解。推理过程如下：<br />由于 ![](https://g.yuque.com/gr/latex?a_m.f%3Es_m%5Cgeq%20s_n#card=math&code=a_m.f%3Es_m%5Cgeq%20s_n&id=tRksh)，因此 ![](https://g.yuque.com/gr/latex?a_m%20%5Cnotin%20I-a_n%5Csubseteq%20I%20%3D%20S_%7Bs_n%7D#card=math&code=a_m%20%5Cnotin%20I-a_n%5Csubseteq%20I%20%3D%20S_%7Bs_n%7D&id=UuqML)
因此，![](https://g.yuque.com/gr/latex?T_%7B0%2C%20j%7D%3D%7CI%7C%20%3D%20T_%7B0%2C%20s_n%7D%20%2B%201%20%5Cleq%20T_%7B0%2C%20s_m%7D%20%2B%201%3D%7CI'%7C#card=math&code=T_%7B0%2C%20j%7D%3D%7CI%7C%20%3D%20T_%7B0%2C%20s_n%7D%20%2B%201%20%5Cleq%20T_%7B0%2C%20s_m%7D%20%2B%201%3D%7CI%27%7C&id=TIDZi)，即 ![](https://g.yuque.com/gr/latex?%7CI'%7C%20%5Cgeq%20T_%7B0%2C%20j%7D#card=math&code=%7CI%27%7C%20%5Cgeq%20T_%7B0%2C%20j%7D&id=QtvhX)。

结合 ![](https://g.yuque.com/gr/latex?a_n%20%3D%20a_m#card=math&code=a_n%20%3D%20a_m&id=Vt9LY) 的情况，我们使用贪心法的选择一定在某个最优解中。同时，由于我们考虑的情况是进行过 0 至若干次选择之后的情况，即原问题和子问题同时成立上述结论，因此该贪心算法是正确的。


#### 10.1 题目
:::success

- Let S be the set of activities in Activity Selection Problem. Then the earliest finish activity _am _must be included in all the maximum-size subset of mutually compatible activities of S. (F)
- Let S be the set of activities in Activity Selection Problem. Then there must be some maximum-size subset of mutually compatible activities of S that includes the earliest finish activity. (T)
:::

:::danger
![image.png](./assets/1621430027165-81ea27c0-5657-45ab-850b-6d363da92a95.png)
(F)。正解是：<br />![](https://g.yuque.com/gr/latex?c_%7Bj%7D%3D%5Cleft%20%5C%7B%0A%09%5Cbegin%7Balign%7D%0A%09%09%26w_1%20%26j%3D1%09%5C%5C%0A%09%09%26%5Cmax%5C%7Bc_%7Bj-1%7D%2C%20c_%7Bk(j)%7D%2Bw_j%5C%7D%20%26j%3E1%0A%09%5Cend%7Balign%7D%0A%5Cright%20.%0A#card=math&code=c_%7Bj%7D%3D%5Cleft%20%5C%7B%0A%09%5Cbegin%7Balign%7D%0A%09%09%26w_1%20%26j%3D1%09%5C%5C%0A%09%09%26%5Cmax%5C%7Bc_%7Bj-1%7D%2C%20c_%7Bk%28j%29%7D%2Bw_j%5C%7D%20%26j%3E1%0A%09%5Cend%7Balign%7D%0A%5Cright%20.%0A&id=Dl11Y)
因为 ![](https://g.yuque.com/gr/latex?c_j#card=math&code=c_j&id=sFi86) 是单调不减的，因此最近的一定是最好的。只需要考虑取 ![](https://g.yuque.com/gr/latex?w_j#card=math&code=w_j&id=uTvCf) 和不取两种情况即可。这里将第一个下标去掉只是为了简化，本身并没有错误。
:::

:::success
 ![image.png](./assets/1621430094101-b06755e9-293d-4905-8fd5-fddab17465f7.png)
根据算法取一下就行。
:::

:::warning
![image.png](./assets/1621430150938-6c4e717a-aff7-4ea3-9d27-edbcc781ca9e.png)
yds 出的题。答案是 C。这种题目前还不知道怎么做）
:::


#### 10.2 Huffman Codes
每一个字符初始形成一个单节点树，定义树的频率为其中所有字符（叶子结点）频率之和。用一个堆维护所有树的频率，每次取出最小的两棵树作为一个根节点的左右子树合成一棵新树，并将其加入堆中，直到堆中只有一棵树，这棵树就是 Huffman 编码树。这样的树有两个特点：所有字符都在叶子结点，保证任何一个字符的编码不为另一个字符的前缀；不存在只有 1 个儿子的结点。


#### 10.2 题目
:::warning
![image.png](./assets/1621432129009-405c67cd-7edd-4477-b105-05aa8a8d2e98.png)
答案是 (3) 和 (4)。需要特别注意 (4) 的情况：
![image.png](./assets/1621432724134-032cf57b-c832-476e-9f65-76b344272408.png)
我们分析算法就可以知道，如果在某种情况下最小值不唯一的话，它们的选取顺序不会影响最终的编码总长度。
:::

:::warning
![image.png](./assets/1621432746530-91a44f18-8a50-43ff-8853-510c0182290a.png)
答案是 A。能选出来但是不知道什么通用解法qwq
:::


### 11 NP Problems 还没完全学
太难了qwq 暂时不想管，等到看考试题的时候再说吧qwq

#### 11 题目
:::warning

- (F)	All decidable problems are NP problems.
- (T)	All NP problems are decidable.
- (T)	All NP-complete problems are NP problems.
- (T)	All NP problems can be solved in polynomial time in a non-deterministic machine.
- (F)	If a problem can be solved by dynamic programming, it must be solved in polynomial time.	（反例：0-1 背包，见 12 节）
- (T)	If P = NP then the Shortest-Path (finding the shortest path between a pair of given vertices in a given graph) problem is NP-complete. （把握下面这个图）

![image.png](./assets/1621923458339-0eec28c2-5cbc-41b8-bca6-5c22327db79a.png)

- (F)	Given that problem A is NP-complete. If problem B is in NP and can be polynomially reduced to problem A, then problem B is NP-complete.
- 上面两个问题就是 NPC 的证明思路：证明一个 NPC 可以规约到这个 NP 问题，则为 NPC
- (F)	To prove problem B is NP-complete, we can use a NP-complete problem A and use a polynomial-time reduction algorithm to transform an instance of problem B to an instance of problem A. 
:::

:::warning
(C)	Among the following problems, __ is NOT an NP-complete problem.<br />A. Vertex cover problem<br />B. Hamiltonian cycle problem<br />C. Halting problem<br />D. Satisfiability problem
:::

:::warning
(B)	Suppose Q is a problem in NP, but not necessarily NP-complete. Which of the following is FALSE?<br />A. A polynomial-time algorithm for SAT would sufficiently imply a polynomial-time algorithm for Q.<br />B. A polynomial-time algorithm for Q would sufficiently imply a polynomial-time algorithm for SAT.<br />C. If Q ∉ _P_, then _P _≠ _NP_.<br />D. If Q is NP-hard, then Q is NP-complete.
:::

:::warning
(T)	A language L belongs to NP iff there exist a two-input polynomial-time algorithm A that verifies language L in polynomial time.<br />(F)	All languages can be decided by a non-deterministic machine.<br />(T)	All NP problems can be solved in polynomial time in a non-deterministic machine.
:::

:::danger
(T)	If _L_1 ≤_p L_2 and _L_2∈_NP_, then _L_1∈_NP_.

- _L_1 ≤_p L_2_ _可以理解为 _ L_1 可以在多项式时间内规约到_ L_2
:::


#### 11 讨论题
> **The longest Hamiltonian cycle**
> The longest Hamiltonian cycle problem is to find a simple cycle of maximum length in a graph. To prove that it is NPC, we must first prove that it is in NP -- that is, to prove that an answer can be verified to be correct in polynomial time.
> To verify that a cycle is Hamiltonian is easy. But how would you know if a cycle really is the longest?

:::warning
关于该问题的讨论，参见 [最长哈密顿回路问题的难度讨论](https://www.yuque.com/xianyuxuan/notes/yyq314?view=doc_embed)。
:::



### 12 Approximation
设计解决一个问题的算法通常考虑三个方面：Optimality - 解的质量；Efficiency - 计算花费；All instances - 算法的通用性。考虑 Optimality + Efficincy 即为对一些特殊情况的高效率解；考虑 Optimality + All instances 即为不考虑效率的通解；而考虑 Efficiency + All instances 即为 approximation 考虑的问题：在多项式时间内找到一个 near-optimal 的解。
![image.png](./assets/1621509838302-ed73670d-50c3-482a-a431-de65e2d54703.png)
fully的意思是关于(1/epsilon)和n都是多项式级的



#### 12.0 题目
:::success
(T)	![image.png](./assets/1621510539339-3e676949-701a-49bc-897a-86fa0e17185f.png)
(F)	![image.png](./assets/1621510568276-71da2bf4-025d-4f81-8e75-84bfcccdc079.png)

(F)
![image.png](./assets/1625634242514-659a97ad-8053-4179-a489-cccb2ed3cf67.png)
tight：确切有这个近似度的实例；不证明不能优化，也可 P=NP 没关系

(F)
![image.png](./assets/1625634253484-3b1bc56d-e7c8-4d7d-8027-eec194700535.png)
reduce 和近似比没有必然联系
:::

:::danger
(C)	To approximate a maximum spanning tree _T _of an undirected graph _G_=(_V_, _E_) with distinct edge weights _w_(_u_, _v_) on each edge (_u_,_v_)∈_E_, let's denote the set of maximum-weight edges incident on each vertex by _S_. Also let _w_(_E_′)=∑(_u_,_v_)∈_E_′_w_(_u_,_v_) for any edge set _E_′. Which of the following statements is TRUE?<br />A. _S_=_T _for any graph _G_<br />B. _S_≠_T _for any graph _G_<br />C. _w_(_T_)≥_w_(_S_)/2 for any graph _G_<br />D. None of the above
:::

:::danger
![image.png](./assets/1625638016969-72cc0b06-88dd-4390-9bdd-d7bf794b2844.png)
**（以下解析存疑）**<br />题目是寻找旅行商问题的一个 2-approximation 算法<br />最小生成树的总边权一定严格小于旅行商问题的结果，否则旅行商问题的结果删一条边就可以得到一个更小的生成树。<br />pre-order 和 post-order 可以保证每条边最多走两次<br />level-order 会走好多次，所以不能保证是 2-approximation。
:::


#### 12.1 Approximate Bin Packing
其实 OS 里讨论过这个问题：[https://www.yuque.com/xianyuxuan/coding/nghlgc#mfMge](https://www.yuque.com/xianyuxuan/coding/nghlgc#mfMge)
![image.png](./assets/1621509926135-768983d3-59e6-40b3-800a-5cfd253683cc.png)
Optimal: M<br />Next Fit - 如果前一个 bin 能放下就放，放不下新开一个 - Worst: 2M - 1<br />Best Fit - 放进去以后剩余空间最少的 bin - Worst < 1.7M - 1.7<br />First Fit - 第一个能放下的 bin - Worst < 1.7M<br />在线算法最少 5M/3<br />离线算法：降序排序后 first/best fit (decreasing first/best fit) : 11M/9 + 2/3


#### 12.1 题目
:::danger

- (F)	In the bin packing problem, we are asked to pack a list of items L to the minimum number of bins of capacity 1. For the instance L, let FF(L) denote the number of bins used by the algorithm First Fit. The instance L' is derived from L by deleting one item from L. Then FF(L') is at most of FF(L).

反例： <br />Binsize=1<br />L={0.55, 0.7,0.55, 0.1, 0.45, 0.15, 0.3, 0.2}   <br />L'= L- {0.1} = {0.55, 0.7,0.55, 0.45, 0.15, 0.3, 0.2}  
:::

:::warning
(C)	For the bin-packing problem: let _S_=∑_Si_. Which of the following statements is FALSE?<br />A. The number of bins used by the next-fit heuristic is never more than ⌈2_S_⌉<br />B. The number of bins used by the first-fit heuristic is never more than ⌈2_S_⌉<br />C. The next-fit heuristic leaves at most one bin less than half full<br />D. The first-fit heuristic leaves at most one bin less than half full

分析：<br />Optimal Solution M = ⌈_S_⌉<br />A: next-fit M' < 2M - 1 = 2⌈_S_⌉ - 1 <= ⌈2_S_⌉<br />B: first-fit M' < 1.7M - 1.7 = 1.7⌈_S_⌉ - 1.7 <= ⌈2_S_⌉<br />C: 考虑序列 0.2 0.9 0.2 0.9，会留下 2 bins less than half full<br />D: 假如有两个 less than half full，那么后面那个 bin 中的所有 items 可以放入前面那个中，所以最多只有一个。
:::

:::warning
![image.png](./assets/1622529637934-30fa039a-a3c2-4b74-ac97-e39542d8bb7b.png)
分析：<br />考虑 B 选项。直观的思路来源于前面那道题，即 Next Fit 的结果不会有两个连续的 bin 不超过半满。因此最差的情况是，Next Fit 的结果为 ![](https://g.yuque.com/gr/latex?2N#card=math&code=2N&id=xSgHe) 个 bin，其中第 ![](https://g.yuque.com/gr/latex?2k%2B1#card=math&code=2k%2B1&id=VCzHA) 个的容量为 ![](https://g.yuque.com/gr/latex?x#card=math&code=x&id=jHaaN)，而第 ![](https://g.yuque.com/gr/latex?2k%2B2#card=math&code=2k%2B2&id=WeTQB) 个的容量为 ![](https://g.yuque.com/gr/latex?1-x%2B%5Cepsilon#card=math&code=1-x%2B%5Cepsilon&id=oYDgZ)。这样，item 的总大小为 ![](https://g.yuque.com/gr/latex?N%2BN%5Cepsilon#card=math&code=N%2BN%5Cepsilon&id=AA6xP)。当 ![](https://g.yuque.com/gr/latex?%5Cepsilon#card=math&code=%5Cepsilon&id=IDcLX) 足够小的时候，最优解至少为 ![](https://g.yuque.com/gr/latex?N%2B1#card=math&code=N%2B1&id=XiGIe)，即有 ![](https://g.yuque.com/gr/latex?NF(L)%5Cleq%202(OPT(L)-1)%2B1%20%3D%202OPT(L)-1#card=math&code=NF%28L%29%5Cleq%202%28OPT%28L%29-1%29%2B1%20%3D%202OPT%28L%29-1&id=B2XZf)。

考虑 A 选项。有关系 ![](https://g.yuque.com/gr/latex?OPT(L)%20%5Cgeq%20S%20%5Cgeq%20(1-%5Calpha)(NF(L)-1)%20%2B%20%5Cepsilon#card=math&code=OPT%28L%29%20%5Cgeq%20S%20%5Cgeq%20%281-%5Calpha%29%28NF%28L%29-1%29%20%2B%20%5Cepsilon&id=yGz1J)。其中 ![](https://g.yuque.com/gr/latex?S#card=math&code=S&id=hJHrx) 为所有 item 的总大小；前面的不等号是因为，每一个 bin 最多可以装容量为 ![](https://g.yuque.com/gr/latex?1#card=math&code=1&id=OOHri) 的 item；后面的不等号是因为，除了最后一个 bin 以外，前面的每个 bin 至少可以装容量为 ![](https://g.yuque.com/gr/latex?1-%5Calpha#card=math&code=1-%5Calpha&id=nkKAB) 的 item，否则下一个 item 总能够装进这个 bin 中；最后一个 bin 的内容大小没有限制。即有 ![](https://g.yuque.com/gr/latex?OPT(L)%3E(1-%5Calpha)(NF(L)-1)#card=math&code=OPT%28L%29%3E%281-%5Calpha%29%28NF%28L%29-1%29&id=rj6kA)，因此 ![](https://g.yuque.com/gr/latex?NF(L)%3C%20%5Cfrac%201%7B1-%5Calpha%7DOPT(L)%20%2B%201#card=math&code=NF%28L%29%3C%20%5Cfrac%201%7B1-%5Calpha%7DOPT%28L%29%20%2B%201&id=k0aMb)。

C 选项略；D 选项可以通过 A 和 B 推出错误。
:::


#### 12.2 The Knapsack Problem

- 部分背包：贪心
- 0-1 背包
   - greedy - max{_maximum_profit_density_, _maximum_profit_} - approximation ratio = 2
      - 证明：
         - 一定有 ![](https://cdn.nlark.com/yuque/__latex/366fd08408bc63ac2576d2dfc6475aa2.svg#card=math&code=p_%7Bmax%7D%5Cleq%20P_%7Bopt%7D%5Cleq%20P_%7Bfrac%7D&id=DBNrL)，因为 0-1 背包的最优解一定不大于部分背包的最优解。![](https://cdn.nlark.com/yuque/__latex/c228bef9d37fb5e2484a43cf249b5504.svg#card=math&code=p_%7Bmax%7D&id=xpUOo)是能放入背包的项目中最大的 profit，这一关系是显然的。
         - 一定有 ![](https://cdn.nlark.com/yuque/__latex/57fb3f875fe00c9b4f28c5970f13c958.svg#card=math&code=p_%7Bmax%7D%5Cleq%20P_%7Bgreedy%7D&id=ALLKp)，因为 ![](https://cdn.nlark.com/yuque/__latex/212216a559102b2ad3b8272f0f84af7f.svg#card=math&code=p_%7Bmax%7D%5Cleq%20P_%7Bmax%5C_profit%7D%20%5Cleq%20P_%7Bgreedy%7D&id=Y7z2q)
         - 一定有 ![](https://cdn.nlark.com/yuque/__latex/25893ff9b3c2e69dd17a062f6bbe6156.svg#card=math&code=P_%7Bopt%7D%20%5Cleq%20P_%7Bfrac%7D%20%5Cleq%20P_%7Bgreedy%7D%20%2B%20p_%7Bmax%7D&id=LkDtu)，因为如果我们按 profit density 去 greedy，那么 greedy 的结果和部分背包的结果的差别一定只是密度第 _i_ 大的某个项目没有放进来，而这个项目的 profit 不会大于 ![](https://cdn.nlark.com/yuque/__latex/c228bef9d37fb5e2484a43cf249b5504.svg#card=math&code=p_%7Bmax%7D&id=iZiEn)。
         - 因此，![](https://cdn.nlark.com/yuque/__latex/6131de924dc466a2eea9bb168092fedf.svg#card=math&code=%5Cfrac%20%7BP_%7Bopt%7D%7D%7BP_%7Bgreedy%7D%7D%20%5Cleq%20%5Cfrac%20%7BP_%7Bgreedy%7D%2Bp_%7Bmax%7D%7D%7BP_%7Bgreedy%7D%7D%20%3D%201%2B%5Cfrac%20%7Bp_%7Bmax%7D%7D%7BP_%7Bgreedy%7D%7D%5Cleq%201%2B%5Cfrac%20%7BP_%7Bgreedy%7D%7D%7BP_%7Bgreedy%7D%7D%20%3D%202&id=hnPKc)
   - DP - ![](https://cdn.nlark.com/yuque/__latex/cf442197af9e7196e8294361a16297b6.svg#card=math&code=O%28n%5E2p_%7Bmax%7D%29&id=RuvYU)，这不是多项式级的。


#### 12.2 题目
:::warning

- (F)	For the 0-1 version of the Knapsack problem, if we are greedy on taking the maximum profit or profit density, then the resulting profit must be bounded below by the optimal solution minus the maximum profit.
:::


#### 12.3 The K-Center Problem
![image.png](./assets/1621569406503-68accaba-3385-4a77-b7d9-d8722665aba4.png)
![image.png](./assets/1621569443984-03446d23-238a-417e-8aac-a71101c38099.png)
Greedy:
![image.png](./assets/1621569659794-75ee1285-9724-4d6e-8b3e-4cc201dbd40b.png)
找到一个上界：最优解的两倍。这样可以保证，取原来一个圆中任意一个点作为圆心，以原来的圆半径的两倍做为半径，则原来圆中的点都在新的圆中。
![image.png](./assets/1621569830888-cf8e8f03-0fac-4a2d-9ef8-1e70265dad0f.png)
如此选择，使用二分答案
![image.png](./assets/1621569848226-51ff8e70-8769-407c-bf22-198c1b6dd5f0.png)
这样找到的 r，一定不大于 2r*，但是不排除 r=r* 的可能（例如构成等腰三角形的三个点），所以不可以通过除以 2 的方法得到 r*，r 就是 r* 的一个 2-approximation。

另一种思路
![image.png](./assets/1621569869973-c3328326-db55-4ca4-b878-5e712b4d4b6d.png)
讨论
![image.png](./assets/1621569879450-4b9c8521-380f-4a69-a329-744e0afbdd68.png)

#### 12.3 题目
:::warning

- (T)	The K-center problem can be solved optimally in polynomial time if K is a given constant. 

分析：一个圆可以由 2 个点（直径）或者 3 个点（三角形）确定，不妨认为是 3。<br />那么，我们总共可以找到 ![](https://cdn.nlark.com/yuque/__latex/27da85450fb9232e497264044204f465.svg#card=math&code=C_n%5E3%20%5Csimeq%20n%5E3&id=t3pUr) 种 3 个点的组合方式，计算其构成的圆的半径。<br />最优解即为在上述组合方式中每次选出 K 个，判定是否覆盖所有点，记录满足条件的最小结果（半径），因此组合方式是 ![](https://cdn.nlark.com/yuque/__latex/cf89e67ab175ccccccca7745a28dace5.svg#card=math&code=C_%7BC_n%5E3%7D%5E%7B%5Ctext%7B%20%7DK%7D%20%5Csimeq%20C_%7Bn%5E3%7D%5E%7BK%7D%20%5Csimeq%20n%5E%7B3K%7D&id=H71yn) 个。<br />如果认为 K 是常数，则这是一个多项式级别的算法。但是 K 最多可达 n 的大小，因此在最大情况下为 ![](https://cdn.nlark.com/yuque/__latex/41f58950614ed7064a76a6818a69528a.svg#card=math&code=n%5E%7B3n%7D&id=kL9OM)，这不是多项式级别的。
:::


### 13 Local Search 算了


### 14 Randomized Algorithms 也算了


### 15 Parallel Algorithms


### 16 External Sorting
[

](https://cn.bing.com/search?q=%E8%BF%91%E4%BC%BC%E7%AE%97%E6%B3%95%E7%9A%84%E4%B8%8D%E5%8F%AF%E8%BF%91%E4%BC%BC%E6%80%A7&FORM=ANCMS9&PC=U531)
**第十二次：局部搜索**<br />通过学习局部搜索算法及其在博弈问题中的应用，加深理解potential method。主要的例子有：Max-cut, Multicast routing。<br />**第十三次：随机算法**<br />介绍两类随机算法的基本要素和分析方法。分别通过Online Hiring和随机快速排序算法帮助学生理解随机算法的分析原理。<br />**第十四次：外部排序**<br />介绍外部排序的基本框架，从简单解决方案开始，讨论多个环节的多种优化问题。<br />**第十五次：并行算法**<br />介绍并行计算的基本概念和模型，讲解Prefix, Merging, Maximum的并行算法。



