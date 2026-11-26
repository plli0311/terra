"""Render StyleClone 1.0 bilingual rules using only the Python standard library."""
import argparse
import json
import re
import sys
from pathlib import Path

FIELDS = ("style", "subject", "environment", "narrative", "mood", "technical")
MODULES = set("A1 B1 B2 B3 B4 C1 C2 C3 C4 D1 E1 E2 E3".split())
TOKEN = re.compile(r"\{\{([a-z][a-z0-9_]*)\}\}")
IDENT = re.compile(r"[a-z][a-z0-9_]*")
LANGUAGES = ("zh", "en")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"重复 JSON 键：{key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"),
                      object_pairs_hook=no_duplicates)


def filled(value):
    return isinstance(value, str) and bool(value.strip())


def pair(value):
    return isinstance(value, dict) and all(filled(value.get(k)) for k in LANGUAGES)


def validate(profile, task):
    require(profile["system_version"] == "1.0", "不支持的系统版本")
    require(all(filled(profile[k]) for k in ("profile_id", "profile_version")), "缺少档案 ID 或版本")
    require(profile["basis_kind"] in ("observed", "user_defined", "demonstration"), "档案来源类型无效")
    require(set(profile["modules"]) == MODULES, "十三项观察模块不完整")
    require(all(state in ("active", "inactive", "not_applicable", "pending")
                for state in profile["modules"].values()), "模块状态无效")
    refs = profile["references"]
    require(isinstance(refs, dict) and refs and all(filled(v) for v in refs.values()), "缺少可定位的来源")
    slots = profile["slots"]
    conditions = profile["conditions"]
    require(isinstance(slots, dict) and all(IDENT.fullmatch(k) and filled(v) for k, v in slots.items()), "槽位定义无效")
    require(isinstance(conditions, dict) and all(IDENT.fullmatch(k) and pair(v) for k, v in conditions.items()), "条件定义无效")
    if task is not None:
        require(task["profile_id"] == profile["profile_id"] and task["profile_version"] == profile["profile_version"], "任务与风格档案版本不匹配")
        require(filled(task["task_id"]), "任务 ID 为空")
        require(isinstance(task["bindings"], dict) and set(task["bindings"]) <= set(slots), "任务包含未知槽位")
        for key, value in task["bindings"].items():
            require(pair(value) and all("{{" not in value[k] and "}}" not in value[k] for k in LANGUAGES), f"无效的双语绑定：{key}")
        require(set(task["flags"]) == set(conditions) and all(type(v) is bool for v in task["flags"].values()), "条件未确认或含未知条件")
        require(isinstance(task["verbatim"], list) and all(filled(x) for x in task["verbatim"]), "逐字保护清单无效")
    base = profile["rules"]
    require(isinstance(base, list) and base, "风格档案没有规则")
    local = [] if task is None else task["rules"]
    require(isinstance(local, list), "任务规则应为数组")
    rules = base + local
    ids = [r["id"] for r in rules]
    require(all(filled(x) for x in ids) and len(set(ids)) == len(ids), "规则 ID 为空或重复")
    for idx, rule in enumerate(rules):
        rid = rule["id"]
        require(rule["module"] in MODULES and rule["field"] in FIELDS, f"{rid} 分组未知")
        require(rule["priority"] in ("must", "should", "may") and
                rule["variation"] in ("core", "conditional", "project_locked", "free") and
                rule["category"] in ("style", "content", "presentation"), f"{rid} 分类无效")
        require(filled(rule["check"]) and bool(rule["evidence"]) and isinstance(rule["evidence"], list), f"{rid} 缺少依据或验法")
        allowed = set(refs)
        if idx >= len(base):
            allowed.add(task["task_id"])
        require(set(rule["evidence"]) <= allowed, f"{rid} 来源引用无效")
        require(rule["when"] is None or rule["when"] in conditions, f"{rid} 条件未定义")
        require(pair(rule), f"{rid} 缺少双语描述")
        tokens = set(TOKEN.findall(rule["zh"]))
        require(tokens == set(TOKEN.findall(rule["en"])) and tokens <= set(slots), f"{rid} 双语槽位不一致或未定义")
        for lang in LANGUAGES:
            residual = TOKEN.sub("", rule[lang])
            require("{{" not in residual and "}}" not in residual, f"{rid} 槽位语法无效")
        for key in ("requires", "excludes"):
            links = rule[key]
            require(isinstance(links, list) and set(links) <= set(ids) and rid not in links, f"{rid} {key} 引用无效")
    declared = {r["module"] for r in base}
    active = {m for m, s in profile["modules"].items() if s == "active"}
    require(declared == active, "active 模块与风格规则未对齐")
    return rules


