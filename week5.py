# ============================================
# 第 5 周 · 文件读写 / 类与对象 / 正则基础
# 这周有一个坎：类与对象。别的都在它的前后
# ============================================


# ============================================
# 第一部分 · 文件读写
# ============================================
print("=== 1. 读文件 ===")

# 先写一个样本文件
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n第二行\n第三行\n")

# 方式 A：一次读完整个文件
with open("sample.txt", encoding="utf-8") as f:
    content = f.read()
print("读到的内容:", repr(content))

# 方式 B：逐行读（推荐，大文件不占内存）
with open("sample.txt", encoding="utf-8") as f:
    for line in f:
        print("  行:", line.rstrip())      # rstrip 去掉行尾换行符

# 方式 C：读成列表
with open("sample.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("行数:", len(lines))


print("\n=== 2. 写文件 ===")

# "w" = 覆盖写（原来的内容会没）
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# "a" = 追加写（保留原内容，加在后面）
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("追加的一行\n")

# 写多行
with open("output2.txt", "w", encoding="utf-8") as f:
    f.writelines(["苹果\n", "香蕉\n", "橘子\n"])

with open("output2.txt", encoding="utf-8") as f:
    print(f.read())


print("\n=== 3. 打开模式速查 ===")

# "r"  只读（默认）        文件不存在会报错
# "w"  写入，清空原内容    文件不存在会创建
# "a"  追加，保留原内容    文件不存在会创建
# "rb" 二进制读（图片等）
# "wb" 二进制写
# encoding 不写的话，Windows 上默认是 GBK，中文会乱码


print("\n=== 4. 综合：读写 CSV ===")

import csv

# 写 CSV
rows = [
    ["姓名", "周数", "投入"],
    ["迪安2026", 5, 25.5],
    ["鲸鱼娘", 5, 30],
]
with open("data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# 读 CSV
with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print("  ", row)


# ============================================
# 第二部分 · 类与对象（本周的坎）
# ============================================
print("\n=== 5. 第一个类 ===")

class Pet:
    """一只宠物"""

    def __init__(self, name, species):
        """初始化方法：创建对象时自动调用"""
        self.name = name
        self.species = species

    def speak(self):
        """方法：对象能做的动作"""
        print(f"{self.name} 是一只 {self.species}")

# 创建对象（实例化）
pet1 = Pet("鲸鱼娘", "鲸鱼")
pet2 = Pet("小雨", "鲸鱼")

pet1.speak()
pet2.speak()
print("pet1 的名字:", pet1.name)


# ============================================
print("\n=== 6. 类到底解决什么问题 ===")

# 不用类：数据和行为是散的
student_names = ["迪安2026", "小雨"]
student_weeks = [5, 5]

def show_student(i):
    print(f"{student_names[i]} 学到第 {student_weeks[i]} 周")

show_student(0)
# 问题：加一个字段就要加一个列表，索引要自己对齐，容易错


# 用类：数据和它的行为绑在一起
class Student:
    def __init__(self, name, week):
        self.name = name
        self.week = week

    def show(self):
        print(f"{self.name} 学到第 {self.week} 周")

    def advance(self):
        """升高一周"""
        self.week += 1

s1 = Student("迪安2026", 5)
s1.show()
s1.advance()
s1.show()


# ============================================
print("\n=== 7. 类里的 self 是什么 ===")

class Counter:
    def __init__(self):
        self.count = 0          # 这个对象自己的计数器

    def add(self):
        self.count += 1

    def show(self):
        print("当前计数:", self.count)

c1 = Counter()
c2 = Counter()

c1.add()
c1.add()
c2.add()

c1.show()      # 2
c2.show()      # 1    ← 各管各的，互不影响

# self 就是"这个对象自己"
# 两个对象各有各的 self.count


# ============================================
print("\n=== 8. 继承（了解即可） ===")

class Whale(Pet):
    """继承 Pet，多了自己会的东西"""

    def swim(self):
        print(f"{self.name} 在游泳")

w = Whale("鲸鱼娘", "鲸鱼")
w.speak()      # 继承来的
w.swim()       # 自己的


# ============================================
# 第三部分 · 正则基础
# ============================================
print("\n=== 9. 正则是什么 ===")

import re

text = "我的电话是13812345678，备用号是010-87654321"

# 找所有连续 11 位数字
phones = re.findall(r"\d{11}", text)
print("找到的手机号:", phones)

# 找所有形如 3位-8位 的座机号
landline = re.findall(r"\d{3}-\d{8}", text)
print("找到的座机号:", landline)


print("\n=== 10. 常用正则符号 ===")

print("\\d      任意数字          ", re.findall(r"\d", "a1b2c3"))
print("\\w      字母数字下划线     ", re.findall(r"\w+", "hello world_1"))
print("\\s      空白              ", re.findall(r"\s+", "a b  c"))
print(".       任意字符（除换行） ", re.findall(r"a.c", "abc axc a-c"))
print("*       0 次或多次         ", re.findall(r"ab*", "a ab abb abbb"))
print("+       1 次或多次         ", re.findall(r"ab+", "a ab abb"))
print("?       0 或 1 次          ", re.findall(r"ab?", "a ab abb"))
print("{2,4}   2 到 4 次          ", re.findall(r"a{2,4}", "a aa aaa aaaa aaaaa"))
print("[abc]   a 或 b 或 c       ", re.findall(r"[abc]", "abcd"))
print("[^abc]  除了 a b c        ", re.findall(r"[^abc]", "abcx"))
print("^     行首               ", re.findall(r"^a", "abc\nxyz"))
print("$     行尾               ", re.findall(r"c$", "abc"))


print("\n=== 11. 常用组合 ===")

# 匹配一个完整的 11 位手机号（1 开头）
print("手机号:", re.findall(r"1\d{10}", "13812345678 和 23812345678"))

# 匹配邮箱（简化版）
emails = re.findall(r"[\w.]+@[\w.]+", "联系 a@b.com 或 c.d@e.cn")
print("邮箱:", emails)

# 替换
print("脱敏:", re.sub(r"\d{11}", "***********", "电话13812345678"))


# ============================================
# 练习区
# ============================================

# 练习 A：读一个文件，统计最长的一行有多长
#
# def longest_line(path):
#     ...
#
# print(longest_line("week4.py"))
def longest_line(path):
    best = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            length = len(line.rstrip("\n"))
            if length > best:
                best = length
    return best
print(longest_line("week4.py"))

# 练习 B：写一个函数，把一个字典保存成文本文件（每行 键: 值）
#
# def save_dict(d, path):
#     ...
#
# save_dict({"姓名": "迪安2026", "周数": 5}, "info.txt")
def save_dict(d, path):
    with open(path, "w", encoding="utf-8") as f:
        for key, value in d.items():
            f.write(f"{key}: {value}\n")
             
save_dict({"姓名": "迪安2026", "周数": 5}, "info.txt")

# 练习 C：写一个 Student 类
#   属性：name, week, scores（成绩列表）
#   方法：
#     show()      打印学生信息
#     add_score(s)  添加一个成绩
#     average()   返回平均分（没有成绩返回 0）
#
# class Student:
#     def __init__(self, name, week, scores=None):
#         ...
#
# s = Student("迪安2026", 5, [85, 92, 78])
# s.show()
# s.add_score(100)
# print("平均分:", s.average())

class Student:
    def __init__(self, name, week, scores=None):
        self.name = name
        self.week = week
        self.scores = scores if scores is not None else []

    def show(self):
        print(f"{self.name} 学到第 {self.week} 周，成绩: {self.scores}")

    def add_score(self, s):
        self.scores.append(s)

    def average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)


s = Student("迪安2026", 5, [85, 92, 78])
s.show()
s.add_score(100)
print("平均分:", s.average())

s2 = Student("新同学", 5)
print("空成绩平均分:", s2.average())      # 应该是 0


s2.add_score(60)
print("s1 的成绩:", s.scores)             # 应该还是 [85, 92, 78, 100]
print("s2 的成绩:", s2.scores)            # 应该是 [60]
# 练习 D：用正则从一段文字里提取所有日期
#   支持 2026-10-26 和 2026/10/26 两种格式
#
# def find_dates(text):
#     ...
#
# print(find_dates("会议在2026-10-26，下次2026/11/02"))
# # 期望 ['2026-10-26', '2026/11/02']
import re

def find_dates(text):
    return [m.group(0) for m in re.finditer(r"\d{4}([-/])\d{2}\1\d{2}", text)]
print(find_dates("会议在2026-10-26，下次2026/11/02"))


# 练习 E：综合 —— 日志分析器
#   读取一个日志文件，用正则提取所有 ERROR 级别的行，
#   统计每种错误出现的次数，输出前 3 个最多的
#
# def analyze_log(path):
#     ...
log_text = """2026-10-27 09:00:12 INFO  程序启动
2026-10-27 09:00:15 ERROR 数据库连接失败
2026-10-27 09:01:02 INFO  重试中
2026-10-27 09:01:10 ERROR 数据库连接失败
2026-10-27 09:02:33 WARN  响应缓慢
2026-10-27 09:03:01 ERROR 文件不存在
2026-10-27 09:04:15 ERROR 数据库连接失败
2026-10-27 09:05:00 ERROR 权限不足"""

with open("test.log", "w", encoding="utf-8") as f:
    f.write(log_text)

import re

def analyze_log(path):
    counter = {}

    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"ERROR\s+(.+)", line)
            if m:
                msg = m.group(1).strip()
                counter[msg] = counter.get(msg, 0) + 1

    if not counter:
        print("没有找到 ERROR 级别的日志")
        return counter

    ranked = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)

    print(f"共 {sum(counter.values())} 条 ERROR，{len(counter)} 种")
    for msg, count in ranked[:3]:
        print(f"  {count} 次  {msg}")

    return counter


analyze_log("test.log")