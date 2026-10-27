# Vampire Life Wiki: catalogue

Pulled 2026-10-27 through the MediaWiki API (`api.php`). The HTML page itself returns 403, but the API works.
Raw wikitext for every page, with its revision id, is in `research/raw/<Title>.json`.

The wiki is small: **25 articles** (one is a redirect), **1 interactive map** (`Map:Vampire Life World Map`, 13 pins) and 35 images.
The image CDN also returns 403, so no images were downloaded. That includes `Vampire-Life-world-map.png`, the map the pins sit on.

Its own house style: disputed claims carry ⚠️ and code checks carry a date. Most pages credit a source (the game's Discord, "Soups", a video by ItzVexo, a cached Trello board, or a Google Doc by robloxpro492).

Pages that the wiki links to but that **do not exist**: Aging & Levels, Feeding & Desiccation, Sunlight & Protection, Death, Turning, Items & Merchants, Quests & Bounties, Controls.

---

## 1. Pages grouped by what they describe

| Kind | Pages |
|---|---|
| **Race** (playable) | Human, Vampire, Original Vampire, Witch, Werewolf, Original Hybrid, Hybrid (upcoming, empty) |
| **Race variant** (a sub-race of a parent) | Vampire Hunter (Human), Cannibal Vampire, Cannibal Raised Vampire, Vegan Vampire (all Vampire) |
| **Spells / rituals** | Witch Spells: Level Grinding Ritual, Tracking Ritual, Strength Spell, Immortality Spell, Rat Spell |
| **Craftables** | Witch Spells: Praesidium, Temporary Sun Ring, Inhuman Potion, White Oak Dagger, Witch Magic Color Change. Mining: Silver Bar, Ruby Bar (smelted) |
| **Items + merchants** | Items: 7 shops and about 55 stock lines. Mining: ores, Ore Buyer |
| **NPC (enemy)** | Beast Form Vampire. Also mentioned: red-glowing villagers, town guards, hunter NPCs (Lv 100–300 / 700 / 2000), werewolf NPCs (Lv 7k) |
| **Place** | No page of its own. Places come from the map pins and from prose: First Village, Second Village, Vampire Castle, Werewolf Den, Cemetery, Witch House, Church, Tavern, Windmill tower, Blacksmith's Forge, the woods |
| **Mechanic / article** | Beginner Guide, Clash, Mining, Events (Blood Moon, Foggy Night, 2x XP Weekend), Private Servers, Common Misconceptions |
| **Game pass** | Game Passes: Original Vampire (ANTICIPATED), Sun Ring, Hide level & team, Custom Tag, Save Progress. The Witch page also has Powerful Witch (Trello, ⚠️) |
| **Code** | Codes: 9 working, 1 thin, 10 disputed, 3 expired. Last checked Oct 24–25, 2026 |
| **Meta** | Vampire Life Wiki (home), Main Page (redirect), Sources |

---

## 2. Facts each kind actually has

### Race (`{{Character}}` infobox + sections)
Infobox fields used: `name, image, type, obtain, daylight, blood, strengths, weaknesses, status`.
Sections that recur:
- **How to become one**: prose or a bulleted list; requirements are levels, other players, a gamepass, chance %, timing (full moon)
- **Abilities / moveset**: name, **keybind** (X, B, Ctrl+M1, L1+Up…), **unlock level**, **cooldown**, effect, works on (NPCs / players)
  - Vampire: 10 abilities with level + cooldown. Witch: 11 with key + level + cooldown. Original Vampire and Original Hybrid: keybind lists only
- **Strengths / Weaknesses**: short lists
- **Ranks / level ladder**: Witch Novice 0–24 … Scarce 800+. Vampire ranks ⚠️ disputed
- **Clan**: bloodline (vampire), coven (witch), pack (werewolf). The Vampire page also lists bloodline chat commands
- Race-specific mechanics: Feeding & Desiccation, Sunlight, Minions (Vampire); Werewolf Ring and forms (Werewolf); Supreme Witch title and Magic Cauldron (Witch); Sun & immortality (Original)
- Starting gear and level (Human: fists, Lv 0. Witch: Incendia + a passive ability [name not given])

### Transformation (no page of its own; spread across race pages, Beginner Guide and Misconceptions)
| From → To | Method | Requirements | Chance | When |
|---|---|---|---|---|
| Human → Vampire | vampire blood in your system + death + drink blood/blood bag; or the Infect ability (Lv 150 vampire) | — | — | after drinking (Infect: after the victim bites a non-vampire) |
| (gamepass) → Vampire (Natural-Born) | Original Vampire (ANTICIPATED) gamepass | — | — | — |
| (gamepass) → Original Vampire | gamepass only; no level, age or bite route (Discord) | 1,895 R$ / 1,706 Premium | — | — |
| Human → Werewolf | scratch on the back from a werewolf player or a Lv 6,000+ werewolf NPC | must be Human | 5% per scratch | the next full moon |
| Human → Witch | find a Grimoire in the woods (random spawn), hold Make Pact | — | — | respawn as Witch, Lv 0 |
| Vampire/Werewolf → Original Hybrid | vampire: scratched by a werewolf; werewolf: drinks blood while a vampire assists | Lv 5,000; transformer Lv 3,000+; Original Vampire gamepass | 0.5% (also 0.1%) ⚠️ | — |
| Vampire → Cannibal Vampire | drink another vampire's blood | — | 5% per bite | — |
| Cannibal → Vampire (revert) | drink non-vampire blood | — | 20% | — |
| Human → Cannibal Raised | infected by a Cannibal Vampire | — | 1% on completing | — |
| Vampire → Vegan Vampire | feed only on rats | — | — | tag earned |
| Human → Vampire Hunter | quest at the windmill tower near the Merchant in front of the Vampire Castle | must be Human | — | — |
| Witch/Vampire → Human | Human Potion, General Shop, first village | — | — | — |

The example in the brief checks out: Lv 6,000+, 5% per scratch, next full moon, "back scratch" (Common Misconceptions #7).
⚠️ One ambiguity: the Werewolf page says "a werewolf player **or** a werewolf NPC at level 6,000 or higher", while the Beginner Guide says "a Lv 6,000+ werewolf". It is unclear whether the level applies to players too.

### Spell (Witch Spells, Witch abilities)
Facts that appear: incantation (said in chat), caster level, setup (candle layout, heart), components (candles, heart), effect, cooldown, target (Original Vampires only, NPC or ally), how it is unlocked (Rat Spell: a quest).
- **Rituals** are spells with a physical setup: Level Grinding (5 candles in a star → 1 level / 15 min) and Tracking (3–5 candles in a triangle, heart in the middle, "quaerere <username>")
- To cast any witch spell you first need 5 candles from the witch merchant

### Craftable (Witch Spells, Mining)
Facts: where it is made (cauldron in the Witch House in the Cemetery; Blacksmith's Forge), caster level (100+ / 800+ / 1000+), ingredients with quantity and where to get each one, effect, duration (20 / 40 min; 5 h), alternative ingredients (cup **or** bowl). Smelting adds fuel (Coal).
**No rarity anywhere on the wiki.** Rarity exists only in your old handbook.

### Item (Items, Mining, race pages)
Facts: price (cash; sometimes **per buyer race**: Human Blood $50 for humans, $200 for witches and vampires), **race restriction** (HUMANS ONLY, WITCHES ONLY, WEREWOLVES ONLY, VAMPIRE HUNTER ONLY), cost paid in other items (Dagger = 20 Silver + $400; Rapier = 3 Wood Stake + 15 Silver Bar), effect, durability, permanence, whether it can be dropped, blessing (Cross: Human Lv 200+ at the church).
Ways to obtain that appear: bought, crafted, smelted, mined, found on the map (verbena, fragments, Grimoire), extracted with an ability (heart), quest reward (Throwing Knife), gamepass (Sun Ring).

### Merchant / NPC
Shops: Witch Shop (3 items, location "their hideout" — not given), Hunter Shop (6; map pin), General Shop (8; first village), Cook Shop (25; first village), Weapons Shop (7; second village), Vampire Shop (4; inside the castle), Ore Buyer (buys ore in lots of 60; both villages).
Quest givers: the Vampire Hunter quest NPC (windmill tower) and the Rat Alchemist (second village, appears at random).
Enemies: level range, where they spawn, how they spawn (Beast Form: 8k–12k, spawns when a hunter NPC feeds), what they are worth (XP).

### Place (map pins + prose)
Each map pin has a title, a category (Merchants / Villages / Low level npcs / High level Enemys / Bases), a description and x/y on an 873×664 image (origin bottom-left).
Containment appears in prose: Church and Tavern are in the first village, the Witch House is in the Cemetery, the Forge is near the weapons merchant.
Dangers appear in prose: sunlight outdoors, churches burn vampires, guards, red-glowing villagers.

| Pin | Category | x % | y % (from top) |
|---|---|---|---|
| First Village | Villages | 36.0 | 27.7 |
| Vampire Castle | Bases | 77.9 | 23.4 |
| Werewolf Den | Bases | 46.3 | 15.3 |
| Lvl 100-300 Hunters | Low level npcs | 54.5 | 16.3 |
| Level 2000 Hunters | High level Enemys | 19.4 | 13.9 |
| Second Village | Villages | 57.7 | 70.4 |
| Vamp Hunter Tower | Merchants | 57.6 | 35.7 |
| Merchant | Merchants | 55.0 | 70.0 |
| Witch House | Bases | 8.8 | 85.2 |
| Werewolf NPCs Lvl 7k | High level Enemys | 26.0 | 61.6 |
| Werewolf Missions | Merchants | 28.2 | 68.4 |
| Lvl 700 Hunters | Low level npcs | 49.7 | 39.8 |
| Hunter Shop | Merchants | 65.2 | 41.5 |

### Mechanic / article
Levels & XP (sources of XP, sleep XP, boosts and prices, Mining XP 3/6/9), sunlight (burn, holy places, protection options), the Blood Moon (stronger werewolves and vampires, more XP, hostile NPCs), Foggy Night, 2x XP Weekend (Fridays), Clash (skill check, 500-level cutoff since Oct 26), Mining & smelting, death (no ghost state, you just respawn), private server commands, 9 misconceptions.
**The full moon itself has no page**: we only know werewolves turn at it. Its timing and length are [TBC].

### Game pass
Name, Robux price, Premium price, what it grants, related chat commands (/hide, /tag…).

### Code
Code, reward, status group (working / thin / disputed / expired), checked date (one date for the whole page, Oct 24–25, 2026). Disputed codes have no reward listed.

---

## 3. Sources the wiki cites
- **Vampire Life Wiki** (Fandom, CC BY-SA): each page and revision id, in `raw/`
- **Official Discord** (https://discord.com/invite/TUSfpjQaCG): update announcements of Oct 15, Oct 24, Oct 25 and Oct 26, 2026, and the owner's Original Hybrid statements (via screenshots on the wiki). Not scraped.
- **Trello** (the official board): cited for the Shotgun price and the Powerful Witch pass. **No URL is given anywhere on the wiki.**
- **ItzVexo**, "How To BE WEREWOLF in Vampire Life!" (video, Oct 18, 2026)
- **robloxpro492 (tabmahmud)**, a Google Doc
- **Soups / CodeSoups**: wiki editor who supplied facts
- **Destructoid** code list, Oct 24 (mentioned on the Codes page)
- **Your Witch's Handbook** (`recipes.json`): your own tested entries
- The game is by **dutdk** on Roblox.

## 4. Things the old handbook has that the wiki does not
- rarity on everything
- the "Praesidium!" incantation that wakes the potion
- Blood Cup / Blood Dish needing a Lv 100+ vampire
- Sanguis Tuus Vita Mea's 20-min cooldown
- "glowing" verbena
- White Oak Ash Dagger "holds down a vampire permanently", "Inf"
- the name "Framente"
- 8 fragment colours, where the wiki lists 10

## 5. Where the old handbook and the wiki disagree
| Entry | Old handbook | Wiki |
|---|---|---|
| Inhuman Potion | protects Originals from **White Oak Stakes**, duration "Unown" | immunity to the **White Oak Ash Dagger** for **5 hours**, Witch Lv 1000+ |
| Praesidium Potion | "protects the witch who drinks it" | immune to neck snap **and vampire bites**; cup 20 min, bowl 40 min |
| Blood Cup / Dish | "Sold at Merchant, 1st village" | the empty Cup/Dish is sold (General Shop, $450). Witch Spells says "cooking merchant" ⚠️ |
| Sun Ring | "Sun Ring" | "Temporary Sun Ring" (formerly Temporary Daylight Ring); Witch Lv 100+. "Sun Ring" is a separate gamepass |
| Strength! | +20% **damage** | +20% **strength**, no stacking, 38 s cooldown, Lv 25 |
| Fragment colours | orange, black, purple, white, blue, green, red, cyan | violet, black, white, red, green, yellow, cyan, pink, orange, blue |
| Station | Graveyard Altar | cauldron inside the Witch House, in the Cemetery |
| Dagger | 20x Silver **Ore** + 400 Coins, Weapons Merchant | 20 Silver + $400, Weapons Shop (second village) |
