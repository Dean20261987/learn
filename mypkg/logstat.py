"""日志统计 —— 从日志文件里统计 ERROR 消息的出现次数"""

import re


def analyze_log(path):
    """分析日志文件，返回 {错误消息: 出现次数} 字典。"""
    counter = {}

    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"ERROR\s+(.+)", line)
            if m:
                msg = m.group(1).strip()
                counter[msg] = counter.get(msg, 0) + 1

    if not counter:
        return {}

    return counter


if __name__ == "__main__":
    print(analyze_log("test.log"))