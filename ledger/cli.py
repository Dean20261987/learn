"""命令行层：解析参数、调 core、打印结果"""

import argparse
import csv
import os
import pathlib

from ledger import core, storage
from ledger.core import format_cents

_env_path = os.environ.get("LEDGER_PATH")
DEFAULT_PATH = (
    pathlib.Path(_env_path)
    if _env_path
    else pathlib.Path.home() / ".ledger" / "ledger.json"
)


def build_parser():
    parser = argparse.ArgumentParser(prog="ledger", description="命令行记账本")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="记一笔")
    p_add.add_argument("amount", help="金额，如 35 或 12.5")
    p_add.add_argument("note", help="说明，如 午餐")
    p_add.add_argument("--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    p_add.add_argument("--category", default="未分类", help="分类")
    p_add.add_argument("--income", action="store_true", help="记一笔收入（默认是支出）")

    p_edit = sub.add_parser("edit", help="修改一笔")
    p_edit.add_argument("id", help="记录 ID")
    p_edit.add_argument("--amount", default=None, help="新金额")
    p_edit.add_argument("--note", default=None, help="新说明")
    p_edit.add_argument("--category", default=None, help="新分类")
    p_edit.add_argument("--date", default=None, help="新日期")
    kind_group = p_edit.add_mutually_exclusive_group()
    kind_group.add_argument("--income", action="store_true", help="改成收入")
    kind_group.add_argument("--expense", action="store_true", help="改成支出")

    p_list = sub.add_parser("list", help="列出账目")
    p_list.add_argument("--month", default=None, help="月份 YYYY-MM")
    p_list.add_argument("--limit", type=int, default=10, help="最多显示几条")
    p_list.add_argument("--category", default=None, help="只看某个分类")

    p_report = sub.add_parser("report", help="按月汇总")
    p_report.add_argument("--month", default=None, help="月份 YYYY-MM")

    p_export = sub.add_parser("export", help="导出 CSV")
    p_export.add_argument("out", help="输出文件路径，如 账单.csv")
    p_export.add_argument("--month", default=None, help="只导出某月 YYYY-MM")

    p_delete = sub.add_parser("delete", help="删除一笔")
    p_delete.add_argument("id", help="记录 ID")

    return parser


def cmd_add(args, path):
    data = storage.load_ledger(path)
    kind = "income" if args.income else "expense"
    record = core.add_record(
        data,
        args.amount,
        args.note,
        date_str=args.date,
        category=args.category,
        kind=kind,
    )
    storage.save_ledger(data, path)
    label = core.KIND_LABELS[record["kind"]]
    print(
        f"已记账：{record['id']}  {label} {format_cents(record['amount_cents'])} 元  {record['note']}"
    )


def cmd_edit(args, path):
    data = storage.load_ledger(path)

    kind = None
    if args.income:
        kind = "income"
    elif args.expense:
        kind = "expense"

    record = core.update_record(
        data,
        args.id,
        amount_text=args.amount,
        note=args.note,
        date_str=args.date,
        category=args.category,
        kind=kind,
    )
    storage.save_ledger(data, path)
    label = core.KIND_LABELS[record["kind"]]
    print(
        f"已修改：{record['id']}  {label} {format_cents(record['amount_cents'])} 元  {record['note']}"
    )


def cmd_list(args, path):
    data = storage.load_ledger(path)
    records = core.list_records(
        data,
        month=args.month,
        limit=args.limit,
        category=args.category,
    )
    if not records:
        print("还没有记录")
        return
    for r in records:
        label = core.KIND_LABELS[r["kind"]]
        print(
            f"{r['id']}  {r['date']}  {label} {format_cents(r['amount_cents']):>9} 元  "
            f"[{r['category']}]  {r['note']}"
        )


def cmd_report(args, path):
    data = storage.load_ledger(path)
    s = core.summarize(data, month=args.month)
    scope = args.month or "全部"

    print(f"【{scope}】共 {s['count']} 笔")
    print(f"  支出  {format_cents(s['expense_cents']):>10} 元")
    print(f"  收入  {format_cents(s['income_cents']):>10} 元")
    print(f"  结余  {format_cents(s['balance_cents']):>10} 元")

    if s["by_category"]:
        print("  支出分类：")
        total = s["expense_cents"] or 1
        for cat, cents in sorted(
            s["by_category"].items(), key=lambda kv: kv[1], reverse=True
        ):
            print(f"    {cat:<8} {format_cents(cents):>8} 元  {cents / total * 100:5.1f}%")


def cmd_export(args, path):
    data = storage.load_ledger(path)
    rows = core.to_export_rows(data, month=args.month)

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows(rows)

    print(f"已导出 {len(rows) - 1} 条到 {out_path}")


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
        "edit": cmd_edit,
        "list": cmd_list,
        "report": cmd_report,
        "export": cmd_export,
        "delete": cmd_delete,
    }

    try:
        handlers[args.command](args, path or DEFAULT_PATH)
    except ValueError as e:
        print(f"出错了：{e}")
        raise SystemExit(1)