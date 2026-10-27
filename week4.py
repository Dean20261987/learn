# ============================================
# 第 4 周 · 函数 / 模块 / 错误处理
# 从这一周开始，代码从"一次性脚本"变成"能复用的工具"
# ============================================


# ============ 1. 第一个函数 ============
print("=== 1. 第一个函数 ===")

def greet():
    print("你好，世界")

greet()      # 调用：函数名 + 括号
greet()      # 可以调用很多次

# 关键点：
#   def 是"定义"，定义一个工具
#   调用时才真正执行
#   函数体必须缩进


# ============ 2. 带参数的函数 ============
print("\n=== 2. 带参数 ===")

def greet_person(name):
    print(f"你好，{name}")

greet_person("迪安2026")
greet_person("鲸鱼娘")

# 参数 = 函数接收数据的入口
# 定义时的 name 叫"形参"，调用时传的"迪安2026"叫"实参"


# ============ 3. 多个参数 ============
print("\n=== 3. 多个参数 ===")

def introduce(name, week, hours):
    print(f"我是 {name}，正在学第 {week} 周，每天投入 {hours} 小时")

introduce("迪安2026", 4, 25.5)


# ============ 4. 返回值的函数 ============
print("\n=== 4. 返回值 return ===")

def add(a, b):
    return a + b

result = add(3, 5)
print("3 + 5 =", result)

# return 和 print 的区别（非常重要）：
#   print  = 把结果显示给人看
#   return = 把结果交回给程序继续用

def add_print(a, b):
    print(a + b)

x = add(3, 5)          # x = 8        ← 拿到了值
y = add_print(3, 5)    # 屏幕显示 8，但 y = None
print("add 返回:", x)
print("add_print 返回:", y)


# ============ 5. 把第 3 周的代码变成函数 ============
print("\n=== 5. 把旧代码包成函数 ===")

def find_max(numbers):
    """找出列表里的最大值（第 3 周练习 C 的函数版）"""
    highest = numbers[0]
    for n in numbers:
        if n > highest:
            highest = n
    return highest

scores = [85, 92, 58, 77, 100, 63]
print("最大值:", find_max(scores))
print("再来一组:", find_max([3, 9, 2, 7]))

# 注意最高级的好处：现在它能处理任意列表，不再绑死 scores


# ============ 6. 默认参数 ============
print("\n=== 6. 默认参数 ===")

def greet_with_style(name, style="你好"):
    print(f"{style}，{name}")

greet_with_style("迪安2026")                    # 用默认值"你好"
greet_with_style("迪安2026", "早上好")          # 覆盖默认值

# 默认参数必须写在最后！


# ============ 7. 导入模块 ============
print("\n=== 7. 导入模块 ===")

import random
import math

print("随机数:", random.randint(1, 100))
print("随机选一个:", random.choice(["苹果", "香蕉", "橘子"]))
print("圆周率:", math.pi)
print("9 的平方根:", math.sqrt(9))
print("向上取整:", math.ceil(3.2))

# Python 自带很多模块，不用 pip 装
# 用法：import 模块名   然后   模块名.函数()


# ============ 8. 错误处理 try / except ============
print("\n=== 8. 错误处理 ===")

# 没有 try 的版本会直接崩
# print(int("abc"))        # ← 取消注释试试，程序会崩

# 有 try 的版本
def safe_int(text):
    try:
        return int(text)
    except ValueError:
        print(f"「{text}」不是数字，返回 0")
        return 0

print(safe_int("123"))
print(safe_int("abc"))
print(safe_int("45"))

# 常见异常类型：
#   ValueError      值不对（int("abc")）
#   TypeError       类型不对（"a" + 1）
#   ZeroDivisionError  除以 0
#   KeyError        字典里没这个键
#   IndexError      列表越界
#   FileNotFoundError  文件不存在


# ============ 9. 综合：一个带错误处理的小工具 ============
print("\n=== 9. 综合示例：成绩统计器 ===")

def analyze_scores(raw_list):
    """
    输入：字符串列表，如 ["85", "92", "abc", "77"]
    输出：(及格数, 平均分, 跳过的无效项)
    """
    valid = []
    skipped = []

    for item in raw_list:
        try:
            score = float(item)
            if score < 0 or score > 100:
                skipped.append(item)
                continue
            valid.append(score)
        except ValueError:
            skipped.append(item)

    if not valid:
        return 0, 0.0, skipped

    passed = 0
    for s in valid:
        if s >= 60:
            passed += 1

    average = sum(valid) / len(valid)
    return passed, average, skipped

passed, avg, skipped = analyze_scores(["85", "92", "abc", "77", "120", "58"])
print(f"及格人数: {passed}")
print(f"平均分: {avg:.1f}")
print(f"跳过的无效项: {skipped}")


# ============================================
# 动手练习
# ============================================

# 练习 A：写一个函数 is_even(n)，返回 True / False
# 然后用它打印 1-20 里所有偶数
#
def is_even(n):
    return n % 2 == 0

for i in range(1, 21):
    if is_even(i):
        print(i)


# 练习 B：写一个函数 count_words(text)，返回这段文字有几个词
# 提示：text.split() 按空格切分成列表，len() 数个数
#
def count_words(text):
    return len(text.split())
print(count_words("我爱 学习 编程"))    # 应该输出 3


# 练习 C：写一个函数 safe_divide(a, b)
# 正常返回 a/b；如果 b 是 0，捕获 ZeroDivisionError 并返回 None
# 
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # None（不崩）


# 练习 D：写一个函数 word_freq(text)，返回词频字典
# 把第 3 周的练习 D 改成函数版
# 提示：text.split() 切成词，然后字典累加

def word_freq(text):
    counter = {}
    for word in text.split():
        counter[word] = counter.get(word, 0) + 1
    return counter
print(word_freq("我 爱 吃 饭 饭 饭"))

# 练习 E：把本周的函数拼成一个小工具
# 读取你自己写的某个 .py 文件，统计：
#   - 总行数
#   - 空行数
#   - 注释行数（以 # 开头的）
# 提示：with open(路径, encoding="utf-8") as f: 逐行读
#

def analyze_file(path):
    """
    统计文件的总行数、空行数、注释行数、代码行数

    - 空行：去掉前后空白后什么都不剩的行
    - 注释行：去掉前导空白后以 # 开头的行（行尾注释算代码行，不算注释行）
    - 三引号文档字符串不算注释行，算代码行
    成功返回字典，失败返回 None
    """
    total = 0
    blank = 0
    comment = 0

    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                total += 1
                stripped = line.strip()
                if stripped == "":
                    blank += 1
                elif stripped.startswith("#"):
                    comment += 1
    except FileNotFoundError:
        print(f"找不到文件: {path}")
        return None
    except IsADirectoryError:
        print(f"{path} 是文件夹，不是文件")
        return None
    except PermissionError:
        print(f"没有权限读取: {path}")
        return None
    except UnicodeDecodeError:
        print(f"{path} 不是 UTF-8 编码，读不了")
        return None

    code = total - blank - comment

    print(f"文件: {path}")
    print(f"  总行数: {total}")
    print(f"  空行:   {blank}")
    print(f"  注释:   {comment}")
    print(f"  代码行: {code}")

    return {"total": total, "blank": blank, "comment": comment, "code": code}


# 直接运行本文件时才执行；路径不写死，可以用命令行参数传
if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "week3.py"
    result = analyze_file(target)
    if result is not None:
        print("返回的字典:", result)
