# 用 GitLab CI Artifacts 在 Job 之间共享文件

!!! info "预备知识"
    本文预设读者掌握 GitLab CI/CD 的基本概念，以及 `.gitlab-ci.yml` 的基本语法。

默认情况下 job 是独立运行的，彼此不共享资源。但是可以使用 [`cache`](https://docs.gitlab.com/ee/ci/caching/) 和 [`artifacts`](https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html) 在 job 之间共享文件。

- `cache` 用于在互联网上下载依赖：如果依赖项相同，那么同一个 pipeline 中的后续 job 可以使用缓存的依赖项，而不必重新下载。
- `artifacts` 用于在 job 之间传递文件：如果一个 job 生成了一个文件，那么后续的 job 可以使用这个文件，并且可以下载这个文件。

默认情况下，jobs 会从前面所有 stages 完成的 jobs 中下载所欲 artifacts ([ref](https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html#:~:text=Jobs%20downloads%20all%20artifacts%20from%20the%20completed%20jobs%20in%20previous%20stages%20by%20default.))，但是可以通过 `dependencies` 关键字来显式指定要从哪些 jobs 下载。例如指定 `dependencies: []` 可以不从任何 job 下载。

```yaml
default:
  image: ubuntu:18.04

stages:
  - s1
  - s2
  - s3

j1.1:
  stage: s1
  script:
    - echo "j1.1" > j1.1.txt
  artifacts:
    paths:
    - j1.1.txt

j2.1:
  stage: s2
  script:
    - ls
    - cat j1.1.txt
    - echo "j2.1" > j2.txt
  artifacts:
    paths:
    - j2.txt

j2.2:
  stage: s2
  script:
    - ls
    - cat j1.1.txt
    - echo "j2.2" > j2.txt
  artifacts:
    paths:
    - j2.txt

j3.1:
  stage: s3
  script:
    - ls
    - cat j2.txt
```

看看它干了什么：

```log
Downloading artifacts

Downloading artifacts for j1.1 (1620568)...
Downloading artifacts from coordinator... ok        id=1620568 responseStatus=200 OK token=64_n_zpG
Downloading artifacts for j2.1 (1620569)...
Downloading artifacts from coordinator... ok        id=1620569 responseStatus=200 OK token=64_n_zpG
Downloading artifacts for j2.2 (1620570)...
Downloading artifacts from coordinator... ok        id=1620570 responseStatus=200 OK token=64_n_zpG

Executing "step_script" stage of the job script

$ ls
README.md
j1.1.txt
j2.txt
$ cat j2.txt
j2.2
```

即，j3.1 尝试从前面 3 个 jobs 中下载 artifacts，其中来自 j2.1 的 artifact 被 j2.2 的同名 artifact 覆盖了。

## 应用：在不同的 stages 中完成测试，在最后一个 stage 中统计 coverage

