
## 2 Introduction to the Relational Model

### 2.1 Structure of Relational Databases
**关系数据库的一些定义**。<br />一个 **relational database** 由一些 **tables** 组成，每一个 table 都有一个专有的 name。如下图所示是一个名为 course 的 table。<br />我们在 [集合论](https://www.yuque.com/xianyuxuan/coding/lfxqyr#VdEM2) 中学习过关系 (relation) 的概念。关系表示的是一组对象（数据）之间的某种联系。这里 table 实际上就是几组对象的一个关系。关系用 N 元组 (**n-tuple**) 的集合表示。Table 中的每一列是这个 table 所对应关系中的一组对象，它表示的是这个关系中的某一个属性。<br />因此，我们用 **relation** 表示一个 table，每一个 **tuple** 对应 table 中的一行，每个 **attribute** 对应 table 中的一列。一个 tuple 就是其所在 relation 中所有 attribute 合法取值集合的笛卡尔积的一个元素；relation 是 tuple 的集合。<br />我们称一个 relation 的实例（即 table 在某个时刻的快照）为 **relation instance**。
![image.png](./assets/1616590894480-72577b32-ad22-4a9f-9b5d-63d5bae5d007.png)

**Tuple 的无序性**。<br />由于 relation 是 tuple 的一个集合，因此 tuple 是无序的。

**Attribute 的一些概念**。<br />对于一个 relation 的每一个 attribute，都有一个合法取值的集合，称为这个 attribute 的 **domain**。<br />如果一个 domain 中的所有元素（即所有的合法取值）都被视为不可分割的单元，那么我们称这个 domain 是 atomic 的。这里“视为”的含义是：我们在 **使用** 这些值时不再对它们进行拆分，这与这些值本身无关。例如，宿舍地址“碧峰 1 舍 617”既可以作为一个不可分割的单元进行使用（例如收信地址），也可以被分割为若干单元（例如宿舍楼“碧峰 1 舍”，寝室号“617”）进行使用。那么如果我们如前面那样使用，那么这个 domain 是 atomic 的；如果如后面那样使用，则它是 nonatomic 的。<br />本文中，若无说明，我们默认所有 attribute 都具有 atomic domain。

**Null value**。<br />如果某个值未知或不存在，我们用 null value 来表示。


### 2.2 Database Schema
我们用 **relation schema** 来描述一个 relation。需要描述的内容包括这个 relation 包含哪些 attribute，以及每个 attribute 对应的 domain，还有这个 relation 的一些约束条件（integrity-constraint），例如 primary key 和 foreign key。<br />例如图 2.2 中的 relation 就可以用如下的 schema 进行描述：<br />_course(course_id, title, dept_name, credits)_


### 2.3 Keys
**Superkey 的引入和定义。** <br />由于 relation 是 tuple 的一个集合，我们必须采取方式保证其中的 tuple 彼此不同；即，不允许两个 tuple 的所有 attribute 的值完全相同。<br />当然，保证所有 tuple 是 unique 的，并不需要检查其所有 attribute 的值。实际上，在图 2.2 中的 _course_ 关系中，课程号就是彼此不同的；或者在寝室成员的例子中，寝室楼号 + 床号两个 attribute 的值就可以唯一确定一个成员。<br />因此，我们定义一个 relation 的 **superkey** 是 attribute 的一个集合，它包含一个或多个 attribute，通过这些 attribute 的值可以唯一确定一个 tuple；即不存在两个 tuple，它们的 superkey 中每个 attribute 的值都相同。显然，superkey 的任一超集（A 是 B 的 **超集 (superset)**，当且仅当 ![](https://cdn.nlark.com/yuque/__latex/2e9def3789de2cb04ae38db587920983.svg#card=math&code=A%5Csupseteq%20B&height=16&id=FjFOY)）仍然是这个 relation 的 superkey。<br />形式化地，对于一个 relation _r_ ，用 _R_ 表示它的所有 attribute 的集合，我们称 ![](https://cdn.nlark.com/yuque/__latex/8fd3fc3bea2f0034825ccc20691ae170.svg#card=math&code=K%5Csubseteq%20R&height=16&id=ANp1O) 是 _r_ 的一个 **superkey**，如果对于 _r_ 的任一 instance 中的任意两个 tuples ![](https://cdn.nlark.com/yuque/__latex/35b7262c3672f32862b5c1d0b3bd76dc.svg#card=math&code=t_1%5Cneq%20t_2&height=19&id=47DEM)，都有 ![](https://cdn.nlark.com/yuque/__latex/8d324c431eb4b4e1f56971f840dcab85.svg#card=math&code=t_1.K%5Cneq%20t2.K&height=19&id=NBgRK)。

**Candidate keys 和 Primary key。** <br />如我们所说，superkey 的任一超集都是 superkey，因此 superkey 中可能含有冗余或无关的项目。我们希望找到一个最简单的 attribute 组合。如果一个 superkey 的任意子集都不是 superkey，我们称之为 **candidate key** 。<br />一个 relation 可能含有多个 candidate key。例如浙江大学的学生名单，身份证号、学号、寝室楼号 + 床号都是这个 relation 的 candidate key。因此 database 的设计者可以从 candidate keys 中选取一个作为该 database 中 tuple 的识别方式，我们称这个 key 为 **primary key** 。<br />Primary key 的选择必须慎重。例如浙江大学的学生名单中，姓名显然不适合作为 primary key，因为可能有重名；寝室楼号 + 床号也不太适宜，因为它们很可能改变。我们倾向于选择那些不会或者很少会变化的 attribute 作为 primary key。

**Foreign key constraint。** <br />一个 relation _r1_ 的 attributes 可能包含另一个 relation _r2_ 的 primary key，那么我们称这个 attribute 为一个 **foreign key** (from _r1_ referencing _r2_)。 _r1_ 也被称为 foreign key 的 **referencing relation** ， _r2_ 称为 **referenced relation** 。这是一个从 _r1_ 到 _r2_ 的 **foreign key constraint**（外码约束）。<br />考虑这样一个例子。课程可能会在不同的学期中重复开放，或者在同一个学期中有多个教学班。下面的 _section_ relation 就描述了这样的一个关系：
![image.png](./assets/1616644414920-61e31ef7-21a0-4ffa-b901-09a6015ca12d.png)
可以看到，CS-101 课程在 2009 Fall 和 2010 Spring 学期重复开放，而 CS-190 在 2009 Spring 学期有 2 个教学班等。在这样的一个 relation 中，我们选取 _(course_id, sec_id, semester, year)_ 为它的 primary key。<br />我们同样需要描述每一个教师所负责的教学段。下面的 _teaches_ relation 描述了这种关系。我们选取其所有 attribute，即 _(ID, course_id, sec_id, semester, year)_ 为它的 primary key。
![image.png](./assets/1616644651464-0a93ca82-3bb7-4670-adcb-e981bac7f04d.png)
我们注意到， _teaches_ 的 attributes 包含了 _section_ 的 primary keys，因此这里有一个从 _teaches_ 到 _section_ 的 foreign key constraint。

**Referential integrity constraint。** <br />考察这两个 relation 的关系：显然，每一个教学段都需要至少 1 位教师进行教学；亦即，对于 _section_ 中的任意 tuple，其 _(course_id, sec_id, semester, year)_ 必须也等于 _teaches_ 中某个元组这些 attributes 的取值。这是**referential integrity constraint** （参照完整性约束）的一个实例。即，referencing relation 中的任意 tuple 在某些 attributes 上的取值必然等于 referenced relation 中某个 tuple 在对应 attributes 上的取值。<br />但是，由于 _section_ 并不包含 _teaches_ 的 primary keys，因此我们不能声明一个从 _section_ 到 _teaches_ 的 foreign key constraint。


### 2.4 Schema Diagrams
![image.png](./assets/1617344231460-87f3b6b5-32d5-435b-9a1e-b7280da6f057.png)
_instructor(ID, name, dept_name, salary)_<br />_teaches(ID, course_id, sec_id, semester, year)_

**本文中大多数例子都将基于这一 Schema diagram 显示的关系。**


## 3 Formal Relational Query Languages | Relational Algebra
**The Select Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/9b19892825f59b85da1bc4a24e33aad9.svg#card=math&code=%5Csigma_p%28r%29%3D%5C%7Bt%5C%20%7C%5C%20t%5Cin%20r%20%5Cland%20p%28t%29%5C%7D&height=21&id=iiJkS)，即选择出 _r_ 中所有满足命题 _p_ 的元素的集合。 _p_ 是由一系列 ![](https://cdn.nlark.com/yuque/__latex/5c2a3810370e1b59062a92c8c1bdf978.svg#card=math&code=%5Cland%2C%20%5Clor%2C%20%5Clnot&height=16&id=Xfm0X) 连接的命题组成的，每个命题满足形式 `<attribute> op <attribute>` 或者 `<attribute> op <constant>` 。其中 `op` 为 ![](https://cdn.nlark.com/yuque/__latex/d69390f2b310d6fbb96561d6e273c89a.svg#card=math&code=%3D%2C%20%5Cneq%2C%20%3E%2C%20%5Cgeq%2C%20%3C%2C%5Cleq&height=19&id=1WSVo) 之一。<br />例如：![](https://cdn.nlark.com/yuque/__latex/fb33d2e26e5e9e59fb29630dd5a6553d.svg#card=math&code=%5Csigma_%7B%5Ctext%7Bdept_name%3D%22Physics%22%20%7D%5Cland%5Ctext%7B%20salary%3E90000%7D%7D%28%5Ctext%7Binstructor%7D%29&height=21&id=PcAFT)表示 relation _instructor_ 中 _dept_name_ 为 "Physics" 且 _salary_ 大于 90000 的元素形成的子集。

**The Project (投影) Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/f1f6074fede50ea48aaa1b0c07544de4.svg#card=math&code=%5CPi_%7BA_1%2C%20A_2%2C%5C%20%5Cdots%7D%28r%29&height=21&id=2QGuu) 

**The Union Operation.**<br />![](https://cdn.nlark.com/yuque/__latex/f988ba61cd1f9a10c1697259c504f13a.svg#card=math&code=r%5Ccup%20s&height=14&id=zqcT9)

**The Set-Difference Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/8d3702859962d0a225954fa391e9e5a3.svg#card=math&code=r-s&height=16&id=De9dn)

**The Cartesian-Product (笛卡尔积) Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/bb44623b203a1cc8458f27aae1a60329.svg#card=math&code=r%5Ctimes%20s&height=12&id=ZJtm0)

**The Rename Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/21ff166d05fb11f882794f595d979b60.svg#card=math&code=%5Crho_x%28E%29&height=20&id=JqkC2)
![](https://cdn.nlark.com/yuque/__latex/e5db2141043bb88f72d9351c71bdce7f.svg#card=math&code=%5Crho_%7Bx%28A_1%2C%20A_2%2C%20%5C%20%5Cdots%2C%20A_n%29%7D%28E%29&height=23&id=wLM96)

**The Set-Intersection Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/ec013b90a6ac265d78908d07fb82814f.svg#card=math&code=r%5Ccap%20s%20%3D%20r-%28r-s%29&height=20&id=QXyZY)

**The Natural-Join Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/994d92c15adf76eb058ec0342c3456be.svg#card=math&code=r%5CJoin%20s&height=13&id=RIGj6) `\Join` 

**The Assignment Operation.** <br />![](https://cdn.nlark.com/yuque/__latex/f5873ee636f9195df989d86ac2540961.svg#card=math&code=r%5Cleftarrow%20E&height=16&id=cp6mN)

**Outer Join Operations.** <br />Left Outer Join     ⟕ <br />Right outer join     ⟖<br />Full outer join    ⟗

**The Division Operation.** 

**Generalized Projection.** 

**Aggregation.** <br />![](https://cdn.nlark.com/yuque/__latex/2e3e6c8fc31d963bc42216f4f2a58a52.svg#card=math&code=%5Cmathcal%7BG%7D&height=16&id=eXH02)
