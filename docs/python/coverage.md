# 用 Coverage.py 衡量 Python 测试覆盖率

[Coverage.py](https://coverage.readthedocs.io/en/latest/)，一个衡量代码覆盖率的工具；常用来衡量测试的覆盖率。

简单来说，使用 `coverage run` 命令来运行测试，然后使用 `coverage report` 命令来生成报告。

`coverage` 会将执行数据保存在 `.coverage` 文件中。默认情况下，每次运行 `coverage run` 命令时，都会覆盖 `.coverage` 文件。如果想要保留多次运行的执行数据，可以使用 `coverage run` 的 `--append` 选项。

我们有可能会并行执行若干不同的测试，此时可以使用 `coverage combine` 命令来合并多个 `.coverage` 文件。具体来说，它会在当前目录下搜索所有 `.coverage.*` 文件，并将它们合并成一个 `.coverage` 文件。默认情况下，它会删除所有的 `.coverage.*` 文件，但是可以使用 `--keep` 选项来保留这些文件。

`coverage report` 命令会生成一个简单的报告，它会告诉我们每个文件的覆盖率。可以通过 `-m` 选项来显示每个文件中有哪些行没有被运行。

还有 `coverage html` 等命令用来生成更加详细的报告。
