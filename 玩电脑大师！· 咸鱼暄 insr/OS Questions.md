
# 4 Threads & Concurrency

#### 1
![image.png](./assets/1610023059457-89eba3b9-115b-4e26-9894-501045733f3a.png)

# 5 CPU Scheduling

#### 1 Burst?
![image.png](./assets/1610039821012-9af44752-71d3-4796-828f-25fea23fc701.png)

# 9 Main Memory

#### 1
![image.png](./assets/1608309640283-aebe0221-436c-49c2-a4f2-731119da3a48.png)

- **Protection:** 保证进程之间不会互相闯入对方的存储。
- **Fast execution:** 不能由于 protection 降低访问内存的效率。
- **Fast context switch:** 每当进行 context switch 时，可以比较快地找到并访问当前进程的内存。    ？ 不确定（指不能复制一份？）


#### 2
![image.png](./assets/1608309738643-468098f6-7c39-40ac-a126-9aa524f87044.png) <br />Flush 是啥？要不要把现在 TLB 的东西存到内存里？没太想通重新分配内存的时候做的事情）


#### 3
![image.png](./assets/1608309796155-25bb3f8d-e0c3-46cf-9e73-f5b331c8e462.png)
为啥 smaller


#### 4
每个二级/三级页表也是一个 page 那么大？<br />多级页表的多次内存访问怎么办？（多级 TLB？）


#### 5
![image.png](./assets/1608361903042-f3d0aae9-29f6-4097-9df9-14066c583a1f.png)
没看懂这是啥）
