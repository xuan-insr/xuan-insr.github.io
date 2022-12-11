
# 4 实验过程

## 4.1 环境搭建

### 4.1.1 建立映射（略）

### 4.1.2 组织文件结构
![image.png](./assets/1608259008738-47554f7b-4083-44fe-887e-5ec89d18221b.png)
编译前后的文件结构

## 4.2 代码及详细注解

### 4.2.1 创建映射
页表映射函数 `void create_mapping(uint64_t *pgtbl, uint64_t va, uint64_t pa, uint64_t sz, int perm)` 代码如下：
```c
void create_mapping(uint64_t *pgtbl, uint64_t va, uint64_t pa, uint64_t sz, int perm)
{
    int index1, index2, index3;
    static int flag = 0;
    static uint64_t *putbl;
    uint64_t *pmtbl;
    
    index1 = (va & 0x7FC0000000) >> 30;
    pgtbl[index1] = ((uint64_t)(putbl) >> 12 << 10) + 1;

    while (sz > 0)
    {
        if ((flag & 0x1ff) == 0)
        {
            if ((flag & 0xfff) == 0)
            {
                cur += 0x1000;
                putbl = (uint64_t *)cur;
                pgtbl[index1] = ((uint64_t)(putbl) >> 12 << 10) + 1;
            }
            index2 = (va & 0x3FE00000) >> 21;
            cur += 0x1000;
            pmtbl = (uint64_t *)cur;
            putbl[index2] = ((uint64_t)(pmtbl) >> 12 << 10) + 1;
        }
        
        index3 = (va & 0x1FF000) >> 12;
        pmtbl[index3] = (pa >> 12 << 10) + 1 + (perm << 1);
        pa += 0x1000;
        va += 0x1000;
        sz -= 0x1000;
        flag++;
    }
}
```
一些变量的解释：

- 参数 `pgtbl`  - page global table，一级页表的基地址； `va` - 映射的虚拟地址和物理地址的基地址； `sz` - 需要映射的大小； `perm` - 映射的读写权限。
- 全局变量 `cur`  - 当前最后一个页表的地址。在 `paging_init()`  中初始化为 `_end`  的值，即我们的页表放在 `_end` 之后。
- 静态变量 `flag`  - 当前已经分配的三级页表个数。如第 8 行，鉴于 MMU 由高地址和低地址计算得出的VPN[1] 和 VPN[2] 相同，为了区别两次映射，故一次 16MB 的映射用一张二级表。由于 16MB 需要 8 张三级页表，4096 个三级页表的 entry，即 4096 个 frame（8*512=4096），故而此处用 4096 做判断。
- 静态变量 `putbl` - page upper table，二级页表的基地址。如果没有新建二级页表，那么仍然保持上一次进入时的地址；否则为新分配的地址。
- 变量 `pmtbl` - page middle table，三级页表的基地址。
- 变量 `index1` , `index2` , `index3` - 在 1~3 级页表中的页号。

函数的核心是按页分配内存，根据 `va` 推算出各级页表的页号，并将对应的物理地址置入页表中的对应位置。通过 `+1`  来将对应项置为 valid，并用 `perm<<1` 设置各项的权限。<br />每当我们发现 `flag` 为页表大小的整倍数时，这说明我们已经用完了一个三级页表，那么我们会开辟一个新的三级页表。<br />第一次调用该函数时， `putbl` 和 `flag` 都为 0，因此虽然 `pgtbl[index1]`  被赋值为 1，但紧接着它会在 19 行被重新赋值。之后再次调用该函数时， `putbl` 会保持上一次的值，因此是正确的。

