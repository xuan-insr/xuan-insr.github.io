# [WIP] 3 对象存储

!!! abstract
    从这一章开始，我们正式进入 git 的世界！这一章我们会了解到 git 的对象存储系统，并完成 blob 对象的存储和读取以及 tree 对象的读取。

    这章里，我们会实现 `hash-object` 和 `cat-file` 两个指令。

## 3.1 预备知识

### git 的对象存储系统

Git 会将很多信息存储在 git repository (也就是 `.git`) 中，包括所有文件在每次提交时的内容，以及提交历史、目录结构等等信息。而这些信息都是以对象的形式存储的，它们被存储在 `.git/object` 目录中。

Git 的核心部分就是这样的一个类似键值对的存储系统；但是与普通的键值对不同的是，这里的「键」是「值」的哈希值。这样的设计使得 Git 能够通过哈希值来索引对象，从而快速地找到对象。也就是说，我们可以向 Git repo 中插入任何一个对象，它会返回一个唯一的键；在任意时刻，我们都可以通过这个键来取回这个对象。这可以使得我们很容易检查内容是否在传输过程中出现偏差，也可以使得查找对象变得非常高效。

???+ tip "哈希"
    简单来说，哈希 (hash, 也译为散列、杂凑等) 是一个单向的函数：我们可以简单地计算出一个值的哈希值，但是我们不可能通过哈希值还原出原来的值。例如，我们可以创造一个非常简单的哈希算法：`H(x) = x % 10`，即取数据的最后一位；这样，`H(123) = 3`，`H(456) = 6`。但是，我们不可能通过 `3` 还原出 `123`，因为 `3` 可能对应 `3`，或者是 `13`，`23`，`113`, `111113` 等等。

    但是，这样的哈希函数有个问题：它的哈希值的范围是有限的，因此会存在多个值对应同一个哈希值的情况。例如，`H(123) = 3`，`H(113) = 3`，`H(213) = 3` 等等。这种情况被称为「哈希碰撞 (collision)」。但是，Git 通过 SHA-1 哈希算法来计算对象的哈希值。SHA-1 是一个不可逆的哈希算法，它能够将任意长度的数据转换为一个 160 位的哈希值。这个范围非常大，因此 [碰撞概率非常非常低](https://stackoverflow.com/questions/1867191/probability-of-sha1-collisions)，因此 Git 认为任何一个哈希值都是唯一的，即不可能存在两个不同的对象具有相同的哈希值。

    不过，事实上 [SHA-1 已经被证明不安全了](https://shattered.io/)，因此 Git 也已经 [在 v2.13.0 对哈希算法进行了升级](https://github.com/git/git/blob/26e47e261e969491ad4e3b6c298450c061749c9e/Documentation/technical/hash-function-transition.txtL34-L36)。但是，新版本的哈希算法对于所有除了上述发现的冲突外的已知输入都会产出与 SHA-1 相同的结果。所以我们仍然可以使用 SHA-1 来完成我们的任务。

### 对象如何存储、存储到哪里

`git hash-object` 指令完成计算一个对象的 SHA 的功能，并且可以将这个对象存储到 git repo 中。例如：

!!! tip inline end "`>`"
    `>` 是重定向符，它可以将一个命令的输出重定向到一个文件中。例如，`echo "a" > foo` 会将 `echo "a"` 的输出 `a` 写入到文件 `foo` 中。

<!-- termynal -->
```
% echo "SaltyFish Xuan" > me.txt
% git hash-object me.txt -w
ea2aabee9fc38b9a77792e731c0725ad6bc2df9f
% tree . -a
.
├── .git
│   ├── HEAD
│   ├── objects
│   │   └── ea
│   │       └── 2aabee9fc38b9a77792e731c0725ad6bc2df9f
│   └── refs
│       ├── heads
│       └── tags
└── me.txt

7 directories, 3 files
```

在这里，我们创建了一个文件 `me.txt`，并通过 `git hash-object me.txt -w` 将这个文件存储到了 git repo 中。这里的选项 `-w` 表示将这个对象（也就是这个文件的内容）写入到 git repo 中；如果不加这个选项，那么 `git hash-object` 只会计算并打印这个对象的 SHA，而不会将它写入到 git repo 中。

我们可以看到，这个对象的 SHA 是 `ea2aabee9fc38b9a77792e731c0725ad6bc2df9f`；如我们之前所说，SHA-1 生成的结果是 160 位的，这对应了一个 40 位的十六进制数，也就是这里显示的 SHA 值。

而在我们选择写入后，这个对象被写到了 `.git/objects` 中的 `ea/2aabee9fc38b9a77792e731c0725ad6bc2df9f`。也就是说，git 会将 SHA 的前两个字符作为目录名，后面的作为文件名，这样可以避免所有提交都写入到同一个目录中。都写到同一个目录的弊端是，git 有时需要通过不完整的 SHA 来查找对象，因此目录过大会影响效率。

`git hash-object` 还支持从标准输入中读取内容，例如：

!!! tip inline end "`|`"
    `|` 是管道符，它可以将一个命令的输出作为另一个命令的输入。例如，`echo "a" | foo` 会将 `echo "a"` 的输出 `a` 作为 `foo` 的输入。

<!-- termynal -->
```
% echo "SaltyFish Xuan" | git hash-object --stdin
ea2aabee9fc38b9a77792e731c0725ad6bc2df9f
```

我们可以看到，这种方式和前面使用文件的方式得到了相同的结果。这也从侧面告诉我们，git 存储这种内容时，只存储了它的内容，而没有存储文件名等信息。我们再用一个例子加以验证：

!!! tip inline end "`mv`"
    `mv` 可以将文件移动到指定的位置，也可以将文件重命名。

<!-- termynal -->
```
% mv me.txt me2 
% git hash-object me2
ea2aabee9fc38b9a77792e731c0725ad6bc2df9f
```

可以看到，重命名并没有改变这个对象的 SHA。那么，这个 SHA 是如何计算出来的呢？

### `git hash-object` 的实现细节

事实上，当我们用 `git hash-object` 时，git 会根据这个对象的类型和内容的大小作为「头部」放到内容之前，对这个组合进行哈希。

具体来说，一个对象以它的类型开始，即 blob, commit, tag 或 tree（我们会慢慢学习到这些）。类型后面是一个 ASCII 空格（0x20），然后是对象的大小（以字节为单位，用 ASCII 数字表示），然后是空字节 null（0x00），最后是对象的内容。即 `[type] 0x20 [size] 0x00 [content]`。

用 Python 代码表示就是：

```python
hdr = obj_type + b" " + str(len(content)).encode()
obj = hdr + b"\x00" + content
sha = hashlib.sha1(obj).hexdigest()
```

???+ tip "bytes"
    `#!python b" "` 的类型是 `bytes`，即一个字节串。字节串是已经编码过的内容，因而能被直接用来写入文件，或者用于网络交互。`sha1` 的参数就需要是一个 `bytes`。
    
    我们可以通过 `#!python s.encode()` 的方式来将一个字符串编码成 `bytes`；因此上面代码中 `hdr` 就是用空格隔开的对象类型和内容的长度。我们会稍后讨论对象的类型。

    `#!python b"\x00"` 表示一个值为 0 的字节，这和 C 语言中的 `\0` 是同一个东西。Git 使用这样一个空字节来分隔头部和内容。

    最后，我们通过 `hashlib` 库提供的 `sha1` 函数实现计算一个 `bytes` 的 SHA-1 值。我们使用 `#!python hexdigest()` 来得到一个十六进制的字符串，这和我们之前看到的 SHA-1 值是一样的。

而这里的「类型」又是什么呢？事实上，`git hash-object` 有一个选项 `-t` 用来指定对象的类型，它的默认值是 `blob`；也就是说，我们之前并没有指定 `-t`，因此我们之前的尝试中，对象的类型都是 `blob`。Blob (Binary Large OBject) 可以用来存储各种二进制数据，例如文件的内容。我们的标准输入或者文件会被编码成二进制，然后用于上述计算。

我们会稍后介绍其他的对象类型。

我们尝试使用上述逻辑来计算一下我们之前的例子，可以看到，我们算出的 SHA 值和 git 产生的是一致的：

<!-- termynal: {"prompt_literal_start": ["%", ">>>"], title: "", buttons: macos} -->
```
% python
>>> import hashlib
>>> content = "SaltyFish Xuan\n".encode()
>>> obj_type = b"blob"
>>> hdr = obj_type + b" " + str(len(content)).encode()
>>> obj = hdr + b"\x00" + content
>>> sha = hashlib.sha1(obj).hexdigest()
>>> obj
b'blob 15\x00SaltyFish Xuan\n'
>>> sha
'ea2aabee9fc38b9a77792e731c0725ad6bc2df9f'
```

在我们计算出来 SHA 之后，我们就知道这个对象 [会被存储到哪个文件中了](%E5%AF%B9%E8%B1%A1%E5%A6%82%E4%BD%95%E5%AD%98%E5%82%A8%E5%AD%98%E5%82%A8%E5%88%B0%E5%93%AA%E9%87%8C:~:text=git%20%E4%BC%9A%E5%B0%86%20SHA%20%E7%9A%84%E5%89%8D%E4%B8%A4%E4%B8%AA%E5%AD%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%E7%9B%AE%E5%BD%95%E5%90%8D%EF%BC%8C%E5%90%8E%E9%9D%A2%E7%9A%84%E4%BD%9C%E4%B8%BA%E6%96%87%E4%BB%B6%E5%90%8D%EF%BC%8C%E8%BF%99%E6%A0%B7%E5%8F%AF%E4%BB%A5%E9%81%BF%E5%85%8D%E6%89%80%E6%9C%89%E6%8F%90%E4%BA%A4%E9%83%BD%E5%86%99%E5%85%A5%E5%88%B0%E5%90%8C%E4%B8%80%E4%B8%AA%E7%9B%AE%E5%BD%95%E4%B8%AD)。那么，这个文件中保存了什么信息呢？

事实上，git 会将我们刚刚得到的 `obj` 经过压缩之后写入到文件中，即 `#!python file.write(zlib.compress(result))`。

我们可以对它进行解压来验证：

<!-- termynal -->
```
% zlib-flate -uncompress < .git/objects/ea/2aabee9fc38b9a77792e731c0725ad6bc2df9f
blob 15SaltyFish Xuan
```

### 读取文件

我们有了 `git hash-object` 用来存储对象，那么我们也应有命令来读取这个文件的内容。这个命令就是 `git cat-file`。我们来讨论它的一个简化版本。

`git cat-file` 接收两个参数：类型和 SHA。它会读取并解压 git repo 中的对象，删除头部，打印出它的内容。我们暂时可以只把类型当做一个额外的验证，即如果类型不匹配，git 就报错。

例如：

<!-- termynal -->
```
% git cat-file blob ea2aabee9fc38b9a77792e731c0725ad6bc2df9f
SaltyFish Xuan
```

### 树对象

刚刚我们提到，blob 对象包含了一个文件的内容，但是并不包含文件路径等信息。因此，仅仅是 blob 对象并不足以刻画和还原一个仓库的状态。

事实上，git 通过「树 (tree) 对象」来描述一个仓库的状态。树对象中包含了模式、类型、文件名等信息。不妨直接看个例子！

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% git cat-file -p main^{tree}  
100644 blob 567994ceb193ad3c00ebec195c7a702c2223826e    .gitignore
100644 blob efa312a9fe09c9d1995b9ef3ac4dd001baa04897    readme.md
040000 tree 4ac134baee324779055a2f920bd27f21b8a4ad3b    scripts
100644 blob 19bb2f232819b48dace673d19c62e61d284e17fc    setup.py
040000 tree fa87295799e0c8a99ed4df60b330a805deb6822a    xgit
```

这里 `-p` 表示 `--pretty`，即按照对象的类型，以人类可读的方式打印对象的内容。`main^{tree}` 表示 `main` 分支上最新提交所指向的树对象，我们会下一章才会详细介绍提交的具体逻辑。

这里的输出有 4 列，依次表示模式 (file mode)、类型、对象的 hash 值和名字。可以看到，这里有 3 个 blob 对象和另外 2 个 tree 对象。其中，`scripts` 和 `xgit` 是两个子目录，因此它们对应的对象类型是 `tree`，因为他们在文件系统的树状结构[^fs]中确实是子树；而 `readme.md` 和 `setup.py` 是两个文件，因此它们对应的对象类型是 `blob`。

[^fs]: 通常的文件系统在组织上是树状的，但事实上由于软链接和硬链接的存在，它实质上是一个有向无环图。如果您对这个话题感兴趣，可以参考我操作系统笔记中的 [目录结构 | 文件系统](../../核心知识/os/VI_file_system/13_fs_interface/#133-directory-structure--目录结构)。

对于 file mode，git 中主要有 5 种类型：

- 普通文件：`100644` 表示不可执行的普通文件，`100755` 表示可执行的普通文件；
- 符号链接：`120000` 表示符号链接 (symlink, symbolic link, a.k.a. soft link | 软连接)；
- 目录：`040000` 表示目录；
- gitlink：`160000` 表示 gitlink，即子模块 (submodule)。

???+ tip "符号链接"
    符号链接，也称为软连接，是一种特殊的文件类型。它的内容是一个路径，当我们访问这个文件时，系统会将我们重定向到这个路径所指向的文件。

    例如，我们可以使用 `ln -s a a_symlink` 来创建一个符号链接，它指向 `a` 这个文件：

    ```
    % echo "123" > a
    % ln -s a a_symlink
    % ls -lh
    total 4.0K
    -rw-rw-r-- 1 dev dev 4 Jan  2 14:19 a
    lrwxrwxrwx 1 dev dev 1 Jan  2 14:20 a_symlink -> a
    % cat a_symlink
    123
    % readlink a_symlink
    a
    ```

    用 `ls -l` 可以看到，`a_symlink` 的 permission string 是 `lrwxrwxrwx`，这里的第一个字符 `l` 表示这个文件是一个 symlink；在后面我们也可以看到它事实上是指向 `a_symlink -> a` 的。

    当我们 `cat a_symlink` 的时候，系统会将我们重定向到 `a` 这个文件，因此我们看到的是 `a` 的内容。当我们 `readlink a_symlink` 的时候，我们能看到 `a_symlink` 指向文件，这事实上也是 `a_symlink` 这个文件本身的内容。

    我们可以使用 `ln -s /tmp/xyx0102/a a_symlink_abs` 创建一个指向绝对路径的符号链接：

    ```
    % ls -lh
    total 4.0K
    -rw-rw-r-- 1 dev dev  4 Jan  2 14:19 a
    lrwxrwxrwx 1 dev dev  1 Jan  2 14:20 a_symlink -> a
    lrwxrwxrwx 1 dev dev 14 Jan  2 14:21 a_symlink_abs -> /tmp/xyx0102/a
    ```

    注意看第 5 列，`a_symlink` 的大小是 1B，而 `a_symlink_abs` 的大小是 14B，这和它们的内容（即指向的文件的路径这个字符串）的长度是一致的。

    指向相对路径和绝对路径的符号链接有什么区别呢？如果我们将当前目录移动到另一个位置，`a_symlink` 仍然能够指向 `a` 这个文件；但是 `a_symlink_abs` 就不行了，因为它指向的是 `/tmp/xyx0102/a`，而这个文件已经不存在了。类似地，如果我们不移动 `a`，而只移动两个符号链接，那么 `a_symlink_abs` 仍然能够指向 `a`，但是 `a_symlink` 就不行了。

    因此，如我们刚才所说的那样，符号链接仍然还是一个文件。所以 git 在处理它时，也会将它看作一个 blob 对象；其 SHA 值也是由它的内容决定的。

对于上面一个具体的树对象，它也可以通过类似地方式查看内容：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% git cat-file -p fa87295799e0c8a99ed4df60b330a805deb6822a
100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391    __init__.py
100644 blob f01ed6f00183801a41b97b94d34fa6a88f08b78f    cli.py
040000 tree ab23095a203b7d5427a34e6bd67e29cdd955a85d    commands
100644 blob ba652e6c821887b83988d12a5de03b85d0314976    constants.py
100644 blob 5203a0a1944c62265ae663c8b12bdf4d3ee20b57    utils.py
```

这样，我们就看到 `xgit` 这个目录下的内容了。可以看到，它包含了 4 个 blob 对象和 1 个树对象。用类似的方式，我们也可以看到 `commands` 这个目录下的内容。也就是说，树对象如它的名字一样，刻画出了一个目录的结构。

为什么需要 `-p` 呢？请回顾前面我们 `cat-file` 的讨论，我们只是简单地将对象的内容打印出来了。如果我们直接打印它，会得到下面这样的结果：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% git cat-file tree fa87295799e0c8a99ed4df60b330a805deb6822a
100644 __init__.py�⛲��CK�)�wZ���S�100644 cli.py�����A�{��O����40000 commands�# Z ;}T'�Nk�~)��U�]100644 constants.py�e.l���9��*]�;��1Iv100644 utils.pyR���Lb&Z�cȱ+�M>�
                             W                                                                                                        
% xgit cat-file tree fa87295799e0c8a99ed4df60b330a805deb6822a
100644 __init__.py�⛲��CK�)�wZ���S�100644 cli.py�����A�{��O����40000 commands�# Z ;}T'�Nk�~)��U�]100644 constants.py�e.l���9��*]�;��1Iv100644 utils.pyR���Lb&Z�cȱ+�M>�
                             W
```

这就不得不谈到 git 对于树对象的内容的组织方式了。我们刚才提到，一个对象的存储方式是 `[type] 0x20 [size] 0x00 [content]`；而对于树对象，它的 content 是由多个 `[file mode] 0x20 [file name] 0x00 [hash]` 前后连接组成的。因此，我们上面看到的乱码一样的东西，其实是这里的 `[hash]`，因为他们是 20 个字节的二进制数据，并不一定都是可打印字符。

也是因此，当任意一级子目录中的文件发生变化时，其哈希值会变化；由于它的哈希值是所在目录对应的树对象内容的一部分，因此影响了其这个树对象的哈希值
；这进一步会影响整个 work-tree 对应的树对象的哈希值。因此，给定任何一个树对象的哈希值以及对象存储，我们都可以还原出整个仓库的状态。

在本章中，我们会实现通过 `cat-file` 来查看 tree 对象的内容，但是我们把写入 tree 对象的细节留到下一章中！

### 如何给指令添加选项

根据上述讨论，我们预期大家能够实现出具备上述功能的 `hash-object` 和 `cat-file` 指令了！

不过，`hash-object` 这个指令会接收一些选项 (options)，例如 `-w`, `--stdin`, `-t` 等。我们如何在 typer 中实现这些选项呢？

与 `Argument` 类似，我们可以使用 `Option` 来定义一个选项。例如：

```python
@app.command()
def foo(arg: str, opt: Annotated[str, typer.Option("-o", "--opt", help="an option")] = "default"):
    print(arg, opt)
```

这里我们用 `Option` 表示 `opt` 是一个选项，并指定了它的短选项 `-o` 和长选项 `--opt`，以及它的帮助信息。由于我们给它了一个默认值，因此它是可选的。

下面是一些使用这个指令及其选项的例子：

<!-- termynal -->
```
% xgit foo --help

 Usage: xgit foo [OPTIONS] ARG                                                      
                                                                                    
╭─ Arguments ──────────────────────────────────────────────────────────────────────╮
│ *    arg      TEXT  [default: None] [required]                                   │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ --opt   -o      TEXT  an option [default: default]                               │
│ --help                Show this message and exit.                                │
╰──────────────────────────────────────────────────────────────────────────────────╯

% xgit foo hello -o world
hello world
% xgit foo hello --opt world
hello world
% xgit foo hello            
hello default
```

## 3.2 效果

我们会实现两个指令：`hash-object` 和 `cat-file`。它们接收如下的参数和选项：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% xgit hash-object --help
                                                                                    
 Usage: xgit hash-object [OPTIONS] [FILES]...                                       
                                                                                    
 计算对象的哈希值；如果指定了 -w，则将内容写入到对象数据库中。                      
                                                                                    
╭─ Arguments ──────────────────────────────────────────────────────────────────────╮
│   files      [FILES]...  要计算哈希值的文件 [default: None]                         │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────╮
│          -w            将内容写入到对象数据库中                                      │
│ --stdin                从标准输入读取内容                                           │
│          -t      TEXT  指定要创建的对象类型 [default: blob]                         │
│ --help                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────╯

% 
% xgit cat-file --help
                                                                                   
 Usage: xgit cat-file [OPTIONS] [TYPE] [OBJ]                                       
                                                                                   
 根据对象的哈希值，查看对象的内容。                                                
 Usages:                                                                           
                                                                                   
  • xgit cat-file TYPE OBJ                                                         
  • xgit cat-file (-s | -t | -e | -p) OBJ                                          
                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────╮
│   type      [TYPE]  要查看的对象的类型                                             │
│                     [default: None]                                             │
│   obj       [OBJ]   要查看的对象的哈希值                                           │
│                     [default: None]                                             │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────╮
│         -s        显示对象的大小                                                  │
│         -t        显示对象的类型                                                  │
│         -e        检查对象是否存在                                                 │
│         -p        按照对象的类型，显示对象的内容                                     │
│ --help            Show this message and exit.                                   │
╰─────────────────────────────────────────────────────────────────────────────────╯
```

我们预期它能产生和 git 一样的效果：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% echo "Xianyu Xuan" > a.txt
% xgit hash-object a.txt -w
884ca3bad1c062af78606083817f01dc92f3152a
% zlib-flate -uncompress < .git/objects/88/4ca3bad1c062af78606083817f01dc92f3152a
blob 12Xianyu Xuan
% xgit cat-file blob 884ca3bad1c062af78606083817f01dc92f3152a
Xianyu Xuan
% cat a.txt | xgit hash-object --stdin
884ca3bad1c062af78606083817f01dc92f3152a
% xgit cat-file -p fa87295799e0c8a99ed4df60b330a805deb6822a
100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391    __init__.py
100644 blob f01ed6f00183801a41b97b94d34fa6a88f08b78f    cli.py
040000 tree ab23095a203b7d5427a34e6bd67e29cdd955a85d    commands
100644 blob ba652e6c821887b83988d12a5de03b85d0314976    constants.py
100644 blob 5203a0a1944c62265ae663c8b12bdf4d3ee20b57    utils.py
```

会有一些实现过程中的细节，我并没有在这里展开；因为我们期望您多加思考，多尝试 git 的行为，然后实现出您的代码。相关细节会在下一节中给出我的实现。

!!! info ""
    在实现过程中，您有可能会遇到一些困惑，在这里您可以得到答案。

    但是，如果您希望挑战自己的搜索能力 / debug 能力的话，您也可以尝试先不看下面这些内容！

    ??? info "一些提示"
        - 在 tree 对象的存储中，`040000` 有可能被存储为 `40000`。
        - 您可能会发现，使用 Typer 来实现 `cat-file` 这个命令有点困难，因为 `cat-file` 有多种不同的用法，而且一些用法是互斥的；而 Typer 对此并没有很好的支持。Git 本身是使用 C 语言实现的，因此它可以对 argument & options 实现更加自由的 parse。一个解决方案：虽然不太优雅，但是您可以尝试在 `cat-file` 中使用判断来实现对各种用法的约束。

## 3.3 我的实现

!!! success "您可以在 [这个 commit](https://github.com/smd1121/xuan-git/commit/56e91220d1cad7b531e78e05e6d536f313463463) 中看到我的实现。"

TODO


<!-- 
我没有找到关于 git 错误代码的明细，StackOverflow 上有相关的 [讨论](https://stackoverflow.com/questions/4917871/does-git-return-specific-return-error-codes)。总体来说，我们会在程序出现异常时返回非 0 的值，而在程序正常退出时 typer 会帮我们返回 0。

我们会尽可能和 git 保持一致；例如当所在目录并不是一个 git repo 时，我们会返回 128：

!!! tip inline end "`$?`"
    在 bash 中，`$?` 会返回上一个命令的返回值。因此，我们可以通过 `echo $?` 来查看上一个命令的返回值。

    `$?` 是 Special Shell Variables 中的一个，您可以在 [这里](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) 查看更多的特殊变量。

<!-- termynal -->
```
% git cat-file blob abcdef
fatal: not a git repository (or any of the parent directories): .git
% echo $?
128
% 
% xgit cat-file blob abcdef
fatal: not a git repository (or any of the parent directories)
% echo $?
128
```

在我们开始实现对象存储系统之前，我们必须了解它们的确切存储格式。一个对象以一个指定其类型的头部开始： blob ， commit ， tag 或 tree （稍后会详细介绍）。这个标头后面是一个ASCII空格（0x20），然后是对象的大小（以字节为单位，作为ASCII数字），然后是null（0x00）（空字节），然后是对象的内容。

https://stackoverflow.com/questions/22968856/what-is-the-file-format-of-a-git-commit-object-data-structure

![](assets/2023-12-03-16-20-41.png) -->
