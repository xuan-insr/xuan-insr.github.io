!!! question "我在开发分支 a 上做了一些更新，没有 commit，我希望把这些更新 commit 到开发分支 b 上"
    `git stash`，切换分支，然后 `git stash apply`。如果后悔了，可以 `git stash drop`。
