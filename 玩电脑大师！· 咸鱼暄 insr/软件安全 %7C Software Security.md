
## NTU CS 2019 Pwn 学习记录
[https://github.com/yuawn/NTU-Computer-Security](https://github.com/yuawn/NTU-Computer-Security)


### 预备知识

#### ELF, Executable and Linkable Format
![image.png](./assets/1647682796332-4d728ad9-4994-491d-82ca-fec05c0f1ef0.png)
![image.png](./assets/1647682771436-230efa60-044b-434a-817a-08a75925e492.png)
使用 `gcc elf.c -o elf -no-pie` 编译

使用 `readelf -S ./elf` 查看它的 Section Headers：
![image.png](./assets/1647683107974-9314b5ff-76ca-45be-ac44-5055167db339.png)
Offset 就是这个 section 在 elf 中的位置，而 Address 则是这个 section 会被映射到的虚拟内存中的地址。如果编译的时候没有 -no-pie 选项，PIE (Position Independent Executable) 保护就会让这个地址每次都不一样。

![image.png](./assets/1647684813251-bfbdd69e-3767-4193-9aaf-1a7dd2ecd24a.png)
可以看到，当前虚拟内存中的 0x00401000~0x00402000 具有运行权限 x，应当保存有 .text 段的内容；而其它部分则没有 x 权限，这就是 NX 保护。

用 `readelf -St ./elf` 进一步查看细节，其中 `-t` 表示查看 section 的细节
![image.png](./assets/1647691306721-81b7e43c-d36e-4506-9426-032d498ba7d8.png)

