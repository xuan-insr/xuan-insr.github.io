---


## 1 一些基本定义

:::danger
特别注意：此处的定义来源于课件与配套教材。但是，其中部分定义（尤其是关于路径的定义以及一些特别限制）与其他一些资料（尤指 [图论 | 信息安全原理与数学基础](https://www.yuque.com/xianyuxuan/coding/tiympp) 以及 [**OI Wiki**](https://oi-wiki.org/graph/concept)）并不相同；即使是课件和课本中也略有偏差。应以实际题目为基准。
:::

下面的内容，在 [图论 | 信息安全原理与数学基础](https://www.yuque.com/xianyuxuan/coding/tiympp) 介绍过且没有定义上的区别的从略。

- **Graph, 图.** ![](https://cdn.nlark.com/yuque/__latex/c311905eab60237306c75dfad5d0ca29.svg#card=math&code=G%20%3D%20%28V%2C%20E%29&height=20&width=82)。
- **Vertex, [pl.]vertices, 结点.** ![](https://cdn.nlark.com/yuque/__latex/435df676bac289f78f72a1c7afd4fd37.svg#card=math&code=V%28G%29&height=20&width=39)，点集。课程中限定为非空有限集。
- **Edge, 边.** ![](https://cdn.nlark.com/yuque/__latex/67d9dfc543365cc29937e78364f20fd1.svg#card=math&code=E%28G%29&height=20&width=39)，边集。课程中限定为非重集，即不考虑重边；允许为空集；不允许自环
- **Undirected graph, 无向图.** 边为无向边，表示为 ![](https://cdn.nlark.com/yuque/__latex/21625a4ea5cd41fb402fa07444749a9e.svg#card=math&code=%28v_i%2C%20v_j%29&height=21&width=49)。
- **Directed graph (digraph), 有向图.** 边为有向边，表示为 ![](https://cdn.nlark.com/yuque/__latex/184a9a648fc10ee5a83d9ec7d7a784ab.svg#card=math&code=%3Cv_i%2C%20v_j%3E&height=18&width=71)。
- **Complete graph, 完全图.** 
- **Incident, 关联的.** 如果结点 ![](https://cdn.nlark.com/yuque/__latex/9e3669d19b675bd57058fd4664205d2a.svg#card=math&code=v&height=12&width=8) 是边 ![](https://cdn.nlark.com/yuque/__latex/e1671797c52e15f763380b45e841ec32.svg#card=math&code=e&height=12&width=8) 的一个端点，则称 ![](https://cdn.nlark.com/yuque/__latex/e1671797c52e15f763380b45e841ec32.svg#card=math&code=e&height=12&width=8) _**is incident on**_ ![](https://cdn.nlark.com/yuque/__latex/9e3669d19b675bd57058fd4664205d2a.svg#card=math&code=v&height=12&width=8)。
- **Adjacent, 邻接的.** 如果有边 ![](https://cdn.nlark.com/yuque/__latex/21625a4ea5cd41fb402fa07444749a9e.svg#card=math&code=%28v_i%2C%20v_j%29&height=21&width=49)，则称_** ![](https://cdn.nlark.com/yuque/__latex/1df181eaa1bb40a0067c06ead197170d.svg#card=math&code=v_i&height=14&width=13) and ![](https://cdn.nlark.com/yuque/__latex/b047f24e2fa0d6c8825b03766e27b0b5.svg#card=math&code=v_j&height=16&width=14) are adjacent**_； 如果有边 ![](https://cdn.nlark.com/yuque/__latex/184a9a648fc10ee5a83d9ec7d7a784ab.svg#card=math&code=%3Cv_i%2C%20v_j%3E&height=18&width=71)，则称_** ![](https://cdn.nlark.com/yuque/__latex/1df181eaa1bb40a0067c06ead197170d.svg#card=math&code=v_i&height=14&width=13) is adjacent to ![](https://cdn.nlark.com/yuque/__latex/b047f24e2fa0d6c8825b03766e27b0b5.svg#card=math&code=v_j&height=16&width=14), ****![](https://cdn.nlark.com/yuque/__latex/b047f24e2fa0d6c8825b03766e27b0b5.svg#card=math&code=v_j&height=16&width=14)**** is adjacent from ****![](https://cdn.nlark.com/yuque/__latex/1df181eaa1bb40a0067c06ead197170d.svg#card=math&code=v_i&height=14&width=13)**_。
- **Subgraph, 子图.** 
- **Path, 路径.** 教材中这样给出定义：图中的一条路径是一个 **顶点序列** ![](https://cdn.nlark.com/yuque/__latex/66282689533819321519cfa53b4358de.svg#card=math&code=v_1%2C%20v_2%2C%20%5Ccdots%2C%20v_N&height=14&width=97)，使得 ![](https://cdn.nlark.com/yuque/__latex/d0d4ca72589797218ad6550c9cf0a705.svg#card=math&code=%28v_i%2C%20v_%7Bi%2B1%7D%29%5Cin%20E&height=20&width=97),![](https://cdn.nlark.com/yuque/__latex/0910613ed692e7c6c72eeb1cb3d1b3ef.svg#card=math&code=1%5Cleq%20i%3CN&height=16&width=74)（有向图中为![](https://cdn.nlark.com/yuque/__latex/1221bdd16b03be6a8ffa4548c3d63a60.svg#card=math&code=%3Cv_i%2C%20v_%7Bi%2B1%7D%3E%5Cin%20E&height=18&width=115)）。
- **Length of a path, 路径的长度.** 路径上的边数称为其长度。
- **Simple path, 简单路径.** ![](https://cdn.nlark.com/yuque/__latex/8f966f6d05125223685b2a6521b26ef2.svg#card=math&code=v_i%5Cneq%20v_j%2C%201%5Cleq%20i%2C%20j%3CN%2C%20i%5Cneq%20j&height=20&width=189)。特别地，允许 ![](https://cdn.nlark.com/yuque/__latex/e40609c93752c22dc3481fda7e3b8469.svg#card=math&code=v_1%20%3Dv_&height=14&width=58)。
- **Loop, 自环.** 教材中定义 loop 特指自环。
- **Cycle, 圈/环.** ![](https://cdn.nlark.com/yuque/__latex/e40609c93752c22dc3481fda7e3b8469.svg#card=math&code=v_1%20%3Dv_&height=14&width=58)的简单路径。
- **Acyclic, 无环的.** 
- **Connected, 连通的; Strongly connected, 强连通的; Weakly connected, 弱连通的.** 
- **Tree, 树.** 如我们之前所述，树实际上是 a graph that is connected and acyclic。
- **DAG, Directed Acyclic Graph, 有向无环图.** 
- **Degree(v), in-degree(v), out-degree(v).** 
- **Connected component, 连通分量.** 


## 2 图的表示

### 2.1 邻接矩阵 | adjacency matrix
使用一个二维数组。如果存在一条边 ![](https://cdn.nlark.com/yuque/__latex/a34da2252c3f99b900f24e4d686b625c.svg#card=math&code=%3Cu%2Cv%3E&height=16&width=61)，置 `adj[u][v] = 1` 或置为其边权。<br />这种表示方法是简易的，但其空间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/85aa8b6f190f74ecc49fd71ba290ad5c.svg#card=math&code=%5CTheta%28%7CV%7C%5E2%29&height=24&width=56)，因此更适合稠密（dense）图。这种表示方法适用于不考虑重边的情况。<br />稠密图，即其边数 ![](https://cdn.nlark.com/yuque/__latex/27e6754a694f8e39e76bb50281277bb9.svg#card=math&code=%7CE%7C%20%3D%20%5CTheta%28%7CV%7C%5E2%29&height=24&width=100)；对应的是稀疏（sparse）图，稀疏图中有 ![](https://cdn.nlark.com/yuque/__latex/06ef6c0dc74146ffe05e16dad922a448.svg#card=math&code=%7CE%7C%5Cll%7CV%7C%5E2&height=24&width=78)。


### 2.2 邻接表 | adjacency list
使用一个一位数组表示所有顶点；对每个顶点，用一个表存放所有邻接的顶点。<br />空间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/96b64add48b0c59f6b07b490983a4a3b.svg#card=math&code=O%28%7CE%7C%2B%7CV%7C%29&height=20&width=90)。更适合稀疏图。
![image.png](./assets/1606972967293-064516a3-cb09-4a6a-8517-af85907efc86.png)
图源 [https://www.cnblogs.com/dzkang2011/p/bfs_dfs.html](https://www.cnblogs.com/dzkang2011/p/bfs_dfs.html)


## 3 拓扑排序 | Topological Sort
拓扑排序的目标是在一个有向无环图（DAG）中将图中的顶点进行排序，使得对任何有向边 ![](https://cdn.nlark.com/yuque/__latex/a34da2252c3f99b900f24e4d686b625c.svg#card=math&code=%3Cu%2Cv%3E&height=16&width=61)，都有 ![](https://cdn.nlark.com/yuque/__latex/7b774effe4a349c6dd82ad4f4f21d34c.svg#card=math&code=u&height=12&width=9) 在 ![](https://cdn.nlark.com/yuque/__latex/9e3669d19b675bd57058fd4664205d2a.svg#card=math&code=v&height=12&width=8) 的前面。一个例子是排课的预修要求。<br />课本介绍的是 Kahn 算法。其大致思想是：维护一个入度为 0 的顶点的集合 ![](https://cdn.nlark.com/yuque/__latex/5dbc98dcc983a70728bd082d1a47546e.svg#card=math&code=S&height=16&width=10)。每次我们从 ![](https://cdn.nlark.com/yuque/__latex/5dbc98dcc983a70728bd082d1a47546e.svg#card=math&code=S&height=16&width=10) 中取出一个点 ![](https://cdn.nlark.com/yuque/__latex/7b774effe4a349c6dd82ad4f4f21d34c.svg#card=math&code=u&height=12&width=9) 放入列表 ![](https://cdn.nlark.com/yuque/__latex/d20caec3b48a1eef164cb4ca81ba2587.svg#card=math&code=L&height=16&width=11) 用以表示拓扑排序的结果，然后将所有从 ![](https://cdn.nlark.com/yuque/__latex/7b774effe4a349c6dd82ad4f4f21d34c.svg#card=math&code=u&height=12&width=9) 出发的边 ![](https://cdn.nlark.com/yuque/__latex/228cb1cb3d6eacc23e2abc54026d8dfe.svg#card=math&code=%3Cu%2Cv_i%3E&height=16&width=66) 删除。若删除后 ![](https://cdn.nlark.com/yuque/__latex/1df181eaa1bb40a0067c06ead197170d.svg#card=math&code=v_&height=14&width=13) 的入度变为 0，则将其置入 ![](https://cdn.nlark.com/yuque/__latex/5dbc98dcc983a70728bd082d1a47546e.svg#card=math&code=S%20&height=16&width=10) 中。这种做法的正确性是容易理解的，因为当一个结点位于 ![](https://cdn.nlark.com/yuque/__latex/5dbc98dcc983a70728bd082d1a47546e.svg#card=math&code=S&height=16&width=10) 中时，说明要么没有依赖，要么其依赖已经排序在 ![](https://cdn.nlark.com/yuque/__latex/d20caec3b48a1eef164cb4ca81ba2587.svg#card=math&code=L&height=16&width=11) 中了。不断重复这个过程直到 ![](https://cdn.nlark.com/yuque/__latex/5dbc98dcc983a70728bd082d1a47546e.svg#card=math&code=S&height=16&width=10) 为空。如果此时图中还剩下有边，则该图一定有环；否则 ![](https://cdn.nlark.com/yuque/__latex/d20caec3b48a1eef164cb4ca81ba2587.svg#card=math&code=L&height=16&width=11) 即为拓扑排序的结果。<br />集合 ![](https://cdn.nlark.com/yuque/__latex/5dbc98dcc983a70728bd082d1a47546e.svg#card=math&code=S&height=16&width=10) 可以用一个队列实现。<br />容易看到，Kahn 算法中，初始化会遍历一次每个结点；排序过程中对每条边将会操作且仅操作一次，因此总的时间复杂度是 ![](https://cdn.nlark.com/yuque/__latex/4fe9f15fb53c589e023213ae35fcf78f.svg#card=math&code=O%28%7CV%7C%2B%7CE%7C%29&height=20&width=90)。


## 4 最短路 | Shortest Path

### 4.1 迪杰斯特拉算法 | Dijkstra Algorithm
主要思想是，将结点分成两个集合：已确定和未确定最短路长度的。一开始第一个集合里只有起点。<br />然后重复这些操作：

   1. 对那些刚刚被加入第一个集合的结点的所有出边执行松弛操作。
   2. 从第二个集合中，选取一个最短路长度最小的结点，移到第一个集合中。

直到第二个集合为空，算法结束。

如果使用堆来保存最短路长度，则堆的大小为 ![](https://cdn.nlark.com/yuque/__latex/5206560a306a2e085a437fd258eb57ce.svg#card=math&code=V&height=16&width=12)，每次 `decrease_key` 的时间是 ![](https://cdn.nlark.com/yuque/__latex/69d6822b6f2cd456c5708dc6fc6447bb.svg#card=math&code=O%28%5Clog%20V%29&height=20&width=63) 的。总共需要进行 ![](https://cdn.nlark.com/yuque/__latex/3a3ea00cfc35332cedf6e5e9a32e94da.svg#card=math&code=E&height=16&width=12) 次松弛，因此时间复杂度是 ![](https://cdn.nlark.com/yuque/__latex/fa5658c21a16769ab29589ea2ec67faa.svg#card=math&code=O%28E%5Clog%20V%29&height=20&width=78)。如果使用 STL 中的 priority queue 保存，由于其只能入队和出队而不能修改，因此其时间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/44777d840ca162465b73f85b6a6d53b9.svg#card=math&code=O%28E%5Clog%20E%29&height=20&width=78)。


## 5 网络流 | Network Flow
看这个看懂了：[https://www.luogu.com.cn/blog/cicos/Dinic](https://www.luogu.com.cn/blog/cicos/Dinic)
手算网络流：[https://wenku.baidu.com/view/a256d82ef321dd36a32d7375a417866fb94ac052.html](https://wenku.baidu.com/view/a256d82ef321dd36a32d7375a417866fb94ac052.html)


## 6 最小生成树 | Minimum Spanning Tree (MST)
对图 ![](https://cdn.nlark.com/yuque/__latex/9e9992d6bf50b7580f971487c466a8cb.svg#card=math&code=G%3D%28V%2CE%29&height=20&width=82)，称 ![](https://cdn.nlark.com/yuque/__latex/f0eb917c92d6d562752ef473404574aa.svg#card=math&code=H%3D%28V%27%2CE%27%29&height=21&width=94) 为 ![](https://cdn.nlark.com/yuque/__latex/dfcf28d0734569a6a693bc8194de62bf.svg#card=math&code=G&height=16&width=12) 的 **生成子图 (spanning subgraph)** ，如果 ![](https://cdn.nlark.com/yuque/__latex/115498bf6fd3dfb59863f4ae1a406b7c.svg#card=math&code=V%3DV%27%2C%5C%20E%5Csubseteq%20E%27&height=20&width=119)。<br />在此基础上，如果 ![](https://cdn.nlark.com/yuque/__latex/dfcf28d0734569a6a693bc8194de62bf.svg#card=math&code=G&height=16&width=12) 是一个连通无向图，且 ![](https://cdn.nlark.com/yuque/__latex/c1d9f50f86825a1a2302ec2449c17196.svg#card=math&code=H%20&height=16&width=15) 是一棵树，那么称 ![](https://cdn.nlark.com/yuque/__latex/c1d9f50f86825a1a2302ec2449c17196.svg#card=math&code=H%20&height=16&width=15) 为 ![](https://cdn.nlark.com/yuque/__latex/dfcf28d0734569a6a693bc8194de62bf.svg#card=math&code=G&height=16&width=12) 的 **生成树 (spanning tree)。**<br />无向连通图的 **最小生成树 (Minimum Spanning Tree, MST)** 为边权和最小的生成树。<br />非连通图没有生成树，只有生成森林。
