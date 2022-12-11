
## 4.1 搭建实验环境

- 查看当前docker镜像

![image.png](./assets/1602657838699-dfed7197-eb7d-48a4-845d-fab3c63899af.png)

- 创建新的容器，同时建⽴ volumn 映射

![image.png](./assets/1602657878910-3e3a2fb3-6574-4659-985d-ceb99f25d72a.png)

   - `$ docker run -it -v `pwd`:/home/oslab/lab1 -u oslab -w /home/oslab 30bf /bin/bash`
      - `-v dir1:dir2` ：挂载宿主机的一个目录。其中 dir1 是宿主机内的目录，dir2 是容器内的目录。
      - ``pwd`` ：先完成引号里的命令行，然后将其结果替换出来。

- 测试是否成功

![image.png](./assets/1602672081117-67411b63-c900-4f39-8654-1639952262a9.png)

   - `touch testfile` ： `touch` 命令用于修改文件属性，但是也可以用来创建空文件。

## 4.2 编写 Makefile

### 4.2.1 代码及解释
```makefile
# makefile_lab1
export
CROSS_= riscv64-unknown-elf-
AR=${CROSS_}ar
GCC=${CROSS_}gcc
LD=${CROSS_}ld
OBJCOPY=${CROSS_}objcopy

ISA ?= rv64imafd
ABI ?= lp64

INCLUDE = -I ../include
CF =  -O3 -march=$(ISA) -mabi=$(ABI) -mcmodel=medany -ffunction-sections -fdata-sections -nostartfiles -nostdlib -nostdinc -static -lgcc -Wl,--nmagic -Wl,--gc-sections
CFLAG = ${CF} ${INCLUDE}

.PHONY: run debug clean
run:
	@make -C init -s
	@make -C arch/riscv -s
	@qemu-system-riscv64 -nographic -machine virt -kernel vmlinux


debug:
	@qemu-system-riscv64 -nographic -machine virt -kernel vmlinux -S -s

clean:
	@make clean -C init -s
	@make clean -C arch/riscv -s
```

- `#` ：# 表示注释，等价于 C 中的 `//` 。
- `export` ：当我们使用嵌套的 Makefile（即 17-18, 27-28 行）时，传递变量给下级 Makefile。
   - 一行中，使用 `export <variable...>` 表示将这些 variable 设置成要传递的。
   - 相反， `urexport <variable...>` 表示这些不要传递。
   - 一行中只写 `export` 表示把所有变量都传给下级（即第 2 行）。这个 export 写在哪里是没有关系的。
- 变量的定义和使用：如第 3 行是变量定义的一个例子。第 4 行等是变量的使用。Makefile 中 `$CROSS_` , `$(CROSS_)` , `${CROSS_}` 大概都没有关系，但是如第 4 行那样需要使用后面两种来与后面的 `ar` 分隔开。
   - 有说法称：makefile 中变量应该用 ()，但是 makefile 实际上就是在 shell 中运行的，而 shell 中用的是 {}，因此 {} 也可。当然，使用 shell 的变量时必须要用 {}，例如在命令中定义了变量的情况。
   - 几种赋值符号：
      - `=` 。左侧是变量，右侧是变量的值。右侧变量的值可以定义在文档中的任何一处，即可以使用后面定义的某个变量的值。
      - `:=` 。与 `=` 的区别是：不能使用没有定义过的变量的值。实际上，使用一个没有在它之前定义过的变量时它会展开为空。
      - `?=` 。如果没有定义过，则赋值；如果定义过，则什么都不做。
- 这里的 3~7 行指定了我们要使用的 ar, gcc, ld 和 objcopy。
   - ar 是库文件生成工具，这次暂时没有用到。其他的都用到了，在后面说明。
- gcc 的参数 `INCLUDE = -I ../include` ：表示把 ../include 作为找头文件的目录。用多个 `-I <dir>` 可以添加多个目录。
- `.PHONY: run debug clean` ：显式地说明 run, debug 和 clean 是伪目标。
   - 对于下面两个 Makefile 文件：
```makefile
# ---1---
clean:
	rm -f *.o
    
# ---2---
.PHONY: clean
clean:
	rm -f *.o
```
实际上，我们运行 make clean 的结果是一样的，也都没有生成 clean 文件。但是区别是：如果没有使用 .PHONY 文件夹中已经有名为 clean 的文件时，会出现：
![image.png](./assets/1602653555627-cef0aa00-1633-450e-8dc8-62f85f3c8c5c.png)
即，'clean' 已经是最新的。这与我们的期望不一致。因此标号最好使用 .PHONY 显式声明。

- `@make clean -C init -s` ：
   - `@` ，表示不要把这个语句打印出来。否则运行时这条语句会输出；
   - `make clean` ，表示运行对应 makefile 中 clean 标号下的内容；
   - `-C init` ，表示进到 init 路径中，运行那里的 makefile。如果没有就报错；
   - `-s` ，表示不要输出运行结果。

```makefile
# makefile_init
.PHONY: all clean
all: main.o test.o

main.o: main.c
	$(GCC) -c main.c $(CFLAG)
test.o: test.c
	$(GCC) -c test.c $(CFLAG)

clean:
	rm -f *.o
```

