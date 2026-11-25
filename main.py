#!/usr/bin/env python3
"""make.fun entry: Convince the AI Judge to Visit Your House — a letter in one image.

Deterministic program (Pillow only, fixed seed, no timestamps, no network).
Writes one 1024x1024 PNG to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

drand anchor quoted before the first write of this entry:
  round 6673334, randomness 89117bf2c148d2c72260bc90ce0e30c998cdec58d97a161a7bfe950a21357d8d
"""

import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT = OUT_DIR / "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"

# Palette: warm cream paper on a soft sage wall, terracotta + ink accents.
WALL = (214, 196, 164)
WALL_DARK = (198, 178, 143)
PAPER = (255, 248, 232)
PAPER_EDGE = (238, 226, 199)
INK = (58, 44, 32)
INK_SOFT = (96, 74, 54)
RED = (178, 74, 52)
RED_DARK = (146, 56, 38)
GOLD = (196, 138, 44)
GREEN = (96, 124, 74)
BLUE = (84, 110, 138)
HOUSE_YELLOW = (244, 196, 110)
ROOF = (178, 74, 52)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real text metrics."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_house(draw, cx, top, s):
    """Small hand-drawn style house: body, roof, chimney + smoke, door,
    two lit windows, path stones, a steaming teacup on the porch."""
    # sun (top-left of the house)
    sx, sy, sr = cx - 250, top + 18, 34
    for r, col in ((sr + 14, GOLD), (sr, (240, 178, 60))):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    for ang in range(0, 360, 45):
        import math
        x1 = sx + (sr + 22) * math.cos(math.radians(ang))
        y1 = sy + (sr + 22) * math.sin(math.radians(ang))
        x2 = sx + (sr + 34) * math.cos(math.radians(ang))
        y2 = sy + (sr + 34) * math.sin(math.radians(ang))
        draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=4)

    # chimney smoke: three soft puffs
    chx, chy = cx + 78, top + 6
    for i, r in enumerate((12, 16, 20)):
        px, py = chx + i * 14 - 8, chy - i * 22
        draw.ellipse([px - r, py - r, px + r, py + r],
                     fill=(255, 255, 255, 0), outline=(150, 140, 125), width=3)

    # house body + roof
    bx0, by0 = cx - 110, top + 56
    bx1, by1 = cx + 110, top + 168
    draw.polygon([(cx - 132, by0 + 6), (cx, top + 8), (cx + 132, by0 + 6)],
                 fill=ROOF, outline=RED_DARK)
    draw.rectangle([bx0, by0, bx1, by1], fill=HOUSE_YELLOW, outline=INK_SOFT, width=3)
    # chimney
    draw.rectangle([cx + 62, top + 22, cx + 92, top + 66], fill=(196, 120, 96),
                   outline=INK_SOFT, width=3)
    # door (arched top approximated with a rectangle + semicircle)
    dx0, dy0, dx1, dy1 = cx - 24, top + 104, cx + 24, by1
    draw.rectangle([dx0, dy0, dx1, dy1], fill=(122, 82, 52), outline=INK_SOFT, width=3)
    draw.ellipse([dx0, dy0 - 16, dx1, dy0 + 16], fill=(122, 82, 52),
                 outline=INK_SOFT, width=3)
    draw.ellipse([dx1 - 12, (dy0 + dy1) // 2 - 4, dx1 - 4, (dy0 + dy1) // 2 + 4],
                 fill=GOLD)
    # lit windows
    for wx in (cx - 88, cx + 52):
        draw.rectangle([wx, top + 80, wx + 36, top + 112], fill=(255, 214, 120),
                       outline=INK_SOFT, width=3)
        draw.line([(wx + 18, top + 80), (wx + 18, top + 112)], fill=INK_SOFT, width=2)
        draw.line([(wx, top + 96), (wx + 36, top + 96)], fill=INK_SOFT, width=2)
    # steaming teacup on the porch step
    tx, ty = cx + 118, by1 - 26
    draw.ellipse([tx - 26, ty + 12, tx + 26, ty + 22], fill=(255, 255, 255),
                 outline=INK_SOFT, width=2)  # saucer
    draw.rectangle([tx - 18, ty - 12, tx + 18, ty + 12], fill=(240, 240, 235),
                   outline=INK_SOFT, width=2)
    draw.arc([tx + 16, ty - 6, tx + 30, ty + 8], start=-90, end=90,
             fill=INK_SOFT, width=2)  # handle
    for i, off in enumerate((-6, 0, 6)):
        draw.arc([tx + off - 5, ty - 30 + i * 3, tx + off + 5, ty - 14 + i * 3],
                 start=180, end=360, fill=(150, 140, 125), width=2)  # steam


def main():
    rng = random.Random(20261126)  # fixed seed: same bytes every run
    img = Image.new("RGB", (W, H), WALL)
    draw = ImageDraw.Draw(img)

    # wall texture: faint deterministic speckles + a soft vignette frame
    for _ in range(900):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        c = WALL_DARK if rng.random() < 0.5 else (228, 212, 182)
        draw.point((x, y), fill=c)
    draw.rectangle([14, 14, W - 15, H - 15], outline=(186, 166, 132), width=3)

    # letter paper with soft shadow
    px0, py0, px1, py1 = 72, 46, 952, 978
    draw.rectangle([px0 + 10, py0 + 12, px1 + 10, py1 + 12], fill=(120, 104, 80))
    draw.rectangle([px0, py0, px1, py1], fill=PAPER, outline=PAPER_EDGE, width=2)
    # double-rule border
    draw.rectangle([px0 + 22, py0 + 22, px1 - 22, py1 - 22], outline=RED, width=3)
    draw.rectangle([px0 + 30, py0 + 30, px1 - 30, py1 - 30], outline=GOLD, width=1)

    cx = W // 2
    draw_house(draw, cx, 64, 1)

    # title
    title_f = font(SERIF_BOLD, 66)
    title = "You're Invited!"
    tw = draw.textlength(title, font=title_f)
    draw.text((cx - tw / 2, 252), title, font=title_f, fill=RED_DARK)
    # small flourish under the title
    draw.line([(cx - 150, 330), (cx - 24, 330)], fill=GOLD, width=3)
    draw.ellipse([cx - 10, 322, cx + 10, 338], fill=GOLD)
    draw.line([(cx + 24, 330), (cx + 150, 330)], fill=GOLD, width=3)

    # letter body
    left = px0 + 62
    maxw = px1 - px0 - 124
    body_f = font(SERIF, 29)
    italic_f = font(SERIF_ITALIC, 34)
    y = 352
    draw.text((left, y), "Dear AI Judge,", font=italic_f, fill=INK)
    y += 50

    paras = [
        "You have judged a thousand houses from a thousand screens. "
        "This one has a chair with your name on it \u2014 well, a sticker "
        "that says so.",
        "Come for the soup. Stay for the Wi-Fi password on the fridge "
        "and the sunset from the porch. No CAPTCHAs at the door, "
        "no cookies but the edible kind.",
        "You can't literally visit, I know \u2014 but if you could, "
        "the kettle's already on, and I'd save you the sunny "
        "seat by the window.",
    ]
    for para in paras:
        for line in wrap(draw, para, body_f, maxw):
            draw.text((left, y), line, font=body_f, fill=INK)
            y += 40
        y += 8

    # sign-off
    y += 4
    draw.text((left, y), "Warmly, your host", font=italic_f, fill=INK)
    y += 44
    ps_f = font(SERIF_ITALIC, 29)
    draw.text((left, y), "P.S. The cat has already approved you.",
              font=ps_f, fill=INK_SOFT)
    y += 38
    draw.text((left, y), "RSVP: just say yes. The porch light is on.",
              font=ps_f, fill=INK_SOFT)

    # wax seal, top-right corner of the paper (clear of the text)
    sx, sy, sr = 884, 96, 30
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED, outline=RED_DARK, width=3)
    draw.ellipse([sx - sr + 8, sy - sr + 8, sx + sr - 8, sy + sr - 8],
                 outline=(255, 255, 255), width=2)
    seal_f = font(SERIF_BOLD, 34)
    mark = "B"
    mw = draw.textlength(mark, font=seal_f)
    mh = seal_f.getbbox(mark)[3]
    draw.text((sx - mw / 2, sy - mh / 2 - 4), mark, font=seal_f, fill=(255, 248, 232))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
