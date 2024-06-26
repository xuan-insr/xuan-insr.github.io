# 0 写在前面

## 为什么会有这篇文章

在大学，我们曾经尝试过通过 [GitHub](https://github.com/smd1121) 来进行代码的版本管理和协作。但是，当时懒惰，因此一直在使用 [GitHub Desktop](https://desktop.github.com/)；对 git 的真正使用也只是限于 `add`, `commit`, `push`, `pull` 等简单的操作，也从来没学会过如何处理 conflict。

不过，在实习以及现在正式工作之后，面对复杂的代码和各种多人协作的场景，我不得不稍微仔细学习一下 git。为了更好地理解 git 的原理，我打算尝试自己实现一个简化版的 git，并尝试将过程分享出来，从而让大家更好地理解 git 的原理。

我 Google 了 DIY git，找到了一些参考资料。这些参考资料能够在千行以内实现一个简化版的 git，这让我认为这个目标是可行的。不过，我比较在意的一些指令在这些参考资料中并没有实现，因此实现这些指令是我的一个挑战性目标。

<a name="references"></a>
!!! quote "我的学习过程中参考的资料"
    - [Pro Git](https://git-scm.com/book/en/v2) ([中文版](https://git-scm.com/book/zh/v2))
    - [ugit](https://www.leshenko.net/p/ugit/)
    - [wyag](https://wyag.thb.lt/intro)
    - [图解 git](https://marklodato.github.io/visual-git-guide/index-zh-cn.html)
    - [interactive git cheetsheet](https://ndpsoftware.com/git-cheatsheet.html)

    我部分代码的实现，以及本文的部分文段，可能来自于上述资料。除此之外的参考，我会在文中单独标注。

我使用 Python 和 [typer](https://typer.tiangolo.com/) 来实现这个项目，因为这也是我工作中会使用到的东西，我希望在这个过程中也能锻炼这方面的能力。

## 我希望带给大家什么

我希望本文能够像一个「实验指导」一样，在每个章节中为大家介绍尽可能全面的基础知识，陈述章节的目标，最后分享我自己的代码。

如果您也有兴趣也自己 DIY 一个 git，我希望本文能够给您提供所需的知识，引导您完成这个过程。同时我也希望您能将您的实现与我的代码进行对比，从而帮我指出我的代码中可以改进的地方，或者可能存在的错误。

（如果您这样做了，请考虑在您的实现中附上本文的链接，感谢~）

如果您没有兴趣或者时间自己实现一个 git，我也希望本文能够像一个「源码剖析」一样，给您解释我的实现，从而帮助您高效地理解 git 的原理。也希望您能在这个过程中帮我发现问题。

!!! warning
    同时，由于这是我的学习笔记，因此我预期我的实现和设计一定会有一些错误或者不妥当的地方，因此我有可能在学习和实现的过程中对代码做重构或者修改。这些修改能够在本文中得以修正，因此 [仓库](https://github.com/smd1121/xuan-git) 中的提交记录和文章内容可能有所区别。此时应以文章内容为准。

## 我不会尝试做的事

我不会尝试实现 git 的全部功能，我也不一定会和 git 的行为完全一致。

本文的核心目标仍然是学习 git，因此实现哪些功能取决于我想学习哪些功能以及它们背后的原理。

## 我对读者所具备能力的预期

我预设读者具备以下能力，因为这是我的状态：

1. 会搜索，或者会用 ChatGPT
2. 对命令行有基本的了解。我使用的是 macOS 和 ubuntu，因此我会使用 macOS 的终端来展示命令行的效果。如果您使用的是 Windows，我的部分命令可能无法在您的终端中运行，此时需要您回到第 1 条；另外强烈建议使用 WSL！
3. 对 git 的最基本使用有了解，例如 `add`, `commit`, `push`, `pull` 等
4. 掌握至少一门编程语言，因为这是看懂代码的基础。我也不太会 Python，所以我认为会的语言不是 Python 也没关系

对于上述预设以外的知识，我会在文章中进行解释。

## 关于本文使用 Admonitions 的方式

在本文中，我会使用各种不同的 admonitions 来标注一些内容。它们表示如下含义：

<section markdown="1" class="grid">
!!! abstract "摘要"
    文章或者某一部分的摘要

!!! tip "提示"
    一些基础知识，但是可能不是所有人都知道
</section>

<section markdown="1" class="grid">
!!! warning "警告"
    已知可能出现的问题，或者与 git 的行为有明显差异的地方（但我可能不会完全说明比 git **少** 实现了哪些功能）

!!! success "我的代码"
    指示我的代码在哪里
</section>

<section markdown="1" class="grid">
!!! info "额外信息"
    一些我认为有必要陈述的信息

!!! note "次要内容"
    一些可能会有人感兴趣但不重要的内容
</section>

<section markdown="1" class="grid">
!!! quote "参考资料"
    用于标明一些参考或出处
</section>

我并不一定会将所有符合上述描述的内容都用 admonitions 标注出来。如果它们非常短，我可能会在文中直接说明；而如果它们非常长，我可能会将它们放在一个单独的小节中。