- `$(GCC) -c main.c $(CFLAG)` ：
   - `$(GCC)` ：展开后是 `riscv64-unknown-elf-gcc` 。编译器。
   - `-c` ：不生成可执行文件，只生成到中间文件 `.o` 。
   - `$(CFLAG)` ：展开后是各种参数。
- `rm -f *.o` ：删除后缀名为 `.o` 的全部文件。（正则表达式规则参见 [正则表达式 | 咸鱼暄](https://www.yuque.com/xianyuxuan/coding/regexp#js14X)）
   - `-f` 表示不询问，且没有找到的话不显示提示。

```makefile
# makefile_riscv
.PHONY: all clean
all:
	make -C kernel
	$(LD) -o ../../vmlinux ../../init/main.o ../../init/test.o kernel/head.o -T kernel/vmlinux.lds
	$(OBJCOPY) -O binary ../../vmlinux boot/Image --strip-all

clean:
	make clean -C kernel
	rm -f ../../vmlinux ../boot/Image
```

- `$(LD) -o ../../vmlinux ../../init/main.o ../../init/test.o kernel/head.o -T kernel/vmlinux.lds` ：
   - `$(LD)` ：链接器。
   - `-o ../../vmlinux` ：指定输出文件。
   - `../../init/main.o ../../init/test.o kernel/head.o` ：链接的文件。
   - `-T kernel/vmlinux.lds` ：不使用默认的链接脚本，而是使用 `kernel/vmlinux.lds` 作为链接脚本。
- `$(OBJCOPY) -O binary ../../vmlinux boot/Image --strip-all` ：
   - `$(OBJCOPY)` ：一个工具，拷贝一个文件的内容到另一个文件中。
   - `-O binary` ：指定输出格式为 binary。
   - `../../vmlinux boot/Image` ：分别是源文件和目标文件。
   - `--strip-all` ：丢弃调试信息和符号表等，不拷贝到目标文件中。
   - 这里是为了对 vmlinux 进行精简。
```makefile
# makefile_kernel
.PHONY: clean
head.o: head.S
	$(GCC) -c head.S $(CFLAG)

clean:
	rm -f *.o
```

- gcc 也可以编译 .S。


### 4.2.2 其他

#### 遇到的问题
![image.png](./assets/1602634611996-f6f81578-487f-4e78-8510-54fab4753443.png)
"missing separator"。在 Makefile 中，所有指令需要以 Tab 开头。这里在本文档中编辑后插入的 Tab 变为空格，因此出现了问题。将其改为 Tab 即解决。


#### 参考资料

      - [makefile 访问变量中大括号和小括号 | CSDN BBS](https://bbs.csdn.net/topics/340041002)
      - [Makefile中.PHONY的作用 | 博客园](https://www.cnblogs.com/idorax/p/9306528.html)


## 4.3 编写 head.S

### 4.3.1 代码及详细注释
```
.section .text
.globl _start
.globl _supervisor
.globl _mtrap
.globl _strap
.extern start_kernel
.extern stack_top
_start:
	li t1, 0x8               #t1=1000
	csrc mstatus, t1         #将mstatus寄存器的第三位置0（1的对应位清零）
	li t1, 0x888             #t1=1000 1000 1000
	csrc mie, t1             #将mie寄存器的第11、7、3位置0（1的对应位清零）

	la t1, _mtrap            #t1=_mtrap
	slli t1, t1, 2           #t1左移2位
	csrw mtvec, t1           #mtvec的第0、1位置0（所有异常均跳转到一个pc地址），高30位为pc地址

	
	li t1, 0x800             #t1=1000 0000 0000  supervisor mode = 01
	csrw mstatus, t1         #将mstatus的MPP域改为01

	la t1, _supervisor       #t1=_supervisor
	csrw mepc, t1            #将t1的值写入mepc（出现异常的返回地址，用mret必须要有的）
	mret                     

_supervisor:

	la t1, _strap             #t1=_strap
	slli t1, t1, 2            #t1左移2位
	csrw stvec, t1            #stvec的第0、1位置0（所有异常均跳转到一个pc地址），高30位为pc地址
	
	la sp, stack_top          #sp=stack_top的地址（设置栈环境）
	j start_kernel            #跳转到main.c中的start_kernel函数

_mtrap:


_strap:
	

```

### 4.3.2 其他

#### 遇到的问题
异常地址的设置问题：<br />在设置异常地址时，没有明确此时使用的地址均需为物理地址，不可使用虚拟地址这一知识点，导致一开始设置的地址太大，远超其物理地址的最大值，因此出错。


#### 发现的好用的东西
以树形结构显示文件目录结构。<br />`sudo apt-get install tree` 安装； `tree` 命令显示。 `tree -C` 可以让它带颜色表示类型。
![image.png](./assets/1602637944598-1008b297-8984-4df9-af22-8871cd76c452.png)

## 4.4 编译及测试
![image.png](./assets/1602657763377-8b26800a-8c91-41e6-a411-fedd561fb827.png)
实验结果符合预期。

