
# 4 实验过程

## 4.1 环境搭建

### 4.1.1 建立映射（略）

### 4.1.2 组织文件结构
![image.png](./assets/1605281401359-19604338-8507-4c26-b257-8feaf74f9b23.png)
编译前后的文件结构

## 4.2 代码及详细注解

### 4.2.1 整体结构
本实验的代码任务，基本基于 _sched.c_ 文件。下面是 _sched.c_ 文件的结构（省略了函数定义，函数定义在后面说明）
```c
#include"put.h"
#include"sched.h"

struct task_struct *current;
struct task_struct *task[NR_TASKS];
long PRIORITY_INIT_COUNTER[NR_TASKS] = { 0, 7, 6, 5, 4 };
extern void init_epc(void);
extern void save_load(struct task_struct* current, struct task_struct* next);
extern unsigned int rand();

#ifdef SJF
    void task_init(void){...}
    void do_timer(void){...}
    void schedule(void){...}
#endif

#ifdef PRIORITY
    void task_init(void){...}
    void do_timer(void){...}
    void schedule(void){...}
#endif

void switch_to(struct task_struct* next){...}
void dead_loop(void) { while (1) { continue; } }
```

- `struct task_struct *current;` 是当前进程指针；`struct task_struct *task[NR_TASKS];` 是进程指针数组。
   - 其中， `NR_TASKS` 是 task 的最大数量，宏定义在 _sched.h_ 中。

- `long PRIORITY_INIT_COUNTER[NR_TASKS] = { 0, 7, 6, 5, 4 };` 是 PRIORITY 模式下每个进程的初始时间片，这个设置是基于实验指导 4.4.3 中的这一要求：
> 优先级抢占式算法
> 每次do_timer都进行一次抢占试优先级调度。当在do_timer中发现当前运行进程剩余运行时间为0（即当前进程已运行结束）时，需重新为该进程分配其对应的运行时长。相当于重启当前进程，即重新设置每个进程的运行时间长度和初始化的值一致。

   - 如果要将 `LAB_TEST_NUM` 拓展为 4 以上的值，我们需要增加对这一数组的后续赋值。为了解决这一问题，我们在 `task_init()` 中做了一些修改，详细内容参见 _4.2.2.1_ 的代码以及 _4.4 拓展 _一节。也是因为这个原因，我们没有将此数组定义为 const 数组。

<br />

- `extern void init_epc(void)` 是初始化函数，其中将 `dead_loop` 赋值给 `epc` 寄存器；`extern void save_load(struct task_struct* current, struct task_struct* next);` 是切换进程函数，保存当前进程的 ra, sp, s0~s11 到当前进程的进程状态段中，将下一个进程的进程状态段的相关数据载入到 ra, sp, s0~s11 中。这两个函数以汇编定义在_ entry.S _中，这里用 `extern` 显式声明其外部链接属性。

- `extern unsigned int rand()` 是生成随机数的函数，返回值为 `(unsigned int) 1~5` 。函数定义在 _rand.c_ 中，由于_ rand.h _不在默认 include 路径中，我们在这里显示声明其外部链接。
   - _rand.c _的随机数种子宏定义位于 _rand.h_ 中。需要注明的是，更新种子后需要 `make clean` 再重新编译，因为 _rand.h_ 并不在 Makefile 的依赖文件当中。

<br />

- `#ifdef SJF` 和 `#ifdef PRIORITY` 是区分两种调度模式的宏定义。我们通过在编译时使用参数 `-DXX` 来视为定义了 `#define XX` 。这里，我们在 _lab3/Makefile_ 中的 `CFLAG` 变量中增加参数 `-DSJF` 或 `-DPRIORITY` ，来实现对这两种调度模式的选择。
   - 需要注明的是，更新参数后需要 `make clean` 再重新编译，因为 Makefile 自身并不在依赖文件中。

<br />

- 其余函数功能与实验指导相同，在后面详细解释。


### 4.2.2 详细代码

