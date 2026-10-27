# Liber Noctis

**An unofficial field guide to the Roblox game [Vampire Life](https://vampire-life.fandom.com/wiki/Vampire_Life_Wiki), written as an old book.**

Liber Noctis gathers what a player needs to know in one place: the races and how to change between them, spells and rituals, potions and other recipes, items, places, merchants, game passes, codes, and the rules of the world (levels, death, the sun, the moon and events). You read it like a book, with page turns, chapters and a contents page, and every entry links to the things it mentions, so you can follow a potion to its ingredients, then to the merchant who sells them, then to where that merchant stands on the map.

Every fact cites its source, and each entry is marked as **tested** (checked in game), **unconfirmed** (taken from a source but not yet checked) or **broken**. Anything nobody has confirmed yet is marked **TBC** instead of being guessed. Where sources disagree, the book shows both claims.

## A work in progress

The book is far from finished. Some entries are thin, some facts are unconfirmed, and the game keeps changing under it. Help of any size is welcome:

- **Spotted something wrong or out of date?** Open an [issue](https://github.com/Tayvall/Liber-Noctis/issues) and say what it should be, and how you know.
- **Tested something in game?** Telling us that a TBC value, a code or a recipe does or doesn't work is one of the most useful things you can do.
- **Want to write or fix an entry yourself?** See [For developers](#for-developers) below and open a pull request.
- **Ideas for the site itself** (layout, search, reading on a phone) are welcome too.

## Credits

Facts come from the [Vampire Life Wiki](https://vampire-life.fandom.com/wiki/Vampire_Life_Wiki) (text under CC BY-SA), the game's official Discord announcements as quoted there, and the maintainers' own testing. The book's last page lists every source and the people who keep it. Vampire Life is made by dutdk; this guide is not affiliated with it.

---

## For developers

The site is plain HTML, CSS and JavaScript with no framework and no build step to run by hand. All of the book's content lives in JSON files; the page reads them and lays them out.

### Layout

| Path | What it is |
|---|---|
| `index.html` | The whole site: layout, page templates, page turning, search |
| `config.json` | Book title, maintainer, the "last inscribed" date, links |
| `data/book.json` | The chapters and sections, and which entries go in each |
| `data/sources.json` | Every source an entry can cite |
| `data/<kind>/<id>.json` | One file per entry (see the kinds below) |
| `data/bundle.json` | Every data file merged into one, written by the check. Don't edit it by hand |
| `assets/map.png` | The world map |
| `.github/scripts/check.py` | Checks all the data and writes `data/bundle.json` |
| `.github/workflows/pages.yml` | Runs the check on every push and pull request, and publishes `main` |

The kinds of entry, each in its own folder under `data/`:

| Folder | Holds |
|---|---|
| `races/` | Playable races and their variants |
| `transformations/` | Each way of changing from one race to another |
| `spells/` | Spoken spells, rituals and quest-granted spells |
| `recipes/` | Anything crafted or smelted: potions, weapons, charms, materials |
| `items/` | Anything you can hold, buy, find or use |
| `places/` | Locations, with optional map pins |
| `npcs/` | Merchants, ore buyers, quest givers and enemies |
| `gamepasses/` | Robux purchases |
| `articles/` | Free-form pages on how the game works |
| `codes/` | Redeem codes |

### Adding, changing or removing an entry

To add an entry, create a JSON file in the right folder. To change one, edit its file. To remove one, delete it. You don't need to list the file anywhere: the check picks up every file it finds.

1. **The file name is the id.** Use lower-case words joined by hyphens, e.g. `data/items/white-oak-stake.json` has `"id": "white-oak-stake"`. Ids must be unique across the whole book.
2. **Copy an existing entry of the same kind** as a starting point. Every entry has these fields:

   ```json
   {
     "id": "blood-cup",
     "kind": "item",
     "name": "Blood Cup",
     "summary": "One sentence: what it is and why it matters.",
     "trust": "unconfirmed",
     "sources": ["tay", "wiki-witch-spells"],
     "last_updated": "2026-10-27"
   }
   ```

   The rest depends on the kind: an item has `category` and `obtain`, a recipe has `made_at` and `ingredients`, and so on.
3. **Run the check** (below), then open a pull request.

The rules every entry follows:

- **Never invent game facts.** If you can't source something, leave the field out and add its name to `tbc`, e.g. `"tbc": ["cooldown"]`. The page then shows a visible TBC. You can also write `[TBC]` inside text.
- **Every entry lists its `sources`** by id from `data/sources.json`. If you need a new source, add it there first.
- **`trust`** is `tested` only if someone checked it in game, `unconfirmed` if it comes from a source, and `broken` if it was checked and doesn't work. A `works_on` list records results race by race.
- **Leave out fields that don't apply.** Never write `""`, `[]` or `null`; the check rejects them.
- **If sources disagree,** put both claims in `disputed` rather than picking one.
- **Set `last_updated`** to today's date whenever you change an entry.

### Links are stored once and shown both ways

You record a relation on one side only, and the book works out the other side:

- A merchant (`npcs/`) lists what it `sells` and the prices, so each item's page shows "Sold by". **Never put a price on the item itself.**
- A recipe lists its `ingredients`, so each ingredient shows "Used in". A recipe is the thing it makes: there's no separate item for the result.
- A transformation has `from` and `to`, and both races' pages show it under "Ways in / ways out". Don't describe how to become a race in the race's own file.
- A place doesn't list who or what is there: the folk, recipes and finds that point at it with `location` or `made_at` show up on its page by themselves.

### Writing text

Text fields take light markdown:

| You write | You get |
|---|---|
| `**bold**`, `*italic*`, `` `code` `` | **bold**, *italic*, `code` |
| `[[white-oak-stake]]` | a link to that entry, with its page number |
| `[[original-vampire\|Originals]]` | the same link with your own wording |
| `- item` / `1. step` on each line | a bulleted or numbered list |
| a blank line | a new paragraph |

A link to an id that doesn't exist fails the check.

### Where entries appear in the book

`data/book.json` decides that. Races are listed in their section by id. Everything else is placed by a `match` rule on its `kind` plus its `form`, `category` or `section`. For example, the Potions section matches `{ "kind": "recipe", "category": ["potion"] }`. To make a new section, add it to a chapter there; the contents page, chapter indexes and page numbers update themselves.

### Other things you might change

- **The "last inscribed" date, maintainer or links:** `config.json`.
- **Map pins:** give a place `"map": { "x": 36.0, "y": 27.7 }`, as a percentage from the left and from the top of `assets/map.png`. If the map image is missing, the map page shows a placeholder with the pins on it.
- **Codes:** update `status` (`active`, `thin`, `disputed` or `expired`) and `checked` whenever you try one. Codes expire without warning, and the page shows the date they were last checked.
- **Look and behaviour of the site:** all in `index.html`.

### Checking and previewing locally

```sh
python .github/scripts/check.py   # checks ids, links and empty fields, then rewrites data/bundle.json
python -m http.server             # then open http://localhost:8000
```

The page reads `data/bundle.json`, so **run the check after every data change** or the preview will show the old content. Opening `index.html` straight from disk won't work; it needs to be served.

### Publishing

The site is hosted on GitHub Pages. Every push and pull request runs the check, and a push to `main` is only published if the check passes, so a mistake in the data never replaces the live site: the last good version stays up.

One-time setup on a new repository: **Settings → Pages → Source: GitHub Actions**.
