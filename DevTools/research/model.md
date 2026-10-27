# Liber Noctis: data model proposal (for approval)

Based on `research/catalogue.md`. Nothing here is built yet.

## 1. Kinds

There are **10 kinds**. Compared with the brief:
- **added**: `gamepass`
- **folded in**: rituals are `spell` with `form: "ritual"`; sub-races are `race` with `parent`; quests live on the NPC that gives them (the wiki has only two quests)
- **merged**: `recipe` *is* the thing it makes. There is no separate "result" item, so Praesidium Potion is one entry and one page.

### Shared base (every entry)
| field | req | notes |
|---|---|---|
| `id` | ✓ | slug, unique across **all** kinds, so `[[id]]` never needs a prefix |
| `kind` | ✓ | `race` `transformation` `spell` `recipe` `item` `place` `npc` `gamepass` `article` `code` |
| `name` | ✓ | |
| `aka` | | other names, searchable (`"Framente"`, `"Immortality Spell"`) |
| `summary` | ✓ | one or two sentences, markdown |
| `trust` | ✓ | `tested` · `unconfirmed` · `broken` |
| `sources` | ✓ | ≥1 id from `data/sources.json`, as a string or `{ "src": id, "note": "…" }` |
| `last_updated` | ✓ | `YYYY-MM-DD` |
| `see_also`, `tags` | | ids / words |
| `tbc` | | names of fields we know matter but can't source. The template prints them as **[TBC]** instead of hiding them |
| `disputed` | | markdown lines; rendered as a ⚠️ box ("sources disagree") |
| `notes` | | markdown |

Markdown is limited to `**bold**`, `*italic*`, lists, `[[id]]` and `[[id|label]]`. A link renders as *label — p. N*.
Everything else is optional, and **absent means absent**: no `""`, no `null`, no `"Nan"`. The schemas reject empty strings and empty arrays.

### race
`category` (`playable` | `variant`) · `parent` (race id, variants only) · `type_line` ("Turned, not born") · `origin` (`starting` | `turned` | `gamepass` | `earned` | `upcoming`) · `daylight` · `blood` · `starts_with` [md] · `abilities` [{`name`, `key`, `level`, `starting`, `cooldown`, `effect`, `works_on`, `spell` (id)}] · `strengths` [md] · `weaknesses` [md] · `ranks` [{`name`, `from`, `to`}] · `clan` {`name`, `body`} · `tips` [md] · `sections` [{`heading`, `body`}] for things like Feeding or Minions.
*The "Becoming one" steps and the Begins as / Chance / Turns at strip are computed from transformations, never stored on the race.*

### transformation (stored once)
`from` [race ids, any of] or `from_any: true` · `to` (race id) · `method` (short; shows in "Paths of change") · `steps` [md] · `requirements` [md with links] · `chance` · `when` · `cooldown` · `via` (ids of items, gamepasses or NPCs involved, so pages can link back).

### spell
`form` (`spoken` | `ritual`) · `incantation` · `caster` {`race`, `level`} · `unlock` (md, e.g. "the Rat Alchemist quest") · `components` [{`item`, `qty`, `note`}] · `setup` [md] · `effect` · `duration` · `cooldown` · `works_on` · `activates` (recipe id: "Praesidium!" wakes the Praesidium Potion).

### recipe
`category` (`potion` | `trinket` | `weapon` | `material` | `charm`) · `made_at` (place id) · `requires` {`race`, `level`} · `ingredients` [{`item`, `qty`, `note`} or {`any_of`: [ids], `qty`}] · `fuel` [same shape] · `steps` [md] · `effect` · `duration` · `uses` · `rarity` (only if known).

### item
`category` (`ingredient` | `weapon` | `trinket` | `tool` | `consumable` | `food` | `ore` | `furniture`) · `rarity` · `effect` · `use` · `restricted_to` [race ids] · `durability` · `droppable` (bool) · `obtain` [{`method`: `found` | `mined` | `dropped` | `reward` | `ability` | `made` | `gamepass`, plus `place` / `npc` / `race` / `ability` / `gamepass` / `uses` [ids], `text`}].
*Bought and crafted are never written here.* They are computed from merchants and recipes.

