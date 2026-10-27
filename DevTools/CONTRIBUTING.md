# Contributing to Liber Noctis

Everything in the book comes from the JSON files in `data/`. You edit those by hand. There is no editor in the site.

## The short version

1. Copy the template for the kind of thing you're adding from `DevTools/templates/` into its folder, e.g. `DevTools/templates/item.json` → `data/items/wolfsbane.json`.
2. The file name **is** the id: lower-case words joined by hyphens (`white-oak-stake`). It must be unique across the whole book.
3. Fill it in, then open a pull request. The check runs on it and tells you exactly which file and field is wrong. Nothing goes live until it passes.

## Rules every entry follows

- **Never invent game facts.** If you can't source something, leave the field out and add its name to `tbc`, e.g. `"tbc": ["cooldown"]`. The page then shows a visible **TBC**. You can also write `[TBC]` inside text.
- **Every entry lists its `sources`**, by id from `data/sources.json`. Add a new source there first if you need one: `{ "id": "…", "type": "wiki|discord|trello|video|doc|tested", "title": "…", "url": "https://…" }`.
- **`trust`** is `tested` only if someone on the team checked it in game. Use `unconfirmed` for anything taken from a source, and `broken` if it was checked and doesn't work. A `works_on` list records per-race results, e.g. "works on Originals, no effect on normal vampires", each with its own trust mark.
- **Leave out what doesn't apply.** Never write `""`, `[]` or `null`; the check rejects them. `rarity` only exists on recipes and items, and only when Tay has graded it (`common`, `uncommon`, `rare`, `epic`, `legendary`).
- **Sources disagree?** Keep both claims in `disputed` instead of picking one.
- Set `last_updated` to today's date whenever you change an entry.

## Writing text

Text fields take light markdown:

| You write | You get |
|---|---|
| `**bold**`, `*italic*`, `` `code` `` | **bold**, *italic*, `code` |
| `[[white-oak-stake]]` | a link to that entry, with its page number |
| `[[original-vampire\|Originals]]` | the same link, with your own wording |
| `- item` on each line | a bulleted list |
| `1. step` on each line | a numbered list |
| a blank line | a new paragraph |
| `[TBC]` | the TBC mark |

A link to an id that doesn't exist fails the check.

## Checking your work locally (optional)

```sh
python .github/scripts/check.py            # ids, links, empty fields: needs nothing installed
python -m http.server            # then open http://localhost:8000
```

For the full schema check, as CI runs it, use a virtual environment. Never install packages system-wide (on Arch/CachyOS pip refuses anyway):

```sh
python -m venv .venv
.venv/bin/pip install jsonschema
.venv/bin/python .github/scripts/check.py
.venv/bin/python -m unittest DevTools/test_check.py
```

In VS Code, each file's `$schema` line gives you autocomplete and inline errors as you type.

## Each kind, with a template

### race → `data/races/`

A playable race, or a variant of one (`category: "variant"` plus `parent`).

Don't write how to *become* the race here: that goes in a transformation, and the race page builds "Becoming one", the fact strip and "Ways in / ways out" from it.

Optional: `daylight`, `blood`, `starts_with`, `abilities` (`name`, `key`, `level`, `starting`, `cooldown`, `effect`, `targets`, `works_on`, `spell`), `strengths`, `weaknesses`, `ranks`, `clan`, `sections`, `tips`.

```json
{
  "$schema": "../../DevTools/schemas/race.schema.json",
  "id": "new-race",
  "kind": "race",
  "name": "New race",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "category": "variant",
  "parent": "vampire",
  "origin": "earned",
  "type_line": "Vampire variant",
  "strengths": [
    "…"
  ],
  "weaknesses": [
    "…"
  ],
  "abilities": [
    {
      "name": "Ability name",
      "key": "Q",
      "level": 100,
      "cooldown": "15 s",
      "effect": "What it does."
    }
  ]
}
```

### transformation → `data/transformations/`

One way of changing race. Store it once; both races' pages show it.

`from` is a list of race ids (any of them), or use `"from_any": true`. Optional: `steps`, `requirements`, `chance`, `when`, `cooldown`, `via` (items, NPCs or game passes it needs: their pages show "Needed for"), and `featured: true` to make it the way a race page shows first.

```json
{
  "$schema": "../../DevTools/schemas/transformation.schema.json",
  "id": "new-transformation",
  "kind": "transformation",
  "name": "New transformation",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "from": [
    "human"
  ],
  "to": "vampire",
  "method": "Short phrase for the Paths of change list",
  "steps": [
    "First step.",
    "Second step."
  ],
  "chance": "5% per try",
  "when": "At the next full moon"
}
```

### spell → `data/spells/`

A spoken spell (`form: "spoken"`), a ritual (`"ritual"`), or one granted by a quest (`"granted"`).

Optional: `incantation`, `caster` (`race`, `level`), `unlock`, `components` (`item`, `qty`, `note`), `setup`, `effect`, `duration`, `cooldown`, `targets`, `works_on`, `activates` (a recipe the spell wakes; that recipe then shows "Wake it with").

