"""
Rules.py Access rules and win condition for Kirby: Planet Robobot.
"""
from BaseClasses import CollectionState
from worlds.generic.Rules import forbid_item

from . import Constants as C
from .Regions import (_has_ex_cube_threshold, _has_boss_cube_gate,
                      _can_reach_area)


def set_rules(world):
    player = world.player
    options = world.options
    multiworld = world.multiworld

    # Location-specific rules that go beyond simple region access.
    from .Locations import LOCATION_TABLE

    def loc_rule(name, rule):
        try:
            multiworld.get_location(name, player).access_rule = rule
        except KeyError:
            pass

    # Ability Testing Room: needs the item that opens it.
    loc_rule("Ability Testing Room Opened",
             lambda state: state.has(C.ABILITY_TESTING_ROOM, player))

    # Star Dream needs the armor and Level 6 access (the per-level boss gates,
    # including Level 6's, are set in the loop below).
    loc_rule("Defeat Star Dream (Story)",
             lambda state: _can_reach_area(state, player, "Level6"))

    # EX unlock checks need the cube threshold.
    for lv in C.LEVELS:
        loc_rule(f"Unlock {lv} EX Stage",
                 lambda state, lv=lv: _has_ex_cube_threshold(state, player, lv))

    # Vanilla Code Cube gate: each level's boss ("firewall") needs enough cubes.
    # The game enforces this itself, so we only need it in logic that keeps
    # progression faithful to Robobot and means no boss-unlock hacking.
    for lv in C.LEVELS:
        loc_rule(f"Clear {lv} (Boss Defeated)",
                 lambda state, lv=lv: _has_boss_cube_gate(state, player, lv)
                 and (_can_reach_area(state, player, lv))
                 )

    # Robobot Armor Modes. Only applies when armor gating is on: with it off you
    # can scan any Capsule and a mode is never a barrier.
    if options.armor_gating:
        # Most Code Cubes that need a mode are one of three in their stage, so
        # this gates the individual cube rather than the whole stage. Gating the
        # stage would lock away cubes you could genuinely reach without the mode.
        for loc_name, d in LOCATION_TABLE.items():
            if getattr(d, "category", None) != "cube":
                continue
            lv = getattr(d, "level", None)
            st = getattr(d, "stage", None)
            slot = getattr(d, "slot_index", None)
            if not lv or not st or slot is None:
                continue
            need = C.armor_item_for_cube(lv, st, slot + 1)
            if not need:
                continue
            loc_rule(loc_name, lambda state, need=need: state.has(need, player))
            try:
                forbid_item(multiworld.get_location(loc_name, player),
                            need, player)
            except KeyError:
                pass

        # A few stages are built entirely around one mode, so everything in them
        # needs it: the rare sticker, the stage clear, all of it.
        for loc_name, d in LOCATION_TABLE.items():
            lv = getattr(d, "level", None)
            st = getattr(d, "stage", None)
            if not lv or not st:
                continue
            mode = C.STAGE_ARMOR_REQUIREMENT.get((lv, st))
            if not mode:
                continue
            need = f"Armor Mode: {mode}"
            loc_rule(loc_name, lambda state, need=need: state.has(need, player))
            try:
                forbid_item(multiworld.get_location(loc_name, player),
                            need, player)
            except KeyError:
                pass

        # Stage clears are named after the Area and stage number rather than
        # carrying level/stage fields, so they're matched separately.
        for (lv, st), mode in C.STAGE_ARMOR_REQUIREMENT.items():
            try:
                stage_no = int(st.replace("Stage", ""))
            except ValueError:
                continue
            need = f"Armor Mode: {mode}"
            nm = f"{C.area_name(lv)} Stage {stage_no} Clear"
            loc_rule(nm, lambda state, need=need: state.has(need, player))
            try:
                forbid_item(multiworld.get_location(nm, player), need, player)
            except KeyError:
                pass

    # Kirby copy abilities. Same shape as the armor cube gates, but for Kirby's
    # own abilities. With ability gating on, the in-stage enemy that would grant
    # the ability gives nothing until it's been received, so a cube whose puzzle
    # needs that ability is genuinely locked behind it.
    if options.ability_gating:
        for loc_name, d in LOCATION_TABLE.items():
            if getattr(d, "category", None) != "cube":
                continue
            lv = getattr(d, "level", None)
            st = getattr(d, "stage", None)
            slot = getattr(d, "slot_index", None)
            if not lv or not st or slot is None:
                continue
            need = C.ability_item_for_cube(lv, st, slot + 1)
            if not need:
                continue
            loc_rule(loc_name, lambda state, need=need: state.has(need, player))
            try:
                forbid_item(multiworld.get_location(loc_name, player),
                            need, player)
            except KeyError:
                pass

    multiworld.completion_condition[player] = lambda state: _goal_met(state, world)


def _story_bosses_defeatable(state, player) -> int:
    """Count how many story-level bosses are reachable+beatable given items."""
    count = 0
    for lv in C.LEVELS:
        # Level 1 is always reachable; others need their access item.
        if _can_reach_area(state, player, lv):
            count += 1
    return count


def _goal_met(state: CollectionState, world) -> bool:
    player = world.player
    goal = world.options.goal

    if goal == 0:  # story_star_dream
        return _can_reach_area(state, player, "Level6")
    if goal == 1:  # story_boss_count
        needed = world.options.story_boss_count.value
        return _story_bosses_defeatable(state, player) >= needed
    return False
