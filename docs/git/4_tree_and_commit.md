# 123

Commit 的作者 (author) 和 提交者 (committer) 可能不是同一个人，例如 [这个 commit](https://github.com/IsshikiHugh/zju-cs-asio/commit/34e0e297a4c421d22b644d7fbe0757da9a658593) 作者是我，但是提交者是修勾 @IsshikiHugh。

不会完全显示出来，使用的是 `less` 这个命令行工具。这是一个分页器。

````python
import typer
import subprocess

app = typer.Typer()

@app.command()
def show_data():
    # 生成或获取要显示的数据
    data = "这里是您的数据...\n" * 100  # 示例数据

    # 使用分页器显示数据
    with subprocess.Popen(['less'], stdin=subprocess.PIPE, text=True) as proc:
        proc.communicate(data)

if __name__ == "__main__":
    app()
````
