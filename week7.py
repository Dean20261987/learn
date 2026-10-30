# ============================================
# 第 7 周 · 测试（pytest）与项目结构
# 这周的新东西不多，但要改你写代码的习惯：
# 从"跑一次看着对"变成"随时能证明它没坏"
# ============================================
# 运行方式（注意必须在 learn 目录下）：
#   cd D:\Programs\learn
#   python week7.py
# ============================================

import json
import pathlib
import tempfile

import pytest


# ------------------------------------------------------------
# 演示辅助：把一段测试代码写到临时目录，用 pytest 真跑一遍
# （讲义自己也需要"能跑"，不然就是纸上谈兵）
# ------------------------------------------------------------
_demo_seq = 0


def run_demo(title, source):
    """把 source 写成临时测试文件，用 pytest 跑，返回退出码。"""
    print(f"\n--- {title} ---")
    print("测试文件内容：")
    for line in source.strip().splitlines():
        print("    " + line)
    print("--- pytest 输出 ---")
    # 每次用不同的文件名：pytest 会把测试模块缓存进 sys.modules，
    # 同名不同路径的第二个文件会报 "import file mismatch"。
    global _demo_seq
    _demo_seq += 1
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / f"test_demo_{_demo_seq}.py"
        path.write_text(source, encoding="utf-8")
        code = pytest.main([str(path), "-q", "--no-header", "-p", "no:cacheprovider"])
    print("--- 退出码:", int(code), "---")
    return int(code)


# ============================================
# 第一部分 · 为什么需要测试
# ============================================
print("=== 1. 一个真实会发生的悲剧 ===")

# 你第 5 周写过一个求平均分的功能。现在假设它被"优化"了。


def average_v1(nums):
    """第 5 周的版本：空列表返回 0（有 if 保护）"""
    if not nums:
        return 0
    return sum(nums) / len(nums)


def average_v2(nums):
    """某次重构后的版本：为了"少一次判断"，把 if 去掉了"""
    total = 0
    for n in nums:
        total += n
    return total / len(nums)


print("v1 算 [85, 92, 78]：", average_v1([85, 92, 78]))
print("v1 算 []        ：", average_v1([]))

try:
    print("v2 算 []        ：", average_v2([]))
except ZeroDivisionError as e:
    print("v2 算 []        ：炸了 ——", type(e).__name__, e)

# 问题不在 v2 写错了，而在于：**你在改的时候，没有任何东西提醒你"空列表会炸"**。
# 如果当时有一个测试：
#     def test_average_empty():
#         assert average([]) == 0
# 那么改完一运行，红灯立刻亮，你根本不会把 bug 提交上去。
#
# 这类"以前好的功能，改着改着坏了"的问题，叫回归（regression）。
# 测试的唯一使命就是：让回归在变成事故之前暴露出来。

print("\n记忆点：测试不是给老师看的作业，是给未来的自己买的保险。")


# ============================================
# 第二部分 · assert 与最小测试
# ============================================
print("\n=== 2. 测试的全部语法就是 assert ===")

# assert 后面跟一个"应该为真"的表达式。为真 → 什么都不发生；为假 → 抛 AssertionError。
assert 1 + 1 == 2
assert "abc".upper() == "ABC"
print("两行 assert 都通过了，什么都没输出 —— 这就是「绿灯」")

# 为假会怎样？用一个人为写错的期望值来试：
try:
    assert average_v1([85, 92, 78]) == 90, "平均值应该是 85.0，不是 90"
except AssertionError as e:
    print("断言失败 ——", type(e).__name__, ":", e)

# 注意：上面抛的是 AssertionError。而如果函数自己崩了，抛的是别的：
try:
    average_v2([])
except ZeroDivisionError as e:
    print("函数崩溃 ——", type(e).__name__, ":", e)

print("两者是完全不同的两种红灯：")
print("  断言失败 = 函数算完了，但结果和期望不符  → 逻辑错")
print("  抛异常   = 函数根本没算完就中断了        → 实现错")

print("\n记忆点：pytest 没有魔法，它只是帮你批量执行 assert，并把失败信息排版好。")


# ============================================
# 第三部分 · pytest 是怎么找到测试的
# ============================================
print("\n=== 3. 命名约定：pytest 只认这两个前缀 ===")

