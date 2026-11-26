import tempfile
import unittest
from pathlib import Path

from compile_prompts import read_json, render


class TerraTests(unittest.TestCase):
    def setUp(self):
        self.source = Path(__file__).resolve().parent
        self.task = read_json(self.source / "examples/terra/task.json")
        self.profile = read_json(self.source / "examples/terra/profile.json")

    def test_case_records_survive_in_all_versions(self):
        zh, en, short, full = render(self.profile, self.task)
        for output in [zh["technical"][0]["text"], en["technical"][0]["text"], short, full]:
            for row in ["大不列颠与爱尔兰｜1930｜25｜10｜15｜40", "澳大利亚｜1930｜25｜13｜12｜52"]:
                self.assertIn(row, output)

    def test_changed_source_and_missing_rows(self):
        with tempfile.TemporaryDirectory() as root:
            self.task["terra_source"]["csv"] = "case.csv"
            data = Path(root) / "case.csv"
            cols = self.task["terra_source"]["columns"]
            data.write_text(",".join(cols) + "\n甲,示例,25,3,22,12\n", encoding="utf-8-sig")
            with self.assertRaisesRegex(ValueError, "缺少记录"):
                render(self.profile, self.task, terra_root=root)
            self.task["terra_source"]["select"] = ["甲"]
            self.assertIn("甲｜示例｜25｜3｜22｜12", render(self.profile, self.task, terra_root=root)[2])
