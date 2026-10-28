"""数学小工具 —— 演示模块怎么被别的文件 import"""


def add(a, b):
    """两数相加"""
    return a + b


def average(numbers):
    """求平均值，空列表返回 0"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


# 只有直接运行 python mypkg/mathx.py 时，__name__ 才等于 "__main__"
# 被别的文件 import 时，__name__ 是 "mypkg.mathx"，下面这段不执行
if __name__ == "__main__":
    print("自测 add(2, 3) =", add(2, 3))
    print("自测 average([1, 2, 3]) =", average([1, 2, 3]))