# pytest 不是靠"你告诉它测什么"，而是靠扫描目录 + 命名约定：
#
#   文件：test_*.py  或  *_test.py
#   函数：test_*
#   类  ：Test*（首字母大写，且不能有 __init__）
#
# 不符合命名的文件/函数，pytest 会**直接跳过，连提示都没有**。
# 这是新手第一个坑：写了个 check_add() 然后说"pytest 没跑我的测试"。

print("""推荐布局：
    D:\\Programs\\learn\\
    ├── week7.py            ← 讲义（不参与测试）
    ├── mypkg\\              ← 被测的代码
    │   ├── __init__.py
    │   ├── mathx.py
    │   ├── logstat.py
    │   └── notes.py        ← 练习 C 要新建
    └── tests\\              ← 全部测试放这里
        ├── conftest.py     ← 共享的 fixture / 配置
        ├── test_mathx.py
        ├── test_numx.py
        └── test_logstat.py""")

print("""
两种运行方式：
    python -m pytest -q          ← 推荐：把当前目录放进 sys.path，import 才不会失败
    python -m pytest tests\\ -v    ← 只跑 tests 目录，-v 显示每个用例名
不要直接敲 pytest（除非确认它在 PATH 里，且 cwd 也对）""")

print("记忆点：pytest 靠「名字」找测试。名字不对 = 静默跳过，比报错更难查。")


# ============================================
# 第四部分 · 一个测试的三段式
# ============================================
print("\n=== 4. 三段式：准备 → 执行 → 断言 ===")


def test_style_example():
    # 1. 准备（arrange）：把要用的数据造出来
    scores = [85, 92, 78]

    # 2. 执行（act）：调用被测函数，**只调一次**
    result = average_v1(scores)

    # 3. 断言（assert）：拿实际值和期望值比
    assert result == 85.0


# 上面这个函数长得很像"普通代码"，但它是测试：名字以 test_ 开头，里面没有 print。
# 三个部分分清楚，好处是失败时你能一眼看出是"数据造错了"还是"函数算错了"。

print("test_style_example 检查 85 / 92 / 78 的平均值 —— 平均是", average_v1([85, 92, 78]))

# 反面教材（不要这样写）：
#   def test_bad():
#       assert average_v1([85, 92, 78]) == 85.0
#       assert average_v1([60]) == 60.0
#       assert average_v1([]) == 0
# 三个断言塞一个测试里，第一个失败后面就不跑了，你永远不知道另外两个是不是也坏着。
# 一个测试 = 一个概念 = 一个失败点。

print("记忆点：一个测试只测一件事。失败时你要能一眼说出「哪条规则被破坏了」。")

# 现在真跑一个绿的和一个红的：
run_demo("绿灯：空列表有保护", """
def average(nums):
    if not nums:
        return 0
    return sum(nums) / len(nums)

def test_average_normal():
    assert average([85, 92, 78]) == 85.0

def test_average_empty():
    assert average([]) == 0
""")

run_demo("红灯：空列表没保护（同一个测试，只是实现被改了）", """
def average(nums):
    return sum(nums) / len(nums)

def test_average_empty():
    assert average([]) == 0, "空列表应该返回 0"
""")


# ============================================
# 第五部分 · 读懂红灯
# ============================================
print("\n=== 5. 红灯不是骂你，它把现场留给你了 ===")

# 上面那个红灯的输出里有四块信息，逐块看：
#
#   ① 汇总行      FAILED test_demo.py::test_average_empty - ZeroDivisionError
#                 告诉你：哪个文件、哪个函数、什么错
#   ② 分隔线      _______ test_average_empty _______
#                 定位到具体函数
#   ③ 代码现场    assert average([]) == 0
#                 把出错那一行原样打印出来
#   ④ 符号提示    上面那次是 ZeroDivisionError（异常），不是 AssertionError
#                 如果是断言失败，会显示 E  assert 3 == 4 和左右两边的值
#
# 两种红灯要分清：
#   断言失败（AssertionError）→ 函数跑完了，但结果和你期望的不一样 → 逻辑错
#   其他异常（ZeroDivisionError / TypeError …）→ 函数根本没跑完 → 实现错
# 这两种的排查方向完全不同，别混。

print("""记忆点：看到红灯先读①②③④四块，不要急着改代码。
       异常 ≠ 断言失败，前者是"崩了"，后者是"算错了"。""")


