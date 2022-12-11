
## 5 E-R Model
一个 database 可以由两个部分描述：一系列 **entities** 以及这些 entities 之间的 **relationship**。因此，我们称这种描述方式为 E-R Model。我们下面对这两部分进行更详细的学习。


### 5.1 Entity & Relationship
**Entity**（实体）的概念类似于面向对象思想中的 object，例如每一个具体的人、东西、事件等都可以是一个 entity。Entity 有它们自己的 **attributes**。<br />**Entity Set** 的概念则类似面向对象思想中的 class，即一系列同类 entity 的集合，它们有共同的 attributes。<br />例如，下面的这两个 table 展示的就是 2 个 entity sets，其中的每一行都是一个 entity，每一列都是一个 attribute。
![image.png](./assets/1620117313659-777b32a4-42dd-4cdb-959e-f51da4c4063e.png)

**Relationship** 是若干 entities 之间的某种联系。例如，下图中的每一条连线即展示的是某一个 _instructor_ 和某一个 _student_ 之间的指导关系，这些连线的集合即构成了一个 **relationship set **_advisor_：
![image.png](./assets/1620117518355-4a3ff369-2977-44a0-9bd3-644e98863b48.png)
形式化地，若干个 entity set ![](https://cdn.nlark.com/yuque/__latex/a4947032a21ca344853dfdcc7c857aa6.svg#card=math&code=E_1%2C%20E_2%2C%20%5Cdots%2C%20E_n&id=qy4EW) 上的一个 **relationship set** 可以表示为 ![](https://cdn.nlark.com/yuque/__latex/4a4223e91633c6f728d57417549e54d5.svg#card=math&code=%5C%7B%28e_1%2C%20e_2%2C%20%5Cdots%2C%20e_n%29%5C%20%7C%5C%20e_i%5Cin%20E_i%2C%20i%3D1%2C%202%2C%5Cdots%2Cn%5C%7D&id=Jj2I8)，它的每一个元素即为一个 **relationship**。这个 relationship set 是  的一个子集（实际上这就是 n 元关系的定义：[关系 | 集合论](https://www.yuque.com/xianyuxuan/coding/lfxqyr#VdEM2)）。这里的 _n_ 即为一个 relationship set 的 **degree**。当 _n=2_ 时，我们称其中的 relationship 是 **binary relationship**。我们讨论的大多数都是 binary relationship。

Relationship 同样可以包含一些 attribute。例如，上面的 _advisor_ 关系中可能需要包含成为 advisor 的日期，如下图所示：
![image.png](./assets/1620118190910-a5bab884-f11d-4e6d-a5b8-b71016f7e205.png)
这理应是 _advisor_ 的一个 attribute，而不是 _instructor_ 或者 _student_ 的。

**Attribute** 也会包含一些特点。例如：

- 有一些 attribute 可能是 **composite** 的而不是 **simple** 的，即一个 attribute 由多个下级 attribute 组成；这一关系也可能构成嵌套，例如下图中用红框标出的就是 composite attributes：

![image.png](./assets/1620118515379-1b51ec93-a069-48f3-9632-c1c2af1a09d0.png)

- 有一些 attribute 可能是一个可变长度的集合，即为 **multivalued** 而非 **single-valued**。例如一个 _student_ 可能有多个 _phone_number_，因此这就可以设计为一个 multivalued attribute。
- 有一些 attribute 可能可以由其他 attribute 计算出来，我们称之为 **derived attributes**。例如 _age_ 可以根据 _date_of_birth_ 计算出来（而且这种计算是合理的，因为 _age_ 会根据当前时间进行变化）。


### 5.2 Constraints
我们也可以声明一些数据库中数据需要满足的 constraints。<br />**Mapping Cardinality Constraints**，用于 binary relationship：
![image.png](./assets/1620128035603-395ab6b4-40e7-41b8-9062-cb9762df6edb.png)
![image.png](./assets/1620128066861-960afc12-502f-46fc-a6ae-592ccac0a738.png)
**Participation Constraints**，如果 entity set _E_ 中的任一 entity 都至少参与到 relationship set _R_ 的一个 relationship 中，则称 _E_ 在 _R_ 中是 **total participation**，否则称为 **partial participation**。

**Keys**，与我们在 [2.3 Keys | Relational Database](https://www.yuque.com/xianyuxuan/coding/dbs_1#MdWvf) 中学习到的一致。对于一个 relationship set，其涉及的所有 entity set 的 primary keys 组合后会成为该 relationship set 的一个 superkey。


### 5.3 Redundant Attributes
去除冗余属性。这里给出了一个例子。
![image.png](./assets/1620129055989-84017d42-a19d-41b1-adde-ce7cdf94d121.png)


### 5.4 E-R Diagram
如下图所示，在 E-R Diagram 中，我们用矩形表示 entity sets，其中包含了其名称以及 attributes。Primary keys 由下划线标明。我们用菱形表示 relational sets，用直线将其与相关的 entity sets 连接。当 relational sets 也包含了一些 attributes 的时候，我们在方框中列举并用虚线与菱形连接起来。
![image.png](./assets/1620131890575-d85862b4-19ee-4c3d-bccc-243db8d76f12.png)

下图展示的是更加复杂的 entity sets 的形制，其中方框框出了若干 composite attributes，① 处所示的用 `{}` 标明的属性 `phone_number` 是 multivalued attribute，② 出尾部带有 `()` 的属性 `age` 是 derived attribute。
![image.png](./assets/1620131737497-ebeeba38-e800-41f5-ae7d-2ef2b4d129bb.png)

我们需要考虑到的是，我们使用 E-R Model 进行设计后，为了形成 table，我们会将 relationship set 相关的 entity sets 的 primary keys 作为 relationship set 的 attributes 来实现这种联系。但是，如果我们在一个 relationship 中使用同一个 entity sets 不止一次，就会出现命名冲突。例如 _prereq_ (prerequisite) 关系显示课程之间的预修要求，这个 relationship set 的两个课程均来自 _course_ 这个 entity set。这种情况下，我们需要将这两次出现区分出不同的 **roles**，即：
![image.png](./assets/1620132770403-39c18fd6-9fac-47b0-a823-d3f94033cae6.png)

我们考虑 Mapping Cardinality Constraints。在前面的图中，我们用直线连接，表示所连接的 entity set 是 "many"，即另一边的 entity set 中的一个 entity 可以与这边的任意个（包含 0 个）entity 关联；如果用箭头连接，则表示另一边的 entity set 中的一个 entity 只能与这边的 0 个或 1 个 entity 关联。即：
![image.png](./assets/1620133862536-958f94ad-dae3-4d9c-8573-171bad033873.png)
例如 (b) 中展示的关系即为：（箭头表示的是）1 个 student 只能与 0 个或 1 个 instructor 形成 advisor 关系，而（直线表示的是）1 个 instructor 可以与 0 个至任意个 student 形成 advisor 关系。

Participation Constraints 中，我们用双直线表示 total participation。例如下面的图中，_section_ 中的每一个 entity 都必须与至少一个 _course_ 对应（双菱形以及虚下划线会在稍后学习）：
![image.png](./assets/1620136456430-6c255447-037e-42f1-90c7-ed4c3f27b0d5.png)

我们还可以用一种更加一般的方式描述 cardinality constraints 和 participation constraints，如下图中，每个 instructor 与 0 至任意（用 `*` 表示）个 students 联系，每个 student 与确切 1 个 instructor 联系：
![image.png](./assets/1620136529594-3874e173-ba85-4772-94cd-e089a5a8fe64.png)


### 5.5 Extended E-R Features


### 5.6 Reduction to Relational Schemas

- strong entity set with simple attributes：显然
- composite attributes：展开
- multivalued attributes：建立一个新的 relational schema，在这里每一个 tuple 存储一个值，并参照原来 relational schema 的主码形成外码约束
- weak entity set：加上所依赖 entity set 的主码形成 relational schema，并参照其主码形成外码约束，以及级联删除的完整性约束
   - 我们可以发现，一般情况下，连接 weak entity set 和其以来的 entity set 的 relationship set 的 relational schema 是冗余的。
- relationship set：将相关 entity set 的主码全部作为该 relational schema 的 attributes，如果有重名则重命名。建立参照各个 entity set 的主码形成外码约束。
   - relationship set 的主码：只讨论二元
      - many to many：全部
      - many to one / one to many："many" 那一端的主码
      - one to one：任一端的主码。这种情况下，relationship set 也可以与任一端合并；尤其是在 total participate 的情况下，甚至不会有 null。


## 6 Relational Database Design
这里我们讨论基于函数依赖 (functional dependency) 概念的关系数据库设计的规范方法。

我们希望将关系分解 (decompose) 为合理的大小。但是我们需要考虑到有些情况下分解是有损的 (lossy decomposition)：
![image.png](./assets/1621961688184-3fad02df-10b5-4088-acb9-86c9e4c91413.png)

我们的目标是：判定一个给定的关系是不是“好的”；如果不是，将其**无损**地拆分成数个“好的”关系。

在我们的讨论中，我们用 ![](https://g.yuque.com/gr/latex?%5Calpha%2C%20%5Cbeta#card=math&code=%5Calpha%2C%20%5Cbeta&id=XRkYO) 等希腊字母表示属性集。用 ![](https://g.yuque.com/gr/latex?r(R)#card=math&code=r%28R%29&id=nKjF4) 表示一个关系模式，其中 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=B5IKT) 是这个关系模式的属性集；我们可以用 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=CM5pD) 作为 ![](https://g.yuque.com/gr/latex?r(R)#card=math&code=r%28R%29&id=tf6yr) 的简称。


### 第一范式

-  我们称一个关系模式 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=Ozmk8) 属于 **第一范式 (First Normal Form, 1NF)**, 如果 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=piba8) 的所有 attribute 的 domain 都是 atomic 的；即它们被认为是不可分的单元。 


### 函数依赖

-  如果对于 ![](https://g.yuque.com/gr/latex?r(R)#card=math&code=r%28R%29&id=ndkWr) 的任意合法实例，对其中任意两个元组 ![](https://g.yuque.com/gr/latex?t_1%2C%20t_2#card=math&code=t_1%2C%20t_2&id=FLNli) 都有 ![](https://g.yuque.com/gr/latex?t_1%5B%5Calpha%5D%20%3D%20t_2%5B%5Calpha%5D%20%5CRightarrow%20t_1%5B%5Cbeta%5D%20%3D%20t_2%5B%5Cbeta%5D#card=math&code=t_1%5B%5Calpha%5D%20%3D%20t_2%5B%5Calpha%5D%20%5CRightarrow%20t_1%5B%5Cbeta%5D%20%3D%20t_2%5B%5Cbeta%5D&id=jKXI0)，则称这个实例 **满足 (satisfy) ** 函数依赖 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=Wr4eE)，称 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=ndlV2) 在 ![](https://g.yuque.com/gr/latex?r(R)#card=math&code=r%28R%29&id=zjiyd) 上 **成立 (hold)**。即，![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=C4OiV) 表示属性集 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=wCHB4) 可以唯一标识 ![](https://g.yuque.com/gr/latex?%5Cbeta#card=math&code=%5Cbeta&id=lRyfc)，每个 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=IDwnP) 的取值只对应一个 ![](https://g.yuque.com/gr/latex?%5Cbeta#card=math&code=%5Cbeta&id=PjNJH) 的取值。 

-  ![](https://g.yuque.com/gr/latex?K#card=math&code=K&id=BywIp) is a super key of ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=QIIqV) iff ![](https://g.yuque.com/gr/latex?K%5Cto%20R#card=math&code=K%5Cto%20R&id=wfnTq), ![](https://g.yuque.com/gr/latex?K#card=math&code=K&id=ZnwAD) is a candidate key of ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=hwAzM) iff ![](https://g.yuque.com/gr/latex?K%5Cto%20R%20%5Cland%20(%5Cforall%20%5Calpha%20%5Csubset%20K%2C%20%5Clnot%20%5Calpha%20%5Cto%20R)#card=math&code=K%5Cto%20R%20%5Cland%20%28%5Cforall%20%5Calpha%20%5Csubset%20K%2C%20%5Clnot%20%5Calpha%20%5Cto%20R%29&id=m4R8b). 
-  ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=OQCNS) is **trivial** if ![](https://g.yuque.com/gr/latex?%5Cbeta%5Csubseteq%5Calpha#card=math&code=%5Cbeta%5Csubseteq%5Calpha&id=UpYZh). 

-  一些逻辑关系： 
   - Armstrong's Axioms: 
      - reflexivity, 自反: ![](https://g.yuque.com/gr/latex?%5Cbeta%5Csubseteq%5Calpha%5CRightarrow%5Calpha%5Cto%5Cbeta#card=math&code=%5Cbeta%5Csubseteq%5Calpha%5CRightarrow%5Calpha%5Cto%5Cbeta&id=Y4iWk)
      - augmentation, 增补: ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta%5CRightarrow%5Cgamma%5Calpha%5Cto%5Cgamma%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta%5CRightarrow%5Cgamma%5Calpha%5Cto%5Cgamma%5Cbeta&id=bU2iW)
      - transitivity, 传递: ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta%5Cland%5Cbeta%5Cto%5Cgamma%5CRightarrow%5Calpha%5Cto%5Cgamma#card=math&code=%5Calpha%5Cto%5Cbeta%5Cland%5Cbeta%5Cto%5Cgamma%5CRightarrow%5Calpha%5Cto%5Cgamma&id=gok95)
   - Additional rules (can be inferred from Armstrong's Axioms): 
      - union, 合并: ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta%5Cland%5Calpha%5Cto%5Cgamma%5CRightarrow%5Calpha%5Cto%5Cbeta%5Cgamma#card=math&code=%5Calpha%5Cto%5Cbeta%5Cland%5Calpha%5Cto%5Cgamma%5CRightarrow%5Calpha%5Cto%5Cbeta%5Cgamma&id=FF3Sq)
      - decomposition, 分解: ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta%5Cgamma%5CRightarrow%5Calpha%5Cto%5Cbeta%5Cland%5Calpha%5Cto%5Cgamma#card=math&code=%5Calpha%5Cto%5Cbeta%5Cgamma%5CRightarrow%5Calpha%5Cto%5Cbeta%5Cland%5Calpha%5Cto%5Cgamma&id=QJZCx)
      - pseudo-transitivity, 伪传递: ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta%5Cland%5Cdelta%5Cbeta%5Cto%5Cgamma%5CRightarrow%5Calpha%5Cdelta%5Cto%5Cgamma#card=math&code=%5Calpha%5Cto%5Cbeta%5Cland%5Cdelta%5Cbeta%5Cto%5Cgamma%5CRightarrow%5Calpha%5Cdelta%5Cto%5Cgamma&id=pvRWL)
   - 需要理解的是，![](https://g.yuque.com/gr/latex?%5Calpha%5Cbeta%5Cto%5Cgamma#card=math&code=%5Calpha%5Cbeta%5Cto%5Cgamma&id=V8DtM) 与 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cgamma%2C%20%5Cbeta%5Cto%5Cgamma#card=math&code=%5Calpha%5Cto%5Cgamma%2C%20%5Cbeta%5Cto%5Cgamma&id=FQFGd) 没有必然的逻辑关系。

 

-  用 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=B0DwI) 表示 functional dependencies 的一个集合，用 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=BQ1vI) 表示 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=bLFUD) 的 **闭包 (closure)**，即所有能从 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=JCeMa) 中推导 (logically imply) 出的 functional dependencies 的集合。定义属性集 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=Rdg6U) 在 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=F9VRK) 意义下的一个闭包 ![](https://g.yuque.com/gr/latex?%5Calpha%5E%2B#card=math&code=%5Calpha%5E%2B&id=KHxeq) 为 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=goM4R) 在 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=RSz10) 中能够推导出的所有属性的集合；计算方式同编译原理相关内容。 
   - 我们计算所有 ![](https://g.yuque.com/gr/latex?%5Cgamma%5Csubseteq%20R#card=math&code=%5Cgamma%5Csubseteq%20R&id=d7GrQ) 的闭包 ![](https://g.yuque.com/gr/latex?%5Cgamma%5E%2B#card=math&code=%5Cgamma%5E%2B&id=ExJo5)，就可以计算出 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=zAkdg) 上 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=CNzVy) 的闭包。
   - 如果 ![](https://g.yuque.com/gr/latex?%5Calpha%5Csubseteq%20R#card=math&code=%5Calpha%5Csubseteq%20R&id=iPyhc) 满足 ![](https://g.yuque.com/gr/latex?%5Calpha%5E%2B%20%3D%20R#card=math&code=%5Calpha%5E%2B%20%3D%20R&id=fDZQp)，则 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=ngHLu) 是 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=menWy) 的 super key。如果我们按 ![](https://g.yuque.com/gr/latex?%7C%5Calpha%7C#card=math&code=%7C%5Calpha%7C&id=wDHt7) 从小到大的顺序考察，并排除重复，我们就可以以此法计算出 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=zrrqB) 的 candidate key。

 

### 无关属性

- 给定一个 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=PC5El) 以及 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=F9qXA)。我们称一个属性 ![](https://g.yuque.com/gr/latex?A%5Cin%5Calpha#card=math&code=A%5Cin%5Calpha&id=SETPH) 为 **无关属性 (extraneous attribute)** ，如果 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=f42kz) 能够推导出 ![](https://g.yuque.com/gr/latex?(F-%5C%7B%5Calpha%5Cto%5Cbeta%5C%7D)%5Ccup%5C%7B(%5Calpha-A)%5Cto%5Cbeta%5C%7D#card=math&code=%28F-%5C%7B%5Calpha%5Cto%5Cbeta%5C%7D%29%5Ccup%5C%7B%28%5Calpha-A%29%5Cto%5Cbeta%5C%7D&id=SK6h8)，即在 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=p5wLo) 意义下 ![](https://g.yuque.com/gr/latex?%5Cbeta%5Csubseteq(%5Calpha-%5C%7BA%5C%7D)%5E%2B#card=math&code=%5Cbeta%5Csubseteq%28%5Calpha-%5C%7BA%5C%7D%29%5E%2B&id=ICwcR) 。
- 称一个属性 ![](https://g.yuque.com/gr/latex?B%5Cin%5Cbeta#card=math&code=B%5Cin%5Cbeta&id=XZtdB) 为 extraneous attribute 如果 ![](https://g.yuque.com/gr/latex?(F-%5C%7B%5Calpha%5Cto%5Cbeta%5C%7D)%5Ccup%5C%7B%5Calpha%5Cto(%5Cbeta-B)%5C%7D#card=math&code=%28F-%5C%7B%5Calpha%5Cto%5Cbeta%5C%7D%29%5Ccup%5C%7B%5Calpha%5Cto%28%5Cbeta-B%29%5C%7D&id=UuRQD) 能够推导出 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=iB2mA)，即在 ![](https://g.yuque.com/gr/latex?(F-%5C%7B%5Calpha%5Cto%5Cbeta%5C%7D)%5Ccup%5C%7B%5Calpha%5Cto(%5Cbeta-B)%5C%7D#card=math&code=%28F-%5C%7B%5Calpha%5Cto%5Cbeta%5C%7D%29%5Ccup%5C%7B%5Calpha%5Cto%28%5Cbeta-B%29%5C%7D&id=tyh4Z) 意义下 ![](https://g.yuque.com/gr/latex?B%5Cin%20%5Calpha%5E%2B#card=math&code=B%5Cin%20%5Calpha%5E%2B&id=FdNGz)。
- 上述两个 extraneous attribute 的判定都是弱推强。

 

### 正则覆盖

-  ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=iMHx1) 的一个 **正则覆盖 (canonical cover)** ![](https://g.yuque.com/gr/latex?F_c#card=math&code=F_c&id=JInPD) 是最小的与 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=MZg4F) 等价的集合。即 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=RAf4Q) 与 ![](https://g.yuque.com/gr/latex?F_c#card=math&code=F_c&id=yTYeY) 可以互相推出，且 ![](https://g.yuque.com/gr/latex?F_c#card=math&code=F_c&id=wb9l5) 不含 extraneous attributes，且 ![](https://g.yuque.com/gr/latex?F_c#card=math&code=F_c&id=MNaxh) 中 functional dependency 的 lhs 都是唯一的。 
   - 计算 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=pI6gB) 的正则覆盖的算法如下： 
      - 重复以下 2 个步骤，直到 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=gEXgH) 不再变化：1) 使用 union rule，将 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=WaCO3) 内 lhs 相同的 functional dependency 做合并；2) 在 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=k63UR) 中找到一个 extraneous attribute，将其删除。

 

