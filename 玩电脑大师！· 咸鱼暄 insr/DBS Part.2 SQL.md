
## 4 SQL
![image.png](./assets/1619004746932-60b428c5-dd77-4574-9c21-293f8d6ce5e5.png)

### 4.1 SQL Types

- `char(n)` 或 `character(n)` ：固定长度 `n` 的字符串。如果长度不足 `n` ，则在其后追加空格补足。比较不同长度的 `char` 时，比较前会在短值之后加入额外空格使其长度一致。
- `varchar(n)` 或 `character varying(n)` ：可变长度的字符串，最大长度为 `n` 。比较 `char` 和 `varchar`时，有可能会因为数据库系统没有自动在 `varchar` 后增加空格而导致期望之外的结果（这取决于数据库系统）。为了防止这种问题，建议始终使用 `varchar` 。
- `int` 或 `integer` ：整数类型
- `smallint` ：小整数类型
- `numeric(p, d)` ：定点数（小数点位置确定的数），共 `p` 位数字（符号占不占位？），其中 `d` 位在小数点右边。例如， `numeric(3, 1)` 可以精确存储 44.5，但不能精确存储 0.32。
- `real` , `double precision` ：浮点数，双精度浮点数。精度与机器有关。
- `float(n)` ：精度至少为 `n` 的浮点数。
- `boolean` 
- `date` ：containing a (4 digit) year, month and date
- `time` ：Time of day, in hours, minutes and seconds.
- `datetime` ：date plus time of day
- `interval` ：period of time, Subtracting a date/time/timestamp value from another gives an interval value, Interval values can be added to date/time/timestamp values
   - current_date(), current_time(), year(x), month(x), day(x), hour(x), minute(x), second(x)

定义一个类型：<br />`create type Dollars as numeric (12,2) final`<br />使用：`create table department(dept_name varchar (20), building varchar (15), budget Dollars);`

定义一个 domain：<br />`create domain person_name char(20) not null`
```sql
create domain degree_level varchar(10) 
constraint degree_level_test 
check(value in (’Bachelors’, ’Masters’, ’Doctorate’));
```

![](./assets/1618459721058-22da45e5-5a16-45cf-888a-1aaafbdc17b9.png)


### 4.2 SQL Commands
下面格式中换行并不重要。

#### Create Table | 建立关系
**General Form。**
```sql
create table r
	(A1 D1,
   A2 D2,
   ...,
   An Dn,
   <integrity-constraint_1>,
   <integrity-constraint_2>,
   ...,
   <integrity-constraint_k>);
```
其中， `A` 是 relation `r` 中的 attribute， `D` 是它的 domain。<br />`<integrity-constraint>`  是一些完整性约束，例如：

   - `primary key(A, A, ..., A)` ，其中每个 `A` 都是该 relation 中的一个 attribute。这个声明表示这些 `A` 是该 relation 的 primary key。
   - `unique (A, A, ..., A)`，其中每个 `A` 都是该 relation 中的一个 attribute。这个声明表示这些 `A` 是该 relation 的一个 super key。
   - `check (P)`，其中 P 是任意谓词。例如 `check(semester in (’Fall’, ’Winter’, ’Spring’, ’Summer’))`
   - `foreign key(A, A, ..., A) references ref` ，其中每个 `A` 都是该 relation 中的一个 attribute， `ref` 是另一个 relation 的名称。这个声明表示这些 `A` 是该 relation 引用 `ref` 的 foreign key。这种要求称为 referential-intergrity constraint。当进行一个违反参照完整性约束的删除或更改时，数据库默认拒绝这一操作。但是，我们也可以通过一些语句显式规定如何处理这些操作。

例如：
```sql
create table department
	(dept_name	varchar(20),
   building		varchar(15),
   budget			numeric(12, 2),
   primary key(dept_name),
   check (budget > 0)
  );
  
 create table instructor
 	(ID					varchar(5),
   name				varchar(20) not null,
   dept_name	varchar(20),
   salary			numeric(8, 2),
   primary key(ID),
   foreign key(dept_name) references department
   		on delete cascade
   		on update cascade
   );
```
其中第 10 行的 `not null` 是对一个属性的完整性约束，表示这个属性不允许 `null` 值。Primary key 也不能为空值。<br />第 15 行是一个参照完整性约束，

