# DIY a Git

!!! abstract
    通过造轮子来学习 git！

    本文是我 DIY git 过程中的笔记和梳理。我的代码托管在 [GitHub](https://github.com/smd1121/xuan-git)，我会尽可能保持一个干净的提交记录。

## 本文的结构和进展

- 0 写在前面：本文的动机、预期和基本介绍
- 1 构建框架：使用 typer 构建一个命令行工具
- 2 初始化仓库：实现 `init`，从而能够初始化一个仓库
- [WIP] 3 对象存储：介绍 git 的对象存储，实现 `hash-object` 和 `cat-file`，从而能够读取和写入 blob 对象、读取 tree 对象
- [WIP] 4 暂存区：介绍 git 的暂存区，实现 `ls-files` 和 `update-index`，从而能够读取和更新暂存区
- [TODO] 5 gitignore 与提交
- [TODO]
