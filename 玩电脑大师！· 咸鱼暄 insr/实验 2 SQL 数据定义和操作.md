
### 实验目的
1. 掌握关系数据库语言 SQL 的使用
2. 使所有的 SQL 作业都能上机通过


### 实验平台

1. 操作系统： Windows 10
2. 数据库管理系统：SQL Server 2014 


### 实验内容和要求

1. 建立数据库
2. 数据定义： 表的建立/删除/修改；索引的建立/删除；视图的建立/删除
3. 数据更新： 用 insert/delete/update 命令插入/删除/修改表数据
4. 数据查询： 单表查询，多表查询， 嵌套子查询等
5. 视图操作：通过视图的数据查询和数据修改
6. 所有的 SQL 作业都上机通过


### 实验步骤
我们以第 3~4 章的部分作业题为例，贯穿作业题在 SQL 中的实现和验证，完成本次实验的实验内容。涉及的数据库模式是：
![image.png](./assets/1621080154513-8e2b9caa-d9d3-4665-8f80-ddccbaeac9bb.png)

#### 建立数据库
通过 `create database Employee;` 成功创建了 Employee 数据库。
![image.png](./assets/1621079559014-57e8ac50-144e-49e6-8ada-ba209dbe8652.png)


#### 表的建立、删除、修改
我们通过以下代码建立了对应的 4 个表：
```sql
use Employee;

create table employees
(
	employee_name	varchar(20) not null,
	street			varchar(20),
	city			varchar(20),
	primary key (employee_name)
);

create table companies
(
	company_name	varchar(20) not null,
	city			varchar(20),
	primary key (company_name)
);

create table works
(
	employee_name	varchar(20) not null,
	company_name	varchar(20) not null,
	salary			numeric(8, 2),
	primary key (employee_name),
	foreign key (employee_name) references employees,
	foreign key (company_name) references companies,
	check (salary > 0.00)
);

create table manages
(
	employee_name	varchar(20) not null,
	manager_name	varchar(20) not null,
	primary key (employee_name),
	foreign key (employee_name) references employees,
	foreign key (manager_name) references employees
);
```
部分结果如下图所示：
![image.png](./assets/1621080111458-8cb073eb-5f04-40ec-93ab-63ea3a6ac445.png)

我们通过如下代码尝试表的删除和修改：

- `create table test (id int not null);` 建立表：

![image.png](./assets/1621080366628-d0d5049f-03c4-4efa-ac8c-c1c6bb976a09.png)

- 插入一些元组：

![image.png](./assets/1621080499572-a09b2a55-55db-45dc-b709-0b2beeead3a8.png)

- 修改表：增加属性
   - 注意，第 2 行的 `go` 的作用是将缓存中的语句先运行。否则，第 4 行的语句就会因为第 2 行的延迟运行而出现错误。

![image.png](./assets/1621080680869-c483cb9b-cf39-4849-abdd-ca7328e54744.png)

- 修改表：删除属性

![image.png](./assets/1621080832338-fd7ae5d4-8243-4db9-82e6-541d9c82e1a4.png)

- 删除表：运行 `drop table test` 之后，关系 `test` 被删除

![image.png](./assets/1621080909760-0edddfd7-e2da-4b32-a821-045690fd6104.png)


#### 数据的插入、删除、修改

- 插入：

![image.png](./assets/1621085216008-6ed595df-d264-4f3b-86ea-08c30c9e8be3.png)

- 删除：

![image.png](./assets/1621085284362-cb47aafc-8576-4805-90bb-0e630b1fb75f.png)

- 修改：

![image.png](./assets/1621085359327-62d3e8d8-b54c-4513-8c0c-a7b92a2c09af.png)

#### 索引的建立、删除

- 索引的建立
   - 可见，建立索引后查询对应列，结果为顺序排列的顺序，而不是插入的顺序。

![image.png](./assets/1621085604546-e670b9a7-a17b-48ea-8f63-ceabe6609773.png)

- 通过 `drop index works_salary on works` 实现上面索引的删除。


#### 单表查询、多表查询、嵌套子查询

- 单表查询

![image.png](./assets/1621086499826-53c1455f-dd52-4d4f-bd91-ef0c9652e426.png)

- 多表查询

![image.png](./assets/1621086754757-e40153a9-6a9e-4925-8d12-ebd0da833172.png)

- 嵌套子查询

![image.png](./assets/1621086847364-ceb1fe0c-f206-4531-8698-f153e46f3986.png)

#### 视图的建立、删除，通过视图的数据查询、修改
通过下面代码建立视图：
```sql
create view Employee_Company as
	select E.employee_name, C.company_name, C.city
	from employees as E, works as W, companies as C
	where E.employee_name = W.employee_name and W.company_name = C.company_name;
```
进行查询：
![image.png](./assets/1621087680246-dfb0447c-29bb-4ba0-87df-7ed1da0e6919.png)
修改：
![image.png](./assets/1621087787745-6b177b6a-84d1-4188-9559-9eb288e32da7.png)
通过 `drop view Employee_Company` 删除视图。
