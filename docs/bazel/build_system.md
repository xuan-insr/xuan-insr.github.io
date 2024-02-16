# 构建系统基础: Why Bazel

!!! abstract
    读 [Build System Basics](https://bazel.build/basics) 的笔记。

    介绍了为什么要用构建系统，以及 Bazel 提供的解决方案。

#### 为什么需要构建系统

对于一些小的项目，使用编译器或者结合一些脚本能够完成构建的任务。然而，当项目越来越大，会出现各种问题，例如：

- 编译变得很慢：每次编译都需要重新跑一遍脚本
- 由于各种库、工具或者环境变量设置，构建在自己电脑上能跑但是在其他人那里不能
- 每当新增部分的时候都需要修改脚本
- 构建过程出现问题的时候很难定位和解决
- 难以维护外部依赖的版本和更新等等

!!! quote "You've run into a classic problem of scale."

#### 基于任务的构建系统

Task-based build systems，例如 Maven, Gradle 等，将上面的「脚本」拆分成为一个一个 task：每个 task 指定运行哪些脚本从哪些输入生成哪些输出，以及这个 task 依赖哪些 task。这样，这些 build system 就能够根据我们需要的输出来找到所有的依赖，从而运行所有的脚本。

类比到编程语言，从我们的「脚本」到这样的 task-based build systems，就类似于 [从汇编语言到结构化编程的过程](../../cpp/cpp_restart/2_paradigm)：我们将指令结构化、模块化，这样一方面能够提高可维护性，另一方面我们也可以容易地