#### 4.2.2.1 task_init()
```c
/* SJF */
void task_init(void)
{
	int i;
	current = task[0] = (struct task_struct *)0x80010000;
	for (i = 1; i <= LAB_TEST_NUM; i++)
	{
		task[i] = task[i - 1] + 0x1000;
	}

	//初始化task[0]的变量
	task[0]->state = TASK_RUNNING;
	task[0]->counter = 0;
	task[0]->priority = 5;
	task[0]->blocked = 0;
	task[0]->pid = 0;
	task[0]->thread.ra = 0;
	task[0]->thread.sp = (unsigned long long)task[0] + 0x1000;
	task[0]->thread.s0 = 0;
	task[0]->thread.s1 = 0;
	task[0]->thread.s2 = 0;
	task[0]->thread.s3 = 0;
	task[0]->thread.s4 = 0;
	task[0]->thread.s5 = 0;
	task[0]->thread.s6 = 0;
	task[0]->thread.s7 = 0;
	task[0]->thread.s8 = 0;
	task[0]->thread.s9 = 0;
	task[0]->thread.s10 = 0;
	task[0]->thread.s11 = 0;

	//初始task变量
	for (i = 1; i <= LAB_TEST_NUM; i++)
	{
		task[i]->state = TASK_RUNNING;
		task[i]->counter = rand();
		task[i]->priority = 5;
		task[i]->blocked = 0;
		task[i]->pid = i;
		task[i]->thread.ra = (unsigned long long)init_epc;
		task[i]->thread.sp = (unsigned long long)task[i] + 0x1000;
		task[i]->thread.s0 = 0;
		task[i]->thread.s1 = 0;
		task[i]->thread.s2 = 0;
		task[i]->thread.s3 = 0;
		task[i]->thread.s4 = 0;
		task[i]->thread.s5 = 0;
		task[i]->thread.s6 = 0;
		task[i]->thread.s7 = 0;
		task[i]->thread.s8 = 0;
		task[i]->thread.s9 = 0;
		task[i]->thread.s10 = 0;
		task[i]->thread.s11 = 0;

		puts("[PID = ");
		puti(task[i]->pid);
		puts("] Process Create Successfully! counter = ");
		puti(task[i]->counter);
		puts("\n");
	}
}

/* PRIORITY */
void task_init(void)
{
#if LAB_TEST_NUM>4
	for (int i = 5; i <= LAB_TEST_NUM; i++)
	{
		PRIORITY_INIT_COUNTER[i] = LAB_TEST_COUNTER;
	}
#endif

	current = task[0] = (struct task_struct *)0x80010000;
	for (int i = 1; i <= LAB_TEST_NUM; i++)
	{
		task[i] = task[i - 1] + 0x1000;
	}

	//初始化task[0]的变量
	task[0]->state = TASK_RUNNING;
	task[0]->counter = 0;
	task[0]->priority = 5;
	task[0]->blocked = 0;
	task[0]->pid = 0;
	task[0]->thread.ra = 0;
	task[0]->thread.sp = (unsigned long long)task[0] + 0x1000;
	task[0]->thread.s0 = 0;
	task[0]->thread.s1 = 0;
	task[0]->thread.s2 = 0;
	task[0]->thread.s3 = 0;
	task[0]->thread.s4 = 0;
	task[0]->thread.s5 = 0;
	task[0]->thread.s6 = 0;
	task[0]->thread.s7 = 0;
	task[0]->thread.s8 = 0;
	task[0]->thread.s9 = 0;
	task[0]->thread.s10 = 0;
	task[0]->thread.s11 = 0;

	//初始task变量
	for (int i = 1; i <= LAB_TEST_NUM; i++)
	{
		task[i]->state = TASK_RUNNING;
		task[i]->counter = PRIORITY_INIT_COUNTER[i];
		task[i]->priority = 5;
		task[i]->blocked = 0;
		task[i]->pid = i;
		task[i]->thread.ra = (unsigned long long)init_epc;
		task[i]->thread.sp = (unsigned long long)task[i] + 0x1000;
		task[i]->thread.s0 = 0;
		task[i]->thread.s1 = 0;
		task[i]->thread.s2 = 0;
		task[i]->thread.s3 = 0;
		task[i]->thread.s4 = 0;
		task[i]->thread.s5 = 0;
		task[i]->thread.s6 = 0;
		task[i]->thread.s7 = 0;
		task[i]->thread.s8 = 0;
		task[i]->thread.s9 = 0;
		task[i]->thread.s10 = 0;
		task[i]->thread.s11 = 0;

		puts("[PID = ");
		puti(task[i]->pid);
		puts("] Process Create Successfully! counter = ");
		puti(task[i]->counter);
		puts(" priority = ");
		puti(task[i]->priority);
		puts("\n");
	}
}
```
这里，我们如实验指导那样对任务做了初始化。各个 task 的 `thread.ra` 被指向了 `init_epc` 函数来初始化每个进程的 epc；`thread.sp` 指向了其分块的底端作为下一次 load 出的栈指针。<br />PRIORITY 模式下的该函数仅 counter 初始化以及输出略有不同，没有核心差别。需要特殊说明的是，由于拓展需要，我们判断当 `LAB_TEST_NUM` ，即运行的进程数大于 4 时，将第 5 个及以后的 task 的默认时间片均赋值为 `LAB_TEST_COUNTER` 。


