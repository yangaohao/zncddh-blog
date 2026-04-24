---
title: git学习过程
date: 2026-04-24 08:37:35
tags: git
categories: 学习记录

---

````md
# Git 学习笔记

## 一、Git 是什么？

Git 是一个**版本控制工具**，主要用来管理代码的修改历史。

简单理解：

> Git 可以帮我们记录代码的每一次修改，并且可以在需要时回到之前的版本。

Git 常用于：

- 保存代码历史版本
- 回退错误修改
- 多人协作开发
- 创建分支开发新功能
- 将代码上传到 GitHub、GitLab、Gitee 等远程仓库

---

## 二、Git 的基本工作流程

Git 的日常使用流程可以概括为：

```text
工作区 -> 暂存区 -> 本地仓库 -> 远程仓库
````

对应命令：

```bash
git add .
git commit -m "提交说明"
git push
```

### 1. 工作区

工作区就是我们平时写代码、修改文件的地方。

例如：

```text
index.html
style.css
main.js
```

这些文件所在的项目目录就是工作区。

### 2. 暂存区

暂存区用于临时保存准备提交的修改。

把文件加入暂存区：

```bash
git add 文件名
```

添加所有修改：

```bash
git add .
```

### 3. 本地仓库

本地仓库保存已经提交的版本记录。

提交代码：

```bash
git commit -m "提交说明"
```

### 4. 远程仓库

远程仓库一般指 GitHub、GitLab、Gitee 上的仓库。

推送到远程仓库：

```bash
git push
```

---

## 三、安装 Git

### Windows

下载地址：

```text
https://git-scm.com/
```

安装完成后，打开 Git Bash 或终端，输入：

```bash
git --version
```

如果能看到版本号，说明安装成功。

---

### macOS

查看是否已安装：

```bash
git --version
```

使用 Homebrew 安装：

```bash
brew install git
```

---

### Linux

Ubuntu / Debian：

```bash
sudo apt update
sudo apt install git
```

CentOS：

```bash
sudo yum install git
```

---

## 四、Git 初始配置

第一次使用 Git，需要配置用户名和邮箱。

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

查看配置：

```bash
git config --list
```

示例：

```bash
git config --global user.name "zhangsan"
git config --global user.email "zhangsan@example.com"
```

### 笔记

`--global` 表示全局配置，对当前电脑上的所有 Git 项目生效。

---

## 五、创建 Git 仓库

## 方式一：本地初始化仓库

进入项目目录：

```bash
cd my-project
```

初始化 Git：

```bash
git init
```

初始化后，项目中会生成一个隐藏目录：

```text
.git
```

### 笔记

`.git` 文件夹保存了 Git 的版本信息，不要随便删除。

---

## 方式二：克隆远程仓库

从远程仓库下载代码：

```bash
git clone 仓库地址
```

示例：

```bash
git clone https://github.com/user/demo.git
```

进入项目：

```bash
cd demo
```

---

## 六、查看仓库状态

```bash
git status
```

这个命令非常常用，用来查看当前项目的状态。

常见状态：

| 状态        | 含义              |
| --------- | --------------- |
| untracked | 新文件，还没有被 Git 管理 |
| modified  | 文件被修改了          |
| staged    | 文件已加入暂存区        |
| clean     | 没有需要提交的内容       |

### 学习重点

提交代码前，建议先执行：

```bash
git status
```

这样可以确认哪些文件被修改了。

---

## 七、添加文件到暂存区

添加单个文件：

```bash
git add index.html
```

添加多个文件：

```bash
git add index.html style.css
```

添加所有修改：

```bash
git add .
```

### 笔记

`git add .` 会把当前目录下所有修改都加入暂存区。

---

## 八、提交代码

提交暂存区的内容：

```bash
git commit -m "提交说明"
```

示例：

```bash
git commit -m "添加首页页面"
```

推荐写清楚提交内容：

```bash
git commit -m "新增登录功能"
git commit -m "修复按钮样式问题"
git commit -m "更新 README 文档"
```

### 笔记

提交说明不要随便写 `aaa`、`test`，最好说明这次提交做了什么。

---

## 九、查看提交历史

查看详细提交记录：

```bash
git log
```

简洁查看：

```bash
git log --oneline
```

示例：

```text
a1b2c3d 添加首页页面
e4f5g6h 初始化项目
```

### 笔记

每一次提交都会生成一个 commit id，可以用来回退版本。

---

## 十、查看文件修改内容

查看工作区修改：

```bash
git diff
```

查看暂存区修改：

```bash
git diff --cached
```

### 使用场景

提交之前，可以先用 `git diff` 查看自己改了哪些内容。

---

## 十一、撤销修改

### 1. 撤销工作区修改

```bash
git restore 文件名
```

示例：

```bash
git restore index.html
```

旧写法：

```bash
git checkout -- index.html
```

### 注意

这个操作会丢弃当前文件的修改，需要谨慎使用。

---

### 2. 取消暂存

如果已经执行了 `git add`，但不想提交某个文件，可以取消暂存：

```bash
git restore --staged 文件名
```

示例：

```bash
git restore --staged index.html
```

旧写法：

```bash
git reset HEAD index.html
```

---

## 十二、删除文件

删除文件：

```bash
rm index.html
```

提交删除操作：

```bash
git add .
git commit -m "删除 index.html"
```

也可以使用 Git 命令删除：

```bash
git rm index.html
git commit -m "删除 index.html"
```

---

## 十三、分支管理

分支可以理解为一条独立的开发线。

常见分支：

| 分支            | 说明        |
| ------------- | --------- |
| main / master | 主分支       |
| dev           | 开发分支      |
| feature-login | 登录功能分支    |
| bugfix        | 修复 bug 分支 |

---

### 1. 查看分支

```bash
git branch
```

查看本地和远程分支：

```bash
git branch -a
```

---

### 2. 创建分支

```bash
git branch 分支名
```

示例：

```bash
git branch dev
```

---

### 3. 切换分支

```bash
git switch 分支名
```

示例：

```bash
git switch dev
```

旧写法：

```bash
git checkout dev
```

---

### 4. 创建并切换分支

```bash
git switch -c 分支名
```

示例：

```bash
git switch -c feature-login
```

旧写法：

```bash
git checkout -b feature-login
```

---

### 5. 合并分支

先切换到要合并到的目标分支：

```bash
git switch main
```

合并其他分支：

```bash
git merge feature-login
```

### 笔记

意思是：把 `feature-login` 分支的代码合并到 `main` 分支。

---

### 6. 删除分支

删除本地分支：

```bash
git branch -d 分支名
```

强制删除：

```bash
git branch -D 分支名
```

删除远程分支：

```bash
git push origin --delete 分支名
```

---

## 十四、远程仓库

远程仓库一般托管在：

* GitHub
* GitLab
* Gitee
* Bitbucket

---

### 1. 查看远程仓库

```bash
git remote -v
```

---

### 2. 添加远程仓库

```bash
git remote add origin 仓库地址
```

示例：

```bash
git remote add origin https://github.com/user/demo.git
```

---

### 3. 修改远程仓库地址

```bash
git remote set-url origin 新仓库地址
```

---

### 4. 删除远程仓库地址

```bash
git remote remove origin
```

---

## 十五、推送代码到远程仓库

第一次推送：

```bash
git push -u origin main
```

以后推送：

```bash
git push
```

如果主分支是 `master`：

```bash
git push -u origin master
```

### 笔记

`-u` 的作用是建立本地分支和远程分支的关联，以后可以直接使用 `git push`。

---

## 十六、拉取远程代码

拉取远程代码并合并：

```bash
git pull
```

这个命令相当于：

```bash
git fetch
git merge
```

只获取远程代码，不自动合并：

```bash
git fetch
```

---

## 十七、解决冲突

多人同时修改同一个文件时，可能会出现冲突。

冲突文件中可能会出现：

```text
<<<<<<< HEAD
本地代码
=======
远程代码
>>>>>>> origin/main
```

需要手动修改成正确内容。

修改完成后：

```bash
git add .
git commit -m "解决合并冲突"
```

### 笔记

冲突不是错误，只是 Git 不知道应该保留哪一份代码，需要开发者手动判断。

---

## 十八、版本回退

### 1. 回退到上一个版本

```bash
git reset --hard HEAD^
```

### 2. 回退到指定版本

先查看提交记录：

```bash
git log --oneline
```

然后复制 commit id：

```bash
git reset --hard commit_id
```

示例：

```bash
git reset --hard a1b2c3d
```

### 注意

`--hard` 会丢弃当前工作区修改，使用前一定要确认。

---

## 十九、查看操作记录

如果误操作，可以查看 Git 操作历史：

```bash
git reflog
```

然后恢复到指定版本：

```bash
git reset --hard commit_id
```

### 笔记

`git reflog` 是 Git 的“后悔药”，可以找回很多误操作前的版本。

---

## 二十、.gitignore 文件

`.gitignore` 用来告诉 Git 哪些文件不需要提交。

常见内容：

```gitignore
# 依赖目录
node_modules/

