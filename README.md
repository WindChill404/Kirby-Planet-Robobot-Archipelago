# Kirby: Planet Robobot Archipelago

An Archipelago randomizer for **Kirby: Planet Robobot** (Nintendo 3DS).

Disclaimer: The code for this integration and this readme were created by AI. I am working on making at least this more human so you might notice some of my annotations. I will also be honest and say that I haven't tested on a physical 3DS, only Azahar on Windows, so take that path at your own risk. Please reach out to me on Discord for any questions or issues.

Code Cubes, stickers, copy abilities, level clears, and Robobot Armor modes become Archipelago
items and locations. Progress is tracked live in the running game over a small
memory bridge, so almost nothing is baked into the ROM: the only patched files
are a handful of the game's own script archives.

Works on **Azahar** (emulator) and maybe on a **modded 3DS** running Luma3DS.

> No game data is distributed. Everything is built from a ROM you supply.

---

## Contents

- [What you need](#what-you-need)
- [1. Install the apworld](#1-install-the-apworld)
- [2. Install the memory bridge plugin](#2-install-the-memory-bridge-plugin)
- [3.(Optional) Point the world at your ROM]
- [4. Generate a game](#4-generate-a-game)
- [5. Build and install the patched game](#5-build-and-install-the-patched-game)
- [6. Play](#6-play)
- [Options reference](#options-reference)
- [Client commands](#client-commands)
- [Troubleshooting](#troubleshooting)
- [Known issues](#known-issues)
- Credits/Special Thanks

---

## What you need

| Thing | Notes |
|---|---|
| [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) 0.5.0+ | The launcher and client |
| `kirby_robobot.apworld` | This integration |
| A **decrypted North American** Planet Robobot ROM with no save data | `.cci` or `.3ds` (same format, different extension). Dump it yourself. If you need fresh saves deleting the files in-game works. |
| [`default.3gx`](https://github.com/LittleCube-hax/albw-ap-plugin/releases/tag/v0.1.3-3DS) | The memory bridge plugin. See [step 2](#2-install-the-memory-bridge-plugin). |
| [Azahar](https://github.com/azahar-emu/azahar) **or** a modded 3DS | Luma3DS 10.2+ on hardware |

---

## 1. Install the apworld

Open the Archipelago Launcher, choose **Browse Files**, and drop
`kirby_robobot.apworld` into the `custom_worlds/` folder. Double-clicking the
file also works.

Restart the Launcher afterwards so it picks the world up.

---

## 2. Install the memory bridge plugin

`default.3gx` is a CTRPluginFramework plugin that opens a **UDP server on port
45987** inside the running game and answers read/write requests for the game's
memory. The Archipelago client talks to it to see what you have collected and to
hand you items. The plugin is deliberately game-agnostic — it knows nothing about
Kirby, it just moves bytes. 

Download it [here](https://github.com/LittleCube-hax/albw-ap-plugin/releases/tag/v0.1.3-3DS) and rename it to default.3gx.

### Placing the plugin

**On a 3DS (Luma3DS):**

```
SD:/luma/plugins/<TITLE_ID>/default.3gx
```

Then enable plugins in the Luma configuration menu (hold **Select** at boot →
*Enable game patching* / plugin loader, depending on your Luma version).

**On Azahar:**

```
<Azahar user folder>\sdmc\luma\plugins\default.3gx
```
If these folders don't already exist, make them and name them as listed above.

Find the user folder in Azahar with **File → Open Azahar Folder**. 

**Enable** the plugin
loader under **Emulation → Configure → System** (some builds list it under
*Debug*).

---

## 3. (OPTIONAL) Point the world at your ROM

`rom_file` is the only entry — and if you leave it blank, the client
asks for the ROM the first time you open a patch and saves your answer here. This should not need to ever be changed unless you move your game location.

Optionally, in the Launcher, choose **Open host.yaml** and find the `kirby_robobot_options`
section: 

```yaml
kirby_robobot_options:
  rom_file: "C:/path/to/Kirby - Planet Robobot (USA).cci"
  mod_path: ""              # where to install the finished mod, see below
  make_zip: false           # zip the mod folder, useful for real hardware
```

Setting `mod_path` lets the build step install the mod for you automatically:

- **Azahar** — `<Azahar folder>/load/mods`
- **3DS** — `<SD card>/luma/titles`

---

## 4. Generate a game

Launcher → **Generate Template Options** creates
`Players/Templates/Kirby Planet Robobot.yaml`. Edit it, put your copy in
`Players/` or send it to the host, and generate as usual.

A minimal example:

```yaml
name: YourName
game: Kirby: Planet Robobot
Kirby: Planet Robobot:
  goal: story_star_dream
  story_boss_count: 6
  rare_sticker_checks: true
  sticker_checks: false
  open_all_stages: true
  ability_gating: true
  armor_gating: true
  death_link: false
  kirby_color: random
```

See the [options reference](#options-reference) below.

---

## 5. Build and install the patched game

Generation produces a patch file for your slot. **Open it** (drag onto the launcher, or
Launcher → *Open Patch*). 

The first time you do this it will automatically open the client, but on subsequent plays you will have to open it yourself.

Put the folder it makes into `<Azahar folder>/load/mods`. You might need to make these folders. To find, you can also right-click and select open > mods location on the game, but make sure that the title ID folder isn't within a title ID folder (ex: should be `<Azahar folder>\load\mods\0004000000183600\romfs` and `ap_seed.txt`)

If the title menu looks unchanged after installing (there should be an 'AP:D' in place of the 'Back' button is on file select), the mod is **not** loading
— fix that before going further, because nothing else will work.

---

## 6. Play

1. Start the Archipelago client for this world from the Launcher if not already open from patching.
2. Launch the game.
3. Connect it to your room as usual (`/connect <address>` if needed) - I usually do this on the area select screen but I'm not sure if it matters.
4. In the client, run:

   ```
   /3ds 127.0.0.1 or whatever it says on screen        # Azahar
   /3ds 111.222.3.44    # a real 3DS, use your console's IP
   ```

The client confirms when the bridge answers. Load your save file and play.

---

## Options reference

| Option | Values | Meaning |
|---|---|---|
| `goal` | `story_star_dream`, `story_boss_count` | Victory condition |
| `story_boss_count` | 1–6 | Bosses needed when using the boss-count goal |
| `rare_sticker_checks` | on/off (default **on**) | The 35 in-stage Rare Stickers become locations |
| `sticker_checks` | on/off (default off) | **Stickersanity.** All 138 normal stickers become locations | This can make logic really weird since technically they are all available right away - use them at your own risk.
| `open_all_stages` | on/off (default **on**) | Normal stages are open from the start | I highly reccomend this stays on.
| `ability_gating` | on/off | Copy abilities must be received before Kirby can use them |
| `armor_gating` | on/off | Robobot Armor modes must be received before the armor can use them |
| `death_link` | on/off | Share deaths with other players |
| `kirby_color` | `pink` … `white`, `random` | Cosmetic recolor, baked into the patched ROM |

### A note on Stickersanity

Normal stickers are picked up passively as you play, so turning this on adds a
large number of locations that are open almost everywhere at once. That can make
for strange or difficult logic.

### A note on gating

Ability gating and armor mode gating are **separate**. A copy ability only
affects Kirby on foot; an armor mode only affects the Robobot Armor. Receiving
one never grants the other.

With gating on, some Code Cubes genuinely require a specific ability or mode, and
the logic accounts for that.

### Boss gates

Each area's boss sits behind a Code Cube gate, exactly as in the original game —
but it counts **only the cubes Archipelago has sent you**, never the ones you
physically pick up. You can walk up to the gate at any time; it opens when you
have earned it.

---

## Client commands

| Command | What it does |
|---|---|
| `/3ds <address>` | Connect to the memory bridge |
| `/watchsave` | Log every byte of the save area that changes. Noisy; for debugging. |
| `/armorlog` | Log each Robobot Armor copy check and its result. For debugging. |

---

## Troubleshooting

**The client says it can't reach the game.**
The plugin is not running, or the address is wrong. Confirm the plugin loaded
(the title screen marker), check the IP, and make sure UDP 45987 is not
firewalled. On Azahar, try `127.0.0.1` or whatever is shown on screen.

**The title screen looks stock.**
The LayeredFS mod is not loading. Check that the mod folder is under the right
title ID and that your emulator or Luma has mods enabled.

**ctrtool errors while opening the patch.**
Your ROM is probably still encrypted. It must be a **decrypted** dump. Also
confirm `ctrtool` is on your `PATH` or that `ctrtool_path` points at it.

**Items arrive but nothing happens in game.**
Items are handed to Kirby as real pickups, so they only apply while you are in a
stage. Anything received on the world map is delivered when you next enter one.

**A rare sticker will not send its check.**
Stickers only register as *new* on the results screen at the end of a stage. If
you already own it, the game will not hand it over. The client works around this
automatically, but you must actually finish the stage.

---

## Known issues

- **Robobot Armor cannot re-absorb a dropped ability star.** If the armor's mode
  is knocked out, the star it leaves behind cannot be scanned back up. Under
  investigation.
- **DeathLink currently doesn't work.**

---

## Credits/Special Thanks

- **firubii** — [KirbyLib](https://github.com/firubii/KirbyLib), and the Mint VM
  documentation that made patching the game's scripts possible at all. Honestly the greatest Kirby modder to ever do it.
- **randomsalience** and **LittleCube** — the memory bridge plugin, originally
  written for the A Link Between Worlds integration and reused here unchanged.
- The Kirby modding community for the retexture pack used by `kirby_color`, specifically want to shout out **DudeLuke** as the main incorporation for colors is his mod [here](https://gamebanana.com/mods/377858).

---

## Legal

This project ships no Nintendo assets. It requires a ROM you dump yourself from
hardware you own. Kirby: Planet Robobot is © HAL Laboratory and Nintendo.
