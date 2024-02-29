管道 (pipe) `|` 和 `|&` 用于将一个命令的输出传递给另一个命令的输入。

如果使用 `|`，则将命令的标准输出 (stdout) 传递给另一个命令的标准输入 (stdin)；如果使用 `|&`，则将命令的标准输出 (stdout) 和标准错误 (stderr) 传递给另一个命令的标准输入。

???+ example
    ```bash title="examples/common_scripts/print.sh"
    --8<-- "bash/examples/common_scripts/print.sh"
    ```

    ```bash title="examples/common_scripts/read.sh"
    --8<-- "bash/examples/common_scripts/read.sh"
    ```

    !!! success "效果"
        ```
        % cd examples/common_scripts

        % ./print.sh | ./read.sh
        stderr
        from stdin: stdout

        % ./print.sh |& ./read.sh
        from stdin: stdout
        from stdin: stderr
        ```

请注意：以 `|` 连接的命令是并行执行的。例如：

```
% (sleep 1 ; >&2 echo "1") | echo "2"
2
1
```

显然，并行执行会在不同的 sub shell 中执行：

```
% echo $BASHPID
29823

% >&2 echo $BASHPID | echo $BASHPID
30402
30401
```


另需注意的是，默认情况下 pipeline 中的命令失败不会导致整个 pipeline 停止和失败；pipeline 的返回值是最后一个命令的返回值。例如：

```
% false | echo "This will be printed"
This will be printed
% echo $?
0
```

为了避免错过可能的错误，可以使用 `set -o pipefail`。此时如果有任何命令失败，整个 pipeline 的返回值就是最后一个失败的命令的返回值。

```
% set -o pipefail

% false | echo "This will still be printed"
This will still be printed
% echo $?
1

% exit 1 | exit 2 | echo "This will still be printed"
This will still be printed
% echo $?
2
```

See Also: 

- TODO: `|&` 是 `2>&1 |` 的缩写。
- TODO: time
- TODO: Each command in a multi-command pipeline, where pipes are created, is executed in its own subshell, which is a separate process (see Command Execution Environment)
