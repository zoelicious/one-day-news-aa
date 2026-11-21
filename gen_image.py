#!/usr/bin/env python3
"""Build the news-image-20261121 front page (1024x1024) in code with PIL.

35 stories for Saturday 21 November 2026. Cream newspaper, red masthead,
13 numbered illustrated panels, world map with numbered pins, ALSO list
14-35, DATE CHECK box, region bar (sums to 35), 6-number stat strip and a
"THE DAY IN UTC" timeline. Deterministic: same input -> same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (248, 241, 222)
PAPER = (250, 244, 228)
INK = (26, 26, 26)
RED = (179, 39, 30)
RED_DARK = (140, 28, 22)
GREY = (110, 104, 90)
RULE = (60, 55, 45)
BLUE = (38, 84, 124)
GREEN = (46, 110, 74)
GOLD = (198, 142, 32)
SKY = (214, 228, 235)
LAND = (232, 214, 178)
LAND_EDGE = (170, 150, 110)

FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = os.path.join(FDIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap by measured width."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill=INK, leading=None, align="left", max_w=None):
    if leading is None:
        leading = int(f.size * 1.22)
    for ln in lines:
        if align == "center":
            d.text((x + (max_w - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=fill)
        else:
            d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# region codes: EU AS ME AF AM OC GL
PANELS = [
    # n, headline, deck, source, region, art
    (1, "COP31 DRAGS ON WITH NO DEAL",
     "Climate talks in Antalya pass day 13; a third draft drops fossil fuels and splits nearly 200 nations.",
     "Reuters", "GL", "cop"),
    (2, "THREE MISSILES DOWN OVER RIYADH",
     "Saudi-led coalition intercepts Houthi missiles; no casualties.",
     "AP", "ME", "missile"),
    (3, "6.7 QUAKE SHAKES PERU",
     "Junin tremor strikes at 00:09 UTC, 108 km deep; no deaths, no tsunami.",
     "USGS", "AM", "quake"),
    (4, "DOUBLE-TAP HITS KRYVYI RIH",
     "Russian strike kills 2 and injures 42 in the central Ukrainian city.",
     "Reuters", "EU", "blast"),
    (5, 'ZELENSKY: CRIMEA BRIDGE "WILL NOT STAY"',
     "Kyiv leader tells NBC the bridge is a target.",
     "NBC", "EU", "podium"),
    (6, "IRAN CLAIMS U.S. DRONE DOWN",
     "Tehran claims 58th U.S. drone down over Hormuz; U.S. silent.",
     "AFP", "ME", "drone"),
    (7, "IRAN: URANIUM STAYS HOME",
     "Tehran says its stockpile stays in Iran and seeks a \u201cfair solution\u201d.",
     "Reuters", "ME", "atom"),
    (8, "TRUMP VOWS TAX ON FOREIGN DATA CENTRES",
     "Washington pledges a levy on overseas centres; no details yet.",
     "AP", "AM", "servers"),
    (9, "CHINA: JAPAN MUST 'CORRECT' TAIWAN WORDS",
     "Beijing objects; Tokyo says its stance is unchanged.",
     "Reuters", "AS", "flags"),
    (10, "146 SAFE AS JET LANDS IN DAVAO",
     "Air Niugini 767 makes an emergency landing; all aboard safe.",
     "AP", "OC", "plane"),
    (11, "AUSTRALIA, CHINA TO TALK AI",
     "Albanese ends an 11-day trip with an AI dialogue agreed in Canberra.",
     "AFP", "OC", "aichat"),
    (12, "BITCOIN SLIPS BELOW $59,000",
     "Falls 3.9% in 24 hours to $58,983.",
     "Reuters", "AM", "bitcoin"),
    (13, "RUSSELL FASTEST IN WET VEGAS PRACTICE",
     "1:34.041 in the rain; Verstappen takes pole.",
     "AP", "AM", "f1"),
]

BRIEFS = [
    # n, one-line story, source, region
    (14, "Rutte in Warsaw for NATO talks", "Reuters", "EU"),
    (15, "Denmark expels Russian attache", "AFP", "EU"),
    (16, "Bayelsa funeral boat sinks; 4+ dead", "AP", "AF"),
    (17, "Israeli strikes on Gaza kill 6", "Al Jazeera", "ME"),
    (18, "Houthis hit Hodeidah, threaten Jeddah", "Reuters", "ME"),
    (19, "Vance: Iran strike is Trump's call", "AP", "AM"),
    (20, "Roundup deal: $7.25bn in Missouri", "Reuters", "AM"),
    (21, "Texas execution takes 63 minutes", "AP", "AM"),
    (22, "Palisades fire verdict: 12 dead in LA", "Reuters", "AM"),
    (23, "Youth climate hearing in Vancouver", "AFP", "AM"),
    (24, "First U.S. measles death of 2026", "AP", "AM"),
    (25, "Migrant caravan of ~300 enters Mexico", "AFP", "AM"),
    (26, "Kim visits factory in Pyongyang", "AP", "AS"),
    (27, "Taipei passes budget", "Reuters", "AS"),
    (28, "Bangkok unveils arsenic plan", "AFP", "AS"),
    (29, "SCO forum meets in New Delhi", "Reuters", "AS"),
    (30, "Myanmar sanctions tightened", "AP", "AS"),
    (31, "Sejong train derails; 5 of 21 cars", "Reuters", "AS"),
    (32, "Rahul 124*; India 344/2 in Wellington", "AP", "AS"),
    (33, "BepiColombo at Mercury, 19:24 CET", "ESA", "AS"),
    (34, "Starc 7/58 as Ashes open in Perth", "AFP", "OC"),
    (35, "U.S. OKs ~900,000 AI chips for China", "Reuters", "AS"),
]

REGION_ORDER = [("Europe", "EU", 4), ("Asia", "AS", 10), ("Middle East", "ME", 5),
                ("Africa", "AF", 1), ("Americas", "AM", 11), ("Oceania", "OC", 3),
                ("Global", "GL", 1)]
REGION_COLOR = {"EU": (58, 96, 150), "AS": (198, 110, 32), "ME": (150, 70, 110),
                "AF": (110, 130, 60), "AM": (60, 130, 110), "OC": (90, 120, 180),
                "GL": (120, 90, 140)}

STATS = [
    ("3", "MISSILES DOWN\nOVER RIYADH"),
    ("6.7", "QUAKE IN PERU\n00:09 UTC"),
    ("146", "SAFE AFTER\nDAVAO LANDING"),
    ("$58,983", "BITCOIN, DOWN\n3.9% IN A DAY"),
    ("124*", "RAHUL IN\nWELLINGTON"),
    ("19:24", "CET: BEPICOLOMBO\nREACHES MERCURY"),
]

TIMELINE = [
    "00:09 UTC \u00b7 M6.7 quake, Peru",
    "02:00 RIYADH \u00b7 Blasts over capital",
    "DAYTIME \u00b7 COP31 talks drag on",
    "18:24 UTC \u00b7 BepiColombo burn (19:24 CET)",
]

# pin positions (lon, lat) + small manual offsets to avoid overlap
PINS = {
    1: (30.7, 36.9, 0, 0), 2: (46.7, 24.7, 0, 0), 3: (-75.5, -11.0, 0, 0),
    4: (33.4, 47.9, 0, 0), 5: (30.5, 50.4, -14, -10), 6: (56.0, 26.5, 0, 0),
    7: (51.4, 35.7, 12, -10), 8: (-77.0, 38.9, 0, 0), 9: (116.4, 39.9, 0, 0),
    10: (125.6, 7.0, 0, 0), 11: (149.1, -35.3, 0, 0), 12: (-74.0, 40.7, 14, 10),
    13: (-115.1, 36.1, 0, 0),
}

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
           (-75, 62), (-60, 55), (-55, 47), (-65, 44), (-75, 38), (-80, 32),
           (-85, 29), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
           (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-52, 5), (-50, 0),
           (-42, -5), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -42),
           (-70, -52), (-73, -50), (-73, -40), (-72, -30), (-70, -18), (-77, -12),
           (-81, -5), (-80, 2)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
           (18, 56), (21, 55), (28, 59), (30, 60), (25, 65), (20, 70), (12, 71),
           (5, 60), (5, 58), (-5, 50), (-10, 44)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
           (43, 12), (51, 11), (48, 2), (40, -5), (40, -15), (35, -25), (28, -33),
           (20, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
           (-17, 12)],
    "AS": [(30, 60), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
           (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
           (142, 50), (140, 40), (135, 35), (127, 35), (122, 30), (120, 22),
           (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
           (80, 13), (77, 8), (72, 20), (66, 25), (60, 25), (57, 26), (52, 28),
           (48, 30), (43, 35), (40, 36), (36, 36), (30, 36), (28, 41), (30, 45)],
    "OC": [(114, -22), (114, -30), (115, -35), (124, -33), (129, -32), (132, -32),
           (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
           (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
           (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
}


# ---------------------------------------------------------------- art
def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy, r = x + w // 2, y + h // 2 + 4, min(w, h) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 90), outline=BLUE, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=(255, 255, 255), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    d.ellipse([cx - r // 2, cy - r, cx - r // 4, cy - r // 3], fill=(120, 180, 90))
    d.ellipse([cx + r // 5, cy + r // 4, cx + r // 2, cy + r // 2], fill=(120, 180, 90))
    d.ellipse([cx + r + 6, cy - r - 2, cx + r + 14, cy - r + 6], fill=GOLD)


def art_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 68))
    for i, px in enumerate([x + w * 0.2, x + w * 0.5, x + w * 0.8]):
        d.line([px, y + h - 14, px + 14, y + 22], fill=(255, 200, 90), width=2)
        d.ellipse([px + 8, y + 14, px + 20, y + 26], fill=(255, 220, 120))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(40, 40, 44))
    for bx in [x + 12, x + w // 2 - 4, x + w - 26]:
        d.rectangle([bx, y + h - 26, bx + 14, y + h - 14], fill=(70, 70, 78))
    d.ellipse([x + w - 30, y + 8, x + w - 20, y + 18], fill=(250, 250, 240))


def art_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.25), (x + w * 0.55, y + h * 0.55),
               (x + w * 0.8, y + h * 0.2), (x + w, y + h * 0.6), (x + w, y + h)],
              fill=(120, 110, 90))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.25), (x + w * 0.55, y + h * 0.55),
               (x + w * 0.8, y + h * 0.2), (x + w, y + h * 0.6), (x + w, y + h)],
              outline=(60, 55, 45))
    pts = []
    for i in range(9):
        px = x + 6 + i * (w - 12) / 8
        py = y + h * 0.55 + (14 if i % 2 else -14)
        pts.append((px, py))
    d.line(pts, fill=RED, width=2)
    d.line([x + w * 0.3, y + h * 0.25, x + w * 0.42, y + h * 0.75,
            x + w * 0.36, y + h], fill=(40, 35, 30), width=2)


def art_blast(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 196))
    d.rectangle([x + 8, y + h * 0.45, x + w - 8, y + h], fill=(150, 140, 125))
    d.rectangle([x + w * 0.2, y + h * 0.2, x + w * 0.45, y + h * 0.45], fill=(120, 112, 100))
    d.rectangle([x + w * 0.6, y + h * 0.3, x + w * 0.85, y + h * 0.45], fill=(120, 112, 100))
    cx, cy = x + w * 0.32, y + h * 0.18
    for r, col in [(16, (200, 120, 60)), (11, (230, 160, 70)), (6, (250, 210, 110))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.line([x + w * 0.7, y + 6, x + w * 0.55, y + h * 0.35], fill=(90, 85, 75), width=2)


def art_podium(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 90, 150))
    d.rectangle([x, y, x + w, y + h // 2], fill=(250, 210, 60))
    d.rectangle([x + w * 0.35, y + h * 0.55, x + w * 0.65, y + h], fill=(90, 60, 40))
    d.rectangle([x + w * 0.3, y + h * 0.45, x + w * 0.7, y + h * 0.58], fill=(120, 85, 55))
    d.ellipse([x + w * 0.44, y + h * 0.22, x + w * 0.56, y + h * 0.42], fill=(240, 205, 170))
    d.line([x + w * 0.3, y + h * 0.45, x + w * 0.32, y + h * 0.2], fill=INK, width=1)
    d.ellipse([x + w * 0.3, y + h * 0.14, x + w * 0.36, y + h * 0.22], fill=INK)


def art_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 16, cy - 5, cx + 16, cy + 5], fill=(60, 60, 66))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for sx in (-1, 1):
        d.line([cx + sx * 16, cy, cx + sx * 26, cy - 8], fill=(60, 60, 66), width=2)
        d.line([cx + sx * 20, cy - 12, cx + sx * 32, cy - 12], fill=(90, 90, 96), width=2)
        d.line([cx + sx * 16, cy, cx + sx * 26, cy + 8], fill=(60, 60, 66), width=2)
        d.line([cx + sx * 20, cy + 12, cx + sx * 32, cy + 12], fill=(90, 90, 96), width=2)
    for dx, dy in [(x + w - 18, y + 8), (x + w - 10, y + 14), (x + w - 24, y + 16)]:
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=RED)


def art_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 210))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 24, cy - 9, cx + 24, cy + 9], outline=BLUE, width=2)
    d.ellipse([cx - 9, cy - 24, cx + 9, cy + 24], outline=BLUE, width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def art_servers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 60))
    for i in range(3):
        rx = x + 8 + i * (w - 16) // 3
        rw = (w - 16) // 3 - 4
        d.rectangle([rx, y + 6, rx + rw, y + h - 6], fill=(70, 95, 120), outline=(180, 200, 215))
        for j in range(3):
            ry = y + 10 + j * (h - 20) // 3
            d.rectangle([rx + 4, ry, rx + rw - 4, ry + 6], fill=(40, 210, 140))
    d.ellipse([x + w - 22, y + 4, x + w - 6, y + 20], fill=GOLD)
    d.text((x + w - 18, y + 5), "$", font=font(SANS_B, 11), fill=INK)


def art_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 225))
    d.rectangle([x + 8, y + 8, x + w // 2 - 4, y + h - 8], fill=(200, 40, 40))
    for sx in range(5):
        d.ellipse([x + 14 + sx * 3, y + 14, x + 20 + sx * 3, y + 20], fill=(255, 220, 60))
    d.rectangle([x + w // 2 + 4, y + 8, x + w - 8, y + h - 8], fill=(250, 250, 250),
                outline=(180, 40, 40))
    d.ellipse([x + w // 2 + 14, y + h // 2 - 10, x + w // 2 + 34, y + h // 2 + 10],
              fill=(200, 40, 40))
    d.line([x + w // 2 - 2, y + h - 8, x + w // 2 + 2, y + h - 8], fill=INK, width=2)


def art_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w * 0.15, y + h * 0.2, x + w * 0.85, y + h * 0.55], fill=(250, 250, 250),
              outline=(60, 90, 120), width=2)
    d.polygon([(x + w * 0.8, y + h * 0.3), (x + w * 0.95, y + h * 0.45), (x + w * 0.8, y + h * 0.5)],
              fill=(60, 90, 120))
    d.polygon([(x + w * 0.45, y + h * 0.2), (x + w * 0.55, y + h * 0.05), (x + w * 0.6, y + h * 0.22)],
              fill=(60, 90, 120))
    d.rectangle([x, y + h - 10, x + w, y + h - 6], fill=(90, 90, 90))
    d.line([x + 6, y + h - 8, x + w - 6, y + h - 8], fill=(255, 255, 255), width=1)
    d.ellipse([x + w - 24, y + 4, x + w - 8, y + 20], fill=(40, 160, 80))
    d.line([x + w - 20, y + 12, x + w - 16, y + 16], fill=(255, 255, 255), width=2)
    d.line([x + w - 16, y + 16, x + w - 11, y + 8], fill=(255, 255, 255), width=2)


def art_aichat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 235))
    d.rounded_rectangle([x + 8, y + 8, x + w // 2 + 8, y + h // 2 + 4], radius=8,
                        fill=(255, 255, 255), outline=BLUE)
    d.rounded_rectangle([x + w // 2 - 8, y + h // 2, x + w - 8, y + h - 8], radius=8,
                        fill=(210, 230, 245), outline=BLUE)
    d.text((x + 14, y + 12), "Hello.", font=font(SANS, 10), fill=INK)
    d.text((x + w // 2, y + h // 2 + 6), "Agreed.", font=font(SANS, 10), fill=INK)


def art_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 238, 220))
    cx, cy, r = x + w // 2 - 8, y + h // 2, min(w, h) // 2 - 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26))
    d.text((cx - 7, cy - 13), "B", font=font(SANS_B, 22), fill=(255, 255, 255))
    pts = [(x + w - 26, y + 8), (x + w - 18, y + 16), (x + w - 10, y + 10), (x + w - 2, y + 18)]
    d.line(pts, fill=RED, width=2)
    d.polygon([(x + w - 2, y + 18), (x + w - 8, y + 18), (x + w - 2, y + 12)], fill=RED)


def art_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 36))
    d.polygon([(x + 8, y + h * 0.6), (x + w * 0.35, y + h * 0.45), (x + w * 0.7, y + h * 0.45),
               (x + w - 8, y + h * 0.6), (x + w - 8, y + h * 0.7), (x + 8, y + h * 0.7)],
              fill=(200, 30, 30))
    d.ellipse([x + w * 0.25, y + h * 0.65, x + w * 0.35, y + h * 0.8], fill=INK,
              outline=(200, 200, 200))
    d.ellipse([x + w * 0.65, y + h * 0.65, x + w * 0.75, y + h * 0.8], fill=INK,
              outline=(200, 200, 200))
    for i in range(4):
        for j in range(2):
            col = (20, 20, 20) if (i + j) % 2 == 0 else (240, 240, 240)
            d.rectangle([x + w - 26 + i * 6, y + 6 + j * 6, x + w - 20 + i * 6, y + 12 + j * 6],
                        fill=col)
    d.line([x + 6, y + h - 6, x + w - 6, y + h - 6], fill=(250, 210, 60), width=2)


ART = {"cop": art_cop, "missile": art_missile, "quake": art_quake, "blast": art_blast,
       "podium": art_podium, "drone": art_drone, "atom": art_atom,
       "servers": art_servers, "flags": art_flags, "plane": art_plane,
       "aichat": art_aichat, "bitcoin": art_bitcoin, "f1": art_f1}


def chip(d, x, y, text, f):
    tw = d.textlength(text, font=f) + 10
    d.rounded_rectangle([x, y, x + tw, y + f.size + 6], radius=6,
                        outline=GREY, fill=(255, 255, 255))
    d.text((x + 5, y + 3), text, font=f, fill=GREY)
    return tw


def num_badge(d, cx, cy, n):
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=(255, 255, 255), width=2)
    t = str(n)
    f = font(SANS_B, 10 if len(t) < 2 else 9)
    d.text((cx - d.textlength(t, font=f) / 2, cy - f.size / 2 - 1), t, font=f,
           fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def build(out_path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 26
    CW = W - 2 * MX  # 972

    # masthead
    f_mast = font(SERIF_B, 46)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 8), t, font=f_mast, fill=RED)
    d.line([MX, 62, W - MX, 62], fill=RULE, width=2)
    d.line([MX, 66, W - MX, 66], fill=RULE, width=1)

    # date line
    f_date = font(SERIF_B, 38)
    t = "Saturday 21 November 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 72), t, font=f_date, fill=INK)
    f_sub = font(SANS_B, 13)
    t = "35 STORIES  ·  7 REGIONS  ·  ONE DAY OF WORLD NEWS"
    d.text(((W - d.textlength(t, font=f_sub)) / 2, 118), t, font=f_sub, fill=RED_DARK)

    # subheadline (3 lead stories)
    f_sh = font(SERIF_I, 15)
    sub = ("COP31 talks drag past deadline in Antalya  ·  Three missiles down over Riyadh  ·  "
           "6.7 quake shakes Peru")
    lines = wrap(d, sub, f_sh, CW - 40)
    y = draw_lines(d, lines, MX + 20, 140, f_sh, fill=INK, align="center", max_w=CW - 40)
    assert len(lines) <= 2, f"subheadline wrapped to {len(lines)} lines"

    # stat strip: 6 boxes
    y = 176
    bw, gap = 158, 5
    x = MX
    f_num = font(SERIF_B, 22)
    f_lab = font(SANS_B, 8)
    for num, lab in STATS:
        d.rectangle([x, y, x + bw, y + 46], outline=RULE, width=1, fill=(255, 252, 244))
        d.text(((x + bw / 2) - d.textlength(num, font=f_num) / 2, y + 2), num,
               font=f_num, fill=RED)
        ly = y + 28
        for ln in lab.split("\n"):
            d.text((x + bw / 2 - d.textlength(ln, font=f_lab) / 2, ly), ln,
                   font=f_lab, fill=INK)
            ly += 9
        x += bw + gap

    # region bar
    y = 228
    f_rh = font(SANS_B, 10)
    d.text((MX, y), "STORIES BY REGION", font=f_rh, fill=INK)
    d.text((W - MX - d.textlength("TOTAL 35", font=f_rh), y), "TOTAL 35", font=f_rh, fill=RED)
    y += 16
    bx = MX
    f_rc = font(SANS_B, 9)
    for name, code, count in REGION_ORDER:
        wseg = int(CW * count / 35)
        col = REGION_COLOR[code]
        d.rectangle([bx, y, bx + wseg - 1, y + 18], fill=col)
        lab = f"{name} {count}"
        tw = d.textlength(lab, font=f_rc)
        tx = bx + (wseg - tw) / 2
        if wseg < tw + 6:
            d.text((bx + 2, y + 20), lab, font=f_rc, fill=INK)
        else:
            d.text((tx, y + 4), lab, font=f_rc, fill=(255, 255, 255))
        bx += wseg

    # timeline strip
    y = 278
    f_th = font(SANS_B, 10)
    d.text((MX, y), "THE DAY IN UTC", font=f_th, fill=RED)
    d.line([MX, y + 20, W - MX, y + 20], fill=RULE, width=1)
    f_tt = font(SANS_B, 9)
    seg = CW / len(TIMELINE)
    for i, lab in enumerate(TIMELINE):
        cx = MX + seg * i + seg / 2
        d.ellipse([cx - 5, y + 15, cx + 5, y + 25], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx - d.textlength(lab, font=f_tt) / 2, y + 29), lab, font=f_tt, fill=INK)

    # hero panels 1-3
    y = 324
    hw, hgap = 320, 6
    f_hh = font(SERIF_B, 15)
    f_hd = font(SANS, 10)
    f_src = font(SANS, 8)
    for i, (n, head, deck, src, reg, art) in enumerate(PANELS[:3]):
        x = MX + i * (hw + hgap)
        d.rectangle([x, y, x + hw, y + 140], outline=RULE, width=1, fill=(255, 252, 244))
        ART[art](d, x + 1, y + 1, hw - 2, 62)
        num_badge(d, x + 14, y + 14, n)
        hy = y + 66
        lines = wrap(d, head, f_hh, hw - 12)
        assert len(lines) <= 2, f"hero {n} headline {len(lines)} lines"
        hy = draw_lines(d, lines, x + 6, hy, f_hh, leading=17)
        lines = wrap(d, deck, f_hd, hw - 12)
        assert len(lines) <= 2, f"hero {n} deck {len(lines)} lines"
        hy = draw_lines(d, lines, x + 6, hy + 1, f_hd, fill=(60, 55, 45), leading=12)
        assert hy <= y + 124, f"hero {n} text ends {hy - y}"
        chip(d, x + 6, y + 140 - 15, src, f_src)

    # small panels 4-13: 2 rows x 5
    y0 = 470
    sw, sgap = 190, 5
    f_sh2 = font(SERIF_B, 11)
    f_sd = font(SANS, 9)
    for idx, (n, head, deck, src, reg, art) in enumerate(PANELS[3:]):
        row, col = divmod(idx, 5)
        x = MX + col * (sw + sgap)
        y = y0 + row * 114
        d.rectangle([x, y, x + sw, y + 108], outline=RULE, width=1, fill=(255, 252, 244))
        ART[art](d, x + 1, y + 1, sw - 2, 40)
        num_badge(d, x + 13, y + 13, n)
        hy = y + 44
        lines = wrap(d, head, f_sh2, sw - 10)
        assert len(lines) <= 2, f"panel {n} headline {len(lines)} lines"
        hy = draw_lines(d, lines, x + 5, hy, f_sh2, leading=13)
        lines = wrap(d, deck, f_sd, sw - 10)
        assert len(lines) <= 2, f"panel {n} deck {len(lines)} lines"
        hy = draw_lines(d, lines, x + 5, hy + 1, f_sd, fill=(60, 55, 45), leading=11)
        assert hy <= y + 93, f"panel {n} text ends {hy - y}"
        chip(d, x + 5, y + 108 - 13, src, f_src)

    # bottom: map (left) + ALSO list (right)
    y = 698
    f_bh = font(SANS_B, 11)
    d.text((MX, y), "WHERE IT HAPPENED", font=f_bh, fill=RED)
    d.text((MX + 484, y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=f_bh, fill=RED)
    d.line([MX, y + 15, MX + 458, y + 15], fill=RULE, width=1)
    d.line([MX + 484, y + 15, W - MX, y + 15], fill=RULE, width=1)

    # map
    mx0, my0, mw, mh = MX, y + 20, 458, 168
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], outline=RULE, width=1, fill=(243, 236, 214))

    def ll2xy(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (75 - lat) / 130 * mh)

    for pts in CONTINENTS.values():
        d.polygon([ll2xy(lon, lat) for lon, lat in pts], fill=LAND, outline=LAND_EDGE)
    for n, (lon, lat, ox, oy) in PINS.items():
        px, py = ll2xy(lon, lat)
        num_badge(d, px + ox, py + oy, n)

    # ALSO list: 2 columns x 11
    f_al = font(SANS, 9)
    f_an = font(SANS_B, 9)
    f_as = font(SANS, 8)
    col_w = 239
    for i, (n, text, src, reg) in enumerate(BRIEFS):
        col, row = divmod(i, 11)
        x = MX + 484 + col * (col_w + 6)
        yy = y + 22 + row * 16
        d.text((x, yy), f"{n}.", font=f_an, fill=RED)
        tw = d.textlength(text, font=f_al)
        sw_ = d.textlength(f"({src})", font=f_as)
        assert tw + 4 + sw_ <= col_w - 18, f"brief {n} too wide: {text} ({src})"
        d.text((x + 18, yy), text, font=f_al, fill=INK)
        d.text((x + 18 + tw + 4, yy), f"({src})", font=f_as, fill=GREY)

    # DATE CHECK box
    y = 900
    d.rectangle([MX, y, W - MX, y + 62], outline=RED, width=2, fill=(255, 246, 240))
    f_dc = font(SANS_B, 11)
    f_dt = font(SANS, 10)
    d.text((MX + 8, y + 5), "DATE CHECK \u2014 LEFT OUT ON PURPOSE", font=f_dc, fill=RED)
    dc = ("UK\u2013EU reset deal  ·  Wall Street slide into correction  ·  Russian strikes on Kyiv "
          "bridges  ·  Missiles landing in Poland  ·  Cyclone Akvan landfall  (all Friday 20 Nov)  ·  "
          "Voyager 1 one light-day from Earth (18 Nov).  NOT YET CONFIRMED WHEN DRAWN: final COP31 "
          "text; confirmation BepiColombo is in Mercury orbit.")
    lines = wrap(d, dc, f_dt, CW - 16)
    draw_lines(d, lines, MX + 8, y + 22, f_dt, leading=12)
    assert len(lines) <= 3, f"DATE CHECK wrapped to {len(lines)} lines"

    # HOW WE CHECKED legend + footer
    y = 968
    f_lg = font(SANS, 9)
    leg = ("HOW WE CHECKED: every story carries its source \u2014 Reuters · AP · AFP · Al Jazeera · "
           "USGS · ESA · NBC. Claims are marked CLAIM. Figures are as reported on 21 Nov 2026.")
    lines = wrap(d, leg, f_lg, CW)
    y = draw_lines(d, lines, MX, y, f_lg, fill=GREY, leading=11)
    f_ft = font(SERIF_I, 11)
    t = "Every story here happened, or was first reported, on Saturday 21 November 2026."
    d.text(((W - d.textlength(t, font=f_ft)) / 2, y + 4), t, font=f_ft, fill=INK)
    f_ft2 = font(SANS, 8)
    t2 = "Original drawings, not photographs  ·  THE WORLD IN ONE DAY  ·  Saturday 21 November 2026"
    d.text(((W - d.textlength(t2, font=f_ft2)) / 2, y + 21), t2, font=f_ft2, fill=GREY)

    # sanity: region counts and story totals
    total = len(PANELS) + len(BRIEFS)
    assert total == 35, total
    counts = {}
    for _, _, _, _, reg, *_ in PANELS:
        counts[reg] = counts.get(reg, 0) + 1
    for _, _, _, reg in BRIEFS:
        counts[reg] = counts.get(reg, 0) + 1
    for name, code, want in REGION_ORDER:
        assert counts.get(code, 0) == want, (name, counts.get(code, 0), want)

    img.save(out_path, "PNG", optimize=True)
    print("saved", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