# ============================================
# 第六部分 · 参数化
# ============================================
print("\n=== 6. 参数化：一组数据测十个用例 ===")

# 假设要测 is_even。最笨的写法是复制五遍函数，只改数字——那是体力活，而且漏测。
# pytest 的 parametrize 让你把"输入 → 期望"写成表：

run_demo("参数化：五组数据，五个独立用例", """
import pytest

def is_even(n):
    return n % 2 == 0

@pytest.mark.parametrize("n, expected", [
    (0, True),
    (6, True),
    (-4, True),
    (7, False),
    (-3, False),
])
def test_is_even(n, expected):
    assert is_even(n) is expected
""")

# 注意两点：
#   ① 第一个参数是**字符串**，写的是后面函数参数的名字，多个用逗号隔开
#   ② 用 is 而不是 == 比布尔值（True/False 是单例，is 更严格也更清楚）
#
# 好处：跑完是 5 个用例，不是 1 个。哪个数据挂了，报告里直接写 [7-False]。

print("记忆点：能写成表格的测试，就不要复制粘贴。表越大，参数化越值。")


# ============================================
# 第七部分 · 测异常
# ============================================
print("\n=== 7. 有些代码的正确行为就是「炸」 ===")

# 比如"读一个不存在的文件"——正确行为是抛 FileNotFoundError，不是返回空字符串。
# 这种时候你要断言"它确实抛了"，而不是断言返回值。

run_demo("两种异常测试", """
import json
import pytest

def load_json(text):
    return json.loads(text)

def test_bad_json_raises():
    # 坏 JSON 必须抛 JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        load_json("{不是合法JSON")

def test_bad_json_message():
    # 还能顺便检查错误消息里有没有关键字
    with pytest.raises(json.JSONDecodeError, match="Expecting"):
        load_json("{不是合法JSON")

def test_good_json_ok():
    # 反面对照：正常输入不该抛
    assert load_json('{"a": 1}') == {"a": 1}
""")

# with 语句的语义：这段代码必须抛指定类型的异常，否则测试失败。
# 忘了 with 就直接写 load_json("{坏")，异常会冲出去把整个测试标记成 ERROR。

print("记忆点：测「该炸的时候炸了」用 pytest.raises；测「不该炸的时候没炸」就是普通断言。")
# ============================================
# 第八部分 · fixture 与 tmp_path
# ============================================
print("\n=== 8. fixture：把「每次都要准备的东西」抽出来 ===")

# 测试经常需要同一份准备数据，或者一个临时目录。
# pytest 用 fixture（夹具）解决：函数上加 @pytest.fixture，测试函数把名字写成参数就自动注入。
#
# 最常用的内置 fixture 是 tmp_path —— 每次测试给你一个全新的临时目录，
# 测试结束自动清理。写文件类测试必须用它，否则会把垃圾留在项目目录里。

run_demo("用 tmp_path 做文件往返测试", """
import json

def save_notes(notes, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def load_notes(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def test_roundtrip(tmp_path):
    # tmp_path 是一个 pathlib.Path，指向本次测试专属的空目录
    path = tmp_path / "notes.json"
    data = {"2026-10-30": "第7周开工"}
    save_notes(data, path)
    assert load_notes(path) == data

def test_missing_returns_empty(tmp_path):
    assert load_notes(tmp_path / "没有这个文件.json") == {}
""")

# 自己写 fixture 的样子（讲义不跑，看清楚结构就行）：
#
#   import pytest
#
#   @pytest.fixture
#   def sample_notes():
#       return {"2026-10-30": "第7周开工", "2026-10-31": "继续"}
#
#   def test_something(sample_notes):        # ← 参数名 = fixture 名
#       assert len(sample_notes) == 2
#
# fixture 还可以写 yield，做"用前准备、用后清理"：
#   @pytest.fixture
#   def temp_log(tmp_path):
#       p = tmp_path / "test.log"
#       p.write_text("ERROR 数据库连接失败\\n", encoding="utf-8")
#       yield p          # ← 测试用 p
#       # yield 后面的代码在测试结束后执行（这里其实不用清理，tmp_path 会自动删）

print("记忆点：tmp_path 是文件测试的标配。不用它 = 测试会污染你的项目目录。")


# ============================================
# 第九部分 · 给已有模块补测试
# ============================================
print("\n=== 9. 拿你写过的模块练手 ===")

