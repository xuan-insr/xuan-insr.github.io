
# 4 实验过程

## 4.1 环境搭建

### 4.1.1 建立映射
![image.png](./assets/1603847056666-0b5c0604-8c20-4ec6-9b3f-40a0042ab76a.png)

### 4.1.2 组织文件结构
![image.png](./assets/1603847148948-45b99625-e794-41c9-941a-632e5d8a686a.png)
makefile 的修改在此略去。



## 4.2 代码及详细注释

### head.S
```
.align 3
.section .text.init
.globl _start
.globl _supervisor
.globl _mtrap
.globl clean_loop
.globl time_interupt
.globl encall_from_s
.globl exit
.globl is_int
.globl other_trap
.extern start_kernel
.extern stack_top
.extern _strap 
.extern bss_start
.extern bss_end
_start:
	#关闭所有中断
	li t1, 0x8               #t1=1000
	csrc mstatus, t1         #将mstatus寄存器的第三位置0（1的对应位清零）
	li t1, 0x888             #t1=1000 1000 1000
	csrc mie, t1             #将mie寄存器的第11、7、3位置0（1的对应位清零）


	#设置M异常地址
	la t1, _mtrap            #t1=&_mtrap
	csrw mtvec, t1           

	#初始化.bss
	la t1, bss_start         #t1=bss段start的地址
	la t2, bss_end           #t2=bss段end的地址
	li t3, 0x0               #填入的内容

clean_loop:
	sb t3, 0(t1)             #往t1的内存中写入t3的内容（每次1个字节）
	addi t1, t1, 1           #t1的值往后1个字节
	bne t1, t2, clean_loop   #比较，如果t1和t2的值不等，则继续往内存中存t3的内容

	#初始化mtimecmp寄存器
	li t1, 0x200bff8         #t1=mtime的地址
	li t2, 0x2004000         #t2=mtimecmp的地址
	ld t4, 0(t1)             #读mtime的8字节的内容到t4中
	li t3, 1000000
	add t4, t4, t3           #t4加上1000000
	sd t4, 0(t2)             #将a0的值存入地址为t2的内存中（8字节）

	#设置时钟中断委托(mstatus和sstatus  mie和sie应该是子集的关系，所以放一起写了)
	li t1, 0x20              #10 0000     mideleg的第5位置1
	csrs mideleg, t1
	li t1, 0xa               #1010        mstatus的第3、1位置1 mie && sie
	csrs mstatus, t1
	li t1, 0x0a0             #1010 0000   mie的第7、5位置1   mtie && stie
	csrs mie, t1

	#切换模式
	li t1, 0x800             #t1=1000 0000 0000  supervisor mode = 01
	csrs mstatus, t1         #将mstatus第11位置1
	li t1, 0x1000            #t1=0001 0000 0000 
	csrc mstatus, t1         #将mstatus第12位清0

	#切换模式
	la t1, _supervisor       #t1=_supervisor
	csrw mepc, t1            #将t1的值写入mepc（出现异常的返回地址，用mret必须要有的）
	mret                     

_supervisor:
	#设置S异常处理地址
	la t1, _strap            #t1=&_strap
	csrw stvec, t1            
	
	la sp, stack_top         #sp=stack_top的地址（设置栈环境）
	j start_kernel           #跳转到main.c中的start_kernel函数
	                         
_mtrap:
	#保存寄存器
	sd sp, -8(sp)
	sd ra, -16(sp)
	sd gp, -24(sp)
	sd tp, -32(sp)
	sd t0, -40(sp)
	sd t1, -48(sp)
	sd t2, -56(sp)
	sd s0, -64(sp)
	sd s1, -72(sp)
	sd a0, -80(sp)
	sd a1, -88(sp)
	sd a2, -96(sp)
	sd a3, -104(sp)
	sd a4, -112(sp)
	sd a5, -120(sp)
	sd a6, -128(sp)
	sd a7, -136(sp)
	sd s2, -144(sp)
	sd s3, -152(sp)
	sd s4, -160(sp)
	sd s5, -168(sp)
	sd s6, -176(sp)
	sd s7, -184(sp)
	sd s8, -192(sp)
	sd s9, -200(sp)
	sd s10, -208(sp)
	sd s11, -216(sp)
	sd t3, -224(sp)
	sd t4, -232(sp)
	sd t5, -240(sp)
	sd t6, -248(sp)
	csrr t0, mstatus
	csrr t1, mepc
	sd t0, -256(sp)        	 		#保存mstatus
	sd t1, -264(sp)	         		#保存mepc
	addi sp, sp, -264

	#通过检查mcause，来判断为何种异常
	csrr t0,mcause
	srai t2, t0, 63          		#算术右移63位
	bnez t2, is_int          		#若非0，则跳往is_int

	#判断是不是environment call from S-mode
	li t1, 9	           
	beq t0, t1, encall_from_s
	j other_trap	         		#其他异常

	#判断是不是machine timer interrupt
is_int:
	andi t0, t0, 0x7ff	     		#去掉最高位
	li t1, 7    
	beq	t0, t1, time_interupt
	j other_trap


time_interupt:
	#禁用时钟中断
	li t1, 0x80              		#1000 0000
	csrc mie, t1             		#对应位清0

	#设置stip为1
	li t1, 0x20              		#10 0000
	csrs mip, t1           

	#恢复寄存器mepc和mstatus
	ld t0, 0(sp)
	ld t1, 8(sp)
  	csrw mepc, t0 	         		#恢复寄存器mepc
  	csrw mstatus, t1 	    	 	#恢复寄存器mstatus
	j exit

encall_from_s:
	#mtimecmp+=fff000
	li t1, 0x2004000         		#t1=mtimecmp的地址
	ld t0, 0(t1)             		#读mtime的8字节的内容到t0中
	li t3, 0xfff000
	add t0, t0, t3           		#a0加上fff000
	sd t0, 0(t1)             		#将t0的值存入地址为t1的内存中（8字节）

	#清stip
	li t1, 0x20              		#10 0000
	csrc mip, t1

	#使能时钟中断
	li t1, 0x80              		#1000 0000
	csrs mie, t1             		#对应位置1

	#恢复寄存器mepc和mstatus
	ld t0, 0(sp)
	addi t0, t0, 4           		#mepc+4
	ld t1, 8(sp)
  	csrw mepc, t0 	         		#恢复寄存器mepc
  	csrw mstatus, t1 	     		#恢复寄存器mstatus
	j exit

other_trap:
	#恢复寄存器mepc和mstatus
	ld t0, 0(sp)
	ld t1, 8(sp)
  	csrw mepc, t0 	         		#恢复寄存器mepc
  	csrw mstatus, t1 	     		#恢复寄存器mstatus

exit:
	#恢复寄存器
    ld t6, 16(sp)
    ld t5, 24(sp)
    ld t4, 32(sp)
    ld t3, 40(sp)
    ld s11, 48(sp)
    ld s10, 56(sp)
    ld s9, 64(sp)
    ld s8, 72(sp)
    ld s7, 80(sp)
    ld s6, 88(sp)
    ld s5, 96(sp)
    ld s4, 104(sp)
    ld s3, 112(sp)
    ld s2, 120(sp)
    ld a7, 128(sp)
    ld a6, 136(sp)
    ld a5, 144(sp)
    ld a4, 152(sp)
    ld a3, 160(sp)
    ld a2, 168(sp)
    ld a1, 176(sp)
    ld a0, 184(sp)
    ld s1, 192(sp)
    ld s0, 200(sp)
    ld t2, 208(sp)
    ld t1, 216(sp)
    ld t0, 224(sp)
    ld tp, 232(sp)
    ld gp, 240(sp)
    ld ra, 248(sp)
	ld sp, 256(sp)
	mret
```