SQL 禁止任何破坏完整性约束的更新。例如：

   - 插入或修改的一个 tuple 在任一 primary key，或标记了 `not null` 的属性上取空值；
   - 插入或修改的一个 tuple 在 primary key 的取值与一个其他 tuple 相同；
   - 插入或修改的一个 tuple 在 foreign key 的取值，在 referenced relation 上没有对应取值；等。


#### Delete | 删除
`delete from r` 将 relation `r` 中所有元组删除<br />`delete from r where P` 将 relation `r` 中所有满足谓词 `P` 的元组删除<br />`drop table r` 将 relation `r` 删除<br />`alter table r add A D` 在 relation `r` 中增加一个 attribute `A` ，其域为 `D` 。已经存在的 tuple 的这一 attribute 的值设为 `NULL` <br />`alter table r drop A` 从 relation `r` 中删除 attribute `A` <br />`alter table r drop foreign key A` 从 relation `r` 中删除 foreign key constraint `A` 。注意：这一操作只删除 **约束** ，即对该 relation 作修改时不再检查取值是否满足 foreign key 的引用要求；但是这并不删除 attribute `A` 。


#### Queries | 查询
**General Form。**
```sql
select A1, A2, ...
from E1, E2, ...
where P;
```
其中：

   - 每个 `A` 代表一个 attribute 或者 attribute 和常数进行 `+ - * /` 运算的表达式（例如 `salary*12` , `a*b*c` 等）。可以通过 `select *` 表示选择所有满足条件的结果，不对 attribute 进行投影。类似地，可以通过 `select r.*` 表示选择 `r` 中的所有 attributes 作为结果 relation 中的 attributes。
   - 每个 `E` 代表一个 relation 或若干个 relation 的 **join**，如 `r1 natural join r2 natural join r3` 。关于连接（join）的更多内容，参见
   - `P` 是一个谓词 (predicate)，其中是用逻辑连词 `and` , `or` , `not` 链接的包含比较运算符 `>, <, >=, <=, =, <>` 的表达式，可以使用括号来声明优先级。如果省略 `where` ，则 `P` 为 true。

这个语句默认不删除筛选出的重复 tuple，因为这非常费时。但是我们可以通过在 `select` 后增加 `distinct` 关键字来强行删除重复，如 `select distinct dept_name from instructor` 。我们也可以添加 `all` 关键字来显式指明不删除重复；由于这是默认的操作，我们一般省略不写。

这个语句计算所有 `E` 的 Cartesian-product，然后选取其中满足 P 的 tuple 的相应 attributes 加入 result relation。这可以使用嵌套循环遍历每一种组合方式实现。

例如：
```sql
select name, title
from instructor natural join teaches, course
where teaches.course_id = course.course_id;

select name, title
from instructor natural join teaches natural join course;
```
注意这两条语句的区别：由于 `instructor` 和 `course` 都有 `course_id` 和 `dept_name` 字段，那么前面一条语句通过第 3 行的谓词，只筛选 `course_id` 一致的 tuple，不要求课程的 `dept_name` 和教师的一致；而后面一条语句通过 natural join 连接，就会同时要求 `dept_name` 一致。

**Display Order。**<br />`select` 语句还可以添加 `order by` 子句来实现对 tuple 显示次序的控制。例如
```sql
select *
from instructor
order by salary desc, name asc;
```
这里 salary 是首要关键字，以降序 `desc` 排列；name 是次要关键字，以升序 `asc` 排列。如果不显式声明升序或降序，则采取升序。

**Predicates。**<br />`where` 子句的谓词除了上述写法外，还支持以下两种写法：

   - `where salary between 90000 and 100000` ，意义是显然的。类似地，还有 `not between` 关键字。
   - `where (a1, a2, ..., an) op (b1, b2, ..., bn)` ，其中 `ai` 和 `bi` 是一些 attributes， `op` 是比较运算符。这个语句等价于 `where a1 op b1 and a2 op b2 and ... and an op bn` 。


