# 1 构建框架

!!! abstract
    在这部分中，我们会 setup 一个基本的命令行工具。这个工具不会实现任何真实的功能，但是能运行！

    在这章，我们学习如何搭建一个命令行工具的框架。

## 1.1 效果

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```
% xgit --help

Usage: xgit [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────╮
│ --help          Show this message and exit.    │
╰────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────╮
│ commit                                         │
│ init                                           │
╰────────────────────────────────────────────────╯

% xgit commit
Hello World
% xgit init
Hello World
```

可以看到这章其实和 git 没什么关系！

## 1.2 我学了什么

这一章四舍五入是在搭环境，因此您可以直接看我写出来的框架。当然您也可以尝试自己解决下面的问题！

### 构建一个命令行工具

我选择使用 Python 的 typer 库来构建命令行工具，它能帮助我们完成参数解析、提示信息等各种工作。

当然，您也可以像 [我阅读的参考资料](references) 那样使用 `argparse` 来完成基本的参数解析工作。

### 怎样更简便地使用这个 CLI 工具

在 [Typer 的 User Guide](https://typer.tiangolo.com/tutorial/first-steps/) 中，使用方式都形如 `python main.py`；如果有多个 command，则形如 `python main.py command`。

但是，我们希望能像 `git` 那样使用 `git command` 的形式。因此，我使用 setuptools 来完成 `xgit` 的构建和安装。

## 1.3 我的实现

!!! success "您可以在 [这个 commit](https://github.com/smd1121/xuan-git/commit/1a4e1286c25459fae80c8031fa68a2bf349efc5b) 中看到我的实现。"

核心的目录结构如下：


!!! tip inline end "`tree`"
    `tree` 是一个命令行工具，它可以以树状的形式展示目录结构。

<!-- termynal: {"prompt_literal_start": ["%"], title: "", buttons: macos} -->
```bash
% tree .
.
├── setup.py
└── xgit
    ├── __init__.py
    └── cli.py
```


简单来说，在这个目录中：

- `xgit` 是一个包。这是一个 Python 中的概念，但是不了解也暂时没什么关系
    - `__init__.py` 是一个空文件，它的存在是为了让 Python 认为这是一个包
        - 以防您真的感兴趣：[为什么需要 `__init__.py`](https://stackoverflow.com/questions/448271/what-is-init-py-for)
    - `cli.py` 是命令行工具的源码
- `setup.py` 是一个用于安装的脚本

`cli.py` 的内容如下：

```python title="xgit/cli.py"
import typer

app = typer.Typer(add_completion=False)

@app.command()
def init():
    print("Hello World")

@app.command()
def commit():
    print("Hello World")

def main():
    app()
```

这四舍五入就是 typer 的一个最小的例子。您可以尝试通过 `python cli.py --help` 或者 `python cli.py init` 来运行这个程序。

- `app` 是一个 `Typer` 对象，它是我们的命令行工具的入口
    - `add_completion=False` 的作用您可以自己探索！
- `@app.command()` 是一个装饰器，它的作用是将下面的函数注册为一个命令

`setup.py` 的内容如下：

```python title="setup.py"
import setuptools

setuptools.setup(
    name="xgit",
    packages=setuptools.find_packages(),
    install_requires=["typer>=0.9.0"],
    entry_points = {
            'console_scripts' : [
                'xgit = xgit.cli:main'
            ]
        }
)
```

有了这个脚本，我们就可以在其所在文件夹通过 `pip install .` 来安装我们的命令行工具了。安装完成后，我们就可以通过 `xgit` 来使用我们的命令行工具了。效果参见 [1.1 效果](11-效果)。

我们可以使用 `pip install -e .` 来安装一个「可编辑」的版本。这种模式下，`xgit` 的行为会随着我们的代码的修改而改变，这样我们就可以在不重新安装的情况下修改代码并测试了。

我不打算展开讲解 setuptools 的使用，因为我们之后也不太会修改这个文件了。如果您对此感兴趣，可以参考 [这篇文章](https://packaging.python.org/tutorials/packaging-projects/)。

???+ note "chores"
    如果您看了 [我的 commit](https://github.com/smd1121/xuan-git/commit/1a4e1286c25459fae80c8031fa68a2bf349efc5b)，您可能会发现一些其他的文件。

    其中 `scripts/` 目录下的两个文件是用于完成 lint，即代码风格检查的。这里用到了 `isort`, `pylint`，以及后面的 commit 中添加的 `black`。它们会完成对代码风格（如缩进、import 排序等）的自动化调整，并通过静态分析帮我检查代码中可能的问题。

    我会在每次提交之前通过执行 `./scripts/lint_all.sh` 来完成这些调整和检查。通常这些工作会在 IDE 中完成，但是我懒得配置 :p

    （以防有人不知道，上面的 `:p` 是个颜表情）
