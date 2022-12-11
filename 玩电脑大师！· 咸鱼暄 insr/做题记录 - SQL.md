	最近在学数据库，感觉什么都不会；然后发现 LeetCode 上有一些 SQL 的题，做来看看。如果有做的不怎么好的题，就写下来。<br />以下题目都来自 LeetCode！


### 简单题

#### #182 - having
编写一个 SQL 查询，查找 Person 表中所有重复的电子邮箱。<br />示例：
```
+----+---------+
| Id | Email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
```
根据以上输入，你的查询应返回以下结果：
```
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
```
说明：所有电子邮箱都是小写字母。

```sql
select Email
from Person
group by Email
having count(*) > 1
```
group by 和 having 语句


#### #181 
Employee 表包含所有员工，他们的经理也属于员工。每个员工都有一个 Id，此外还有一列对应员工的经理的 Id。
```
+----+-------+--------+-----------+
| Id | Name  | Salary | ManagerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | NULL      |
| 4  | Max   | 90000  | NULL      |
+----+-------+--------+-----------+
```
给定 Employee 表，编写一个 SQL 查询，该查询可以获取收入超过他们经理的员工的姓名。在上面的表格中，Joe 是唯一一个收入超过他的经理的员工。
```
+----------+
| Employee |
+----------+
| Joe      |
+----------+
```

愚蠢的做法：
```sql
select Name as Employee
from Employee as S
where ManagerID is not null
      and Salary > (select Salary from Employee as T where
                    T.Id = S.ManagerId);
```
首先根本没必要判断 is not null，因为等号自己就判断了）其次这种很慢，因为是每个 tuple 搜了一遍

聪明点的做法：
```sql
select S.Name as Employee
from Employee as S, Employee as T
where S.ManagerId = T.Id and S.Salary > T.Salary;
```


#### #620 - order by
您需要编写一个 SQL查询，找出所有影片描述为非 boring (不无聊) 的并且 id 为奇数 的影片，结果请按等级 rating 排列。

例如，下表 cinema:
```
+---------+-----------+--------------+-----------+
|   id    | movie     |  description |  rating   |
+---------+-----------+--------------+-----------+
|   1     | War       |   great 3D   |   8.9     |
|   2     | Science   |   fiction    |   8.5     |
|   3     | irish     |   boring     |   6.2     |
|   4     | Ice song  |   Fantacy    |   8.6     |
|   5     | House card|   Interesting|   9.1     |
+---------+-----------+--------------+-----------+
```
对于上面的例子，则正确的输出是为：
```
+---------+-----------+--------------+-----------+
|   id    | movie     |  description |  rating   |
+---------+-----------+--------------+-----------+
|   5     | House card|   Interesting|   9.1     |
|   1     | War       |   great 3D   |   8.9     |
+---------+-----------+--------------+-----------+
```
```sql
select *
from cinema
where description <> 'boring' and id & 1
order by rating desc;
```
SQL 也支持取模和位运算之类的东西）<br />order by desc asc 实现排序


#### #196
