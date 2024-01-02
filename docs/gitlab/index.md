# GitLab CI/CD

--8<-- "snippets/blog_like_contents.md"

## 内容一览

## 零散内容

[Predefined Variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)

.gitlab-ci.yml 指定 GitLab CI/CD 的配置，定义了要执行 job 的结构和顺序，以及遇到什么条件时应当做什么事。

每个 job 都有一个 script section，并属于一个 stage。stage 描述了 job 的执行顺序：stage 中的 job 会并行执行；后面的 stage 中的 job 会在前面的 stage 中的 job 执行完毕后再执行。

可以使用 `needs` 关键字来自定义 job 之间的依赖和执行顺序。

`rule` 制定何时运行或跳过一个 job；旧版本中的 `only` 和 `except` 也可以用 `rule` 来实现。