`paging_init()` 函数调用 `create_mapping()` 进行了分页的初始化：
```c
void paging_init()
{
	uint64_t *pgtbl = &_end;
	cur = (uint64_t)&_end;

	create_mapping(pgtbl, (uint64_t)&text_start + offset, (uint64_t)&text_start, (uint64_t)&rodata_start - (uint64_t)&text_start, 5);
	create_mapping(pgtbl, (uint64_t)&rodata_start + offset, (uint64_t)&rodata_start, (uint64_t)&data_start - (uint64_t)&rodata_start, 1);
	create_mapping(pgtbl, (uint64_t)&data_start + offset, (uint64_t)&data_start, 0x1000000 - ((uint64_t)&data_start - (uint64_t)&text_start), 3);
	
	create_mapping(pgtbl, (uint64_t)&text_start, (uint64_t)&text_start, (uint64_t)&rodata_start - (uint64_t)&text_start, 5);
	create_mapping(pgtbl, (uint64_t)&rodata_start, (uint64_t)&rodata_start, (uint64_t)&data_start - (uint64_t)&rodata_start, 1);
	create_mapping(pgtbl, (uint64_t)&data_start, (uint64_t)&data_start, 0x1000000 - ((uint64_t)&data_start - (uint64_t)&text_start), 3);

	create_mapping(pgtbl, 0x10000000, 0x10000000, 0x1000, 3); 
}
```
即我们的 page table 放在 _end 后面，对 Kernel 在低地址和高地址分别进行一次映射。我们将 UART 所在的页（0x10000000 开始的 0x1000）进行等值映射。<br />对不同的段，我们进行了不同的保护。X, W, R 三个保护位分别表示可执行、可写、可读，对 text 段映射时的 perm 为 5，即 101，表示 r-x；对 rodata 段映射的 perm 为 1，即 001，表示 r--；对 data 段映射时的 perm 为 3，即 011，表示 rw-。<br />对这些保护的验证，参见 4.5 小节。


### 4.2.2 修改 entry.S 和 head.S
增加的部分代码如下，其中已经包含了详细的注释：
```
	#通过检查scause，来判断为何种异常
    csrr t0,scause		#scause=0x8000000000000005
    srai t2, t0, 63          #算术右移63位
    bnez t2, is_int_S          #若非0，则跳往is_int_S

	#判断是不是Instruction Page Fault
    li t1, 12
    beq t0, t1, instruction_page_fault
    li t1, 13
    beq t0, t1, load_page_fault
    li t1, 15
    beq t0, t1, store_page_fault
    j other_trap_S	         #其他异常

	#判断是不是machine timer interrupt
	is_int_S:
    #测试样例
    ############测试store_page_fault
    #li t3, 1
    #la t4, rodata_start
    #addi t4, t4, 8
    #sd t3, (t4)
    #############测试instruction_page_fault
    #li t3, 1
    #la t4, data_start
    #jr t4

    andi t0, t0, 0x7ff	     #去掉最高位
    li t1, 5
    beq	t0, t1, time_interupt_S
    j other_trap_S

	time_interupt_S:
    #时钟中断委托,调用sched.c
    call do_timer
    j other_trap_S
  
  instruction_page_fault:
    #调用instruction page fault的处理函数
    call do_instruction_page_fault
    j sepc_4
    ecall 

  load_page_fault:
    #调用load page fault的处理函数
    call do_load_page_fault
    j sepc_4

  store_page_fault:
    #调用store page fault的处理函数
    call do_store_page_fault
    j sepc_4

  sepc_4:
    ld t0, 0(sp)	
    addi t0, t0, 4  #sepc+4
    csrw sepc, t0	#恢复sepc
    j s_exit

  other_trap_S:
    ecall
```
```
  init_epc:
    la t0, dead_loop
    csrw sepc, t0
    ecall
    #对sstatus的spp位 强行赋值为1
    li t1, 0x100              
    csrs sstatus, t1
    sret
```
```
#设置mscratch
	la t1, stack_top
	csrw mscratch, t1
```
```
#设置时钟中断委托
	li t1, 0x20              #10 0000     mideleg的第5位置1
	csrs mideleg, t1

	#设置instruction/load/store page fault委托
	li t1, 0xB
	slli t1, t1, 12				#t1=1011 0000 0000 0000
	csrs medeleg, t1

	li t1, 0x12a             #0001 0010 1010   初始化mstatus（spp，spie，mie，sie）
```
```
_supervisor:
	#设置satp寄存器为0，关闭MMU
	li t1, 0
	csrw satp, t1

	#设置S异常处理地址
	la t4, _strap
	li t2, 0x80000000
	li t3, 0xffffffe000000000
	sub t3, t3, t2
	add t4, t4, t3          
	mv s1, t4
	la t5, init_stack_top         #sp=init_stack_top的地址（设置高地址空间的栈环境）
	add t5, t5, t3
	mv s2, t5

	la t6, start_kernel           #s3=main.c中的start_kernel函数的虚拟地址
	add t6, t6, t3
	mv s3, t6

	la t2, stack_top              #sp=stack_top的地址（设置低地址空间的栈环境）
	mv sp, t2
	
	call paging_init

	#设置satp
	li t1, 0x8000000000000000
	la t0, _end
	srli t0, t0, 12
	add t1, t1, t0
	csrw satp, t1

	csrw stvec, s1  
	mv sp, s2
	jr s3                        #跳转到main.c中的start_kernel函数
	                         
_mtrap:
	#交换mscratch和sp
	csrrw sp,mscratch,sp
```