# 日志文件
*.log

# 系统文件
.DS_Store

# 环境变量文件
.env

# 构建目录
dist/
build/

# 编辑器配置
.vscode/
.idea/
```

### 常见使用场景

不应该提交到 Git 的文件：

* 依赖包
* 日志文件
* 临时文件
* 密码、密钥、环境变量文件
* 编译打包后的文件

---

### 已经提交过的文件如何忽略？

如果文件已经被 Git 跟踪，再写入 `.gitignore` 不会立即生效。

需要先取消跟踪：

```bash
git rm -r --cached 文件或目录
```

示例：

```bash
git rm -r --cached node_modules
git commit -m "移除 node_modules 跟踪"
```

---

## 二十一、stash 临时保存修改

当你正在修改代码，但需要临时切换分支时，可以使用 `stash`。

保存当前修改：

```bash
git stash
```

查看 stash 列表：

```bash
git stash list
```

恢复最近一次保存：

```bash
git stash pop
```

恢复但不删除 stash：

```bash
git stash apply
```

删除 stash：

```bash
git stash drop
```

清空所有 stash：

```bash
git stash clear
```

### 笔记

`stash` 适合临时保存没有提交的修改。

---

## 二十二、标签 tag

标签一般用于标记项目版本。

例如：

```text
v1.0.0
v1.1.0
v2.0.0
```

创建标签：

```bash
git tag v1.0.0
```

查看标签：

```bash
git tag
```

推送标签：

```bash
git push origin v1.0.0
```

推送所有标签：

```bash
git push origin --tags
```

删除本地标签：

```bash
git tag -d v1.0.0
```

删除远程标签：

```bash
git push origin --delete v1.0.0
```

---

## 二十三、常用 Git 命令总结

| 命令                   | 作用         |
| -------------------- | ---------- |
| `git init`           | 初始化 Git 仓库 |
| `git clone`          | 克隆远程仓库     |
| `git status`         | 查看仓库状态     |
| `git add .`          | 添加所有修改到暂存区 |
| `git commit -m "说明"` | 提交代码       |
| `git log --oneline`  | 查看提交历史     |
| `git branch`         | 查看分支       |
| `git switch 分支名`     | 切换分支       |
| `git switch -c 分支名`  | 创建并切换分支    |
| `git merge 分支名`      | 合并分支       |
| `git pull`           | 拉取远程代码     |
| `git push`           | 推送代码       |
| `git remote -v`      | 查看远程仓库     |
| `git stash`          | 临时保存修改     |
| `git reset --hard`   | 回退版本       |
| `git reflog`         | 查看操作记录     |

---

## 二十四、常见问题笔记

### 1. git push 失败怎么办？

可能是远程仓库有新代码，本地没有同步。

解决：

```bash
git pull
git push
```

如果出现冲突，需要先解决冲突。

---

### 2. 怎么查看当前在哪个分支？

```bash
git branch
```

带 `*` 的就是当前分支。

---

### 3. 提交说明写错了怎么办？

修改最近一次提交说明：

```bash
git commit --amend -m "新的提交说明"
```

---

### 4. 文件 add 错了怎么办？

```bash
git restore --staged 文件名
```

---

### 5. 怎么把本地分支推送到远程？

```bash
git push -u origin 分支名
```

---

## 二十五、推荐提交规范

提交信息建议使用统一格式：

```text
类型: 提交说明
```

常见类型：

| 类型       | 说明          |
| -------- | ----------- |
| feat     | 新功能         |
| fix      | 修复 bug      |
| docs     | 文档修改        |
| style    | 样式修改        |
| refactor | 代码重构        |
| test     | 测试相关        |
| chore    | 工具、依赖、构建等杂项 |

示例：

```bash
git commit -m "feat: 新增用户登录功能"
git commit -m "fix: 修复登录按钮样式问题"
git commit -m "docs: 更新 Git 教程"
git commit -m "style: 调整首页布局"
```

---

## 二十六、完整操作示例

新建项目：

```bash
mkdir demo
cd demo
git init
```

创建 README 文件：

```bash
echo "# Demo 项目" > README.md
```

查看状态：

```bash
git status
```

添加文件：

```bash
git add .
```

提交代码：

```bash
git commit -m "初始化项目"
```

添加远程仓库：

```bash
git remote add origin https://github.com/user/demo.git
```

设置主分支名称：

```bash
git branch -M main
```

推送代码：

```bash
git push -u origin main
```

---

## 二十七、学习路线

建议按照下面的顺序学习 Git：

### 第一阶段：基础操作

重点掌握：

```bash
git init
git status
git add .
git commit -m "说明"
```

---

### 第二阶段：远程仓库

重点掌握：

```bash
git remote
git push
git pull
git clone
```

---

### 第三阶段：分支管理

重点掌握：

```bash
git branch
git switch
git merge
```

---

### 第四阶段：问题处理

重点掌握：

```bash
git restore
git reset
git stash
git reflog
```

---

## 二十八、Git 日常开发流程

### 个人项目常用流程

```bash
git status
git add .
git commit -m "提交说明"
git push
```

---

### 团队项目常用流程

```bash
git pull
git switch -c feature-login

# 修改代码

git add .
git commit -m "feat: 新增登录功能"
git push -u origin feature-login
```

然后在 GitHub / GitLab / Gitee 上创建 Pull Request 或 Merge Request。

---

## 二十九、重点记忆

Git 最核心的几个命令：

```bash
git status
git add .
git commit -m "提交说明"
git push
git pull
```

Git 最核心的流程：

```text
修改文件 -> 添加到暂存区 -> 提交到本地仓库 -> 推送到远程仓库
```

Git 最重要的思想：

> 每一次 commit 都是一个可以回到的版本节点。

---

## 三十、总结

Git 是开发中非常重要的工具。刚开始学习时，不需要一次性掌握所有命令，先熟悉最常用的流程即可。

日常开发最常用的命令是：

```bash
git status
git add .
git commit -m "提交说明"
git pull
git push
```

掌握这些命令后，再逐步学习分支、合并、冲突、回退和 stash，就可以应对大多数开发场景。

```
```

