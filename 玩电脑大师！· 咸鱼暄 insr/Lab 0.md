
### 4.1 搭建 Docker 环境

#### 4.1.1 什么是 Docker
Lab 0 的指导 3.2 中说：
> Docker 是一种利用容器（container）来进行创建、部署和运行应用的工具。Docker 把一个应用程序运行需要的二进制文件、运行需要的库以及其他依赖文件打包为一个包（package），然后通过该包创建容器并运行，由此被打包的应用便成功运行在了 Docker 容器中。之所以要把应用程序打包，并以容器的方式运行，主要是因为在生产开发环境中，常常会遇到应用程序和系统环境变量以及一些依赖的库文件不匹配，导致应用无法正常运行的问题。Docker 带来的好处是只要我们将应用程序打包完成（组装成为 Docker imgae），在任意安装了 Docker 的机器上，都可以通过运行容器的方式来运行该应用程序，因而将依赖、环境变量等带来的应用部署问题解决了。
> Docker 和虚拟机功能上有共同点，但是和虚拟机不同，Docker 不需要创建整个操作系统，只需要将应用程序的二进制和有关的依赖文件打包，因而容器内的应用程序实际上使用的是容器外 Host 的操作系统内核。这种共享内核的方式使得 Docker 的移植和启动非常的迅速，同时由于不需要创建新的 OS，Docker 对于容器物理资源的管理也更加的灵活，Docker 用户可以根据需要动态的调整容器使用的计算资源（通过 cgroups）。

这里我们作一些简单的说明以便更好的理解。


##### 容器（Container）及其特点

   - **可移植**。一个容器包含了应用程序的代码或二进制文件，以及一套运行它所需要的完整的运行时环境。因此我们可以方便地将该应用程序移植到其他环境中而不需要在新环境中进行配置，只需要在新环境中运行这个容器即可。
   - **安全**。另外，容器之间是相互隔离的。因此我们可以在同一个机器中运行多个容器并且避免它们相互干扰。
   - **轻量级**。同时，虚拟机也可以实现上述两个需求。但如下图所示，每一个虚拟机都包含一套独立的操作系统，因此虚拟机的安装、启动都会比较慢。而容器则使用的是共同的操作系统内核，因此开始得快，并且使用更少的计算和内存。    

![image.png](./assets/1602140515353-7888b114-f5e0-40c4-b6aa-422443c48d3a.png)
(a)                                                                  (b)
图 0   容器 和 虚拟机[4]

##### Docker 与容器
我们在安装操作系统（Windows, Linux 等）时，都会用到 **镜像（images）**，我们利用这个镜像来在我们的计算机上安装操作系统。Docker 的思路类似。开发者将应用程序和运行环境打包为一个 **镜像**，用户在 Docker 中利用这个镜像创建一个 **容器**。容器之于镜像，就类似于面向对象程序设计中的对象之于类。