```json
{
  "$schema": "../../DevTools/schemas/spell.schema.json",
  "id": "new-spell",
  "kind": "spell",
  "name": "New spell",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "form": "spoken",
  "incantation": "Words to say!",
  "caster": {
    "race": "witch",
    "level": 25
  },
  "effect": "What it does.",
  "cooldown": "30 s"
}
```

### recipe → `data/recipes/`

Anything crafted or smelted. The recipe *is* the thing it makes: there's no separate item for the result.

`made_at` is a place id. Ingredients are `{ "item": id, "qty": n }`, or `{ "any_of": [id, id], "qty": n }` when either will do. Optional: `requires`, `fuel`, `steps`, `effect`, `duration`, `uses`, `rarity`, `works_on`.

```json
{
  "$schema": "../../DevTools/schemas/recipe.schema.json",
  "id": "new-recipe",
  "kind": "recipe",
  "name": "New recipe",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "category": "potion",
  "made_at": "witch-house",
  "rarity": "rare",
  "ingredients": [
    {
      "item": "heart",
      "qty": 1
    }
  ],
  "effect": "What it does.",
  "duration": "20 min"
}
```

### item → `data/items/`

Anything you can hold, buy, find or use.

**Never write a price here.** Prices go on the merchant who sells it (`npcs/`), and the item page shows "Sold by" by itself. Likewise "Used in" comes from recipes. `obtain` is only for other ways: `found`, `mined`, `dropped`, `reward`, `ability`, `made`, `gamepass`. Optional: `rarity`, `effect`, `use`, `restricted_to`, `durability`, `droppable`, `works_on`.

```json
{
  "$schema": "../../DevTools/schemas/item.schema.json",
  "id": "new-item",
  "kind": "item",
  "name": "New item",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "category": "ingredient",
  "effect": "What it does when used or worn.",
  "obtain": [
    {
      "method": "found",
      "text": "Where and how."
    }
  ]
}
```

### place → `data/places/`

A location. Give it `map: { "x": 36.0, "y": 27.7 }` (% from left, % from top of `assets/map.png`) to put a pin on the map.

The place page lists the folk, recipes and finds that point at it, so you don't list them here. Optional: `region` (the place it's inside), `pin`, `stations`, `features`, `dangers`, `connects`.

```json
{
  "$schema": "../../DevTools/schemas/place.schema.json",
  "id": "new-place",
  "kind": "place",
  "name": "New place",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "region": "first-village",
  "features": [
    "What is here."
  ]
}
```

### npc → `data/npcs/`

A merchant (`role: "merchant"`), ore buyer (`"buyer"`), quest giver (`"quest"`) or foe (`"enemy"`).

Each `sells` line is `item` (an id) or `name` (for goods with no page), with `price`, or `price_by_race` like `{ "human": 50, "witch": 200 }`, and/or `materials`. Optional: `restricted_to`, `limit`, `buys`, `level`, `spawn`, `hostile`, `quest` (`requires`, `objectives`, `rewards`), `map`.

```json
{
  "$schema": "../../DevTools/schemas/npc.schema.json",
  "id": "new-npc",
  "kind": "npc",
  "name": "New npc",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "role": "merchant",
  "location": [
    "first-village"
  ],
  "sells": [
    {
      "item": "heart",
      "price": 100
    }
  ]
}
```

### gamepass → `data/gamepasses/`

A Robux purchase.

Optional: `robux`, `robux_premium`, `grants`, `commands`.

```json
{
  "$schema": "../../DevTools/schemas/gamepass.schema.json",
  "id": "new-gamepass",
  "kind": "gamepass",
  "name": "New gamepass",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "robux": 100,
  "grants": [
    "What it gives."
  ]
}
```

### article → `data/articles/`

A free-form page about how the game works.

`section` must be one of the Workings section ids in `data/book.json`: `levels`, `life`, `sun`, `moon`, `combat`, `gathering`, `passes`, `codes`, `myths`. Each item in `sections` is a heading plus markdown.

```json
{
  "$schema": "../../DevTools/schemas/article.schema.json",
  "id": "new-article",
  "kind": "article",
  "name": "New article",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "section": "levels",
  "sections": [
    {
      "heading": "A heading",
      "body": "Text, with [[witch]] links to other entries."
    }
  ]
}
```

### code → `data/codes/`

A redeem code.

`status` is `active`, `thin`, `disputed` or `expired`. **Always update `checked`** when you try a code: codes expire without warning, and the page shows the date.

```json
{
  "$schema": "../../DevTools/schemas/code.schema.json",
  "id": "new-code",
  "kind": "code",
  "name": "New code",
  "summary": "One sentence: what it is and why it matters.",
  "trust": "unconfirmed",
  "sources": [
    "tay"
  ],
  "last_updated": "2026-10-27",
  "code": "EXAMPLECODE",
  "reward": "2× XP for 1 h",
  "status": "active",
  "checked": "2026-10-27"
}
```

## Where entries appear in the book

`data/book.json` decides that. A race appears in its race's sub-chapter (with its variants). Everything else is placed by `kind` plus `form`, `category` or `section`. Add a new section there if you need one: the contents, chapter indexes and stops update themselves.
