---
name: git-commit
description: 安全提交学习代码。当主人说「提交」「commit」「推到 GitHub」「push」时使用：先跑一遍确认没坏，再分类暂存（排除临时产物与备份），按「第N周：主题」格式写 commit message，最后汇报提交号。
---

# 提交学习代码

项目：`D:\Programs\learn`（GitHub `Dean20261987/learn`）。
本机沙箱为 danger-full-access，`git add/commit` 可执行；**push 前先问主人**（推到公开仓库属于对外动作）。

## 一、提交前必做四件事

### 1. 跑一遍，确认没坏

```powershell
cd D:\Programs\learn
python weekN.py
```

exit code 必须是 0。**跑不过就不提交**——提交一个坏状态比不提交更糟。

### 2. 看变更全貌

```powershell
git status --short
git diff --stat
```

把输出分成三类，**分开提交**：

| 类 | 例子 | 提交信息 |
|---|---|---|
| 学习代码 | `week6.py`、`tools.py`、`mytools/`、`mypkg/logstat.py` | `第6周：模块与包、__main__、项目结构（练习A-E）` |
| 视觉/杂项 | `art/*.png`、`art/*.html` | `色块画：…` |
| 配置 | `.gitignore`、`.dsh/skills/` | `工具：新增工作区技能` / `配置：忽略 notes.json` |

### 3. 确认临时产物没被加进去

这些**永远不该进仓库**（`.gitignore` 里应该有）：

```
__pycache__/  *.pyc  *.bak  test.log  info.txt  output*.txt
sample.txt  data.csv  notes.json  迁移交接.md  鲸鱼娘日记.md
```

检查办法：`git status --short` 里出现它们 → 先补 `.gitignore`，别用 `git add .` 硬塞。

> **反面教材**：不要 `git add -A`。它会把备份文件、临时产物、别人的图全吞进来，历史上出现过一次。

### 4. 看看有没有 `.py` 文件是 0 字节

```powershell
Get-ChildItem *.py, mypkg\*.py, mytools\*.py | Where-Object { $_.Length -eq 0 }
```

有输出就说明有文件没保存，先处理再提交。

## 二、提交

```powershell
git add <明确列出的文件>
git commit -m "第N周：<主题>（练习A-E）"
```

message 规范：
- 学习周：`第N周：<主题>`，练习全做完加 `（练习A-E）`
- 其他：`<类别>：<做了什么>`
- 一行说完，不加句号，不复述代码

## 三、推送（先问主人）

```powershell
git push
```

推完核对：

```powershell
git log --oneline -3
git status --short     # 应该干净
```

## 四、汇报格式

```
提交：<短 hash>  <message>
文件：N 个（列出）
剩余未提交：<有/无，以及为什么>
```

## 五、红线

- 不 `git push --force`、不 `git reset --hard`、不改写历史
- 不动 `鲸鱼娘日记.md`、`本鲸的日记.md`、`.credentials` 之类私密文件（本来也在 gitignore 里）
- 主人没说提交时不主动提交
- 提交失败（hook/冲突）→ 如实贴报错，不要偷偷 `--no-verify`
