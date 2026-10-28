"""文本小工具"""


def shout(s):
    """给字符串加大写和感叹号，shout("hi") → "HI!" """
    upper = s.upper()      # "hi" → "HI"
    return upper + "!"     # 字符串拼接：+ 号在两边都是字符串时是"接起来"