#!/usr/bin/env python3
"""Render emoji (or an emoji grid) to PNG so the game's canvas/viewport can be snapshotted.

Usage:
  python emoji-to-png.py "🟦🟥🟩" -o shot.png            # single line of emoji
  python emoji-to-png.py -f grid.txt -o shot.png         # one row per line in file
  python emoji-to-png.py -f grid.txt --cell 48 -o shot.png
  python emoji-to-png.py -f grid.txt --bg "#111111" -o shot.png

Options:
  -f FILE        read rows from a file (one row per line) instead of a positional arg
  --cell N       pixel size per emoji cell (default 32)
  --bg COLOR     background colour, hex or name (default transparent)
  --pad N        padding in pixels around the grid (default 0)
  -o FILE        output path (default emoji-shot.png)
"""
import argparse
import sys
from PIL import Image, ImageDraw, ImageFont, ImageColor

# Windows emoji font; fall back to Segoe UI for glyphs it lacks
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\SegoeUIEmoji.ttf",
    r"C:\Windows\Fonts\seguisym.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_emoji(draw, ch, xy, font, size):
    """Draw one emoji centred at xy, falling back through fonts for missing glyphs."""
    for path in FONT_CANDIDATES:
        try:
            f = ImageFont.truetype(path, size)
        except Exception:
            continue
        if f.getmask(ch).getbbox():
            draw.text(xy, ch, font=f, anchor="mm")
            return
    draw.text(xy, ch, font=font, anchor="mm")


def rows_from_args(args):
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            return [line.rstrip("\n") for line in fh if line.strip()]
    if args.emoji:
        return [args.emoji]
    print("error: give an emoji string or -f FILE", file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("emoji", nargs="?", help="emoji string to render (one row)")
    ap.add_argument("-f", "--file", help="file with one emoji row per line")
    ap.add_argument("--cell", type=int, default=32, help="pixels per emoji cell (default 32)")
    ap.add_argument("--bg", default=None, help="background colour (hex or name)")
    ap.add_argument("--pad", type=int, default=0, help="padding in pixels (default 0)")
    ap.add_argument("-o", "--out", default="emoji-shot.png", help="output PNG path")
    args = ap.parse_args()

    rows = rows_from_args(args)
    font = load_font(args.cell)

    # Measure the widest row (each char = one cell)
    width = max(len(r) for r in rows) * args.cell
    height = len(rows) * args.cell
    pad = args.pad

    bg = (0, 0, 0, 0) if not args.bg else ImageColor.getrgb(args.bg)
    img = Image.new("RGBA", (width + 2 * pad, height + 2 * pad), bg)
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            # Draw each glyph centred in its cell
            draw_emoji(draw, ch,
                       (pad + x * args.cell + args.cell / 2,
                        pad + y * args.cell + args.cell / 2),
                       font, args.cell)

    img.save(args.out)
    print(f"wrote {args.out} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