# 下面用"测试的思维"检查第 6 周的四个模块。
# 每个 try/except 就是一条声明：这个函数"应该"这样表现。

# 先确认 cwd 对，否则 import 会失败（第 6 周踩过这个坑）
if not pathlib.Path("mypkg").is_dir():
    raise SystemExit(
        "请在项目根目录下运行：\n"
        "    cd D:\\Programs\\learn\n"
        "    python week7.py"
    )
# 如果哪天它不这样了，这里会打印 ❌ —— 这就是测试的价值。

from mypkg import mathx
from mypkg.logstat import analyze_log
from mytools import numx, textx

checks = []


def check_equal(desc, actual, expected):
    if actual == expected:
        checks.append((desc, True, ""))
    else:
        checks.append((desc, False, f"期望 {expected!r}，实际 {actual!r}"))


def check_raises(desc, fn, exc_type):
    try:
        fn()
    except exc_type:
        checks.append((desc, True, ""))
    except Exception as e:
        checks.append((desc, False, f"抛了 {type(e).__name__}，期望 {exc_type.__name__}"))
    else:
        checks.append((desc, False, f"应该抛 {exc_type.__name__}，但没有抛"))


check_equal("mathx.add(2, 3) == 5", mathx.add(2, 3), 5)
check_equal("mathx.average([1, 2, 3]) == 2.0", mathx.average([1, 2, 3]), 2.0)
check_equal("mathx.average([]) == 0（空列表保护）", mathx.average([]), 0)
check_equal("numx.is_even(-4) is True", numx.is_even(-4), True)
check_equal("numx.is_even(7) is False", numx.is_even(7), False)
check_equal('textx.shout("hi") == "HI!"', textx.shout("hi"), "HI!")
check_equal(
    "analyze_log('test.log') 统计正确",
    analyze_log("test.log"),
    {"数据库连接失败": 3, "文件不存在": 1, "权限不足": 1},
)
check_raises(
    "analyze_log('不存在.log') 抛 FileNotFoundError",
    lambda: analyze_log("绝对不存在的文件.log"),
    FileNotFoundError,
)


for desc, ok, err in checks:
    print(f"  {'✅' if ok else '❌'}  {desc}" + (f"   ← {err}" if err else ""))

print(f"\n  通过 {sum(1 for _, ok, _ in checks if ok)} / {len(checks)} 条")

print("""
注意这是「手工版测试」：用 if 比、自己记结果、自己数通过几条。
pytest 做的本质是同一件事，只是它会自动发现用例、自动执行、
失败时打印漂亮报告、并且用退出码告诉 CI「这次过没过」。
练习 A–E 就是把这种手工 check 升级成真正的 pytest 用例。""")

print("记忆点：测试的第一价值不是「发现新 bug」，是「防止旧功能变坏」。")


# ============================================
# 第十部分 · 项目结构
# ============================================
print("\n=== 10. 让项目能长大：tests\\ 与 pyproject.toml ===")

print("""现在的结构（第 6 周结束）：
    learn\\
    ├── week2.py … week6.py     ← 讲义，一个个独立脚本
    ├── tools.py                 ← 散在根目录
    ├── mypkg\\  mytools\\         ← 你的两个包
    └── notes.json  test.log     ← 脚本产物

第 7 周结束应该长这样：
    learn\\
    ├── week2.py … week7.py     ← 讲义，位置不动
    ├── mypkg\\
    │   ├── __init__.py
    │   ├── mathx.py
    │   ├── logstat.py
    │   └── notes.py            ← 新增：从 week6.py 搬出来的 save/load_notes
    ├── mytools\\                ← 位置不动
    ├── tests\\                  ← 新增：所有测试
    │   ├── conftest.py         ← 共享 fixture
    │   ├── test_mathx.py
    │   ├── test_numx.py
    │   ├── test_notes.py
    │   └── test_logstat.py
    └── pyproject.toml          ← 新增：告诉工具"这个项目是什么、怎么跑测试\"""")

print("""为什么测试要单独放 tests\\，不跟源码混在一起：
    ① 源码目录只放"要被 import 的东西"，测试永远不会被产品代码 import
    ② 打包/发布时可以直接排除 tests\\，不用一个个挑
    ③ 一个源码文件对应一个 test_*.py，找起来按名字对得上
    ④ pytest 默认就在 tests\\ 里扫，不会去翻 week*.py 讲义（那些一 import 就打印一大堆）""")

