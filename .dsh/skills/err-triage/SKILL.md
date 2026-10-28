---
name: err-triage
description: Python 报错分诊。当主人贴出 traceback 或说「报错了」「跑不起来」时，按固定顺序定位真因（保存状态→文件位置→工作目录→缩进→名字拼写），给出结论+原因+修法+防再犯。适用于 Windows + VS Code + Python 3.12 环境。
---

# 报错分诊

目标：**用最少的问题定位真因**，不要一上来就改代码。

## 第一步：只读三样东西

1. **最后一行**：`SyntaxError` / `IndentationError` / `ModuleNotFoundError` / `ImportError` / `FileNotFoundError` / `NameError` / `TypeError` / `AttributeError` / `KeyError` / `UnicodeDecodeError`
2. **报错里的绝对路径**：那一串就是「程序以为自己在哪」
3. **行号和它上面 2 行**：Python 的缩进/语法错误经常指在「退出错误块」的那一行，真凶在上一行

## 第二步：五查清单（按命中率排序）

| 顺序 | 查什么 | 命令 | 命中表现 |
|---|---|---|---|
| 1 | **文件保存了吗** | `Get-Item <f> \| Select Length` | 0 字节 / 行数比预期少 → 编辑器里有、磁盘上没有 |
| 2 | **在哪个目录跑** | `Get-Location` 或看 traceback 路径 | 路径不是 `D:\Programs\learn` |
| 3 | **文件名对不对** | `Get-ChildItem *.py` | 成了 `x.py.txt`；或撞了标准库名（`random.py`、`json.py`、`re.py`） |
| 4 | **缩进** | 看 `def`/`if` 后一行是否有 4 空格 | `IndentationError`、`'return' outside function` |
| 5 | **名字拼写/全角** | 对照 `def` 的名字 | `ｃｏｕｎｔ` 全角、少写 `s`、大小写不一致 |

## 第三步：常见错误的真因对照

| 报错 | 真因（按概率） | 不是这个 |
|---|---|---|
| `ModuleNotFoundError: No module named 'x'` | ①cwd 不对 ②文件名后缀被藏 ③真没写这个文件 | 不是「Python 没装包」 |
| `ImportError: cannot import name 'f' from 'm'` | ①文件 0 字节/没保存 ②函数名不符 ③函数被嵌进别的函数里 | 不是「模块坏了」 |
| `SyntaxError` 指着一行中文 | 全角标点 `（）`、`，`、`：` | 不是「中文不能写」 |
| `SyntaxError: 'return' outside function` | `return` 缩进退回第 0 列 | 不是 return 写错 |
| `FileNotFoundError: 'x.txt'` | 相对路径按 cwd 解析，cwd 不是脚本目录 | 不是文件没生成 |
| `UnicodeDecodeError` 读中文文件 | `open()` 没写 `encoding="utf-8"` | — |
| `NameError: name 'x' is not defined` | ①`from m import y` 后直接用 `x` ②变量名拼错 ③用在了定义之前 | — |
| `TypeError: 'NoneType' object is not ...` | 函数忘了 `return`，默认返回 None | — |
| `AttributeError: module 'x' has no attribute 'y'` | 名字在模块里没定义；或装了两个同名模块 | — |

## 第四步：给主人的回复模板

```
结论：<一句话，真因是什么>
证据：<哪个命令/哪个数字证明了它>
修法：<具体到第几行、改成什么>
防再犯：<一条习惯或设置>
```

**禁止**：
- 说「应该是……你试试」——先查证再下结论
- 改主人的学习代码（只指出位置，让他自己改）
- 一次抛五条可能性让主人自己挑

## 第五步：修完必须复验

改完要**跑一遍**确认，不能只看代码说「这样应该就好了」。复验命令和期望输出一起给出。

## 环境备忘（本机）

- Python：`D:\Programs\Python\Python312\python.exe`（3.12.10）
- 项目：`D:\Programs\learn`，**所有命令先 `cd` 到这里**
- VS Code 必须「文件 → 打开文件夹」，否则集成终端 cwd 是 VS Code 安装目录
- 终端中文乱码是控制台编码问题，不是代码问题：`chcp 65001` 或 `$env:PYTHONIOENCODING="utf-8"`