#### Rename | 重命名
我们可以用 `as` 关键字在查询语句中作重命名，格式为 `old_name as new_name` 。例如：
```sql
select T.name as instructor_name, S.course_id
from instructor as T, teaches as S
where T.ID = S.ID
```
这里我们将 select 子句中的 name 更名为 instructor_name，使其在结果关系中意义更为明确；同时我们在 from 子句中将 instructor 和 teaches 更名为 T 和 S，以便减少 where 子句中比较时的代码量。<br />请注意，将 instructor 和 teaches 更名为 T 和 S 是暂时的，这不会影响这两个 relation 的名称，而只是一个临时的别名。

重命名的一个重要应用是在同一个 relation 中作比较的情况。例如：
```sql
select distinct T.name
from instructor as T, instructor as S
where T.salary > S.salary and S.dept_name = 'Biology';
```
这一查询返回的是工资比 Biology 系中某个老师工资高的所有老师姓名。如果不作重命名，这一查询将无法如此实现。

在重命名语句中， `as` 是可以省略的。即，我们可以直接写作 `old_name new_name` 。


#### String Operations | 字符串运算
**Patterns**。<br />SQL 中可以使用关键字 `like` 来进行模式识别。 `%` 匹配任意子串（包括空串）， `_` 匹配任意字符。例如 '___%abc' 匹配任意以 abc 结尾的、前面有至少三个任意字符的字符串。使用 `like` 关键字的查询的 `where` 子句的一个例子是 `where building like '%Watson%'` 。<br />为了在字符串中匹配 '%' 和 '_'，我们需要定义转义字符 (escape character)。我们通过 `escape` 关键字定义转义字符。例如我们使用 `\` 作为转义字符时， `\%` , `\_` , `\\` 分别匹配字符 %, _, \。例如 `like '100\%' escape '\'` 。<br />`not like` 匹配不满足对应模式的 token。

不同数据库提供不同的字符串操作。例如：<br />**Concatention**。 `||` <br />**Converting from upper to lower case and vice versa**。 `upper(s)` , `lower(s)` <br />etc.


#### Set Operations | 集合运算
`union` 运算实现集合（关系）的并。例如：
```sql
(select course_id from section where sem = 'Fall' and year = 2009)
union
(select course_id from section where sem = 'Spring' and year = 2010)
```
这一语句返回在 2009 秋季学期和 2010 春季学期开设所有课程的 ID 的并集。

类似地，还有 `intersect` 和 `except` 实现交集和差集运算。<br />我们可以通过 `union all` , `intersect all` , `except all` 来保留所有重复。


#### Null Values | 空值
如果算术表达式的任一输入为 null，则结果为 null。<br />`where` 子句可以通过 `is null` 和 `is not null` 进行筛选，例如 `where salary is null` 。

涉及空值的比较运算的结果为 unknown。例如， `null <> null` 和 `null = null` 均为 unknown。<br />unknown 在一些永真的逻辑式中不影响其结果，例如 unknown and false = false；但是 unknown and true = unknown。<br />类似地，也有 `is unknown` 和 `is not unknown` 。

特别地，使用 `select distinct` 时，重复元组会被去除。在此时进行判断时，('A', null) 和 ('A', null) 会被认为是一样的 tuple 从而只保留一个。


#### Aggregate Functions | 聚集函数
聚集函数包括 `max` , `min` , `sum` , `avg` , `count` 。下面展示其应用方法：
```sql
select count(*), avg(salary) as avg_salary
from instructor
where dept_name = 'Comp.Sci.';
```
这会返回一个仅有 1 个 tuple，2 个 attributes 的 relation。<br />`count(distinct ID)` 用来计数，但去除重复。