### entry.S
```
.align 3
.section .text.entry
.globl _strap
.globl s_exit
.extern strap_c
_strap:
	#保存寄存器
	sd sp, -8(sp)
	sd ra, -16(sp)
	sd gp, -24(sp)
	sd tp, -32(sp)
	sd t0, -40(sp)
	sd t1, -48(sp)
	sd t2, -56(sp)
	sd s0, -64(sp)
	sd s1, -72(sp)
	sd a0, -80(sp)
	sd a1, -88(sp)
	sd a2, -96(sp)
	sd a3, -104(sp)
	sd a4, -112(sp)
	sd a5, -120(sp)
	sd a6, -128(sp)
	sd a7, -136(sp)
	sd s2, -144(sp)
	sd s3, -152(sp)
	sd s4, -160(sp)
	sd s5, -168(sp)
	sd s6, -176(sp)
	sd s7, -184(sp)
	sd s8, -192(sp)
	sd s9, -200(sp)
	sd s10, -208(sp)
	sd s11, -216(sp)
	sd t3, -224(sp)
	sd t4, -232(sp)
	sd t5, -240(sp)
	sd t6, -248(sp)
	addi sp, sp, -248

	#调用C函数
	call strap_c  

	ecall 

s_exit:
	#恢复寄存器
    ld t6, 0(sp)
    ld t5, 8(sp)
    ld t4, 16(sp)
    ld t3, 24(sp)
    ld s11, 32(sp)
    ld s10, 40(sp)
    ld s9, 48(sp)
    ld s8, 56(sp)
    ld s7, 64(sp)
    ld s6, 72(sp)
    ld s5, 80(sp)
    ld s4, 88(sp)
    ld s3, 96(sp)
    ld s2, 104(sp)
    ld a7, 112(sp)
    ld a6, 120(sp)
    ld a5, 128(sp)
    ld a4, 136(sp)
    ld a3, 144(sp)
    ld a2, 152(sp)
    ld a1, 160(sp)
    ld a0, 168(sp)
    ld s1, 176(sp)
    ld s0, 184(sp)
    ld t2, 192(sp)
    ld t1, 200(sp)
    ld t0, 208(sp)
    ld tp, 216(sp)
    ld gp, 224(sp)
    ld ra, 232(sp)
	ld sp, 240(sp)
	sret
```

