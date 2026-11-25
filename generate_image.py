#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261124.

A dated front page: TUESDAY 24 NOVEMBER 2026, four verified stories from
24 November 2026 (Arab News, SCMP, Just Security / AP), plus a strip of
three more. Flat vector pictograms drawn with PIL only — no photos, no
network, no timestamps. Output is deterministic: same input, same bytes.
Run: python3 generate_image.py  ->  entry.png (1024x1024)
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (20, 36, 62)
GOLD = (212, 175, 105)
PAPER = (250, 248, 243)
INK = (24, 28, 36)
GREY = (90, 96, 108)
WHITE = (255, 255, 255)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_skyline(d, cx, cy, color):
    # Riyadh tower: skyline bars with one tall tower + antenna
    base = cy + 55
    bars = [(-150, 30, 46), (-98, 58, 40), (-52, 84, 44), (8, 110, 42),
            (58, 66, 40), (106, 40, 46)]
    for dx, h, w in bars:
        d.rectangle([cx + dx, base - h, cx + dx + w, base], fill=color)
    d.rectangle([cx - 52, base - 84, cx - 8, base], fill=color)
    # antenna on the tallest bar (centre cx+29)
    d.line([cx + 29, base - 110, cx + 29, base - 138], fill=color, width=4)
    d.ellipse([cx + 25, base - 144, cx + 33, base - 136], fill=(224, 122, 54))


def draw_pin(d, cx, cy, color):
    # location pin (Gaza strike location)
    d.ellipse([cx - 52, cy - 62, cx + 52, cy + 42], fill=color)
    d.polygon([(cx - 40, cy + 18), (cx + 40, cy + 18), (cx, cy + 78)], fill=color)
    d.ellipse([cx - 22, cy - 32, cx + 22, cy + 12], fill=WHITE)
    d.ellipse([cx - 22, cy - 32, cx + 22, cy + 12], outline=color, width=3)


def draw_block(d, cx, cy, color):
    # apartment block, one section tilted/broken (Zaporizhzhia)
    base = cy + 55
    d.rectangle([cx - 150, base - 100, cx - 30, base], fill=color)
    d.rectangle([cx - 10, base - 100, cx + 110, base], fill=color)
    d.rectangle([cx + 118, base - 70, cx + 150, base], fill=(150, 60, 52))
    for wx in (-135, -105, -75, -45):
        d.rectangle([cx + wx, base - 88, cx + wx + 18, base - 66], fill=WHITE)
        d.rectangle([cx + wx, base - 54, cx + wx + 18, base - 32], fill=WHITE)
    for wx in (5, 35, 65):
        d.rectangle([cx + wx, base - 88, cx + wx + 18, base - 66], fill=WHITE)
        d.rectangle([cx + wx, base - 54, cx + wx + 18, base - 32], fill=WHITE)
    # crack: jagged vertical split at the right edge of the middle block
    d.line([cx + 108, base - 100, cx + 96, base - 72, cx + 110, base - 44,
            cx + 98, base - 16, cx + 108, base],
           fill=(150, 60, 52), width=5)


def draw_court(d, cx, cy, color):
    # courthouse pediment + columns (US jury verdict)
    base = cy + 55
    d.polygon([(cx - 150, base - 78), (cx + 150, base - 78), (cx, base - 128)],
              fill=color)
    d.ellipse([cx - 14, base - 116, cx + 14, base - 88], fill=GOLD)
    for x in (-120, -60, 0, 60, 120):
        d.rectangle([cx + x - 11, base - 76, cx + x + 11, base], fill=color)
    d.rectangle([cx - 150, base - 6, cx + 150, base], fill=color)


PANELS = [
    dict(tag="RIYADH", color=(31, 90, 140), draw=draw_skyline,
         head="Houthi attack on Riyadh tower injures 11",
         sub="Tower in financial district hit; 11 injured"),
    dict(tag="GAZA", color=(150, 60, 52), draw=draw_pin,
         head="Israeli strike kills Hamas security chief in Gaza",
         sub="Naeem Abu Nahal among seven killed"),
    dict(tag="UKRAINE", color=(176, 124, 38), draw=draw_block,
         head="Zaporizhzhia strike kills 2, wounds 40",
         sub="Apartment block hit overnight; four children hurt"),
    dict(tag="UNITED STATES", color=(32, 110, 94), draw=draw_court,
         head="US jury convicts Huawei of stealing trade secrets",
         sub="Federal jury verdict in trade-secrets case"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- banner ---
    d.rectangle([0, 0, W, 140], fill=NAVY)
    d.rectangle([0, 140, W, 146], fill=GOLD)
    f_date = font(FB, 56)
    d.text((W // 2, 62), "TUESDAY  24 NOVEMBER 2026", font=f_date,
           fill=WHITE, anchor="mm")
    f_sub = font(FB, 21)
    d.text((W // 2, 112), "T H E   W O R L D   I N   O N E   D A Y", font=f_sub,
           fill=GOLD, anchor="mm")

    # --- 2x2 panels ---
    px, py, pw, ph, gap = 8, 154, 500, 392, 8
    f_tag = font(FB, 19)
    f_head = font(FB, 26)
    f_sub2 = font(FR, 19)
    for i, p in enumerate(PANELS):
        x = px + (i % 2) * (pw + gap)
        y = py + (i // 2) * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=WHITE,
                    outline=(214, 210, 202), width=2)
        d.rectangle([x, y, x + pw, y + 6], fill=p["color"])
        d.text((x + 24, y + 34), p["tag"], font=f_tag, fill=p["color"])
        d.line([x + 24, y + 62, x + pw - 24, y + 62], fill=(228, 224, 214),
               width=2)
        p["draw"](d, x + pw // 2, y + 128, p["color"])
        lines = wrap(d, p["head"], f_head, pw - 48)
        ly = y + 218
        for ln in lines:
            d.text((x + 24, ly), ln, font=f_head, fill=INK)
            ly += 34
        sub_lines = wrap(d, p["sub"], f_sub2, pw - 48)
        sy = y + ph - 22 - 24 * len(sub_lines)
        for ln in sub_lines:
            d.text((x + 24, sy), ln, font=f_sub2, fill=GREY)
            sy += 24

    # --- bottom strip ---
    sy0 = 154 + 2 * 392 + 8  # 946
    d.rectangle([0, sy0, W, H], fill=NAVY)
    f_strip = font(FB, 17)
    strip = ("SAUDI BUDGET SR1.39TN  \u2022  INDIA: $1.6BN NEPAL RELIEF  "
             "\u2022  DENMARK BANS SCHOOL PHONES")
    assert d.textlength(strip, font=f_strip) <= W - 32, "strip too wide"
    d.text((W // 2, sy0 + 26), strip, font=f_strip, fill=WHITE, anchor="mm")
    f_src = font(FR, 15)
    d.text((W // 2, sy0 + 56),
           "Sources: Arab News \u2022 AP \u2022 SCMP \u2022 Just Security  —  24 Nov 2026",
           font=f_src, fill=(168, 178, 196), anchor="mm")

    img.save("entry.png", format="PNG", optimize=True)
    data = open("entry.png", "rb").read()
    print(f"entry.png: {len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