print("""pyproject.toml 最小可用版本（复制到 learn\\pyproject.toml）：
    [project]
    name = "learn"
    version = "0.1.0"
    requires-python = ">=3.12"

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    addopts = "-q"

加了 [tool.pytest.ini_options] 之后，直接敲 python -m pytest 就会：
    · 只在 tests\\ 里找测试
    · 默认 -q（简洁输出）
其他参数不用背，`python -m pytest --help` 随时查。""")

print("""conftest.py 是什么：
    它不是一个测试文件，是 pytest 的"本地配置 + 共享 fixture 仓库"。
    放在 tests\\ 下，pytest 会自动加载，里面写的 fixture 同一目录下所有测试都能用。
    空文件也有用：它标记"从这一层开始算测试根目录"。""")

print("记忆点：结构不是给别人看的，是给「三个月后的你」看的。目录一乱，测试先废。")


# ============================================
# 练习区（A ~ E）
# ============================================
print("\n" + "=" * 60)
print("练习区（A ~ E）")
print("=" * 60)
print("""
五道练习的完整要求、骨架、提示、期望输出，都写在 week7.py 末尾的注释里
（用 VS Code 打开往下翻）。运行时不打印，因为讲义只负责讲，题要你自己看。

顺序与目标：
    A  写第一个测试文件 tests\\test_mathx.py              → 3 个用例
    B  参数化测 is_even（五组数据）                      → 5 个用例
    C  把 save/load_notes 搬进 mypkg\\notes.py，测坏 JSON → 1 个用例
    D  用 tmp_path 做文件往返测试                        → 2 个用例
    E  给 logstat 写三个用例 + 收尾 tests\\ / pyproject  → 3 个用例

全部做完跑：
    cd D:\\Programs\\learn
    python -m pytest -q

期望：14 passed（A3 + B5 + C1 + D2 + E3），退出码 0。
""")

# 练习 A：写第一个测试文件
#   1. 新建 tests\ 目录，里面新建 test_mathx.py
#   2. 测 mypkg.mathx 的两个函数：
#        add(2, 3) == 5
#        average([1, 2, 3]) == 2.0
#        average([]) == 0          ← 别忘了这条边界
#   3. 三个测试写三个函数，不要塞一个里
#
# --- tests\test_mathx.py 骨架 ---
# from mypkg.mathx import add, average
#
#
# def test_add():
#     assert add(2, 3) == ...
#
#
# def test_average_normal():
#     ...
#
#
# def test_average_empty():
#     ...
#
# 提示：avg 的三条里有一条是"边界"，想想第 6 周 mathx.py 里那个 `if not numbers`
# 验证：python -m pytest tests/test_mathx.py -q
#       期望 3 passed
# 常见坑：
#   ModuleNotFoundError: No module named 'mypkg'
#       → 没在 learn 目录下跑，或者用了 pytest 而不是 python -m pytest


# 练习 B：参数化测 is_even
#   用 @pytest.mark.parametrize 一次覆盖五组数据：
#       0 → True、6 → True、-4 → True、7 → False、-3 → False
#   文件：tests\test_numx.py
#
# --- 骨架 ---
# import pytest
# from mytools.numx import is_even
#
#
# @pytest.mark.parametrize("n, expected", [
#     (0, True),
#     ...
# ])
# def test_is_even(n, expected):
#     assert is_even(n) is expected
#
# 提示：装饰器里第一个参数是字符串，写的是下面函数的参数名
# 验证：python -m pytest tests/test_numx.py -q
#       期望 5 passed
# 常见坑：
#   TypeError: test_is_even() missing 2 required positional arguments
#       → 参数名写错（"n, expected" 里的名字必须和函数签名一致）
#   跑出 1 passed 而不是 5 passed
#       → 忘了 @pytest.mark.parametrize 这行，或者拼成了 @pytest.parametrize