### 4.2.3 修改 sched.c
我们将 task 的地址改为了虚拟地址：
```c
	current = task[0] = (struct task_struct *)(cur + offset + 0x1000);
	for (int i = 1; i <= LAB_TEST_NUM; i++)
	{
		task[i] = (struct task_struct *)((unsigned long long)task[i - 1] + 0x1000);
	}
```
page table 放在 _end 后面，几个 struct 依次放在 page table 的后面。

另外更改了输出信息：
```c
	puts("[!] Switch from task ");
	puti(current->pid);
	puts(" [task struct: ");
	putullHex((unsigned long long)current);
	puts(", sp: ");
	putullHex(current->thread.sp);
	puts("] to task ");
	puti(next->pid);
	puts(" [task struct: ");
	putullHex((unsigned long long)next);
	puts(", sp: ");
	putullHex(next->thread.sp);
	puts("], prio: ");
	puti(next->priority);
	puts(", counter: ");
	puti(next->counter);
	puts("\n");
```
其中， `putullHex()` 是一个定义在 `put.c` 中的函数：
```c
void putullHex(unsigned long long x)
{
    puts("0x");
    unsigned long long digit = 1, tmp = x;
    while (tmp >= 16)
    {
        digit *= 16;
        tmp /= 16;
    }
    while (digit >= 1)
    {
        *UART16550A_DR = (unsigned char)itoch(x/digit);
        x %= digit;
        digit /= 16;
    }
    return;
}
```


### 4.2.4 对不同 section 的保护
通过修改调用 `create_mapping` 时的 `perm` 参数，修改对不同 section 所在页属性的设置，完成对不同 section 的保护。我们已经在 4.2.1 中完成。<br />在 head.S 中，通过修改 `medeleg` 寄存器，将 instruction/load/store page fault 托管到 S 模式下：
```
	#设置instruction/load/store page fault委托
	li t1, 0xB
	slli t1, t1, 12				#t1=1011 0000 0000 0000
	csrs medeleg, t1

	li t1, 0x12a          #0001 0010 1010   初始化mstatus（spp，spie，mie，sie）     
	csrs mstatus, t1
```
我们在 strap.c 中增加了 page fault 的相关 handler：
```c
void do_instruction_page_fault(void)
{
	puts("do_instruction_page_fault\n");
}

void do_load_page_fault(void)
{
	puts("do_load_page_fault\n");
}

void do_store_page_fault(void)
{
	puts("do_store_page_fault\n");
}
```


## 4.3 编译及测试
我们在 SJF 和 PRIORITY 模式下测试均得到预期结果：
![image.png](./assets/1608465902579-626a084d-468f-4f5a-9fb4-fbac6f2b8dba.png)
![image.png](./assets/1608471105748-fcd6bf8f-041e-4c86-9f6a-0f5f1b76e6d4.png)
我们发现输出中同一进程的 sp 会有变化，进行单步调试和分析后我们得出以下结果：由于在切换进程的时候，需要保存寄存器，故而此时 sp-256；后进入 do_timer 函数，函数需要用到栈， sp-16；后进入 schedule 函数，也用到栈，sp-64。然后进入上下文切换保存寄存器的代码，将此时的 sp 保存在 struct->tread.sp 中。因此在输出 struct->tread.sp 的值时，会与初始值有 336 的偏差。


