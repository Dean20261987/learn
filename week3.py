# ============================================
# 第 3 周 · 条件 / 循环 / 列表 / 字典
# 每一节都有"动手改"的地方，改完运行看输出
# ============================================


# ============ 1. 条件判断 if / elif / else ============
print("=== 1. 条件判断 ===")

score = 85

if score >= 90:
    print("优秀")
elif score >= 75:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 关键点：Python 用「缩进」表示代码属于哪个分支
# 冒号 : 后面换行，然后缩进 4 个空格

# 比较运算符：== != > < >= <=
# 逻辑运算符：and（且） or（或） not（非）

age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("可以入场")
else:
    print("不能入场")


# ============ 2. for 循环 ============
print("\n=== 2. for 循环 ===")

# range(5) 产生 0,1,2,3,4
for i in range(5):
    print("第", i, "次")

print("---")

# range(1, 6) 产生 1,2,3,4,5（含头不含尾）
for i in range(1, 6):
    print(f"{i} 的平方是 {i * i}")


# ============ 3. while 循环 ============
print("\n=== 3. while 循环 ===")

count = 0
while count < 3:
    print("count =", count)
    count = count + 1      # 写成 count += 1 也行

print("循环结束，count =", count)

# ⚠️ 忘了写 count += 1 会死循环，按 Ctrl+C 可以中断


# ============ 4. 列表 list ============
print("\n=== 4. 列表 ===")

fruits = ["苹果", "香蕉", "橘子"]
print(fruits)
print("第一个:", fruits[0])       # 索引从 0 开始
print("最后一个:", fruits[-1])     # -1 表示倒数第一个
print("一共:", len(fruits), "个")

# 遍历列表
for fruit in fruits:
    print("我喜欢吃", fruit)

# 常用操作
fruits.append("葡萄")        # 末尾加一个
print("加完:", fruits)

fruits.remove("香蕉")        # 删除指定元素
print("删完:", fruits)

print("橘子在不在？", "橘子" in fruits)


# ============ 5. 字典 dict ============
print("\n=== 5. 字典 ===")

# 键值对：键 → 值
student = {
    "name": "迪安2026",
    "week": 3,
    "hours": 25.5,
    "is_beginner": True,
}

print(student)
print("名字:", student["name"])
print("周数:", student["week"])

# 安全取值：键不存在时不报错，返回默认值
print("分数:", student.get("score", "还没考"))

# 新增 / 修改
student["score"] = 88
print("加分后:", student)

# 遍历字典
for key in student:
    print(f"  {key} = {student[key]}")

for key, value in student.items():
    print(f"  {key}: {value}")


# ============ 6. 综合：成绩统计 ============
print("\n=== 6. 综合示例：成绩统计 ===")

scores = [85, 92, 58, 77, 100, 63]

total = 0
passed = 0
highest = scores[0]
lowest = scores[0]

for s in scores:
    total += s
    if s >= 60:
        passed += 1
    if s > highest:
        highest = s
    if s < lowest:
        lowest = s

average = total / len(scores)

print("成绩:", scores)
print(f"平均分: {average:.1f}")     # .1f 表示保留 1 位小数
print(f"最高分: {highest}")
print(f"最低分: {lowest}")
print(f"及格人数: {passed} / {len(scores)}")


# ============================================
# 动手练习（把下面注释掉的代码写完再运行）
# ============================================

# 练习 A：判断奇偶
# 遍历 1 到 20，如果是偶数打印 "X 是偶数"，奇数打印 "X 是奇数"
#
for i in range(1, 21):
    if i % 2 == 0 :
        print(f"{i} 是偶数")
    else:
        print(f"{i} 是奇数")


# 练习 B：累加求和
# 用 for 循环算出 1+2+3+...+100 的结果，打印出来

total = 0
for i in range(1,101):
    total += i
print(total) 


# 练习 C：找最大值（不许用 max()）
# 从 scores 列表里手动找出最大值并打印
scores = [85, 92, 58, 77, 100, 63]
highest = scores[0]
for s in scores:
    if s > highest:
        highest = s

print("最大值:", highest)



# 练习 D：统计词频
# 统计一句话里每个字出现了几次，用字典保存，把出现次数最多的字找出来

sentence = "我爱吃饭饭饭"
counter = {}
for ch in sentence:
    counter[ch] = counter.get(ch, 0) + 1

print(counter)          

best_char = None
best_count = 0
for ch, count in counter.items():
    if count > best_count:
        best_char = ch    
        best_count = count
print(f"出现最多的是「{best_char}」，{best_count} 次")
# 练习 E：乘法表
# 打印 9x9 乘法表（用两层 for 循环）
#
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}*{i}={j * i}", end=" ")
    print()
