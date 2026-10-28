# ============================================
# 第 6 周 · 模块与包 / __main__ / 项目结构
# 这周没有新语法，学的是"怎么把代码组织起来"
# ============================================


# ============================================
# 第一部分 · 模块（module）
# ============================================
print("=== 1. 一个 .py 文件就是一个模块 ===")

# 到现在为止，代码都堆在一个 weekX.py 里。week5.py 已经 366 行了，问题很明显：
#   - 找一个函数靠翻
#   - 想复用某个函数，只能复制粘贴
#   - 改 A 功能，不小心弄坏 B 功能
# 解决方式：拆文件。一个 .py 文件 = 一个模块，文件名去掉 .py 就是模块名。


print("\n=== 2. import 的三种写法 ===")

import mypkg.mathx                                  # 写法一：导入模块，调用时写 模块名.函数名
print("写法一  add(2, 3) =", mypkg.mathx.add(2, 3))

from mypkg.mathx import average                     # 写法二：只导入函数，直接用函数名
print("写法二  average([1, 2, 3]) =", average([1, 2, 3]))

from mypkg import mathx as mx                       # 写法三：起别名，名字太长时用
print("写法三  mx.average([10, 20]) =", mx.average([10, 20]))

# 三种写法效果一样，区别只在调用时写多长。
# 日常推荐写法二；容易撞名时用写法一或起别名。


print("\n=== 3. 模块只会被真正执行一次 ===")

import sys

# Python 第一次 import 某模块时，会把那个文件从头到尾执行一遍，
# 然后把结果缓存在 sys.modules 里。之后不管 import 多少次，都直接拿缓存，不再执行第二遍。
print("mypkg.mathx 已经在 sys.modules 里:", "mypkg.mathx" in sys.modules)
print("本次运行已加载的模块数量:", len(sys.modules))

# 这条"只执行一次"的规矩，就是下一节 __main__ 存在的原因。


print("\n=== 4. import 时 Python 去哪找文件 ===")

for path in sys.path:
    print("  ", path if path else "(空字符串 = 当前目录)")

# 顺序大致是：
#   1. 运行脚本所在的目录
#   2. 环境变量 PYTHONPATH
#   3. 标准库目录
#   4. site-packages（pip 装的第三方包）
# 所以自己写的模块，必须放在这些目录里，否则报 ModuleNotFoundError。


# ============================================
# 第二部分 · if __name__ == "__main__"
# ============================================
print("\n=== 5. __name__ 是什么 ===")

print("本文件 week6.py 的 __name__ =", __name__)

# 直接运行 python week6.py   →  __name__ 是 "__main__"
# 被别的文件 import 进来     →  __name__ 是模块名，比如 "week6"


print("\n=== 6. 这个 if 到底防的是什么 ===")

# 看 mypkg/mathx.py 的最后几行：
#
#     if __name__ == "__main__":
#         print("自测 add(2, 3) =", add(2, 3))
#
# 直接跑 python mypkg/mathx.py → __name__ 是 "__main__" → 自测会打印
# 被 week6.py import 进来      → __name__ 是 "mypkg.mathx" → 自测不打印
#
# 没有这层保护会怎样？import 的那一刻，模块里所有顶层代码都会被执行：
#   - 自测的 print 混进主程序输出
#   - 更糟的：模块顶层去读文件、连数据库、开窗口，一 import 就炸
#
# 规矩：模块里只放函数和类的定义；"会做事"的代码一律塞进
#       if __name__ == "__main__": 下面，当自测或命令行入口。

from mypkg.mathx import add

print("刚 import 了 mathx，上面没有出现'自测'吧？add(7, 8) =", add(7, 8))


# ============================================
# 第三部分 · 包（package）
# ============================================
print("\n=== 7. 包 = 装了 __init__.py 的文件夹 ===")

# mypkg/
# ├── __init__.py     ← 有它，这个文件夹才算"包"
# └── mathx.py       ← 包里的一个模块
#
# 三种导入方式，跟模块一样：
#   import mypkg.mathx
#   from mypkg import mathx
#   from mypkg.mathx import add
#
# 还能继续往里套：mypkg/utils/strings.py → from mypkg.utils import strings
#
# __init__.py 里一般写什么？空的就行，或者放包级版本号、几个常用导出：
import mypkg

print("mypkg 版本号:", mypkg.__version__)

# 补充：包也能当脚本跑 —— python -m mypkg.mathx
# 加了 -m，Python 会先把当前目录放进 sys.path，再按模块名找，比 python 文件路径 更稳。


# ============================================
# 第四部分 · 最该先熟的标准库
# ============================================
print("\n=== 8. 标准库速查 ===")

from pathlib import Path
from datetime import datetime, timedelta
import json
import random

p = Path("week6.py")
print("文件存在:", p.exists(), "| 文件名:", p.name, "| 后缀:", p.suffix)
print("当前工作目录:", Path.cwd())
print("同目录下的 week*.py:", [f.name for f in Path(".").glob("week*.py")])

