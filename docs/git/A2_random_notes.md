- `HEAD` 的 `ref: refs/heads/master` 不存在是正常的，因为我们还没有提交

- `git diff-files`
    - `git diff` == `git diff-files -p`
- `git diff-index`
    - `git diff HEAD` == `git diff-index -p HEAD`
图解： https://git-scm.com/docs/gitcore-tutorial#:~:text=how%20various%20diff%2D*%20commands%20compare%20things

Git will never go looking for files to compare, it expects you to tell it what the files are, and that's what the index is there for.

- `git write-tree`, `git commit-tree`
    - `git commit`

Git contrib/examples 有很多指令的 script 实现 https://github.com/git/git/commit/49eb8d39c78f161231e63293df60f343d208f409


- init
- worktree <-> index: add, rm, mv, restore(1), diff(1)
    - hash-object, cat-file
    - index: ls-files, update-index
    - 
- index <-> repo: commit, 
- on the repo: bisect, log, 

- not implmementing:
    - `git grep`
    - `git show`, looks like a better `git cat-file`


`git restore`:
- `git restore FILE`: 恢复文件到 index 的状态
- `git restore --staged FILE`: 将 index 中的文件恢复到 HEAD 的状态，不影响本地文件
    - `git add FILE` 的逆运算

恢复谁：`-W/--worktree` and / or `-S/--staged`，未指定则 `-W`
从哪里恢复：`-s <tree>/--source=<tree>`，未指定时，如果有 `-S` 则 `HEAD`，否则 `index`

- `git restore --source=COMMIT FILE`: 将文件恢复到某个 commit 的状态，不影响本地文件

- THIS COMMAND IS EXPERIMENTAL. THE BEHAVIOR MAY CHANGE.