### strap.c
```c
#include<put.h>
static int count = 0; 

int strap_c(void)
{
	puts("[S] Supervisor Mode Timer Interrupt ");
	puti(count);
	puts("\n");
	count++;
	return 0;
}
```


## 4.3 实验结果
![image.png](./assets/1604113595112-873bfe3d-b9c8-4257-82fc-820b75871618.png)
如图所示，实验结果符合预期。


# 5 思考题
**1 观察vmlinux和image，解释为什么要初始化bss段。**<br />为了防止未初始化的全局变量有非0的值。

**2 当处理同步异常时应该在退出前给mepc+4，当处理中断时则不需要，请解释为什么要这样做。**<br />mepc保存异常的返回地址。对于中断来说，中断返回地址mepc的值被更新为下一条尚未执行的指令。而对于同步异常来说，中断返回地址mepc的值被更新为当前发生异常的指令pc。当有ecall产生的时候，由于mepc的值被更新为ecall指令本身的地址。因此，在异常返回时候，如果直接使用mepc保存的pc值作为返回地址，则会再次进入异常，形成死循环。所以我们需要执行mepc=mepc+4指令。


# 6 心得体会
好好看指导。由于未仔细的看指导，导致同步异常时mepc忘记加4，改bug改了很久；保证lab1正确很重要。由于我们组的lab1存在一些问题，直接导致lab2出错；debug需要耐心和细心。 <br />写代码的时候要充分理解riscv手册中的内容，对于每个寄存器的功能都要了解透，这次的lab因为我们没有掌握mtvec中base域的内容，导致对他进行了错误的操作，花了好久才找到错误的原因。在debug的时候也需要一定的技巧，不要上来就一顿continue，错过了原来想调试的位置，不过gef很好用也很酷炫，i了。