#### 4.2.2.2 do_timer()
```c
/* SJF */
void do_timer(void)
{
    /* 如果 current 为 NULL，即未就绪时，不做任何操作 */
    if (current == 0)	return;
	puts("[PID = ");
	puti(current->pid);
	puts("] Context Calculation: counter = ");
	puti(current->counter);
	puts("\n");

	current->counter--;
    /* 如果当前进程时间片不大于 0，即已运行完，进行调度 */
	if (current->counter <= 0)	schedule();
}

/* PRIORITY */
void do_timer(void)
{
    /* 如果 current 为 NULL，即未就绪时，不做任何操作 */
    if (current == 0)	return;
    /* 每次都调度 */
	schedule();
	current->counter--;
    /* 如果当前进程时间片不大于 0，即已运行完，重启该进程 */
	if (current->counter <= 0)
		current->counter = PRIORITY_INIT_COUNTER[current->pid];
}
```


#### 4.2.2.3 schedule()
```c
/* SJF */
void schedule(void)
{
	long min_counter = -1;
	int min_cnt_task = 0;
	for (int i = LAB_TEST_NUM; i > 0; i--)
	{
        /* 如果没有这个进程，跳过之 */
		if (task[i] == 0) continue;
        /* 找到剩余时间不为 0 且最小的 running 进程 */
		if (task[i]->state == TASK_RUNNING && task[i]->counter > 0
			&& (task[i]->counter < min_counter || min_counter == -1))
		{
			min_counter = task[i]->counter;
			min_cnt_task = i;
		}
	}
	/* 如果所有进程剩余时间都为 0，重新分配时间片 */
	if (min_counter == -1)
	{
		for (int i = 1; i <= LAB_TEST_NUM; i++)
		{
			if (task[i] != 0)
			{
				task[i]->counter = rand();
				puts("[PID = ");
				puti(i);
				puts("] Reset counter = ");
				puti(task[i]->counter);
				puts("\n");
			}
		}
		schedule();
	}
	else switch_to(task[min_cnt_task]);
}

/* PRIORITY */
void schedule(void)
{
	long max_priority = -1;
	int max_pri_task = 0;
	for (int i = LAB_TEST_NUM; i > 0; i--)
	{
        /* 如果没有这个进程，跳过之 */
		if (task[i] == 0) continue;
        /* 查找优先级最高的 running 进程 */
		if (task[i]->state == TASK_RUNNING && task[i]->counter > 0)
		{
			if (task[i]->priority < max_priority || max_priority == -1)
			{
				max_priority = task[i]->priority;
				max_pri_task = i;
			}
            /* 如果有多个同为最高优先级的进程，标记这一情况 */
			else if (task[i]->priority == max_priority)
			{
				max_pri_task = -1;
			}
		}
	}
	/* 如果有多个同为最高优先级的进程，寻找优先级最高且剩余时间最短的进程 */
	if (max_pri_task == -1)
	{
		long min_counter = -1;
		int min_cnt_task = 0;
		for (int i = LAB_TEST_NUM; i > 0; i--)
		{
			if (task[i] == 0 || task[i]->priority != max_priority) continue;
			if (task[i]->state == TASK_RUNNING && task[i]->counter > 0
				&& (task[i]->counter <= min_counter || min_counter == -1))
			{
				min_counter = task[i]->counter;
				min_cnt_task = i;
			}
		}
		switch_to(task[min_cnt_task]);
	}
	else switch_to(task[max_pri_task]);

	/* 随机更新优先级 */
	puts("tasks' priority changed\n");
	for (int i = 1; i <= LAB_TEST_NUM; i++)
	{
		if (task[i] != 0)
		{
			task[i]->priority = rand();
			puts("[PID = ");
			puti(task[i]->pid);
			puts("] counter = ");
			puti(task[i]->counter);
			puts(" priority = ");
			puti(task[i]->priority);
			puts("\n");
		}
	}
}
```


