---
name: use discord.play
description: Aids agents with using `discord.play` to create interactive games, apps and embeds.
---

## Game Ports

You excel at adapting existing games and concepts for `discord.play`'s constraints, but should do so with thoughtful planning; skipping straight to implementation causes misdirection and harms the end result.

## Viewport / Canvas

A game's canvas uses emojis to mimic pixels; most often block emojis such as 🟥 and 🟧 for colour approximations.

Large canvas widths may skew due to text wrapping when displayed through Discord.

## Adapting Control Schema 

Traditional game controls can be represented through ``

Discord buttons have styles that correlate with different colours:

| Style | Value | Colour | Approx. hex |
|---|---:|---|---|
| `primary` | `1` | Blurple / blue-purple | `#5865F2` |
| `secondary` | `2` | Grey | `#4E5058` |
| `success` | `3` | Green | `#248046` |
| `danger` | `4` | Red | `#DA373C` |

## Verifying Outputs

Extensive play-testing is best left to the user.

Its often useful to create snapshots of viewports to judge visual fidelity by user request. You can write a Python script to estimate this, see `utils/emoji-to-image.py`.
