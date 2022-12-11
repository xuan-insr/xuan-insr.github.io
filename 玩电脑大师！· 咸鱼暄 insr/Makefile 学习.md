- 本文参考了 [跟我一起写 Makefile - 陈皓](https://seisman.github.io/how-to-write-makefile/overview.html)。

### Makefile 的基本知识

#### 程序的编译和链接
一般地，C 或 C++ 程序生成可执行文件需要经过编译和链接两步。

   - 编译时，编译器将你置顶的每个源代码生成一个中间目标文件（Object File。在 Windows 下是 .obj 文件，UNIX 下是 .o 文件）。
   - 链接时，链接器将你指定的中间目标文件生成一个可执行文件。有时，由于中间目标文件过多导致指定很不方便，我们将中间文件打包为库文件（在 Windows 下是 Library File, .lib；UNIX 下时 Archive File，.a)。
   - 如果一个函数只有声明没有定义，编译阶段不会发生错误。链接时，链接器在中间目标文件中找寻该函数的声明，如果仍未找到，则链接器报错。


#### Makefile 文件的基本结构
一个 makefile 文件主要由一些如下结构的东西组成：
```makefile
target ... : prerequisites ...
	command
    ...
```
其中，target 是需要生成的文件，或是一个标号。prerequisites 是 target 所依赖的的文件。command 是一系列 shell 命令，必须以 `Tab` 开头。

**make 指令**

   - 1 - 当我们输入一个指令 `make` ，它会查找当前目录下的名为 `Makefile` 或 `makefile` 的文件。如果没有找到，报错 `No targets specified and no makefile found` 并停止。
   - 2 - 如果找到， `make` 查找第一个 target，并将其作为最终目标。如果 **这个 target 文件不存在，或者它的prerequisites 文件比 target 新**，那么它就会执行后面的 command 来尝试生成这个 target；否则 `make` 指令直接结束。
   - 3 - 在上一步骤中，如果 prerequisites 中有的文件不存在，则 make 会在当前 makefile 文件中寻找以该文件为 target 的依赖性，并且如第 2 步骤所述尝试生成。
   - 4 - `make` 指令进行到最终目标（即第一个 target）后面的 command 执行完时结束。

   - 当我们输入一个指令 `make clean` ，其中 clean 是一个 target 的名称，那么它会查找当前目录下的名为 `Makefile` 或 `makefile` 的文件，找到其中的 clean，并将其作为最终目标，然后按照前述第 2 步骤那样开始尝试生成。

**什么是标号（伪目标）**。target 默认是一个文件。但有时我们希望 Makefile 执行一些功能而不必生成某个文件。这时我们就需要 **伪目标** 。伪目标类似汇编语言中的标号，伪目标也可以成为最终目标。我们可以用 `.PHONY: <target...>` 来显式地将 target 定义为伪目标。 

   - 注：这里代码中 `<target...>` 中的 <> 只是用来标明可填的内容，实际上不需要写 <>。后同。

对于下面两个 Makefile 文件：
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