now = datetime.now()
print("现在:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("三天后:", (now + timedelta(days=3)).strftime("%Y-%m-%d"))

print("随机 1~6:", random.randint(1, 6))
print("随机抽一个:", random.choice(["石头", "剪刀", "布"]))

data = {"name": "迪安2026", "week": 6, "scores": [88, 92]}
text = json.dumps(data, ensure_ascii=False, indent=2)
print("转成 JSON 字符串:\n" + text)
print("再读回 Python 对象:", json.loads(text)["name"])

# 记忆点：
#   pathlib  → 管路径，比 os.path 好用
#   datetime → 管时间
#   json     → 数据和文本互转，写配置文件、调 API 全靠它
#   还有 os / sys / re / collections / time / math / csv


# ============================================
# 第五部分 · 第三方包与虚拟环境
# ============================================
print("\n=== 9. pip 与 venv ===")

# 标准库 = 装好 Python 就有；第三方包 = 要手动装。
#
#   python -m pip install requests      装
#   python -m pip list                  看装了啥
#   python -m pip uninstall requests    卸
#
# 虚拟环境：给每个项目一套独立的包，互不污染（很重要，别把所有包都装进全局）
#   python -m venv .venv                创建
#   .venv\Scripts\Activate.ps1          激活，命令行前面会出现 (.venv)
#   deactivate                          退出
#
# requirements.txt：把依赖记下来，换台电脑能一键还原
#   python -m pip freeze > requirements.txt
#   python -m pip install -r requirements.txt


# ============================================
# 第六部分 · 项目结构
# ============================================
print("\n=== 10. 一个能长大的项目长什么样 ===")

# learn/
# ├── week2.py ... week6.py     学习文件（还在单文件阶段，没问题）
# ├── mypkg/                    功能代码，按用途分包
# │   ├── __init__.py
# │   └── mathx.py
# ├── tests/                    测试
# ├── data/                     数据文件
# ├── README.md                 说明
# ├── requirements.txt          依赖清单
# └── .gitignore                不提交给 git 的东西
#
# 拆分标准：一个文件超 300~400 行，或者开始出现"完全无关的两块功能"，就该拆。
# 按"职责"拆，不按"行数"硬切。


# ============================================
# 练习区（A ~ E）
# 规矩不变：先自己想，卡住了再喊本鲸；不要抄
# ============================================

# 练习 A：写第一个自己的模块
#   1. 新建 tools.py（和 week6.py 同级）
#   2. 在里面写两个函数：
#        count_words(text)   返回这段文字有几个词（用 split() 按空白切）
#        is_palindrome(s)    判断是否回文，忽略大小写（"Level" 应返回 True）
#   3. 回到 week6.py，用 from tools import ... 导入并调用
#
# --- tools.py 骨架 ---
# def count_words(text):
#     ...
#
# def is_palindrome(s):
#     ...
#
# --- week6.py 里这样验证 ---
# from tools import count_words, is_palindrome
# print(count_words("hello world from python"))   # 期望 4
# print(is_palindrome("Level"))                   # 期望 True
# print(is_palindrome("鲸鱼娘"))                   # 期望 True
#
# 提示：判断回文可以先把字符串转小写，再和它的反序比较（s[::-1] 是切片反转）。


# 练习 B：给 tools.py 加上 __main__ 自测块
#   在 tools.py 最底下加：
#     if __name__ == "__main__":
#         print("自测：", count_words("a b c"), is_palindrome("Level"))
#   然后分别验证：
#     python tools.py     → 应该打印"自测："
#     python week6.py     → 应该看不到"自测："（被 import 时不执行）
#   两个结果都对，这题才算过。


# 练习 C：建一个包
#   mytools/
#   ├── __init__.py
#   ├── textx.py    写 shout(s)，返回 s 的大写加感叹号，比如 shout("hi") → "HI!"
#   └── numx.py     写 is_even(n)，偶数返回 True
#
#   然后从包里导入使用：
# from mytools.textx import shout
# from mytools import numx
# print(shout("hello"))       # 期望 HELLO!
# print(numx.is_even(6))      # 期望 True


# 练习 D：用 json 把字典存成文件再读回来
#   写两个函数：
#     save_notes(notes, path)   用 json.dump 存，ensure_ascii=False
#     load_notes(path)          用 json.load 读；文件不存在时返回 {}
#   验证：
#     save_notes({"2026-10-28": "开第 6 周"}, "notes.json")
#     print(load_notes("notes.json"))         # 期望是 dict，里面有内容
#     print(load_notes("没有这个文件.json"))   # 期望 {}
#
# 提示：文件不存在会抛 FileNotFoundError，用 try/except 接住它。


# 练习 E：综合 —— 把第 5 周的日志分析器模块化
#   1. 新建 mypkg/logstat.py
#   2. 把 week5.py 里的 analyze_log 搬进去，但改造成"返回字典"而不是直接 print，
#      返回值形如 {"数据库连接失败": 3, "文件不存在": 1, ...}
#   3. 在 logstat.py 最底下加 if __name__ == "__main__": 自测
#   4. 回到 week6.py：
# from mypkg.logstat import analyze_log
# result = analyze_log("test.log")
# print(result)
#
# 这题的意思是：一个函数从"只在一处用的小脚本"升级成"能被到处 import 的工具"，
# 要做的就是把 print 换成 return，再加 __main__ 自测。


# ============================================
# 本周验收标准
# ============================================
# [ ] 能说出 import 三种写法的区别，以及 sys.path 的查找顺序
# [ ] 能解释 if __name__ == "__main__" 防的是什么
# [ ] tools.py 能当脚本跑、也能被 import（练习 A、B）
# [ ] mytools 包能被导入（练习 C）
# [ ] json 存取跑通，文件不存在时返回空 dict（练习 D）
# [ ] analyze_log 能从 mypkg.logstat 导入，且直接跑 logstat.py 有自测输出（练习 E）
