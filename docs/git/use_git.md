Git 保存的是快照而非版本之间的差别。[ref](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F#:~:text=Snapshots%2C%20Not%20Differences)

#### 配置在哪

git 有一堆配置。它主要分为 3 级：

- 系统级别的配置，保存在 `/etc/gitconfig` 文件中，这个文件对系统上的所有用户都有效。
- 用户级别的配置，保存在 `~/.gitconfig` 文件中，这个文件只对当前用户有效。
- 项目级别的配置，保存在项目的 `.git/config` 文件中，这个文件只对当前项目有效。

???+ info "`/etc` 目录"
    `/etc` 目录是干什么的呢？[这里](https://unix.stackexchange.com/questions/5665/what-does-etc-stand-for) 有一个完整的故事。简单来说，`/etc` 是 `et cetera` 的缩写，本身用来放那些没地方放的东西。随着时间的推移，`/etc` 目录变成了存放配置文件的地方。

    [Filesystem Hierarchy Standard](http://www.pathname.com/fhs/pub/fhs-2.3.pdf) 是一个定义了什么目录是放什么的标准。

#### 如何操作

如果要修改配置，可以直接修改上述文件，也可以通过 `git config` 命令来修改。`git config` 命令可以查询、设置、更改、删除配置。

`git config` 可以通过选项配置要操作的是哪个级别的配置。`--system` 选项表示系统级别，`--global` 选项表示用户级别，`--local` 选项表示项目级别。如果不指定选项，默认是项目级别。

另外，`git -c NAME=VALUE` 可以设置配置只对当前命令有效的配置。

`git config` 提供一系列选项读取或者展示配置的全部键值或部分键值，并提供编程友好的选项。


例如，通过 `git config --list --show-origin`

通过 `git var -l` 可以查看所有的 logical variables，这包含了所有的配置。

#### 有什么配置

??? note "简单看一看觉得有用的配置"
    `alias`，可以设置别名，比如 `git config --global alias.co checkout`，这样就可以用 `git co` 代替 `git checkout`。

#### TODO

- [credentials](https://git-scm.com/docs/gitcredentials)
- sparse-checkout

#### 简单看了一眼的东西

- `git notes` 能够在不更改 commit 的情况下为 commit 添加注释。它的使用不太广泛，GitHub 和 GitLab 也不支持显示 notes。
    - [相关讨论](https://tylercipriani.com/blog/2022/11/19/git-notes-gits-coolest-most-unloved-feature/) 指出，notes 可以用来让一些信息离线记录在 git 中，例如 code review 的信息。
    - 自 2014 年起，GitHub [不再显示 notes 了](https://github.blog/2010-08-25-git-notes-display/)。
    - GitLab 支持 notes 仍然是一个 open issue。
    - ![](assets/2024-06-24-21-16-47.png)
