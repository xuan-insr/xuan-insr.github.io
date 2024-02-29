# Bash

--8<-- "snippets/blog_like_contents.md"

管道和 `xargs`

`find . -name '*.py' | xargs wc -l`

Bash is an acronym for ‘Bourne-Again SHell’. The Bourne shell is the traditional Unix shell originally written by Stephen Bourne. 

### Pipelines

Pipelines 是用 `|` 或 `|&` 连接起来的一系列 commands。一个单独的 command 也算一个 pipeline。

--8<-- "bash/examples/pipe/pipe.md"

### List of Commands

List 是用 `;`, `||`, `&&`, `&` 或换行连接起来的一系列 commands。一个单独的 command 也算一个 list。一个 list 可选地以 `;`, `&` 或换行结尾。

--8<-- "bash/examples/list/list.md"

