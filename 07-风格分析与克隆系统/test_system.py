"""Offline acceptance checks for the bundled documents and examples."""
import copy
import json
import re
import unittest
from pathlib import Path

from compile_prompts import FIELDS, markdown, read_json, render

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"


class SystemTests(unittest.TestCase):
    def setUp(self):
        self.profile = read_json(EXAMPLES / "profile.json")
        self.tea = read_json(EXAMPLES / "teapot.json")

    def test_three_themes_and_conditional_accent(self):
        original = copy.deepcopy(self.profile)
        for name in ("portrait", "teapot", "station"):
            with self.subTest(name=name):
                task = read_json(EXAMPLES / (name + ".json"))
                bundle = render(self.profile, task)
                zh, en, short, full = bundle
                self.assertEqual(zh["_meta"], en["_meta"])
                self.assertEqual(bundle, render(self.profile, task))
                self.assertNotIn("{{", markdown(bundle))
                for f in FIELDS:
                    self.assertEqual([(r["id"], r["priority"]) for r in zh[f]],
                                     [(r["id"], r["priority"]) for r in en[f]])
                    for rule in zh[f]:
                        self.assertIn(rule["text"], full)
                        if rule["priority"] == "must":
                            self.assertIn(rule["text"], short)
                self.assertIn(task["bindings"]["subject"]["zh"], short)
                self.assertIn(task["bindings"]["focus"]["en"], json.dumps(en, ensure_ascii=False))
                self.assertEqual("S05" in {r["id"] for r in zh["style"]}, name != "station")
                if name == "teapot":
                    self.assertFalse(any(x in short for x in ("读者", "门廊")))
        self.assertEqual(original, self.profile)

    def test_template_expansion_and_format_change(self):
        zh, en, short, full = render(self.profile)
        self.assertIn("{{subject}}", short)
        self.assertIn("If ", en["style"][-1]["text"])
        changed = copy.deepcopy(self.tea)
        changed["bindings"]["subject"] = {"zh": "一把陶壶和两只小杯", "en": "one teapot and two small cups"}
        changed["bindings"]["silhouette"] = {"zh": "居中的壶和下方两只杯的外形", "en": "the central pot and both cups below"}
        changed["verbatim"] = ["3:2"]
        changed["rules"][0].update(zh="使用 3:2 横幅。", en="Use a 3:2 landscape frame.")
        result = render(self.profile, changed, "en")
        self.assertIn("两只小杯", result[2])
        self.assertIn("landscape", result[3])
        self.assertIn("壶钮", result[2])
        self.assertNotIn("2:3", markdown(result))

    def test_invalid_instances(self):
        cases = []
        for name in ("missing_slot", "wrong_profile", "unresolved_condition", "protected_text",
                     "broken_dependency", "explicit_conflict", "mismatched_translation"):
            p, t = copy.deepcopy(self.profile), copy.deepcopy(self.tea)
            if name == "missing_slot":
                del t["bindings"]["structure"]
            elif name == "wrong_profile":
                t["profile_version"] = "2.0"
            elif name == "unresolved_condition":
                del t["flags"]["spot_accent"]
            elif name == "protected_text":
                t["verbatim"].append("展期11月28日")
            elif name == "broken_dependency":
                t["flags"]["spot_accent"] = False
                t["rules"][0]["requires"] = ["S05"]
            elif name == "explicit_conflict":
                t["rules"][0]["excludes"] = ["S01"]
            else:
                p["rules"][0]["en"] = "Draw {{focus}}."
            cases.append((name, p, t))
        for name, p, t in cases:
            with self.subTest(name=name), self.assertRaises(ValueError):
                render(p, t)

    def test_drag_document_and_memory_card(self):
        master = (ROOT / "SYSTEM.md").read_text("utf-8")
        card = (ROOT / "MEMORY.md").read_text("utf-8")
        capsule = master.split("## 跨会话调用卡", 1)[1].split("## 1　", 1)[0].strip()
        self.assertIn(capsule, card)
        raw = re.findall(r"```json\n(.*?)\n```", master, re.S)
        profile, task, example_output = map(json.loads, raw)
        self.assertEqual(render(profile)[0], example_output)
        self.assertIn("陶壶", render(profile, task)[2])
        self.assertIn("启动风格分析和克隆系统", capsule)


if __name__ == "__main__":
    unittest.main()