# 练习 C：把 notes 搬进包，然后测"坏 JSON 会炸"
#   1. 把 week6.py 里的 save_notes / load_notes 两个函数搬进新文件 mypkg\notes.py
#      （week6.py 里的原件保留，不要删，那是讲义）
#   2. 在 tests\test_notes.py 里用 pytest.raises 测：
#        读一个内容为 `{不是合法JSON` 的文件，必须抛 json.JSONDecodeError
#
# --- mypkg\notes.py 骨架 ---
# """笔记的 json 存取"""
# import json
#
#
# def save_notes(notes, path):
#     ...
#
#
# def load_notes(path):
#     ...
#
# --- tests\test_notes.py 骨架 ---
# import json
# import pytest
# from mypkg.notes import load_notes
#
#
# def test_bad_json_raises(tmp_path):
#     p = tmp_path / "bad.json"
#     p.write_text("{不是合法JSON", encoding="utf-8")
#     with pytest.raises(...):
#         load_notes(p)
#
# 提示：json 模块里的异常类叫 JSONDecodeError；open() 接受 pathlib.Path，不用转字符串
# 验证：python -m pytest tests/test_notes.py -q
#       期望 1 passed
# 常见坑：
#   测试"通过"了但其实是假的
#       → 用 try/except 包住了异常，应该用 with pytest.raises
#   ImportError: cannot import name 'load_notes'
#       → mypkg\notes.py 没保存，或者函数名拼错（第 6 周踩过两次同样的坑）


# 练习 D：tmp_path 往返测试
#   在 tests\test_notes.py 里再加两个测试：
#       test_roundtrip      → 存进去、读出来，内容要一模一样（含中文）
#       test_missing_file   → 读不存在的文件返回 {}
#
# --- 骨架 ---
# from mypkg.notes import load_notes, save_notes
#
#
# def test_roundtrip(tmp_path):
#     path = tmp_path / "notes.json"
#     data = {"2026-10-30": "第7周开工"}
#     ...
#
# 提示：断言"读回来的 == 写进去的"，不要逐个键比，字典直接比就行
# 验证：python -m pytest tests/test_notes.py -q
#       期望 3 passed（C 的 1 个 + 这里的 2 个）
# 常见坑：
#   跑完发现 learn 目录下多了个 notes.json
#       → 你把临时路径写成了 "notes.json" 字符串，没用 tmp_path


# 练习 E：给日志分析器写三个用例 + 收尾结构
#   1. tests\test_logstat.py 里写三个测试：
#        test_counts_errors    → 造一份日志，断言返回的字典完全相等
#        test_no_errors        → 日志里没有 ERROR，返回 {}
#        test_missing_file     → 文件不存在，抛 FileNotFoundError
#   2. 新建空的 tests\conftest.py
#   3. 新建 learn\pyproject.toml（内容抄第 10 节的模板）
#   4. 最后跑全量：python -m pytest -q，要求全绿
#
# --- tests\test_logstat.py 骨架 ---
# import pytest
# from mypkg.logstat import analyze_log
#
#
# def test_counts_errors(tmp_path):
#     log = tmp_path / "a.log"
#     log.write_text(
#         "2026-10-30 09:00:00 INFO  启动\n"
#         "2026-10-30 09:00:01 ERROR 数据库连接失败\n"
#         "2026-10-30 09:00:02 ERROR 权限不足\n"
#         "2026-10-30 09:00:03 ERROR 数据库连接失败\n",
#         encoding="utf-8",
#     )
#     assert analyze_log(log) == ...
#
# 提示：logstat 是故意不接 FileNotFoundError 的（第 6 周的设计决定），所以第三条要用 pytest.raises
# 验证：python -m pytest -q
#       期望 全部通过（A 3 + B 5 + C 1 + D 2 + E 3 = 14 个）
# 常见坑：
#   断言字典相等失败，但看起来一样
#       → 键的顺序不影响 ==，多半是某个键的值不对，仔细看 pytest 打印的左侧右侧
#   全量跑时 ModuleNotFoundError
#       → pyproject.toml 里的 testpaths 写错，或者没在 learn 根目录运行


# ============================================
# 本周验收标准
# ============================================
# [ ] 能说出 pytest 靠什么找测试（test_*.py 文件名 + test_* 函数名前缀）
# [ ] 能区分 AssertionError（算错了）和 ZeroDivisionError 等（崩了）
# [ ] 会给一个函数写 parametrize 用例，不复制粘贴
# [ ] 会用 pytest.raises 测"该炸的时候炸了"
# [ ] 会用 tmp_path 做文件测试，跑完不在项目目录留垃圾
# [ ] python -m pytest -q 全绿，退出码 0，14 个用例全部通过
# [ ] 能解释为什么测试放 tests\ 而不是和源码混在一起
