"""命令行层：解析参数、调 core、打印结果"""

import argparse
import os
import pathlib

from ledger import core, storage

_env_path = os.environ.get("LEDGER_PATH")
DEFAULT_PATH = (
    pathlib.Path(_env_path)
    if _env_path
    else pathlib.Path.home() / ".ledger" / "ledger.json"
)

def format_cents(cents):
    """整数分 → 显示用的元，如 3500 → '35.00'"""
    return f"{cents / 100:.2f}"


def build_parser():
    """建好所有子命令"""
    parser = argparse.ArgumentParser(prog="ledger", description="命令行记账本")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="记一笔")
    p_add.add_argument("amount", help="金额，如 35 或 12.5")
    p_add.add_argument("note", help="说明，如 午餐")
    p_add.add_argument("--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    p_add.add_argument("--category", default="未分类", help="分类")

    p_list = sub.add_parser("list", help="列出账目")
    p_list.add_argument("--month", default=None, help="月份 YYYY-MM，如 2026-11")
    p_list.add_argument("--limit", type=int, default=10, help="最多显示几条")

    p_report = sub.add_parser("report", help="按月汇总")
    p_report.add_argument("--month", default=None, help="月份 YYYY-MM")

    p_delete = sub.add_parser("delete", help="删除一笔")
    p_delete.add_argument("id", help="记录 ID，如 20261102-001")

    return parser


def cmd_add(args, path):
    data = storage.load_ledger(path)
    record = core.add_record(
        data,
        args.amount,
        args.note,
        date_str=args.date,
        category=args.category,
    )
    storage.save_ledger(data, path)
    print(f"已记账：{record['id']}  {format_cents(record['amount_cents'])} 元  {record['note']}")


def cmd_list(args, path):
    data = storage.load_ledger(path)
    records = core.list_records(data, month=args.month, limit=args.limit)
    if not records:
        print("还没有记录")
        return
    for r in records:
        print(
            f"{r['id']}  {r['date']}  {format_cents(r['amount_cents']):>8} 元  "
            f"[{r['category']}]  {r['note']}"
        )


def cmd_report(args, path):
    data = storage.load_ledger(path)
    summary = core.summarize(data, month=args.month)
    scope = args.month or "全部"
    print(f"【{scope}】共 {summary['count']} 笔，合计 {format_cents(summary['total_cents'])} 元")
    for category, cents in sorted(
        summary["by_category"].items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {category}: {format_cents(cents)} 元")


def cmd_delete(args, path):
    data = storage.load_ledger(path)
    record = core.delete_record(data, args.id)
    storage.save_ledger(data, path)
    print(f"已删除：{record['id']}  {record['note']}")


def main(argv=None, path=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "report": cmd_report,
        "delete": cmd_delete,
    }

    try:
        handlers[args.command](args, path or DEFAULT_PATH)
    except ValueError as e:
        print(f"出错了：{e}")
        raise SystemExit(1)