**Aggregation with Grouping.** <br />我们可以通过 `group by` 子句来对 tuples 进行分组，然后再用聚集函数进行统计。例如：
```sql
select dept_name, avg(salary) as avg_salary
from instructor
group by dept_name;
```
对于每一个 dept_name，结果 relation 中会有一个 tuple 表示 instructor 中所有对应取值的 tuple 的 salary 的平均值。注意到 select 子句中还选择了 dept_name 这一 attribute，这是合理的；因为对于结果中的每一个 tuple，其 dept_name 是一定的，因为我们就是使用 dept_name 进行分组的。

但是，如果 select 中的某个 attribute 既不是 group by 子句中的一个分组依据，又没有用聚集函数进行统计，那么这就会引发一个错误。因为此时同一个分组中的这个 attribute 可能不同，因此结果 relation 中不知道如何选取这个 attribute 的值。例如：
```sql
/* erroneous query */
select dept_name, ID, avg(salary)
from instructor
group by dept_name;
```
此时，结果会按照 dept_name 进行分组；每一个分组的 dept_name 是可知的，但是某个分组中可能有多个不同 ID，因此 SQL 不能知道使用哪个 ID 作为结果中该分组的 ID。因此这是一个错误的查询。

**Having clause.** <br />有时我们希望对聚合函数的值而不是某个 tuple 的值进行筛选；即，我们对分组后的结果进行筛选，这时我们添加 `having` 子句。例如：
```sql
select dept_name, avg(salary)
from instructor
group by dept_name
having avg(salary) > 42000;
```

查询的操作顺序是：首先根据 from 子句计算出一个关系；然后用 where 子句对这个关系中的 tuples 进行筛选；然后根据 group by 对 tuples 进行分组；然后对各个分组计算 having 子句；最后根据 select 产生出结果。

**Null Values.** <br />Null 不影响 `count` 进行计数；除此以外的聚集函数在计算时会忽略空值。如果忽略空值后的输入值集合为空集，则聚集函数会返回 null。


#### Nested Subqueries | 嵌套子查询
```sql
select count(distinct ID)
from takes
where (course_id, sec_id, semester, year) in (select course_id, sec_id, semester, year
                                              from teaches
                                              where teaches.ID = 10101);
```
`in` 连接词用于测试 tuple 是否在某个 relation 中。类似地，也有 `not in` 。<br />`in` 和 `not in` 操作符也可以用于枚举集合，例如 `where name in ('Mozart', 'Einstein')` 。

```sql
select name
from instructor
where salary > some(select salary
                    from instructor
                    where dept name = ’Biology’);
```
`a > some r` 表示 a 至少大于 r 中的一个 tuple。类似地，还有 `< some` , `= some` , `>= all` , `<> all` 等。这也可以用在 having 子句中，例如：
```sql
select dept name
from instructor
group by dept name
having avg (salary) >= all (select avg (salary)
                            from instructor
                            group by dept name);
```

`exists r` 在 r 非空的时候返回 true，反之返回 false。例如：
```sql
select course id
from section as S
where semester = 'Fall' and year = 2009 and
      exists (select *
              from section as T
              where semester = 'Spring' and year = 2010 and
                    S.course_id = T.course_id);
```
类似地，也有 `not exists` 。<br />注意到在上面查询中，外层查询中定义的名称 `S` 在子查询中也用到了，这称为 correlated subquery。这种使用的规则与编程语言的变量作用域类似：外层可以在内层中使用，反之不行。

