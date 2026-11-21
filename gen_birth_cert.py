#!/usr/bin/env python3
"""Generate the v4 meme image: a Leonida birth certificate for GTA VI.

Deterministic (PIL only, no network, no clock, no randomness): re-running
reproduces birth-certificate.png byte-for-byte. The make.fun ghost comes
from the official press kit (assets/mark-1024.png) and is pasted as the
attending physician's seal, so the mascot is the real logo, not a redraw.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "birth-certificate.png")
MARK = os.path.join(HERE, "assets", "mark-1024.png")

W = H = 1024
PAPER = (246, 239, 221, 255)      # warm cream
NAVY = (31, 42, 68, 255)          # ink
NAVY_SOFT = (74, 84, 110, 255)   # labels
GOLD = (176, 141, 46, 255)        # rules
RED = (179, 38, 30, 255)          # stamp
MAGENTA = (200, 30, 107, 255)     # make.fun accent

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked_width(draw, text, fnt, tracking):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if text else 0


def draw_tracked(draw, cx, y, text, fnt, fill, tracking=4):
    w = tracked_width(draw, text, fnt, tracking)
    x = cx - w / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def field(draw, y, label, value):
    """One certificate row: small-caps label left, bold value right, dots between."""
    lf = font(SERIF_B, 21)
    vf = font(SERIF_B, 34)
    lx = 96
    draw.text((lx, y), label, font=lf, fill=NAVY_SOFT)
    lw = draw.textlength(label, font=lf)
    vw = draw.textlength(value, font=vf)
    vx = 1024 - 96 - vw
    # dotted leader between label and value
    dot_y = y + 26
    x = lx + lw + 14
    while x < vx - 12:
        draw.ellipse((x, dot_y, x + 3, dot_y + 3), fill=(150, 140, 115, 255))
        x += 10
    draw.text((vx, y - 6), value, font=vf, fill=NAVY)


def main():
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # faint paper texture: sparse darker speckles, fixed grid (deterministic)
    for gx in range(60, W, 97):
        for gy in range(60, H, 89):
            d.point((gx, gy), fill=(233, 224, 198, 255))

    # double border
    d.rectangle((28, 28, W - 29, H - 29), outline=NAVY, width=5)
    d.rectangle((44, 44, W - 45, H - 45), outline=GOLD, width=2)

    # header
    draw_tracked(d, W // 2, 72, "STATE OF LEONIDA", font(SERIF_B, 40), NAVY, 10)
    center(d, W // 2, 128, "DEPARTMENT OF HEALTH  •  BUREAU OF VITAL RECORDS",
           font(SERIF, 22), NAVY_SOFT)
    d.line((150, 168, W - 150, 168), fill=GOLD, width=2)

    # title
    center(d, W // 2, 188, "CERTIFICATE OF LIVE BIRTH", font(SERIF_B, 50), NAVY)
    # divider with diamond
    d.line((150, 258, 440, 258), fill=GOLD, width=2)
    d.line((584, 258, W - 150, 258), fill=GOLD, width=2)
    d.polygon([(512, 248), (524, 258), (512, 268), (500, 258)], fill=GOLD)

    # fields
    rows = [
        ("NAME", "GRAND THEFT AUTO VI"),
        ("DATE OF BIRTH", "NOVEMBER 19, 2026"),
        ("PLACE OF BIRTH", "VICE CITY, LEONIDA"),
        ("WEIGHT", "214 GB"),
        ("LENGTH", "13 YEARS IN THE MAKING"),
        ("FATHER", "ROCKSTAR GAMES"),
        ("MOTHER", "13 YEARS OF WAITING"),
    ]
    y = 292
    for label, value in rows:
        field(d, y, label, value)
        y += 64

    # kicker line under the fields
    d.line((150, 736, W - 150, 736), fill=GOLD, width=2)
    center(d, W // 2, 752, "This baby took 13 years. Worth every contraction.",
           font(SERIF_I, 23), NAVY_SOFT)

    # bottom zone: ghost seal (left) + stamp (right)
    ghost = Image.open(MARK).convert("RGBA").resize((160, 160), Image.LANCZOS)
    img.paste(ghost, (96, 800), ghost)
    d.text((272, 812), "ATTENDING PHYSICIAN:", font=font(SERIF_B, 20), fill=NAVY_SOFT)
    d.text((272, 840), "DR. GHOST", font=font(SERIF_B, 32), fill=NAVY)
    d.text((272, 884), "make.fun GENERAL HOSPITAL", font=font(SERIF_B, 22), fill=MAGENTA)

    # red stamp, rotated
    stamp = Image.new("RGBA", (280, 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle((5, 5, 274, 114), outline=RED, width=4)
    sd.rectangle((11, 11, 268, 108), outline=RED, width=2)
    center(sd, 140, 16, "FINALLY", font(SERIF_B, 38), RED)
    center(sd, 140, 62, "DELIVERED", font(SERIF_B, 38), RED)
    stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (655, 805), stamp)

    img.convert("RGB").save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
