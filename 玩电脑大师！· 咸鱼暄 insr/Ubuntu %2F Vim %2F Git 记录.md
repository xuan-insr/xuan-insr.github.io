
### Vim
**粘贴** vim 粘贴防止重新缩进 (indent): `:set paste`，然后进 Insert mode<br />**删除** `dd`删除当前行，`:%d`全删除


### Git

- git 保存用户名密码  [https://stackoverflow.com/questions/35942754/how-can-i-save-username-and-password-in-git](https://stackoverflow.com/questions/35942754/how-can-i-save-username-and-password-in-git)
   - `git config --global credential.helper store`
- git 放弃修改 [https://blog.csdn.net/baidu_35007727/article/details/122927676](https://blog.csdn.net/baidu_35007727/article/details/122927676) `git checkout .`


### 其他
**ssh 免密登录** [https://zhuanlan.zhihu.com/p/342653729](https://zhuanlan.zhihu.com/p/342653729)

`sudo -u <usr> <cmd>`，以另一个用户的身份运行

在`~/.ssh/config`里可以设置快速 ssh 的 Host 名字，hostname 和 user
![image.png](./assets/1663636843744-6912414a-01d7-4f35-b645-5bed119384e3.png)