### place
`region` (parent place id) · `map` {`x`, `y`} as % of `assets/map.png` · `pin` (`village` | `base` | `merchant` | `enemies` | `area`) · `stations` [names] · `features` [md] · `dangers` [md] · `connects` [ids].

### npc
`role` (`merchant` | `buyer` | `quest` | `enemy`) · `location` [place ids] · `sells` [{`item`, `price`, `price_by_race` {race: n}, `materials` [{`item`, `qty`}], `restricted_to` [race ids], `limit`, `note`}] · `buys` [{`item`, `qty`, `price`}] · `level` · `spawn` · `hostile` · `quest` {`requires` [md], `objectives` [md], `rewards` [md]}.

### gamepass
`robux` · `robux_premium` · `grants` [md] · `commands` [{`cmd`, `does`}].

### article (mechanics, guides)
`section` (Workings section id) **or** `race` (puts the article inside that race's sub-chapter) · `body` (md, optional lead) · `sections` [{`heading`, `body`}].

### code
`code` · `reward` · `status` (`active` | `thin` | `disputed` | `expired`) · `checked` (date). Every code page and the codes list show *"checked {date}: codes expire without warning"*.

## 2. Relations

Each relation is stored once and read both ways:

| stored on | field | shown as |
|---|---|---|
| recipe | `ingredients[].item`, `fuel[].item` | Item / recipe page → **Used in** |
| npc | `sells[].item`, `sells[].materials[].item` | Item page → **Sold by** (with price) and **Used in** |
| npc | `buys[].item` | Item page → **Bought by** |
| transformation | `from`, `to` | Race page → **Ways in / ways out**, **Becoming one**, fact strip. Races opener → **Paths of change** |
| transformation | `via` | Item / gamepass page → **Needed for** |
| npc | `location` · recipe `made_at` · item `obtain[].place` · place `region` | Place page → **Who and what is here** |
| spell | `activates` | Recipe page → stat strip "Wake it with" |
| spell | `caster.race` | Race page → **Spells** |
| race | `parent` | Race page → **Variants** |
| any | `see_also` | See-also cards (both directions) |
| any | `[[id]]` in prose | link with page number. CI also checks the target exists |

**CI fails on**:
- schema violations
- duplicate ids
- `id` ≠ filename
- unknown ids in any reference or `[[link]]`
- unknown source ids
- `rarity` on a kind other than recipe or item
- `map` coordinates outside 0–100

## 3. One real example per kind

```jsonc
// data/races/werewolf.json
{ "id": "werewolf", "kind": "race", "name": "Werewolf", "category": "playable", "origin": "turned",
  "type_line": "Turned, not born",
  "summary": "A race you catch, not choose: a scratch, a 5% chance, and the next full moon.",
  "trust": "unconfirmed", "sources": ["wiki-werewolf", "itzvexo-werewolf", "discord-2026-10-15"],
  "last_updated": "2026-10-27",
  "blood": "No blood meter. Hunger is managed by eating bodies with the devour action.",
  "abilities": [
    { "name": "Howl", "effect": "Summons other werewolves." },
    { "name": "Poison", "effect": "Any werewolf attack poisons vampires." }
  ],
  "strengths": ["The strongest werewolf on the server gets the **Alpha** tag, a 20% buff.",
                "Full wolf mode with the [[werewolf-ring]]."],
  "weaknesses": ["Cannot bite [[original-vampire|Originals]]."],
  "clan": { "name": "Pack", "body": "The werewolf counterpart of bloodlines and covens." },
  "tbc": ["daylight", "abilities.key", "abilities.level", "strengths", "weaknesses"] }

// data/transformations/human-to-werewolf.json
{ "id": "human-to-werewolf", "kind": "transformation", "name": "Human to Werewolf",
  "from": ["human"], "to": "werewolf", "method": "A werewolf's scratch, then the full moon",
  "summary": "Get scratched on the back by a strong werewolf and wait for the moon.",
  "requirements": ["You must be [[human]]. Revert first with a [[human-potion]] if you are not."],
  "steps": ["Find a werewolf player, or a werewolf NPC of level 6,000 or higher ([[werewolf-npcs-7k]]).",
            "Get scratched on the back until the infection takes.",
            "Wait for the full moon. You turn the moment it rises."],
  "chance": "5% per scratch", "when": "The next full moon",
  "via": ["human-potion", "werewolf-npcs-7k"],
  "disputed": ["The Werewolf page puts the Lv 6,000 limit on NPCs only; the Beginner Guide applies it to any werewolf."],
  "trust": "unconfirmed", "sources": ["wiki-werewolf", "wiki-beginner-guide", "wiki-misconceptions"],
  "last_updated": "2026-10-27" }

// data/spells/tracking-ritual.json   (migrated: "Locate Spell")
{ "id": "tracking-ritual", "kind": "spell", "form": "ritual", "name": "Tracking Ritual",
  "aka": ["Locate Spell"], "incantation": "Quaerere <username>",
  "summary": "Find and spy on a player anywhere on the map.",
  "caster": { "race": "witch" },
  "components": [{ "item": "candle", "qty": 3, "note": "up to 5 may be placed; 3 trigger it" },
                 { "item": "heart", "qty": 1 }],
  "setup": ["Place three candles in a triangle.", "Hold the heart and click the ground inside the candles.",
            "Say the incantation with the player's username."],
  "effect": "Tracks the named player.",
  "trust": "unconfirmed", "sources": ["handbook", "wiki-witch-spells"], "last_updated": "2026-10-27",
  "tbc": ["caster.level", "duration", "cooldown"] }

// data/recipes/praesidium-potion.json
{ "id": "praesidium-potion", "kind": "recipe", "category": "potion", "name": "Praesidium Potion",
  "aka": ["Praesidium"], "rarity": "rare", "made_at": "witch-house",
  "summary": "A remedy that guards the drinker against a vampire's bite.",
  "effect": "Immunity to neck snaps and vampire bites.",
  "duration": "20 min with a [[blood-cup]] · 40 min with a [[blood-dish]]",
  "ingredients": [{ "any_of": ["blood-cup", "blood-dish"], "qty": 1 }, { "item": "verbena", "qty": 1 }],
  "steps": ["Have a vampire fill a cup or dish with blood.", "Combine it with a verbena flower at the cauldron.",
            "Say [[praesidium|“Praesidium!”]] in chat when you use it."],
  "trust": "tested", "sources": ["handbook", "wiki-witch-spells"], "last_updated": "2026-10-27" }

// data/items/dagger.json   (bought for silver + cash: the price lives on the Weapons Shop)
{ "id": "dagger", "kind": "item", "category": "weapon", "name": "Dagger", "rarity": "uncommon",
  "summary": "A short blade from the weaponsmith, and the base of two witch brews.",
  "effect": "Damage scales with your level and, for humans, Strength.",
  "trust": "unconfirmed", "sources": ["handbook", "wiki-items", "discord-2026-10-26"], "last_updated": "2026-10-27" }
  // page shows → Sold by: Weapons Shop — $400 + 20 × Silver — p. 51
  //            → Used in: Inhuman Potion — p. 22 · White Oak Ash Dagger — p. 39

// data/places/witch-house.json   (was the "Graveyard Altar")
{ "id": "witch-house", "kind": "place", "name": "Witch House", "region": "cemetery",
  "pin": "base", "map": { "x": 8.8, "y": 85.2 }, "stations": ["Magic Cauldron"],
  "summary": "Witch spawn and crafting house in the cemetery.",
  "features": ["The Magic Cauldron, where every witch craft is made."],
  "trust": "unconfirmed", "sources": ["wiki-map", "wiki-witch"], "last_updated": "2026-10-27",
  "tbc": ["dangers"] }
  // page shows → Made here: Praesidium Potion, Temporary Sun Ring, Inhuman Potion, …

// data/npcs/general-shop.json
{ "id": "general-shop", "kind": "npc", "role": "merchant", "name": "General Shop",
  "aka": ["Merchant, 1st village"], "location": ["first-village"],
  "summary": "The first village's everyday merchant.",
  "sells": [
    { "item": "human-blood",  "price_by_race": { "human": 50, "witch": 200, "vampire": 200 } },
    { "item": "human-potion", "price_by_race": { "human": 50, "witch": 250, "vampire": 250 } },
    { "item": "cup", "price": 450 }, { "item": "dish", "price": 450 },
    { "item": "xp-booster", "price": 100000 }, { "item": "lantern", "price": 350 },
    { "item": "metal-ring", "price": 5000 }, { "item": "pumpkin-lantern", "price": 400 } ],
  "trust": "unconfirmed", "sources": ["wiki-items"], "last_updated": "2026-10-27" }

// data/gamepasses/original-vampire-pass.json
{ "id": "original-vampire-pass", "kind": "gamepass", "name": "Original Vampire (ANTICIPATED)",
  "robux": 1895, "robux_premium": 1706,
  "summary": "The only way to become an Original Vampire.",
  "grants": ["[[original-vampire]] status", "The Natural-Born [[vampire]] start"],
  "trust": "unconfirmed", "sources": ["wiki-game-passes", "wiki-misconceptions"], "last_updated": "2026-10-27" }
  // page shows → Needed for: Original Vampire, Natural-Born Vampire, Original Hybrid

// data/articles/clash.json
{ "id": "clash", "kind": "article", "section": "combat", "name": "Clash",
  "summary": "A timed skill check when two fighters meet blow for blow, in PvP or PvE.",
  "sections": [
    { "heading": "The skill check", "body": "A bar appears: **CLICK & HOLD M1**. Keep the marker in the target zone to build seconds; whoever holds more when the timer ends wins." },
    { "heading": "Level range", "body": "Since 26 Oct 2026, clashes don't happen across a level gap of 500 or more." } ],
  "disputed": ["Whether a far higher player can still force a clash on a lower one is unknown."],
  "trust": "unconfirmed", "sources": ["wiki-clash", "discord-2026-10-26"], "last_updated": "2026-10-27" }

// data/codes/thx17klikes.json
{ "id": "thx17klikes", "kind": "code", "name": "THX17KLIKES", "code": "THX17KLIKES",
  "summary": "Likes-milestone reward.", "status": "active", "checked": "2026-10-25",
  "reward": "3x XP for 1 h, 150k Cash and 200 Werewolf Skin Fragments",
  "trust": "unconfirmed", "sources": ["wiki-codes"], "last_updated": "2026-10-27" }
```
`data/sources.json` holds entries like `{ "id": "wiki-witch-spells", "type": "wiki", "title": "Witch Spells", "url": "https://vampire-life.fandom.com/wiki/Witch_Spells", "rev": 508, "date": "2026-10-26" }`, plus `handbook`, `discord-*`, `trello`, `itzvexo-werewolf` and `robloxpro492-doc`.

## 4. Migrating `recipes.json` (all 17)

| old | → kind / id | what changes |
|---|---|---|
| Change Spell Colour | recipe `magic-colour-change` | ingredients: Colored Fragment (any colour), Heart, Ruby; rarity legendary |
| Sun Ring | recipe `temporary-sun-ring` | renamed per wiki, Witch Lv 100+; "Sun Ring" kept in `aka` |
| Praesidium Potion | recipe `praesidium-potion` | cup **or** dish via `any_of`; durations from `stat` |
| Inhuman Potion | recipe `inhuman-potion` | Lv 1000+, 5 h; Stake-vs-Ash-Dagger conflict goes in `disputed` |
| White Oak Ash Dagger | recipe `white-oak-ash-dagger` | Lv 800+; "Inf" → `uses` [TBC, see Q6] |
| Praesidium! | spell `praesidium` | `activates: praesidium-potion` |
| Strength! | spell `strength` | Lv 25, 38 s, no stacking; the Witch ability links to it |
| Sanguis Tuus Vita Mea | spell `sanguis-tuus-vita-mea` | Lv 2000+, 20 min cooldown, works on Original Vampires |
| Locate Spell | spell `tracking-ritual` (ritual) | wiki name; "Locate Spell" kept in `aka` |
| Dagger | item `dagger` | price moves to `weapons-shop.sells` |
| Heart | item `heart` | obtain: ability Heart Extraction (vampire, witch) |
| Blood Cup | item `blood-cup` | obtain: made from [[cup]] by a vampire; "sold at merchant" now belongs to Cup |
| Blood dish | item `blood-dish` | same as Blood Cup |
| Metal Ring | item `metal-ring` | General Shop, $5000 |
| Vampire Blood | item `vampire-blood` | Vampire Shop, $250 |
| Framente <Colour> | item `colored-fragment` | found anywhere on the map; one entry, colours listed |
| Verbena | item `verbena` | found anywhere on the map; aka Vervain |

**Dropped fields**: `rarity` on spells, `station` on non-recipes, every empty `""` / `[]`, `incantation` on non-spells, and `type` (replaced by `kind` + `category`).
**New entries the migration needs** (all from the wiki): cup, dish, candle, ruby, silver, white-oak-stake, witch-house, cemetery, first-village, general-shop, vampire-shop, weapons-shop.

**Typo fixes**:
1. `Graveyarm Altar` → becomes the place `witch-house`, so the string is gone
2. `1z White Oak Stake` → 1x
3. `perminantly` → permanently
4. `Unown` → absent (the wiki gives 5 h)
5. `Nan` ×2 → absent
6. `cadles` → candles
7. `Blood dish` → Blood Dish
8. `Temporary lets` → Temporarily lets
9. `Will Protect` → protects
10. `lvl 100+` → Lv 100+
11. `400 Coins` → $400 (the game's currency is cash)

## 5. Book placement

`data/book.json` lists chapters and sections. Each section has a match rule, e.g. `{ "id": "potions", "match": { "kind": "recipe", "category": "potion" } }`, so new entries file themselves.

| Chapter | Sections |
|---|---|
| **I Races** | one sub-chapter per race: Humans (+ Vampire Hunter), Vampires (+ Cannibal, Cannibal Raised, Vegan; minions, feeding), Original Vampires, Witches, Werewolves, Hybrids (Original Hybrid + the upcoming Hybrid) |
| **II Grimoire** | Spells (spoken), Potions, Rituals |
| **III Items & Alchemy** | Ingredients (ingredients, ores, materials), Weapons, Trinkets (trinkets, charms, tools, food) |
| **IV Realm** | Map, Places, Merchants & folk (all NPCs) |
| **V Workings** | Levels & XP · Day, Night & the Sun · The Moon & Events · Combat (Clash) · Gathering (Mining) · Game Passes & Servers · Codes · Common Misconceptions |

Chapter V is wider than the brief because the catalogue has these pages. "The full moon" sits in The Moon & Events, mostly [TBC].

## 6. Files and contributors

**Recommendation: one file per entry, in a folder per kind.**

| | one file per entry | one file per kind |
|---|---|---|
| merge conflicts | rare (two people rarely edit the same file) | frequent (`items.json` will have about 80 entries) |
| errors | CI names the exact file | one stray comma breaks a whole kind |
| adding an entry | copy a template, new file | find the right place in a long array |
| seeing everything at once | harder | easy |
| deploy | CI bundles into `data/bundle.json` | could be served as is |

Local preview needs **no build step**. `python -m http.server` serves folder listings, so when `bundle.json` is missing, the page reads `data/<kind>/` from those listings. On Pages it uses the bundle CI made.

```
index.html  book.css  book.js  config.json  .nojekyll
assets/map.png
data/  book.json  sources.json
       races/ transformations/ spells/ recipes/ items/ places/ npcs/ gamepasses/ articles/ codes/
schemas/  base.schema.json  <kind>.schema.json …
tools/check.py     # stdlib: ids, refs, [[links]], dupes → writes data/bundle.json; schemas too if jsonschema is installed
templates/<kind>.json
.github/workflows/pages.yml   # on PR: check. On push to main: check → bundle → deploy-pages
README.md  CONTRIBUTING.md
```
**"A typo never breaks the live site"**: Pages deploys only from the Action, and only after the check passes. A failed check leaves the last good site live. This needs Settings → Pages → Source = **GitHub Actions**.
Each data file starts with `"$schema": "../../schemas/item.schema.json"`, so VS Code autocompletes fields and flags errors as you type.
For running the check locally on CachyOS:
```
python -m venv .venv
.venv/bin/pip install jsonschema
.venv/bin/python tools/check.py
```
Without the venv, the stdlib checks still run.

**Contributor template** (`templates/item.json`, one per kind; required fields first, optional ones as a commented list in CONTRIBUTING):
```json
{
  "$schema": "../../schemas/item.schema.json",
  "id": "my-item-name",
  "kind": "item",
  "name": "My Item Name",
  "category": "ingredient",
  "summary": "One sentence: what it is and why you'd want it.",
  "trust": "unconfirmed",
  "sources": ["handbook"],
  "last_updated": "2026-10-27"
}
```

## 7. Conflicts with the brief (please decide)

1. **Rarity colours fail AA as text.** On the darkest parchment (#d3b886): Common 2.9, Uncommon 2.7, Rare 3.3, Epic 3.7, Legendary 2.1. Legendary fails even on light parchment (3.3). Gold #c9a45c on the Items and Realm leather stops is 2.7.
   **Proposal:**
   - the rarity *label* in ink, the colour only on the gem (with a dark outline so it passes 3:1)
   - stop labels in bright gold #f3dca0 (≥4.7 on every chapter colour)
   - the parchment reaches #d3b886 only in the margin outside the text block. Muted ink and gold-brown headings stay ≥4.5 where text sits.
2. **Page numbers depend on screen size.** The packing is measured, so "p. 25" and "of 72" differ between a phone and a PC, and after a resize. Deep links use ids, so they are unaffected.
3. **"Data cached for the session" without browser storage**: kept in memory. A reload re-fetches, served from the HTTP cache.
4. **The map image can't be downloaded** (CDN 403). The pins are real, from the wiki map (873×664), but you'll need to save `Vampire-Life-world-map.png` as `assets/map.png`. Until then a labelled placeholder shows.
5. **The fact strip doesn't fit every race.** Human has no way in, and Original Vampire is gamepass-only. The strip shows "You spawn as one" or "Gamepass" for those instead of the three cells.

## 8. Suggestions (not built unless you say yes)

- **S1 Licence credit.** The wiki's text is CC BY-SA. The "Of This Book" page and the README should credit the Vampire Life Wiki contributors and link the pages we drew on. Reason: it's required if we copy wording, and polite if we only use facts. I'll paraphrase rather than copy.
- **S2 Trust meaning.** "✓ Tested" means someone on *your* team checked it in game. Wiki facts are sourced but untested, so they get "? Unconfirmed" without [TBC]. [TBC] is only for facts nobody has sourced. Reason: otherwise either almost everything is [TBC], or "Tested" stops meaning anything.
- **S3 "Disputed" box.** The wiki marks ⚠️ disagreements: hybrid chance 0.5% vs 0.1%, vampire ranks, Shotgun price. A small ⚠️ box keeps both claims instead of us picking one. It is not in the mockup.
- **S4 `aka` in search.** Old names (Locate Spell, Sun Ring, Framente, Graveyard Altar) keep finding the new entries.
- **S5 Split files.** `index.html` + `book.css` + `book.js` instead of one file. Reason: easier for contributors to diff. No build step either way.

## 9. Questions I need answered

1. Is the **Graveyard Altar** the Magic Cauldron in the Witch House (the wiki's name)? Or a separate altar in the graveyard?
2. Is **"Framente"** what the game calls the fragment, or a typo for "Fragment"? The wiki says "Colored Fragment".
3. Is **rarity** shown in the game, or is it your own grading? Either way it stays only where your handbook had it. I just want the legend to say which.
4. The **official Trello URL**: the wiki cites it but never links it.
5. **Config values**: maintainer name for "Set down by…", and the game version (the wiki never states one).
6. **White Oak Ash Dagger "Inf"**: unlimited uses? And "holds down a vampire permanently": while staked, or forever?
7. **Ruby in Magic Colour Change**: raw Ruby ore or a Ruby Bar? The wiki says "1 Ruby" and the mining note implies ore.
