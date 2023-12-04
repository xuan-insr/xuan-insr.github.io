# 2 初始化仓库

!!! abstract
    在这部分中，我们会实现 `xgit init` 指令，它会初始化一个空的仓库。

    在这章，我们学习如何实现一个命令。

这是一个非常简单的部分！我们创建一个 `.git` 仓库，然后在其中创建一些文件和目录。我们暂时不讨论这些文件和目录的作用，只是简单地创建它们。

## 2.1 效果

我们可以通过 `--help` 来查看 `xgit init` 的使用方法：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% xgit --help
                                                                                 
 Usage: xgit [OPTIONS] COMMAND [ARGS]...                                         
                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                   │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────╮
│ commit                                                                        │
│ init                初始化一个 git 仓库。                                        │
╰───────────────────────────────────────────────────────────────────────────────╯

% xgit init --help
                                                                                 
 Usage: xgit init [OPTIONS] [DIRECTORY]                                          
                                                                                 
 初始化一个 git 仓库。                                                           
                                                                                 
╭─ Arguments ───────────────────────────────────────────────────────────────────╮
│   directory      [DIRECTORY]  要初始化 git 仓库的目录 [default: .]               │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                   │
╰───────────────────────────────────────────────────────────────────────────────╯
```

可以看到 `xgit init` 会在指定目录下初始化一个 git 仓库；如果没有指定，则默认在当前路径下新建。

作为一个示例，我们在一个空目录下运行 `xgit init .`，可以看到它创建了 `.git` 目录，并创建了一些文件和目录（这里 `HEAD` 是文件，其他的都是目录）：

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% mkdir git_test
% cd git_test
% xgit init .
Initialized empty Git repository in /private/tmp/git_test/.git
% tree . -a
.
└── .git
    ├── HEAD
    ├── objects
    └── refs
        ├── heads
        └── tags

6 directories, 1 file
```

我们会在后面讨论这些文件和目录的作用。这次我们的目标就是把它们创建出来！

## 2.2 预备知识

`.git` 目录包含 git 完成版本控制所需要的 **全部** 信息。即使目录中的其它文件全部被删除，我们也可以通过 `.git` 目录中的信息来恢复它们。我们在后面的章节中再逐步了解这些信息。

在这节中，我们希望创建一个命令 `xgit init`，它接受一个可选的参数作为创建 git 仓库的目录；即如果没有指定目录，则默认在当前目录下创建。

在 typer 中，通过给实现命令的函数添加参数，就能在生成出的命令中接收对应的参数；而如果这个参数有默认值，那么它就是可选的。

## 2.3 我的实现

!!! success "您可以在 [这个 commit](https://github.com/smd1121/xuan-git/commit/2d4a22863bad3835a0da2f8eedb66335b8390bb8) 中看到我的实现。"

我们增加了一些文件和目录：

```diff
    % tree . --gitignore       
    .
    ├── readme.md
    ├── scripts
    │   ├── lint.sh
    │   └── lint_all.sh
    ├── setup.py
    └── xgit
        ├── __init__.py
        ├── cli.py
+       ├── commands
+       │   ├── __init__.py
+       │   └── init.py
+       └── constants.py
```

我们不妨先来看看 `cli.py` 中的改动：

```diff title="diff of xgit/cli.py"
diff --git a/xgit/cli.py b/xgit/cli.py
index 88ba1d6..cc30cab 100644
--- a/xgit/cli.py
+++ b/xgit/cli.py
@@ -1,14 +1,16 @@
 import typer
 
+from xgit.commands import init

 app = typer.Typer(add_completion=False)
 
-@app.command()
-def init():
-    print("Hello World")
+app.command()(init.init)

 
 @app.command()
 def commit():
     print("Hello World")


 def main():
     app()
```

我们从 `xgit.commands` 中导入了 `init`，并将 `init.init` 注册为 `app` 的一个命令。这样，我们就可以通过 `xgit init` 来调用 `init.init` 了。

`commands` 是我们创建的一个新文件夹，用于存储命令的源码。我们在其中创建了一个空的 `__init__.py`，这使得我们能够将 `commands` 视为一个包，因此能够在 `cli.py` 中使用 `from xgit.commands import init`。

我们用 `app.command()(init.init)` 来注册 `init.init`，这是注册命令的另一种方式。我们仍然保留了 dummy 的 `commit` 命令，因为当只有一个命令时，typer 的行为会有一些不同；如果感兴趣那样会发生什么的话您可以自己试一试。

我们来看看 `init.py` 的内容：

```python linenums="1" title="xgit/commands/init.py"
from pathlib import Path

from typer import Argument
from typing_extensions import Annotated

from xgit.constants import GIT_DIR


def init(directory: Annotated[str, Argument(help="要初始化 git 仓库的目录")] = "."):
    """
    初始化一个 git 仓库。
    """
    directory: Path = Path(directory)
    git_dir: Path = directory / GIT_DIR

    git_dir.mkdir(exist_ok=True)
    (git_dir / "objects").mkdir(exist_ok=True)
    (git_dir / "refs").mkdir(exist_ok=True)
    (git_dir / "refs" / "heads").mkdir(exist_ok=True)
    (git_dir / "refs" / "tags").mkdir(exist_ok=True)

    if not (git_dir / "HEAD").exists():
        with (git_dir / "HEAD").open("w") as f:
            f.write("ref: refs/heads/master\n")

    print(f"Initialized empty Git repository in {git_dir.absolute()}")
```

我们可以看到，我们使用了 `typer.Argument` 来定义一个参数，它会被 typer 自动解析。我们使用了 `typing_extensions.Annotated` 来为这个参数添加了一个 `help`，这样我们就可以通过 `--help` 来查看这个参数的帮助信息了。

???+ info "类型注解与 `Annotated`"
    我们知道，Python 是一个动态类型语言，这意味着我们不需要在定义变量时指定它的类型。但是，为了让 IDE 和静态分析工具就能够更好地理解代码，从而提供更好的提示和检查，Python 提供了类型注解的功能。

    `typing_extensions` 中的 `Annotated` 允许开发者在提供类型注解的同时提供一些额外信息。`Annotated` 主要是给库使用的，它的第一个参数表示这个变量的类型，而后面的参数表示额外的信息。
    
???+ info "命令的参数"
    这里的 `init` 被注册为一个 command，因此它的参数 `directory` 会被理解为 command 的一个参数 (argument)；即使我们不写类型注解也是如此。
    
    但是，我们通过 `name: Annotated[str, typer.Argument()]` 的方式明确说明它是一个参数，因为这样我们可以给 typer 提供更多信息，例如这里例子中的 `help`。

    另外，由于我们给这个参数了一个默认值 `= "."`，因此它成为了一个可选参数。在 `--help` 中，我们看到 `Usage: xgit init [OPTIONS] [DIRECTORY]`，这里 `DIRECTORY` 被 `[]` 包裹，说明它是一个可选的参数。

`xgit.constants` 是我们新建的 `xgit/constants.py`，它会用来存放一些常量，目前只有 git 目录的名字：

```python title="xgit/constants.py"
GIT_DIR = ".git"
```

`Path` 是 `pathlib` 提供的一个类，它包装了关于路径、文件、目录的一些操作。`/` 运算符会将两个 `Path` 连接起来，因此 `directory / GIT_DIR` 会得到一个新的 `Path`，它表示 `directory` 中的 `.git` 目录。

我们创建了 `.git` ，并在其中创建了一些文件和目录。在下一章开始，我们会用到这些文件和目录。

您可以在 [2.1 效果](21-效果) 中回顾我们这一章的效果。
