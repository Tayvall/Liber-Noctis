#!/usr/bin/env python3
"""Check every data file and bundle them into data/bundle.json.

  python .github/scripts/check.py            check, then write data/bundle.json
  python .github/scripts/check.py --no-write check only

Needs only the standard library.
"""
import json, re, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDERS = {"races": "race", "transformations": "transformation", "spells": "spell", "recipes": "recipe", "items": "item",
           "places": "place", "npcs": "npc", "gamepasses": "gamepass", "articles": "article", "codes": "code"}
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
# which kinds a reference field may point at
RACE, PLACE, THING = {"race"}, {"place"}, {"item", "recipe"}
REF_KINDS = {"parent": RACE, "to": RACE, "from": RACE, "race": RACE, "restricted_to": RACE,
             "made_at": PLACE, "region": PLACE, "place": PLACE, "location": PLACE, "connects": PLACE,
             "item": THING, "any_of": THING, "items": THING, "activates": {"recipe"}, "npc": {"npc"},
             "gamepass": {"gamepass"}, "spell": {"spell"}, "via": None, "see_also": None}


def load(path, errors, root):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"{path.relative_to(root)}: not valid JSON ({e})")


def png_size(path):
    """Width and height from a PNG header, so the book can lay out pages before images load."""
    with open(path, "rb") as f: head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n": raise ValueError("not a PNG")
    return struct.unpack(">II", head[16:24])


def walk(value, path=""):
    """Yields (key, value, path) for every key/value pair, and ('', string, path) for strings in lists."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield k, v, f"{path}/{k}"
            yield from walk(v, f"{path}/{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            if isinstance(v, str):
                yield "", v, f"{path}/{i}"
            yield from walk(v, f"{path}/{i}")


def check(root=ROOT):
    errors, entries, files = [], {}, {}
    data = root / "data"
    sources = load(data / "sources.json", errors, root) or {"sources": []}
    book = load(data / "book.json", errors, root) or {"chapters": []}
    config = load(root / "config.json", errors, root) or {}
    source_ids = {s.get("id") for s in sources.get("sources", [])}

    for folder, kind in FOLDERS.items():
        for path in sorted((data / folder).glob("*.json")):
            rel = str(path.relative_to(root))
            e = load(path, errors, root)
            if not isinstance(e, dict):
                if e is not None: errors.append(f"{rel}: must be one {{ … }} object")
                continue
            if e.get("kind") != kind: errors.append(f"{rel}: kind must be \"{kind}\" in this folder")
            if e.get("id") != path.stem: errors.append(f"{rel}: id must match the file name (\"{path.stem}\")")
            if not SLUG.match(str(e.get("id", ""))): errors.append(f"{rel}: id must be lower-case words joined by hyphens")
            if e.get("id") in entries: errors.append(f"{rel}: duplicate id \"{e['id']}\" (also in {files[e['id']]})")
            for k, v, p in walk(e):
                if v in ("", [], {}, None): errors.append(f"{rel}: {p} is empty. Leave a field out instead of blanking it")
            entries[e.get("id")], files[e.get("id")] = e, rel
            # shortcut: PNG only, add other formats here if they're ever needed
            for img in e.get("images", []):
                try: img["w"], img["h"] = png_size(data / "images" / img["file"])
                except (OSError, ValueError, KeyError, TypeError): errors.append(f"{rel}: image \"{img.get('file') if isinstance(img, dict) else img}\" must be a .png in data/images")

    # references, links and sources, now that every id is known
    kind_of = {i: e.get("kind") for i, e in entries.items()}
    def ref(rel, p, target, allowed):
        if target not in kind_of: errors.append(f"{rel}: {p} points at unknown id \"{target}\"")
        elif allowed and kind_of[target] not in allowed: errors.append(f"{rel}: {p} must point at a {' or '.join(sorted(allowed))}, but \"{target}\" is a {kind_of[target]}")
    for i, e in entries.items():
        rel = files[i]
        for s in e.get("sources", []):
            sid = s.get("src") if isinstance(s, dict) else s
            if sid not in source_ids: errors.append(f"{rel}: unknown source \"{sid}\" (add it to data/sources.json)")
        for k, v, p in walk(e):
            if k == "price_by_race" and isinstance(v, dict):
                for r in v: ref(rel, f"{p}/{r}", r, RACE)
            if k in REF_KINDS:
                for t in (v if isinstance(v, list) else [v]):
                    if isinstance(t, str): ref(rel, p, t, REF_KINDS[k])
            if isinstance(v, str):
                for t in LINK.findall(v): ref(rel, p, t.strip(), None)
    for ch in book.get("chapters", []):
        for sec in ch.get("sections", []):
            for r in sec.get("races", []): ref("data/book.json", f"{ch.get('id')}/{sec.get('id')}", r, RACE)

    bundle = {"config": config, "book": book, "sources": sources.get("sources", []),
              "entries": list(entries.values())}
    return errors, bundle


def main():
    errors, bundle = check()
    for m in errors: print("✗", m)
    if errors:
        print(f"\n{len(errors)} problem(s) found. Nothing was bundled.")
        sys.exit(1)
    if "--no-write" not in sys.argv:
        (ROOT / "data" / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"✓ {len(bundle['entries'])} entries are fine" + ("" if "--no-write" in sys.argv else ", written to data/bundle.json"))


if __name__ == "__main__":
    main()