## 4.4 一些问题及解决

- 在检验时钟中断中嵌套异常的情况时，没有考虑到spp位会在异常sret的时候清零，而导致时钟中断sret返回到user mode，而触发instruction page fault。故而一开始在跑的时候，可以输出store page fault，但不会回到触发异常的下一行指令，反而会不断的输出instruction page fault。

![image.png](./assets/1608466510943-e5401230-c499-4946-9205-69e8e4caebef.png)

- 我们组事先保存了高地址处的栈地址和start_kernel的高地址，然后才去调用的map。但由于一开始用t0和t1保存地址，从而使得在调用map之后，t0和t1的值发生了变化（t1和t0寄存器为被调用者保存）。

- 我们尝试运行 64 个进程时出现了 load page fault：

![image.png](./assets/1608471166074-f9f14e71-29df-4df7-ba0c-28097249ce84.png)
在 4 个进程的模式下进行检查，发现进程地址异常大：
![image.png](./assets/1608471207605-ca1459fc-9cc6-42a6-acaf-02156e951301.png)
后来我们发现，是因为我们在给进程分配地址时，不能用 `task[i] = task[i-1] + 0x1000` 使得当前进程的地址为上一地址的进程 +0x1000，因为这样实际上增加的是 0x1000 个 task_struct 的大小。应该写成 `task[i] = (struct task_struct *)((unsigned long long)task[i - 1] + 0x1000);` 。


## 4.5 思考题

- 如下图所示，可以在代码中人为加入对rodata段的写操作和对data段的执行操作

![image.png](./assets/1608465690366-9dc14494-696d-4aea-9118-3b8eeb52e47c.png)

- 若rodata段成功被保护（属性为可读），则会跳出store page fault的错误信息；

![image.png](./assets/1608465755118-c90947ce-8e61-445d-a148-c49da7fdaac6.png)

- 若data段成功被保护（属性为可读可写），则会跳出instruction page fault的错误信息；

![image.png](./assets/1608465777972-d8ad7d6f-f90f-4d31-bb8b-f78d1b8bd2d1.png)
注：

- 由于所有段都可读，所以没法输出 load page fault。但 4.4 节中出现错误时触发过 load page fault。
- 对于instruction page fault的处理，我们简单处理为sepc+4，若执行的错误指令位于data段的起始处，则sepc+4依旧在data段中，从而导致instruction page fault持续不断的输出，直到sepc离开data段，进入可执行段。


## 4.6 拓展
如上次实验一样，在 _sched.h_ 中把 `LAB_TEST_NUM` 更改为 63 ， `make clean` 后重新编译运行，在两种调度方式下都得到了正确的结果：

### 4.6.1 PRIORITY
![image.png](./assets/1608470692333-e91014f5-4202-4236-9d37-e3d25596b12e.png)

### 4.6.2 SJF
![image.png](./assets/1608470914310-1a1daebf-df77-43c1-a37b-715959ad20c7.png)

# 5 心得体会
这次实验虽然延长到了三周，但是我们几乎直到最后一刻还在努力地 debug，从这里就可以看出实验的难度之大了。<br />虚拟内存的概念是整个操作系统里面最难的一部分之一，从理论上我就觉得这个很难了，当时花了一个晚上才弄明白要如何分配内存。虽然这个实验只要写 create_mapping 和 paging_init 两个函数，但是我依旧很难下手。最终，在我们的共同努力下，才完成这两个函数的编写。<br />这个实验的另外一个难点是修改 head.S，汇编部分代码的书写总是非常难的，因为这涉及到 riscv 更加底层的知识，尤其是对它寄存器的设置，我们在调试的时候多次被这个东西难倒。<br />最后，我们在这个实验中也有些收获，我们现在已经对分页的机制非常了解了，并且也学会了如何对物理页进行映射。此外，我们还学会了如何在调试的时候查看 C 语言的代码。
