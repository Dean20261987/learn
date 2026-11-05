# learn

迪安2026 的 Python 学习仓库。

从零开始学，一周一个主题，周末做一个能跑的东西。目标：做出可商业化的 AI 产品。

**当前进度：第 9 周**

---

## 两个能用的工具

### `ledger` —— 命令行记账本

三层结构（存储 / 业务 / 命令行），数据存在本地 JSON，纯标准库。

```powershell
ledger add 35 午餐 --category 吃饭     # 记一笔支出
ledger add 5000 工资 --income          # 记一笔收入
ledger list                            # 最近 10 笔
ledger list --category 吃饭            # 只看某个分类
ledger list --month 2026-11            # 只看某个月
ledger report                          # 收支 / 结余 / 分类占比
ledger report --month 2026-11          # 按月汇总
ledger edit <ID> --note 午饭加饮料     # 改一笔（也能改金额、类型、分类、日期）
ledger edit <ID> --income              # 支出改成收入
ledger export 账单.csv                 # 导出 Excel 可直接打开的 CSV
ledger delete <ID>                     # 删一笔
```

- **安装**：`python -m pip install -e .`（装完就有 `ledger` 命令）
- **账本位置**：`~/.ledger/ledger.json`，可用环境变量 `LEDGER_PATH` 改到别处
- **数据格式**：v2。每条记录带 `kind`（`expense` / `income`），金额用符号区分方向（支出为负、收入为正），单位是**整数分**。读到 v1 老文件会自动迁移。

### `preorder` —— 预定单记录（桌面界面）

Tkinter 做的本地小工具，两个标签页：**预订单**（买模型）和**代工**（请人加工）。

- **启动**：双击 `预定单.bat`，或 `python -m preorder`
- **数据位置**：`~/.preorder/orders.json`
- 支持搜索、按状态筛选、标记到货、统计已付/待付

---

## 目录

| 路径 | 内容 |
|---|---|
| `week2.py` ~ `week7.py` | 每周讲义（边读边跑） |
| `week8.md` | 第 8 周项目需求书 |
| `ledger/` | 命令行记账本 |
| `preorder/` | 预定单桌面工具 |
| `mypkg/`、`mytools/` | 第 5–6 周的练习包 |
| `tests/` | 全部测试（130+ 个） |
| `art/` | 配图 |
| `日志.md` | 每日学习日志 |
| `迁移交接.md` | 换会话时的状态交接 |

零散文件：`hello.py`（第一个程序）、`profile.py`、`tools.py`、`data.csv`、`sample.txt` 等是各周练习产物。

## 环境

- Python 3.12（Windows 10/11）
- **不需要任何第三方库**，全部用标准库
- 测试用 pytest（第 7 周装的）

## 测试

```powershell
python -m pytest                       # 全部
python -m pytest tests/test_core.py -v # 单个文件，看得清
```

`pyproject.toml` 里配了 `testpaths = ["tests"]` 和 `addopts = "-q"`，所以在项目根目录直接 `python -m pytest` 就行。

## 学习进度

| 周 | 主题 | 产出 |
|---|---|---|
| 1–4 | 基础语法、数据结构、函数、错误处理 | `hello.py` + 小练习 |
| 5 | 文件读写 / 类与对象 / 正则 | `week5.py` |
| 6 | 模块与包、`if __name__ == "__main__"` | `mypkg/`、`mytools/` |
| 7 | pytest 测试 | 14 个测试，`pyproject.toml` |
| 8 | 项目：命令行记账本 | `ledger/`，48 个测试，打包成命令 |
| 9 | 给 ledger 加功能 | 收入 / `edit` / 导出 CSV / 数据迁移 v1→v2 |

每周的细节和踩过的坑都写在 `日志.md` 里，一天一条。
