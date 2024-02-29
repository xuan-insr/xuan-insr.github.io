???+ example "本节使用的示例脚本"
    ```bash title="examples/common_scripts/succeed.sh"
    --8<-- "bash/examples/common_scripts/succeed.sh"
    ```

    ```bash title="examples/common_scripts/fail.sh"
    --8<-- "bash/examples/common_scripts/fail.sh"
    ```

由换行或 `;` 连接起来的 2 个 pipeline 会顺次执行，返回值为其中最后一个命令的返回值。

???+ success "效果"
    ```
    % ./fail.sh ; ./succeed.sh
    fail
    succeed
    % echo $?
    0
    ```

    ```
    % ./succeed.sh ; ./fail.sh
    succeed
    fail
    % echo $?
    1
    ```

由 `&&` 连接起来的 2 个 pipeline 会顺次执行，当且仅当第一个 pipeline **成功**时才会执行第二个 pipeline。返回值为最后一个**执行了的**命令的返回值。

???+ success "效果"
    ```
    % ./fail.sh && ./succeed.sh
    fail
    % echo $?
    1
    ```

    ```
    % ./succeed.sh && ./fail.sh
    succeed
    fail
    % echo $?
    1
    ```


由 `||` 连接起来的 2 个 pipeline 会顺次执行，当且仅当第一个 pipeline **失败**时才会执行第二个 pipeline。返回值为最后一个**执行了的**命令的返回值。

???+ success "效果"
    ```
    % ./fail.sh || ./succeed.sh
    fail
    succeed
    % echo $?
    0
    ```

    ```
    % ./succeed.sh || ./fail.sh
    succeed
    % echo $?
    0
    ```

    ```
    % ./fail.sh || ./fail.sh
    fail
    fail
    % echo $?
    1
    ```
    