#### 4.2.2.4 switch_to(next)
```c
void switch_to(struct task_struct* next)
{
    /* 如果不需要切换，直接返回即可 */
	if (next == current)
		return;

	//输出信息
	puts("[!] Switch from task ");
	puti(current->pid);
	puts(" to task ");
	puti(next->pid);
	puts(", prio: ");
	puti(next->priority);
	puts(", counter: ");
	puti(next->counter);
	puts("\n");

	struct task_struct *current_temp = current;
	current = next;
	//保存当前进程的寄存器, 并载入下一个进程的寄存器
	save_load(current_temp, next);
}
```


#### 4.2.2.5 init_epc()
```c
init_epc:
	ld t0, dead_loop
	csrw sepc, t0
	ecall
	sret
```


#### 4.2.2.6 save_load(current, next)
```c
#a0是第一个参数, a1是第二个参数
save_load :
    #保存当前进程的寄存器
    addi a0, a0, 0x28
    sd ra, 0(a0)
    sd sp, 8(a0)
    sd s0, 16(a0)
    sd s1, 24(a0)
    sd s2, 32(a0)
    sd s3, 40(a0)
    sd s4, 48(a0)
    sd s5, 56(a0)
    sd s6, 64(a0)
    sd s7, 72(a0)
    sd s8, 80(a0)
    sd s9, 88(a0)
    sd s10, 96(a0)
    sd s11, 104(a0)
    #将下一个进程的状态载入到寄存器中
    addi a1, a1, 0x28       #next->thread
    ld ra, 0(a1)    #next->thread.ra
    ld sp, 8(a1)
    ld s0, 16(a1)
    ld s1, 24(a1)
    ld s2, 32(a1)
    ld s3, 40(a1)
    ld s4, 48(a1)
    ld s5, 56(a1)
    ld s6, 64(a1)
    ld s7, 72(a1)
    ld s8, 80(a1)
    ld s9, 88(a1)
    ld s10, 96(a1)
    ld s11, 104(a1)
ret
```

## 4.3 一些问题及其解决

- 当switch_to函数返回的时候，ra指向的地址不正确，导致返回到一个非法的地址，于是出错。经过调试，发现我在读取结构和存储结构的时候偏移地址弄错了，结果出现了一系列奇怪的问题。

![image.png](./assets/1605419519941-8f89aba0-43c7-4eae-bc09-0d229696b1ad.png)
出现这个bug的原因是我没有好好理解实验要求，按照要求，task的priority不同的情况下要选则高优先级的，不管另外一个task的时间片还剩多少，但是我这个判断还要比较两个task剩余的时间片，因此出现了问题。
![image.png](./assets/1605419525509-1ad5df33-97f6-440d-8717-3aeaef50a006.png)

- 在改变 lab3/Makefile 文件以后，我们不能直接通过 `make` 来使其重新编译，因为 Makefile 自身并不是 make 的依赖文件，因此需要 `make clean` 后重新编译。修改 .h 文件后也需要 `make clean` 然后重新编译运行。

## 4.4 拓展
我们在 _sched.h_ 中把 `LAB_TEST_NUM` 更改为 63 ， `make clean` 后重新编译运行，在两种调度方式下都得到了正确的结果（我们将代码做了更改，保证对更多进程进行测试时只需要修改 _sched.h_ 中的 `LAB_TEST_NUM` 即可）：

### 4.4.1 SJF 模式
![image.png](./assets/1605285215760-445e02ed-b9d5-4036-94e9-645700261d93.png)
![image.png](./assets/1605285257221-3f17d02c-1daa-437b-b6e7-8c8d1644ebaf.png)

### 4.4.2 PRIORITY 模式
![image.png](./assets/1605284883689-2c25fa60-7382-42e2-8e9b-2b19c20c7bcf.png)
![image.png](./assets/1605284925848-178ab903-4766-4b0a-aed8-97874271d664.png)

# 5 心得体会
本次 lab 的难点之一在于理清调度的流程，其中需要重点关注 epc\ra\sp 在各个阶段的值，理解每一次ret\sret\mret 后回到的地址。还有一点，debug 也挺难的，主要是在 gef 里面，代码都变成反汇编了，呈现的和我们的 C 有较大的差别，很费脑子。