4.1.1 参考了：<br />[1] [Docker 教程 | 菜鸟教程](https://www.runoob.com/docker/docker-tutorial.html)
[2] [Linux 容器的解释 | Sohu](https://www.sohu.com/a/202921030_610730)
[3] [为什么需要 Docker | 知乎](https://zhuanlan.zhihu.com/p/54512286)
[4] [What is a Container | Docker](https://www.docker.com/resources/what-container#/virtual_machines)


#### 4.1.2 操作步骤
![image.png](./assets/1601428365520-8da6e30f-ae79-4780-b62c-f5335f1d77f6.png)
图 1 (a)    安装 Docker (a)

- `$ curl -fsSL [https://get.docker.com](https://get.docker.com) | bash -s docker --mirror Aliyun`
   - `curl` 是一个利用 URL 规则在命令行下工作的文件传输工具。参数：
      - `-f` , `--fail` 显示错误信息而非错误页面的 HTML（图 2 中 1，2 框）。
      - `-L` , `--location` 会跟随重定向。
      - `-s` , `--silent` 不显示统计信息（试了一下，好像只有管道处理运行结果的时候才有用）。
      - `-S` , `--show-error` 在 `-s` 的情况下显示错误输出。
      - 即，参数 `-fsSL` 的含义大概是：跟随重定向；正确时不显示输出，错误时只显示错误信息。
      - 这里 -sS 好像还是没有很搞清楚。因为尝试了 `curl -s [http://www.baidu.com](http://www.baidu.com)` 发现还是会有输出。

![image.png](./assets/1601611392413-2c4041df-ff62-43cd-9893-5fbc8978fd63.png)
图 2    -f 作用测试

   - `|` 是管道符。 `command 1 | command 2` 的作用是执行指令 1，然后将其正确输出作为指令 2 的操作对象 (The  standard  output  of command1 is connected via a pipe to the standard input of command2)。
   - `bash` , GNU Bourne-Again SHell 。启动了一个 bash 子进程。参数：
      - `-s` ，指定操作数从标准输入获得。这里就是获得 curl 的结果。

![image.png](./assets/1601428886206-7de2c2cf-a1ec-4bae-8b64-27563c701203.png)
图 1 (b)    安装 Docker (b)

- `$ sudo chmod a+rw /var/run/docker.sock`
   - `sudo` , Switch User DO 。以系统管理者的身份执行指令。
   - `chmod` , CHange MODe 。控制用户对文件的权限。参数：
      - `a` , all。指改变的是 **全部用户** 的权限。
      - `+` 。指下面是为指定的用户 **增加** 权限。
      - `rw` , read & write。改变的是 **可读** 和 **可写** 权限。
   - `/var/run/docker.sock`。指这里调整的是对这个文件的权限。
- `$ cat oslab.tar | docker import - oslab:2020`
   - `cat` , concatenate。连接文件并打印到标准输出设备上。
   - `docker import` 。创建镜像。参数：
      - `-` 。指从标准输入中创建镜像。这里就是从 `cat oslab.tar` 的输出结果通过管道建立。
      - `oslab:2020` 。指创建的镜像（image）的仓库源为 oslab，标签为 2020。
- `$ docker image ls`
   - 列出本地主机上的镜像。

![image.png](./assets/1601627831807-6cc1bbb0-871c-4a59-81ad-c7f92eafe6a6.png)
图 3    Docker 创建容器

- `$ docker run -it oslab:2020 /bin/bash`
   - `docker run` 。从镜像创建一个新容器并运行一个命令。参数：
      - `-i` 。以交互模式运行容器。
      - `-t` 。为容器重新分配一个伪输入终端。
      - `oslab:2020` 。镜像。
      - `/bin/bash` ，运行的命令。是因为 docker 后台必须运行一个进程，否则容器就会退出，在这里表示启动容器后启动 bash。
- `$ docker ps` 和 `$ docker ps -a` ：显示当前/所有容器。
- `$ docker start 0fb5` ：启动 ID 前四位为 0fb5 的容器。
- `$ docker exec -it -u oslab -w /home/oslab 0f /bin/bash`
   - `docker exec` 。在已经运行的容器中执行命令。参数：
      - `-it` 。同前。
      - `-u oslab` , `--user oslab` 。设置用户名为 oslab。
      - `-w /home/oslab` , `--workdir /home/oslab` 。不进入容器的默认工作目录，而是进入 /home/oslab。
      - `0f` 。容器 ID 前两位。
      - `/bin/bash` 。同前。


### 4.2 编译 Linux 内核
![image.png](./assets/1601650380023-2323cff7-ba8d-4dc4-9c29-f409fcedba99.png)
图 4    配置环境变量和编译 Linux 内核

- `# export TOP='pwd'` 
   - `export [var]=[value]` 。设置环境变量 `var` 值为 `value` 。
      - 环境变量在子进程中仍然有效，而其他变量则无法延伸到子进程中。为了在任何地方运行某个程序，我们将其路径加入环境变量 PATH 中即可。如图，我们用 `echo` 验证了 `/opt/riscv/bin` 已经加入了 PATH。
      - 注意：每次重新进入时都需要重新配置 PATH。可直接使用 `export PATH=$PATH:/opt/riscv/bin`来配置。

- `make -C linux O=$TOP/build/linux CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv CONFIG_DEBUG_INFO=y defconfig all -j$(nproc)  `
   - `make` 的作用是根据给出文件的内容进行构建。参数：
      - `-C DIR` 。在读取 Makefile 之前，进入到目录 DIR，然后执行 make。
      - `O=DIR` 。规定输出路径为 DIR。
      - `CROSS_COMPILE=` 。规定使用的交叉编译器的前缀。
         - 交叉编译器就是在一种计算机环境中运行的，编译出在另外一种环境下运行的代码的编译程序。
      - `ARCH=` 。选择编译的是哪一种 CPU architecture。


### 4.3 使用 QEMU 运行内核
![image.png](./assets/1601644753479-14d3d1bb-4a73-4141-8908-1cbe6f737071.png)
图 5    运行 qemu

- `qemu-system-riscv64 -nographic -machine virt -kernel linux/arch/riscv/boot/Image -device virtio-blk-device,drive=hd0 -append "root=/dev/vda ro console=ttyS0" -bios default -drive file=rootfs.ext4,format=raw,id=hd0 -netdev user,id=net0 -device virtio-net-device,netdev=net0` 
- 退出： `Ctrl+A` ; then `X` 。


### 4.4 使用 GDB 对内核进行调试
![image.png](./assets/1602230600804-7035c12e-ccfd-4fb9-b480-cbcb24cc6408.png)
图 6(a)    使用 gdb 调试

- `qemu-system-riscv64 -nographic -machine virt -kernel linux/arch/riscv/boot/Image -device virtio-blk-device,drive=hd0 -append "root=/dev/vda ro console=ttyS0" -bios default -drive file=rootfs.ext4,format=raw,id=hd0 -netdev user,id=net0 -device virtio-net-device,netdev=net0 -S -s`
   - `-S` 表示在开始的时候冻结 CPU 直至远程 gdb 输入相关指令
   - `-s` 即 `-gdb tcp::1234` ，表示启动 gdbserver 并在 tcp::1234 端口监听。
- `riscv64-unknown-linux-gnu-gdb linux/vmlinux` 运行 gdb。

![image.png](./assets/1602231055244-64bca6a3-0fe6-40e2-aa8a-6013b38b4a9d.png)
图 6(b)    使用 gdb 调试

- `(gdb) target remote localhost:1234` 连接到 qemu。
- 通过 `(gdb) continue` 让 qemu 从暂停状态开始运行。当 qemu 终止，continue 结束，远程连接关闭。

![image.png](./assets/1602240648865-75c0c34f-0a4e-4c1a-b9cc-78a75ec9afab.png)
图 6(c)    使用 gdb 调试


### 4.5 遇到的问题与心得体会

- 一些命令或程序的参数很难搞清楚其具体含义和作用。进行搜索后，很多参数的解释都是帮助文本中的原文，但实际上这些原文和操作尝试并不足够试验出其作用，尤其是有时结果与预期不符，如 curl 的 `-sS` 。
- 一些工具的使用目前未见其意义。如，我通过查找资料理解了 Docker 的思路和用途，并写在了 4.1.1 小节；但是经过资料查找，并不是很能理解 QEMU 是什么，也很难了解 QEMU+GDB 的调试作用。搜索引擎获得的相关资料非常有限。
- 由于上述两个问题，我的每一个步骤都缺乏预期结果。在对各种命令及其参数的搜索、理解后，尝试进行运行时，有时结果与预期不符，更多时候由于一些参数意义没有能够搞清导致不清楚这个步骤会带来什么样的结果。这种情况在 4.3-4.4 尤为常见，比如在和同学交流后才发现原来的 4.4 由于参数不正确产生了错误的结果。

- 总体来说，Lab 0 的指导十分详尽，我也成功跟随 Lab 0 的步骤简单体验了 Docker、qemu 和 gdb。过程中最大的感触是：尽可能把每一个命令和它的参数搞清楚，这对相关指令直至整个系统的使用都具有一定意义。
