"""Bind selected Terra CSV records to a single bilingual StyleClone slot."""
import csv
from pathlib import Path


def bind_source(task, root):
    source = task["terra_source"]
    root = Path(root).resolve()
    rel = Path(source["csv"])
    path = (root / rel).resolve()
    if rel.is_absolute() or root not in path.parents or path.suffix.lower() != ".csv":
        raise ValueError("terra_source.csv 必须指向仓库内的 CSV")
    columns, key, selected = source["columns"], source["key"], source["select"]
    if not isinstance(columns, list) or not columns or len(columns) != len(set(columns)) or key not in columns:
        raise ValueError("columns 必须列出唯一字段并包含记录键")
    if not isinstance(selected, list) or not selected or len(selected) != len(set(selected)):
        raise ValueError("select 必须明确列出不重复的记录键值")
    rows = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        header = reader.fieldnames or []
        if not set(columns) <= set(header) or len(header) != len(set(header)):
            raise ValueError("CSV 表头缺少指定字段或含重名字段")
        for record in reader:
            if None in record or any(v is None for v in record.values()):
                raise ValueError(f"CSV 第 {reader.line_num} 行与表头列数不符")
            ident = record[key]
            if ident not in selected:
                continue
            if ident in rows:
                raise ValueError(f"记录键不唯一：{ident}")
            values = [record[c] for c in columns]
            if any(not v.strip() or any(ch in v for ch in ('｜', '\n', '\r', '{{', '}}')) for v in values):
                raise ValueError(f"所选记录缺值或包含歧义分隔符：{ident}")
            rows[ident] = "｜".join(values)
    missing = [k for k in selected if k not in rows]
    if missing:
        raise ValueError(f"CSV 缺少记录：{missing}")
    locked = [rows[k] for k in selected]
    slot = source["slot"]
    if slot in task["bindings"]:
        raise ValueError(f"数据槽位与人工绑定重复：{slot}")
    value = " / ".join(locked)
    return {**task, "bindings": {**task["bindings"], slot: {"zh": value, "en": value}},
            "verbatim": list(dict.fromkeys(task["verbatim"] + locked))}
