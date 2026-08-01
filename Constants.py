"""
Constants.py Static structural data for Kirby: Planet Robobot that is not
derived from the map scan (ability lists, mode lists, sub-game round counts,
boss names). Kept separate from the auto-generated game_data.json.
"""

GAME_NAME = "Kirby: Planet Robobot"

# --- The 27 usable Copy Abilities (Normal is Kirby with no ability) ---
# The 27 copy abilities, taken from the game's own Cmn.StepAbilityKind enum
# (mint/Default.bin) rather than guessed. An earlier hand-written list had Water
# and Wing, which aren't in Robobot at all.
#
# Maps the player-facing name -> the value the game stores in memory. The game's
# internal names differ for three of them (Esper/Sniper/Ufo), so we show the
# names players actually know.
ABILITY_VALUES = {
    "Ice": 1, "Whip": 2, "ESP": 3, "Cutter": 4, "Crash": 5, "Circus": 6,
    "Jet": 7, "Stone": 8, "Archer": 9, "Spark": 10, "Smash": 11, "Sleep": 12,
    "Sword": 13, "Doctor": 16, "Ninja": 17, "Parasol": 18, "Hammer": 20,
    "Beam": 23, "Fire": 24, "Fighter": 25, "Wheel": 26, "Bomb": 27,
    "Poison": 28, "Mike": 29, "Mirror": 30, "UFO": 31, "Leaf": 32,
}
COPY_ABILITIES = sorted(ABILITY_VALUES)
assert len(COPY_ABILITIES) == 27

# Cmn.StepAbilityKind.Normal Kirby with no copy ability. Writing this is how we
# make him drop an ability he hasn't been given.
ABILITY_NONE_VALUE = 0

# --- Robobot Armor + its 14 modes ---
# The base armor is one item; each mode gates a scanned ability.

ARMOR_BASE = "Robobot Armor"
ARMOR_MODES = [
    "Beam", "Bomb", "Cutter", "Fire", "Ice", "Jet", "Mike", "Parasol",
    "Spark", "Stone", "Sword", "Wheel", "ESP", "Halberd",
]
assert len(ARMOR_MODES) == 14

# --- Main story: 6 levels ---
LEVELS = ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6"]

# Story-mode bosses in clear order (used for goal counting / boss-defeat checks)
STORY_BOSSES = [
    "Gigavolt",           # Level 1 (Area 5 boss variant)
    "Holo Defense API",   # Level 2
    "Clanky Woods",       # Level 1 mid-boss style kept for completeness
    "Mecha Knight",       # Level 4
    "Dedede Clone / D3",  # Level 5
    "Susie / Mecha Knight+",  # Level 5
    "President Haltmann",  # Level 6
    "Star Dream",         # Level 6 final
]

# The EX stage of each level is unlocked with a Key item.
EX_STAGE_KEYS = [f"{lv} EX Key" for lv in LEVELS]

# --- Kirby 3D Rumble (Confetti) : 3 levels ---

# --- Proper in-game names ----------------------------------------------------
# The game calls these Areas, not Levels. Internal ids stay "LevelN" (that's what
# the ROM and memory use), but everything the player sees uses the real names.
CODE_CUBE = "Code Cube"

