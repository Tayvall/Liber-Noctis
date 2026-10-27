"""Tests for .github/scripts/check.py. Run: python -m unittest DevTools/test_check.py"""
import json, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".github" / "scripts"))
import check

REAL = Path(__file__).resolve().parent.parent
BASE = {"summary": "x", "trust": "unconfirmed", "sources": ["tay"], "last_updated": "2026-10-27"}


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        shutil.copytree(REAL / "DevTools" / "schemas", self.root / "DevTools" / "schemas")
        (self.root / "data").mkdir()
        self.write("data/sources.json", {"sources": [{"id": "tay", "type": "tested", "title": "Tay"}]})
        self.write("data/book.json", {"chapters": [{"id": "c", "numeral": "I", "ordinal": "First", "title": "C", "intro": "x",
                                                    "sections": [{"id": "s", "title": "S"}]}]})
        self.write("config.json", {})
        self.item("heart", name="Heart", category="ingredient")

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, rel, obj):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj) if not isinstance(obj, str) else obj)

    def item(self, id, folder="items", **f):
        self.write(f"data/{folder}/{id}.json", {"id": id, "kind": "item", **BASE, **f})

    def errors(self):
        return check.check(self.root)[0]

    def test_valid_data_passes(self):
        self.assertEqual(self.errors(), [])

    def test_real_data_passes(self):
        self.assertEqual(check.check(REAL)[0], [])

    def test_unknown_link_and_reference(self):
        self.item("cup", name="Cup", category="ingredient", notes="See [[no-such-thing]].", see_also=["ghost"])
        msgs = " ".join(self.errors())
        self.assertIn('unknown id "no-such-thing"', msgs)
        self.assertIn('unknown id "ghost"', msgs)

    def test_wrong_target_kind(self):
        self.item("cup", name="Cup", category="ingredient", restricted_to=["heart"])
        self.assertTrue(any("must point at a race" in m for m in self.errors()))

    def test_duplicate_id_across_kinds(self):
        self.write("data/places/heart.json", {"id": "heart", "kind": "place", "name": "Heart", **BASE})
        self.assertTrue(any("duplicate id" in m for m in self.errors()))

    def test_empty_field_and_bad_json(self):
        self.item("cup", name="Cup", category="ingredient", effect="")
        self.write("data/items/bad.json", '{"id": "bad",')
        msgs = " ".join(self.errors())
        self.assertIn("is empty", msgs)
        self.assertIn("not valid JSON", msgs)

    def test_id_must_match_file_and_folder(self):
        self.write("data/items/cup.json", {"id": "mug", "kind": "place", "name": "Cup", **BASE})
        msgs = " ".join(self.errors())
        self.assertIn("must match the file name", msgs)
        self.assertIn('kind must be "item"', msgs)

    def test_templates_are_valid_entries(self):
        shutil.rmtree(self.root / "data")
        shutil.copytree(REAL / "data", self.root / "data")
        for t in (REAL / "DevTools" / "templates").glob("*.json"):
            e = json.loads(t.read_text())
            folder = next(f for f, k in check.FOLDERS.items() if k == e["kind"])
            self.write(f"data/{folder}/{e['id']}.json", e)
        self.assertEqual(check.check(self.root)[0], [])

    @unittest.skipIf(check.schema_validator(REAL) is None, "jsonschema not installed")
    def test_schema_rejects_rarity_where_it_does_not_belong(self):
        self.write("data/places/hut.json", {"id": "hut", "kind": "place", "name": "Hut", "rarity": "rare", **BASE})
        self.assertTrue(any("hut.json" in m and "rarity" in m for m in self.errors()))


if __name__ == "__main__":
    unittest.main()