### 无损分解

-  我们之前提到了我们希望进行 **lossless decomposition**。即对于 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=eN6UJ) 及它的一个拆分 ![](https://g.yuque.com/gr/latex?(R_1%2C%20R_2)#card=math&code=%28R_1%2C%20R_2%29&id=b71Ru)，如果对于 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=ILQ3s) 的任何可能实例 ![](https://g.yuque.com/gr/latex?r#card=math&code=r&id=HpLWp)，都有 ![](https://g.yuque.com/gr/latex?r%20%3D%20%5CPi_%7BR_1%7D(r)%5CJoin%5CPi_%7BR_2%7D(r)#card=math&code=r%20%3D%20%5CPi_%7BR_1%7D%28r%29%5CJoin%5CPi_%7BR_2%7D%28r%29&id=GjE0T)，那么这个拆分是 lossless 的。 
   - 即，如果 ![](https://g.yuque.com/gr/latex?R_1%5Ccap%20R_2%5Cto%20R_1%5Clor%20R_1%5Ccap%20R_2%5Cto%20R_2#card=math&code=R_1%5Ccap%20R_2%5Cto%20R_1%5Clor%20R_1%5Ccap%20R_2%5Cto%20R_2&id=cRqdm)，那么这个拆分是 lossless 的。

 

### 保持依赖的分解

-  如果 ![](https://g.yuque.com/gr/latex?R_1%2C%20R_2%2C%20%5Cdots%2C%20R_n#card=math&code=R_1%2C%20R_2%2C%20%5Cdots%2C%20R_n&id=KgSdj) 是 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=aacSU) 的一个 decomposition，记 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=qwBvU) 在 ![](https://g.yuque.com/gr/latex?R_i#card=math&code=R_i&id=r62eV) 上的一个 **restriction** ![](https://g.yuque.com/gr/latex?F_i#card=math&code=F_i&id=JVfHu) 是 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=Qerpn) 中只包含 ![](https://g.yuque.com/gr/latex?R_i#card=math&code=R_i&id=nZBth) 中属性的 functional dependency 的集合。如果 ![](https://g.yuque.com/gr/latex?(%5Ccup_%7Bi%3D1%7D%5En%20F_i)%5E%2B%20%3D%20F%5E%2B#card=math&code=%28%5Ccup_%7Bi%3D1%7D%5En%20F_i%29%5E%2B%20%3D%20F%5E%2B&id=MprIv)，则称 decomposition ![](https://g.yuque.com/gr/latex?R_1%2C%20R_2%2C%20%5Cdots%2C%20R_n#card=math&code=R_1%2C%20R_2%2C%20%5Cdots%2C%20R_n&id=UVVEZ) 是 **dependency-preserving** 的。 
   - 检查一个 decomposition 是否是 dependency-preserving decomposition 的算法是： 
      - 对于每个 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta%5Cin%20F#card=math&code=%5Calpha%5Cto%5Cbeta%5Cin%20F&id=Ljeme)，令 ![](https://g.yuque.com/gr/latex?res%20%3D%20%5Calpha#card=math&code=res%20%3D%20%5Calpha&id=QBoWS)。
      - 做若干次对 ![](https://g.yuque.com/gr/latex?R_i#card=math&code=R_i&id=lRH3d) 的遍历，对于每一个 ![](https://g.yuque.com/gr/latex?i#card=math&code=i&id=fXDoE) ，计算 ![](https://g.yuque.com/gr/latex?temp%20%3D%20(res%5Ccap%20R_i)%5E%2B%5Ccap%20R_i#card=math&code=temp%20%3D%20%28res%5Ccap%20R_i%29%5E%2B%5Ccap%20R_i&id=niqAe)，令 ![](https://g.yuque.com/gr/latex?res%20%3D%20res%20%5Ccup%20temp#card=math&code=res%20%3D%20res%20%5Ccup%20temp&id=k04Ng)；其中计算闭包是在 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=n1WD3) 意义下进行的。遍历一直持续到经过一次完整的遍历，![](https://g.yuque.com/gr/latex?res#card=math&code=res&id=J4XuD) 没有发生变化。
      - 检查是否有 ![](https://g.yuque.com/gr/latex?%5Cbeta%5Csubseteq%20res#card=math&code=%5Cbeta%5Csubseteq%20res&id=A0wLj)；如果是，说明 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=g6Tg4) 被保留。
      - 如果对于所有 functional dependency 都满足上述条件，说明这是一个 dependency-preserving decomposition。

 

### BCNF

-  我们称一个关系模式 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=CIBhW) 属于 **Boyce-Codd 范式 (Boyce-Codd Normal Form, BCNF)**，如果对于 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=bVgbB) 中任意 functional dependency ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=ULwtJ)，都满足下面至少一条：1) ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=llCS5) is trivial, i.e. ![](https://g.yuque.com/gr/latex?%5Cbeta%5Csubseteq%5Calpha#card=math&code=%5Cbeta%5Csubseteq%5Calpha&id=OiEY8); Or  2) ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=TvS2g) is a super key of ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=AGBQS), i.e. ![](https://g.yuque.com/gr/latex?%5Calpha%5E%2B%20%3D%20R#card=math&code=%5Calpha%5E%2B%20%3D%20R&id=qMnoL). 
   - 将一个不属于 BCNF 的关系模式 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=XjUWk) 分解成若干个 BCNF 的方法是： 
      - 找到一个不满足 BCNF 要求的 functional dependency ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=g6OG4)，我们将 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=nn5dF) 分解为 ![](https://g.yuque.com/gr/latex?%5Calpha%5Ccup%5Cbeta#card=math&code=%5Calpha%5Ccup%5Cbeta&id=YJRAW) 和 ![](https://g.yuque.com/gr/latex?R-(%5Cbeta-%5Calpha)#card=math&code=R-%28%5Cbeta-%5Calpha%29&id=PoJAV) 两部分。
      - 这个分解方式的直观思路是我们希望将 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=Elrfi) 从 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=rUrgI) 中删掉，实现这个目标的方式即为在 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=IlzpJ) 中删除 ![](https://g.yuque.com/gr/latex?%5Cbeta#card=math&code=%5Cbeta&id=fW1D9)。但我们需要保存 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=UUAZg) 与 ![](https://g.yuque.com/gr/latex?%5Cbeta#card=math&code=%5Cbeta&id=KLmUb) 共有的信息，所以我们分解出 ![](https://g.yuque.com/gr/latex?R-(%5Cbeta-%5Calpha)#card=math&code=R-%28%5Cbeta-%5Calpha%29&id=HmSvx) 这一项；另一方面，我们还需要保存 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=OgGED) 这个关系，因此另一部分是 ![](https://g.yuque.com/gr/latex?%5Calpha%5Ccup%5Cbeta#card=math&code=%5Calpha%5Ccup%5Cbeta&id=EUHho)，而由于 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=nzST3)，因此这里 ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=gq1TV) 即为一个 super key。

 

   - 如果需要检查一个关系模式是否属于 BCNF，我们实际上只需要考察 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=X1pnK) 而不需要考察 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=RtzCP)。因为如果 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=FSrVd) 中没有 functional dependency 违反 BCNF 要求，则 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=W2YiI) 也不会有。
   - 但是，如果我们要检查 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=ZLKip) 的一个 decomposition 中的关系是否属于 BCNF，我们不能只考察 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=ZkhdG)。例如 ![](https://g.yuque.com/gr/latex?R%20%3D%20(A%2CB%2CC%2CD%2CE)#card=math&code=R%20%3D%20%28A%2CB%2CC%2CD%2CE%29&id=Fbr5V) 及其拆分 ![](https://g.yuque.com/gr/latex?R_1%20%3D%20(A%2CB)%2C%20R_2%20%3D%20(A%2CC%2CD%2CE)#card=math&code=R_1%20%3D%20%28A%2CB%29%2C%20R_2%20%3D%20%28A%2CC%2CD%2CE%29&id=BEX6O)，只考察  ![](https://g.yuque.com/gr/latex?F%3D%5C%7BA%5Cto%20B%2C%20BC%5Cto%20D%5C%7D#card=math&code=F%3D%5C%7BA%5Cto%20B%2C%20BC%5Cto%20D%5C%7D&id=FD31B) 会发现 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=uNxRZ) 没有与 ![](https://g.yuque.com/gr/latex?R_2#card=math&code=R_2&id=zoGLh) 相关的 functional dependency，因此我们可能会认为 ![](https://g.yuque.com/gr/latex?R_2#card=math&code=R_2&id=ILC6y) 属于 BCNF。但实际上 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=BmqWr) 中的 ![](https://g.yuque.com/gr/latex?AC%5Cto%20D#card=math&code=AC%5Cto%20D&id=JyiTe) 显示 ![](https://g.yuque.com/gr/latex?R_2#card=math&code=R_2&id=Pcj91) 不属于 BCNF。
   - 因此，如果我们要检查 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=bdlp5) 的一个 decomposition 中的关系是否属于 BCNF，我们可以计算每一个 ![](https://g.yuque.com/gr/latex?R_i#card=math&code=R_i&id=MUjaF) 中每一个属性集合在 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=Awfkt) 意义下的闭包，其闭包要么是自己 (trivial)，要么是整个 ![](https://g.yuque.com/gr/latex?R_i#card=math&code=R_i&id=vMip0) (super key)。


### 第三范式
实际上，将一个关系模式分解成 BCNF 并不能保证保持依赖。因此，我们引入 **第三范式 (3rd Normal Form, 3NF)**；这个范式比 BCNF 弱，但是允许我们保持依赖。

-  我们称一个关系模式 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=FexsU) 属于 **第三范式 (3rd Normal Form, 3NF)**，如果对于 ![](https://g.yuque.com/gr/latex?F%5E%2B#card=math&code=F%5E%2B&id=S3gT6) 中任意 functional dependency ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=g4pJ5)，都满足下面至少一条：**1)** ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=Zl5Rh) is trivial, i.e. ![](https://g.yuque.com/gr/latex?%5Cbeta%5Csubseteq%5Calpha#card=math&code=%5Cbeta%5Csubseteq%5Calpha&id=vnXLj); Or  **2)** ![](https://g.yuque.com/gr/latex?%5Calpha#card=math&code=%5Calpha&id=GAW5b) is a super key of ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=ZT6vB), i.e. ![](https://g.yuque.com/gr/latex?%5Calpha%5E%2B%20%3D%20R#card=math&code=%5Calpha%5E%2B%20%3D%20R&id=iGc0w); Or **3)** ![](https://g.yuque.com/gr/latex?%5Cforall%20A%5Cin%20%5Cbeta-%5Calpha#card=math&code=%5Cforall%20A%5Cin%20%5Cbeta-%5Calpha&id=pCxpT), ![](https://g.yuque.com/gr/latex?A#card=math&code=A&id=utMFH) 包含于 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=rAk30) 的一个 candidate key 中（注意，不同的属性可以包含在不同的 candidate key 中）。 
   - 将 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=aRWNS) 分解成 3NF 的算法是：计算 ![](https://g.yuque.com/gr/latex?F#card=math&code=F&id=DhUYd) 的 canonical cover ![](https://g.yuque.com/gr/latex?F_c#card=math&code=F_c&id=DUut8)，对于其中所有 ![](https://g.yuque.com/gr/latex?%5Calpha%5Cto%5Cbeta#card=math&code=%5Calpha%5Cto%5Cbeta&id=jGbFS)，分配一个 ![](https://g.yuque.com/gr/latex?R_i%20%3D%20%5Calpha%5Ccap%5Cbeta#card=math&code=R_i%20%3D%20%5Calpha%5Ccap%5Cbeta&id=dVEHk)。然后检查是否有一个 ![](https://g.yuque.com/gr/latex?R_i#card=math&code=R_i&id=mJ6BS) 是 ![](https://g.yuque.com/gr/latex?R#card=math&code=R&id=fu33F) 的一个 candidate key，如果没有就任取一个 candidate key 分配一个 ![](https://g.yuque.com/gr/latex?R_%7Bi%2B1%7D#card=math&code=R_%7Bi%2B1%7D&id=y3O1S)。最后检查是否有 ![](https://g.yuque.com/gr/latex?R_j%20%5Csubseteq%20R_k#card=math&code=R_j%20%5Csubseteq%20R_k&id=eyIdU)，如果有，删除 ![](https://g.yuque.com/gr/latex?R_k#card=math&code=R_k&id=CUf94)。

 <br /> 
