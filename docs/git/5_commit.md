Blob 类型的对象实现了「存储文件内容」的功能，获得了文件的快照；tree 类型的对象在此之上实现了「存储目录结构（路径、模式）」的功能，获得了 work-tree 的快照。而在此之上，commit 类型的对象则维护了「谁、在什么时候、出于何种目的保存这些快照」的信息，从而以人类可读和可追溯地方式记录了仓库的变化——或者说，用人类的语言标记了一些 tree 对象的 SHA。

看两个例子：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% git cat-file -p 1a4e1286c25459fae80c8031fa68a2bf349efc5b
tree 8b950fd0e5045a016754832f0034ea87a66c2995
author smd1121 <2087868649@qq.com> 1701586413 +0800
committer smd1121 <2087868649@qq.com> 1701586413 +0800

[feat][framework]: basic install & run codes
% git cat-file -p 2d4a22863bad3835a0da2f8eedb66335b8390bb8
tree 08d60cce73001ec2042755b380bd08b1b08c9329
parent 1a4e1286c25459fae80c8031fa68a2bf349efc5b
author smd1121 <2087868649@qq.com> 1701596360 +0800
committer smd1121 <2087868649@qq.com> 1701607564 +0800

[feat][command] implements init
```

`1a4e1286c25459fae80c8031fa68a2bf349efc5b` 是这个仓库的首个提交。它的内容包含了一个 tree 对象的 SHA，以及作者 (author) 和 提交者 (committer) 的信息，同时还有一个提交信息 (commit message) 表示这个提交干了什么。

Commit 的作者和提交者可能不是同一个人，例如 [这个 commit](https://github.com/IsshikiHugh/zju-cs-asio/commit/34e0e297a4c421d22b644d7fbe0757da9a658593) 作者是我，但是提交者是修勾 @IsshikiHugh。

而 `2d4a22863bad3835a0da2f8eedb66335b8390bb8` 是第二个提交，可以看到它多了一个 parent 字段，表示它是基于哪个提交之上修改的；这里的 parent 就是 `1a4e1286c25459fae80c8031fa68a2bf349efc5b`。

一个提交可能没有 parent（例如第一个提交），也可能有多个 parent（例如 merge commit）。也是因此，我们可以从任意一个提交开始，通过 parent 字段一直追溯到第一个提交，从而还原出整个仓库的变化；而由于每个提交都包含了 tree sha，我们也可以还原出任何一个提交的快照。也就是说，这让仓库的全部历史都保存在每一个 commit 里。（所以 git 其实也是区块链。）