AREA_NAMES = {
    "Level1": "Patched Plains",
    "Level2": "Resolution Road",
    "Level3": "Overload Ocean",
    "Level4": "Gigabyte Grounds",
    "Level5": "Rhythm Route",
    "Level6": "Access Ark",
}
AREA_NUMBER = {lv: i + 1 for i, lv in enumerate(
    ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6"])}


def area_name(level_id: str) -> str:
    return AREA_NAMES.get(level_id, level_id)


# Per-area Code Cubes. Each Area's boss firewall counts only that Area's cubes
# (matching vanilla), so cubes are distinct per Area rather than one generic item.
# "<Area Name> Code Cube", one item type per Area, count = that Area's real cube
# total (11/14/18/18/18/21 = 100).
AREA_CUBE_COUNTS = {
    "Level1": 11,
    "Level2": 14,
    "Level3": 18,
    "Level4": 18,
    "Level5": 18,
    "Level6": 21,
}


def area_cube_name(level_id: str) -> str:
    """'Level1' -> 'Patched Plains Code Cube'."""
    return f"{AREA_NAMES[level_id]} Code Cube"


# reverse: "Patched Plains Code Cube" -> "Level1"
AREA_CUBE_ITEM_TO_LEVEL = {
    f"{AREA_NAMES[lv]} Code Cube": lv for lv in AREA_CUBE_COUNTS
}


def area_num(level_id: str) -> int:
    return AREA_NUMBER.get(level_id, 0)


def stage_num(stage_id: str) -> int:
    try:
        return int(stage_id.replace("Stage", ""))
    except ValueError:
        return 0


# The 35 Rare Stickers, by their Rare0XX id -> the sticker's actual name.
# Cross-checked against the game's Sticker/Config.bin and the community
# walkthrough (both agree).
RARE_STICKER_NAMES = {
    0: "Kirby", 1: "Star Rod Kirby", 2: "Nightmare Wizard", 3: "Dark Matter",
    4: "Marx", 5: "Gooey", 6: "Zero", 7: "Gryll", 8: "Ribbon", 9: "Adeleine",
    10: "Star Rod", 11: "Hydra", 12: "Dragoon", 13: "Dark Meta Knight",
    14: "Drawcia", 15: "Daroach", 16: "Sailor Waddle Dee", 17: "Masked Dedede",
    18: "Galacta Knight", 19: "Fluff", 20: "Magolor", 21: "Ultra Sword",
    22: "People of the Sky", 23: "Taranza", 24: "Queen Sectonia", 25: "Claycia",
    26: "King Dedede Icon", 27: "Meta Knight Icon", 28: "Susie",
    29: "Haltmann Works Co. Logo", 30: "HAL", 31: '"Pink Ball" Kanji',
    32: "Dream Hatcher", 33: "Qbby", 34: "Crazy Hand",
}

# --- Food ---------------------------------------------------------------------
# Real in-game food items. Everything here restores 1/5 of Kirby's health except
# the Energy Drink (1/2) and the Maxim Tomato (full). The Invincible Candy isn't
# food, and the reviving tomato is excluded on purpose.
FOOD_ITEMS = [
    "Cheeseburger", "Hot Dog", "Lemon Juice", "Pancakes", "Pizza",
    "Club Sandwich", "Meat", "Mint Ice Cream", "Lollipop", "Vanilla Ice Cream",
    "Strawberry Shortcake", "Watermelon",
]
# Maps each food item to its Scn.Step.Map.BinItemFoodKind value, so the client
# can hand the game the exact food rather than a generic one. Values are from
# the enum in step.bin. Where our pool name doesn't match a specific enum entry
# we pick the closest real food.
FOOD_SUB_KIND = {
    "Cheeseburger": 12,        # JunkHumburger
    "Hot Dog": 11,             # JunkHotdog
    "Lemon Juice": 4,          # DrinkLemonJuice
    "Pancakes": 19,            # SweetsHotCake
    "Pizza": 14,               # JunkPizza
    "Club Sandwich": 17,       # LightSandwich
    "Meat": 13,                # JunkMeat
    "Mint Ice Cream": 20,      # SweetsIceCream
    "Lollipop": 21,            # SweetsLollipopCandy
    "Vanilla Ice Cream": 25,   # SweetsSoftCream
    "Strawberry Shortcake": 24,  # SweetsShortCake
    "Watermelon": 10,          # FruitWatermelon
}


def food_sub_kind(name):
    """The BinItemFoodKind value for a food item name, defaulting to 0."""
    return FOOD_SUB_KIND.get(name, 0)


ENERGY_DRINK = "Energy Drink"     # restores 1/2
MAXIM_TOMATO = "Maxim Tomato"     # full heal
INVINCIBLE_CANDY = "Invincible Candy"   # temporary invincibility (filler)


# --- Sticker source games ----------------------------------------------------
# Several stickers share a display name ("Kirby" appears six times, from six
# different games). Location names must be unique, so a duplicate silently
# overwrote the earlier entry and those checks disappeared from the pool. The
# album's internal code carries the source game as a prefix, so we use it to
# disambiguate: "Sticker: Kirby (Kirby's Epic Yarn)".
STICKER_GAME_PREFIXES = {
    "Pinball": "Kirby's Pinball Land",
    "Bowl": "Kirby's Dream Course",
    "Korokoro": "Kirby Tilt 'n' Tumble",
    "Keito": "Kirby's Epic Yarn",
    "Kwii": "Kirby's Return to Dream Land",
    "Touchsr": "Kirby: Canvas Curse",
    "Yume": "Kirby's Adventure",
    "Denz": "Kirby: Squeak Squad",
    "Fighterz": "Kirby Fighters",
    "K64": "Kirby 64: The Crystal Shards",
    "K1": "Kirby's Dream Land",
    "K2": "Kirby's Dream Land 2",
    "K3": "Kirby's Dream Land 3",
    "Sd": "Kirby Super Star",
    "Da": "Kirby Super Star",
    "Ai": "Kirby Air Ride",
    "At": "Kirby: Triple Deluxe",
    "Td": "Kirby: Triple Deluxe",
    "Ka": "Kirby: Planet Robobot",
    "No": "Kirby: Planet Robobot",
    "Nu": "Kirby: Planet Robobot",
    "Et": "Kirby: Planet Robobot",
    "Us": "Kirby's Dream Land",
    "To": "Kirby's Dream Course",
    "Ki": "Kirby's Dream Land 2",
    "De": "Kirby: Squeak Squad",
    "Fi": "Kirby Fighters",
}


def sticker_source_game(internal: str):
    """Source game for an album entry, from its internal code prefix."""
    if not internal:
        return None
    for pref in sorted(STICKER_GAME_PREFIXES, key=len, reverse=True):
        if internal.startswith(pref):
            return STICKER_GAME_PREFIXES[pref]
    return None


# Code Cubes needed to open each Area's boss door. Read straight out of the
# game's own yaml/Scn/LvMap/IcCube.bin.cmp (the BossUnlock field per level), so
# these are vanilla's real numbers rather than a guess. Level 1 needing 4 matches
# what shows on the stage-select screen.
AREA_CUBE_COUNTS_REQUIRED = {
    "Level1": 4,
    "Level2": 5,
    "Level3": 6,
    "Level4": 6,
    "Level5": 7,
    "Level6": 7,
}


# Which Robobot Armor Mode each Code Cube needs, where one is needed at all.
#
# Keyed by (level, stage, cube slot 1-3). Most stages gate only one of their
# three cubes, so gating the whole stage would lock away cubes you could
# actually reach. Sourced from the per-cube guides on the Kirby wikis.
#
# Only Robobot Armor MODES are listed. Cubes that need one of Kirby's own copy
# abilities (Poison, ESP, Hammer, Doctor and so on) are covered by ability
# gating instead, and plain "use the Robobot Armor" needs no particular mode.
CUBE_ARMOR_REQUIREMENT = {
    ("Level1", "Stage2", 3): "Cutter",
    ("Level1", "Stage4", 3): "Spark",
    ("Level2", "Stage1", 2): "Parasol",
    ("Level2", "Stage2", 1): "Jet",
    ("Level2", "Stage2", 2): "Jet",
    ("Level2", "Stage2", 3): "Jet",
    ("Level2", "Stage3", 2): "Stone",
    ("Level2", "Stage6", 1): "Stone",
    ("Level3", "Stage1", 2): "Fire",
    ("Level3", "Stage2", 1): "Wheel",
    ("Level3", "Stage2", 2): "Wheel",
    ("Level3", "Stage2", 3): "Wheel",
    ("Level3", "Stage4", 2): "Ice",
    ("Level3", "Stage7", 2): "Ice",
    ("Level4", "Stage1", 3): "Stone",
    ("Level4", "Stage2", 3): "Parasol",
    ("Level4", "Stage4", 1): "Jet",
    ("Level4", "Stage4", 2): "Jet",
    ("Level4", "Stage4", 3): "Jet",
    ("Level4", "Stage5", 1): "Bomb",
    ("Level4", "Stage5", 2): "Cutter",
    ("Level4", "Stage5", 3): "Cutter",
    ("Level4", "Stage7", 1): "Stone",
    ("Level4", "Stage7", 2): "Sword",
    ("Level5", "Stage1", 1): "Jet",
    ("Level5", "Stage3", 2): "Spark",
    ("Level5", "Stage7", 2): "Stone",
    ("Level6", "Stage3", 1): "Bomb",
    ("Level6", "Stage3", 2): "Ice",
    ("Level6", "Stage3", 3): "Spark",
    ("Level6", "Stage5", 3): "Jet",
}

# Stages you cannot finish at all without a mode. These are the ones built
# entirely around it, so the stage clear (and anything else inside) needs it.
# 2-2 and 4-4 are Jet flying stages; 3-2 is a Wheel stage.
STAGE_ARMOR_REQUIREMENT = {
    ("Level2", "Stage2"): "Jet",
    ("Level3", "Stage2"): "Wheel",
    ("Level4", "Stage4"): "Jet",
}


# Code Cubes that need a specific KIRBY copy ability (on foot), the same idea as
# CUBE_ARMOR_REQUIREMENT but for Kirby's own abilities rather than armor modes.
# With ability gating on, the enemy that would grant the ability in-stage gives
# nothing until the ability has been received, so these cubes are genuinely
# locked behind their ability. Keyed by (level, stage, cube slot 1-3).
#
# Only cubes whose puzzle has no other solution are listed. Confirmed against
# the gameranx cube guide plus WiKirby/Neoseeker/Fandom stage pages. Cubes that
# accept more than one ability (for example a rope that Cutter or Ninja can cut)
# are deliberately left out so fill isn't over-constrained.
CUBE_ABILITY_REQUIREMENT = {
    ("Level1", "Stage2", 3): "Sword",
    ("Level2", "Stage1", 3): "ESP",
    ("Level3", "Stage4", 2): "Ice",
    ("Level3", "Stage5", 2): "Hammer",
    ("Level3", "Stage7", 1): "ESP",
    ("Level4", "Stage2", 2): "Poison",
    ("Level5", "Stage5", 2): "Hammer",
    ("Level6", "Stage2", 1): "Poison",
    ("Level6", "Stage7", 2): "Doctor",
}


def armor_item_for_cube(level: str, stage: str, slot: int):
    """The Armor Mode item a particular Code Cube needs, or None."""
    mode = CUBE_ARMOR_REQUIREMENT.get((level, stage, slot))
    return f"Armor Mode: {mode}" if mode else None


def ability_item_for_cube(level: str, stage: str, slot: int):
    """The copy-ability item a particular Code Cube needs, or None."""
    ab = CUBE_ABILITY_REQUIREMENT.get((level, stage, slot))
    return f"Ability: {ab}" if ab else None


def armor_item_for_stage(level: str, stage: str):
    """The Armor Mode item a stage demands, or None if it doesn't need one."""
    mode = STAGE_ARMOR_REQUIREMENT.get((level, stage))
    return f"Armor Mode: {mode}" if mode else None