```sql
select distinct S.ID, S.name
from student as S
where not exists((select course_id
                  from course
                  where dept_name = ’Biology’)
                  except
                  (select T.course_id
                  from takes as T
                  where S.ID = T.ID));
```
`not exists (A except B)` 即 A - B 为空，即 ![](https://cdn.nlark.com/yuque/__latex/1d692925920a6f5ff7d9b834b166debc.svg#card=math&code=A%5Csubseteq%20B&height=16&id=HpvIQ)。

`unique r` 在 r 中没有重复 tuple 时返回 true。

子查询也可以出现在 from 子句中：
```sql
select dept_name, avg_salary
from (select dept_name, avg(salary) as avg_salary
      from instructor
      group by dept_name)
      as dept_avg(dept_name, avg_salary)
where avg_salary > 42000;
```

`with` 子句可以添加临时 relation 从而帮助查询。例如：
```sql
with dept_total (dept_name, value) as
        (select dept_name, sum(salary)
         from instructor
         group by dept name),
    dept_total_avg(value) as
        (select avg(value)
         from dept_total)
select dept_name
from dept_total, dept_total_avg
where dept_total.value >= dept_total_avg.value;
```


#### Scalar Subqueries | 标量子查询
如果一个子查询返回的结果是只有 1 个 attribute 和 1 个 tuple 的 relation（即单个值），那么它可以出现在返回单个值的表达式可以出现的任何地方，例如 having 和 where 子句中。<br />这样的出现在 select 语句中，会为结果 relation 添加一个新的 attribute，其值均为该 relation 的值。例如：
```sql
select dept_name, (select count(*)
                   from instructor
                   where department.dept_name = instructor.dept_name)
                  as num instructors
from department;
```


#### Insert | 插入语句
以下三条插入语句等价：
```sql
insert into course
			values ('CS-437', 'Database Systems', 'Comp. Sci.', 4);

insert into course (course_id, title, dept_name, credits)
			values ('CS-437', 'Database Systems', 'Comp. Sci.', 4);
      
insert into course (title, course_id, credits, dept_name)
			values ('Database Systems', 'CS-437', 4, 'Comp. Sci.');
```

我们也可以将查询出的结果 tuples 插入某个 relation：
```sql
insert into instructor
      select ID, name, dept_name, 18000
      from student
      where dept_name = ’Music’ and tot cred > 144;
```
对于这样的语句，我们会首先完成 select 的全部计算后再进行 insert。


#### Update | 更新
如下的语句完成更新，其含义是显然的；值得注意的是其中的 `set` 和 `case (when P then ...)* else ... end` 结构：
```sql
update instructor
set salary = salary * 1.05;

update instructor
set salary = salary * 1.05
where salary < 70000;

update instructor
set salary = salary * 1.05
where salary < (select avg (salary)
                from instructor);
                
update instructor
set salary = case
                when salary <= 100000 then salary * 1.05
                when salary <= 200000 then salary * 1.04
                else salary * 1.03
             end
```

#### 

#### Join Operations | 连接表达式
![](./assets/1618453776845-1984e327-43c1-41c8-9ba0-b85e4e791f14.png)
连接表达式将两个关系以某种关系组合后返回一个新的关系。Join types 定义如何处理那些在另一个 relation 中不对应任何条目的 tuple，我们在第 6 章中已经进行过讨论；Join Conditions 定义依照哪些 tuple 进行连接，以及连接后返回什么样的 attributes。<br />缺省的 Join type 是 inner join，缺省的 join condition 是空（即没有任何附加）。

例如，_instructor(ID, name, dept_name, salary) _和 _teaches(ID, course_id, sec_id, semester, year) _的自然连接可以写作以下任意一种：
```sql
select *
from instructor, teaches
where instructor.ID = teaches.ID;

select *
from instructor natural join teaches;

select *
from instructor join teaches using (ID);

select *
from instructor join teaches on instructor.ID = teaches.ID;
```
这里可以看到，`natural` 指明自然连接，即共有字段都应相等才会被链接；而 `using(A1, A2, ...)` 则显式地指明哪些共有字段需要相等。

对于 `Person(PersonId, LastName, FirstName)` 和 `Address(AddressId, PersonId, City, State)`，无论 person 是否有地址信息，都需要基于上述两表提供 person 的 `FirstName, LastName, City, State`：
```sql
select FirstName, LastName, City, State
from Person natural left join Address;
```
	这里使用到了左外连接，如果 Person 中的某个 tuple 的 PersonID 在 Address 中没有出现，则连接并选择后的结果为 (FirstName, Lastname, _null_, _null_)。`left join` 等价于 `left outer join`。


### 4.3 Accessing SQL From a Programming Language
不想学

### 4.4 Functions and Procedures

#### Functions
如下代码定义了一个函数 `dept_count`：
```sql
create function dept_count(dept_name varchar(20))
  returns integer
  begin
    declare d_count integer;
      select count(*) into d_count
      from instructor
      where instructor.dept_name = dept_name
    return d_count;
  end
```
	如第 1~2 行所示，函数的声明部分的格式为 <br />**create function **_function_name_**(**_parameter_list_**) returns **_return_type_<br />第 4 行声明了一个变量（在 **begin ... end** 范围内的局部变量），其格式为<br />**declare **_var_name var_type_<br />第 5~7 行是一个查询语句，但这里使用到了关键字 `into` 实现将结果存入变量中<br />第 8 行是这个函数的返回语句。

调用：
```sql
select dept_name, budget
from instructor
where dept_count(dept_name) > 12;
```

函数的返回值也可以是一个关系：
```sql
create function instructors_of(dept_name varchar(20))
  returns table(
    ID varchar (5),
    name varchar (20),
    dept_name varchar (20),
    salary numeric (8,2)
  )
  return table(
    select ID, name, dept_name, salary
    from instructor
    where instructor.dept_name = instructor_of.dept_name
  );
```
调用：
```sql
select *
from table (instructors_of (‘Music’));
```
SQL 支持函数重载，规则与 C++ 等类似。


#### Procedure
```sql
create procedure dept_count_proc(in dept_name varchar(20),
																 out d_count integer)
begin
  select count(*) into d_count
  from instructor
  where instructor.dept name= dept count proc.dept name
end
```
	调用：
```sql
declare d_count integer;
call dept_count_proc(‘Physics’, d_count);
```
	SQL 支持过程重载，规则与 C++ 等类似。


#### While
```sql
declare n integer default 0;
while n < 10 do
	set n = n + 1
end while
```


#### Repeat
```sql
repeat
	set n = n  – 1
  until n = 0
end repeat
```


#### For
```sql
declare n integer default 0;
for r as
  select budget from department
  where dept name = ‘Music‘
do
	set n = n− r.budget
end for
```
程序每次读取 select 结果中的一个 tuple，并将其存入 r，开始这次循环；`leave` 同 C 中的 `break`，`iterate` 同 C 中的 `continue`。


#### If - else
```sql
if boolean expression
	then statement
elseif boolean expression
	then statement
else statement
end if
```


#### Exception
![image.png](./assets/1619008272241-226e4bbb-0a49-4ce6-9d12-670f70525189.png)


### 4.5 Triggers | 触发器
触发器实现当某个关系被修改时，自动执行某些动作。一个触发器有三部分要素：引发触发器被检测的 Event，触发器执行需要满足的 Condition 以及触发器执行时的 Action。例如：
```sql
create trigger timeslot_check1 after insert on section
  referencing new row as nrow
  for each row
  when (nrow.time_slot_id not in (select time_slot_id from time_slot)) 
  begin
  	rollback
  end;
  
create trigger timeslot_check2 after delete on timeslot
	referencing old row as orow
  for each row
  when (orow.time_slot_id not in (select time_slot_id
                                  from time_slot)
  			and orow.time_slot_id in (select time_slot_id
  																from section))
  begin
  	rollback
  end;
```
	其中，第 1 行和第 9 行包含两个关于 Event 的声明。除了 `insert` 和 `delete`，还有 `update`；除了 `after`，还有 `before`。<br />第 4 行的 when 语句说明了 Condition，第 5-7 行是 Action。

其他例子：
```sql
create trigger credits_earned after update of takes on (grade)
    referencing new row as nrow
    referencing old row as orow
    for each row
    when nrow.grade <> ’F’ and nrow.grade is not null
         and (orow.grade = ’F’ or orow.grade is null)
    begin atomic
        update student
        set tot_cred = tot_cred + (select credits
                                   from course
                                   where course.course_id= nrow.course_id)
        where student.id = nrow.id;
    end;
```
```sql
create trigger setnull before update on takes
    referencing new row as nrow
    for each row
    when (nrow.grade = ’ ’)
    begin atomic
    		set nrow.grade = null;
    end;
```