def render(profile, task=None, natural_language="zh", terra_root=None):
    if task is not None and "terra_source" in task:
        from terra_handoff import bind_source
        task = bind_source(task, terra_root or Path(__file__).resolve().parent.parent)
    rules = validate(profile, task)
    if task is not None:
        rules = [r for r in rules if r["when"] is None or task["flags"][r["when"]]]
        enabled = {r["id"] for r in rules}
        for r in rules:
            require(set(r["requires"]) <= enabled, f'{r["id"]} 依赖未启用')
            require(not enabled.intersection(r["excludes"]), f'{r["id"]} 与有效规则互斥')
    require(rules, "没有生效规则")
    outputs = {}
    for lang in LANGUAGES:
        meta = {"system_version": "1.0", "profile_id": profile["profile_id"],
                "profile_version": profile["profile_version"], "task_id": None if task is None else task["task_id"],
                "form": "template" if task is None else "instance", "basis_kind": profile["basis_kind"]}
        doc = {"_meta": meta, **{field: [] for field in FIELDS}}
        for r in rules:
            text = r[lang]
            if task is not None:
                for key in TOKEN.findall(text):
                    require(key in task["bindings"], f'{r["id"]} 缺少绑定 {key}')
                text = TOKEN.sub(lambda m: task["bindings"][m[1]][lang], text)
            elif r["when"] is not None:
                condition = profile["conditions"][r["when"]][lang]
                prefix = f"当{condition}时，" if lang == "zh" else f"If {condition}, "
                text = prefix + text
            doc[r["field"]].append({"id": r["id"], "priority": r["priority"], "text": text})
        outputs[lang] = doc
    compact = []
    for field in FIELDS:
        entries = outputs["zh"][field]
        must = [row for row in entries if row["priority"] == "must"]
        compact.extend(row["text"] for row in must or entries[:1])
    natural = [" ".join(row["text"] for row in outputs[natural_language][f])
               for f in FIELDS if outputs[natural_language][f]]
    short = " ".join(compact)
    full = "\n\n".join(natural)
    for literal in ([] if task is None else task["verbatim"]):
        for lang in LANGUAGES:
            text = " ".join(x["text"] for f in FIELDS for x in outputs[lang][f])
            require(literal in text, f"{lang} JSON 缺少保护文字 {literal}")
        require(literal in short and literal in full, f"提示词缺少保护文字 {literal}")
    return outputs["zh"], outputs["en"], short, full


def markdown(bundle):
    zh, en, short, full = bundle
    def fenced(doc):
        return "```json\n" + json.dumps(doc, ensure_ascii=False, indent=2) + "\n```"
    return "\n\n".join(("## ① 中文 JSON", fenced(zh), "## ② English JSON", fenced(en),
                         "## ③ 中文简易提示词", short, "## ④ 完整自然语言提示词", full))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile")
    parser.add_argument("task", nargs="?", help="省略时输出可复用母版")
    parser.add_argument("--natural-language", choices=LANGUAGES, default="zh")
    parser.add_argument("--terra-root", type=Path, help="Terra 仓库根目录；默认使用本系统目录的上级")
    args = parser.parse_args()
    try:
        profile = read_json(args.profile)
        task = read_json(args.task) if args.task else None
        output = markdown(render(profile, task, args.natural_language, args.terra_root))
    except (KeyError, ValueError, OSError, TypeError, AttributeError) as error:
        parser.exit(2, f"输入校验失败：{error}\n")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
