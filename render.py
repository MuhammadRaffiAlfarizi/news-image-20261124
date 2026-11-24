#!/usr/bin/env python3
"""Draws entry.png: THE WORLD IN ONE DAY, Tuesday 24 November 2026.

One image summing up 24 November 2026 world news. All drawing is done
with Pillow shapes and text; no network, no randomness, no clock, so
re-running this script reproduces the same image byte for byte.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
PAPER = (250, 246, 236)
INK = (26, 26, 26)
RED = (176, 42, 32)
NAVY = (31, 56, 100)
DARK = (31, 31, 31)
GREY = (110, 110, 105)
LINE = (60, 60, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_I = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # no oblique face installed; use regular

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, xy, s, f, fill=INK):
    draw.text(xy, s, font=f[0], fill=fill) if isinstance(f, tuple) else draw.text(xy, s, font=f, fill=fill)


def wrap(draw, s, fnt, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, fnt, max_w, fill=INK, lh=None):
    if lh is None:
        lh = fnt.size + 3
    for ln in wrap(draw, s, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_lines(draw, s, fnt, max_w, max_lines):
    """Return (lines, font) shrinking the font until it fits max_lines."""
    size = fnt.size
    while size > 9:
        f = ImageFont.truetype(fnt.path, size)
        lines = wrap(draw, s, f, max_w)
        if len(lines) <= max_lines:
            return lines, f
        size -= 1
    f = ImageFont.truetype(fnt.path, 9)
    return wrap(draw, s, f, max_w), f


# ---------------------------------------------------------------- stories
# (num, region, topic, place, headline, deck, source, status, art)
PANELS = [
    (1, "WORLD", "SPACE", "BRUSSELS", "NATO vows to defend space as satellite fear grows",
     "Rutte: the alliance will meet threats in orbit as reports warn of a Russian nuclear satellite within 60 days.",
     "NATO - Reuters", "CONFIRMED", "satellite"),
    (2, "EUROPE", "WAR", "ZAPORIZHZHIA, UKRAINE", "Russian strike kills 2, wounds 40 in Zaporizhzhia",
     "Overnight attack hits homes; governor says 40 hurt, including children, and people may still be under rubble.",
     "Reuters", "REPORTED", "strike"),
    (3, "AMERICAS", "CARTELS", "SINALOA, MEXICO", "US drone helped catch El Chapo Isidro",
     "A US drone over Mexico helped capture cartel boss Fausto Isidro Meza Flores; Mexico will try him at home.",
     "Mexican officials - AP", "REPORTED", "drone"),
    (4, "SOUTH ASIA", "QUAKE", "TAPLEJUNG, NEPAL", "Quake shakes Nepal, felt in five nations",
     "5.6 by Nepal, 5.3 by USGS, at 01:32 UTC. Felt in five nations. No deaths.",
     "NEMRC - USGS", "CONFIRMED", "quake"),
    (5, "EAST ASIA", "ESPIONAGE", "BEIJING, CHINA", "China sentences official to death for spying",
     "Official surnamed Ma sentenced to death for spying for a foreign country.",
     "Gold Wall Press", "REPORTED", "gavel"),
    (6, "MIDDLE EAST", "IRAN", "WASHINGTON", "Trump threatens new Iran strikes in 2027",
     "Trump warns of renewed strikes in 2027 if no nuclear deal is reached.",
     "CBS - Al Jazeera", "REPORTED", "carrier"),
    (7, "WORLD", "LIBYA", "TRIPOLI", "UN demands probe into Benghazi ship strikes",
     "UN seeks an independent inquiry after blasts on a Russian warship off Benghazi.",
     "UNSMIL", "OFFICIAL", "probe"),
    (8, "MIDDLE EAST", "GAZA", "GAZA CITY", "Strikes kill 3 in Gaza, including UN worker",
     "Israeli strikes kill at least three, an UNRWA worker among them, medics say.",
     "Al Jazeera", "REPORTED", "gaza"),
    (9, "MIDDLE EAST", "YEMEN", "HODEIDA, YEMEN", "Houthis say Saudi strike kills 17",
     "Houthis claim a Saudi-led strike kills 17 and damages telecoms in Hodeida.",
     "Houthi claim - AP", "CLAIM", "missile"),
    (10, "SOUTH ASIA", "CRICKET", "INDORE, INDIA", "Arya smashes record 181 as Delhi win",
     "Arya hits 181 off 68 balls with 19 sixes; Delhi beat Tamil Nadu by 116 runs.",
     "PTI - New Kerala", "CONFIRMED", "cricket"),
    (11, "OCEANIA", "CRICKET", "CARRARA, AUSTRALIA", "Australia 184/8 in 2nd T20I v England",
     "Australia bat first at Carrara; Coles debuts for England. Match in progress.",
     "Guardian - live", "ONGOING", "t20"),
    (12, "EAST ASIA", "DEFENCE", "SEOUL, SOUTH KOREA", "Russian jets enter Seoul air zone",
     "Russian jets fly into Seoul's air defence zone; Seoul corrects airspace claim.",
     "South Korea military", "OFFICIAL", "jets"),
    (13, "EAST ASIA", "MARKETS", "TOKYO - HONG KONG", "Asian stocks leap as Huang rally spreads",
     "Asian shares jump most since July as Nvidia's 31% surge revives the AI trade.",
     "Reuters", "CONFIRMED", "chart"),
    (14, "MIDDLE EAST", "CRASH", "RAS AL-KHAIMAH, UAE", "Coach crash kills 11 in UAE",
     "Eleven die as a coach hits a truck in Ras al-Khaimah, officials say.",
     "The National", "REPORTED", "crash"),
    (15, "AMERICAS", "TERROR", "VILLAVICENCIO, COLOMBIA", "Car bomb injures 23 at governor office",
     "Blast outside Meta governor office injures 23; president blames narco-terrorists.",
     "El Pais - President", "CONFIRMED", "blast"),
]

# (num, region, one-line story, source)
ALSO = [
    (16, "EAST ASIA", "Ulleung alert lifted minutes after jets leave", "JCS"),
    (17, "EUROPE", "EU readies $84b tariff retaliation", "Reuters"),
    (18, "MIDDLE EAST", "UK logs record 30+ Hormuz attacks in October", "UKMTO"),
    (19, "MIDDLE EAST", "Iran vows to fight US blockade", "IRIB"),
    (20, "AFRICA", "Somalia, Uganda step up war on al-Shabaab", "Govt"),
    (21, "AFRICA", "Two Nigerians die in Russian military service", "Access24"),
    (22, "AFRICA", "Borno school enrolment nearly doubles", "Al Jazeera"),
    (23, "AFRICA", "South Africa 209/2 v Bangladesh, 2nd Test", "SuperSport"),
    (24, "EAST ASIA", "SoftBank to invest $2b in Intel, reports say", "Reuters"),
    (25, "EAST ASIA", "China opens Tiangong to foreign astronaut", "Straits Times"),
    (26, "SE ASIA", "Thai-Cambodia border fighting on hold", "Govt"),
    (27, "EAST ASIA", "Seoul summons Russian attache over KADIZ", "AJP"),
    (28, "AMERICAS", "Pennsylvania measles toll reaches 9", "State health"),
    (29, "AMERICAS", "US unveils citizenship test, H-1B changes", "Govt"),
    (30, "AMERICAS", "20 killed in Sinaloa clashes after capture", "AP"),
    (31, "EAST ASIA", "Asia stocks jump most since July on Nvidia rally", "Reuters"),
    (32, "SOUTH ASIA", "Bengal beat UP by 93 runs", "ESPNcricinfo"),
    (33, "SOUTH ASIA", "Kerala crush Assam by 9 wickets", "Cricinfo"),
    (34, "SOUTH ASIA", "Ex-MP Revanna jailed for life for rape", "Court"),
    (35, "OCEANIA", "Fisher in for NZ second Test v India", "NZC"),
    (36, "SOUTH ASIA", "Army hunts for missing after Himalayan flood", "PTI"),
    (37, "WORLD", "Oil near 3-month lows as supply offsets risk", "World Watch"),
]

REGION_COLORS = {
    "EUROPE": (31, 78, 121), "MIDDLE EAST": (139, 46, 31),
    "AFRICA": (46, 125, 50), "SOUTH ASIA": (106, 61, 154),
    "EAST ASIA": (163, 31, 31), "SE ASIA": (15, 118, 110),
    "AMERICAS": (30, 58, 95), "OCEANIA": (47, 125, 91),
    "WORLD": (31, 56, 100),
}
REGION_COUNTS = [
    ("EUROPE", 2), ("MIDDLE EAST", 6), ("AFRICA", 4), ("SOUTH ASIA", 6),
    ("EAST ASIA", 8), ("SE ASIA", 1), ("AMERICAS", 5), ("OCEANIA", 2),
    ("WORLD", 3),
]

STATUS_COLORS = {
    "CONFIRMED": (34, 120, 60), "OFFICIAL": (31, 78, 121),
    "REPORTED": (51, 51, 51), "CLAIM": (197, 90, 17), "ONGOING": (176, 42, 32),
}

NUMBERS = [
    ("40", "wounded in Zaporizhzhia strike"),
    ("5.6", "Nepal quake magnitude"),
    ("181", "Arya runs off 68 balls"),
    ("23", "injured in Colombia car bomb"),
    ("17", "killed in Hodeida strike"),
    ("11", "killed in UAE coach crash"),
]

TIMELINE = [
    ("01:32", "Quake shakes Nepal"),
    ("02:09", "US drone role in El Chapo capture"),
    ("02:15", "NATO vows space defence"),
    ("02:30", "Car bomb rocks Villavicencio"),
    ("02:37", "China spy death sentence"),
]

LEFT_OUT = [
    ("COP31 collapse", "22 Nov"),
    ("BepiColombo Mercury orbit", "21 Nov"),
    ("ICJ Myanmar genocide ruling", "19 Nov"),
    ("Russia warns Estonia", "23 Nov"),
    ("Benghazi ship strikes", "23 Nov"),
    ("Democrats 258 House seats", "22 Nov"),
    ("Bangladesh typhoid drive", "Oct 2025"),
    ("Indonesia trade deal", "19 Nov"),
]


# ---------------------------------------------------------------- pictograms
def pic(img, draw, kind, x, y, w, h):
    """Flat vector-style pictogram clipped inside box (x, y, w, h)."""
    tmp = Image.new("RGBA", (max(1, w), max(1, h)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    _pic_inner(td, kind, 0, 0, w, h)
    img.paste(tmp, (x, y), tmp)


def _pic_inner(draw, kind, x, y, w, h):
    """Flat vector-style pictogram inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if kind == "satellite":
        draw.ellipse([x + 8, y + h - 26, x + 52, y + h + 6], fill=(52, 120, 180))
        draw.arc([x + 8, y + h - 26, x + 52, y + h + 6], 180, 360, fill=(120, 190, 230))
        draw.rectangle([cx - 6, cy - 16, cx + 6, cy + 2], fill=(220, 220, 210))
        draw.rectangle([cx - 26, cy - 10, cx - 8, cy + 0], fill=(70, 130, 200))
        draw.rectangle([cx + 8, cy - 10, cx + 26, cy + 0], fill=(70, 130, 200))
        draw.line([cx + 6, cy - 14, cx + 22, cy - 26], fill=(240, 240, 230), width=2)
        for sx, sy in [(x + 14, y + 8), (x + w - 18, y + 12), (x + w - 30, y + 4)]:
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    elif kind == "strike":
        for bx, bw, bh in [(x + 6, 16, 34), (x + 26, 22, 46), (x + 52, 18, 30)]:
            draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(40, 48, 66))
            for wy in range(3):
                draw.rectangle([bx + 4, y + h - bh + 6 + wy * 10, bx + 8, y + h - bh + 10 + wy * 10], fill=(255, 210, 90))
        ex, ey = cx + 16, y + 14
        for ang in range(0, 360, 45):
            import math
            r = 12
            x2 = ex + int(r * math.cos(math.radians(ang)))
            y2 = ey + int(r * math.sin(math.radians(ang)))
            draw.line([ex, ey, x2, y2], fill=(255, 140, 0), width=3)
        draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 200, 40))
        draw.ellipse([cx - 22, y + 4, cx - 10, y + 14], fill=(150, 150, 150))
        draw.ellipse([cx - 12, y + 2, cx - 2, y + 10], fill=(170, 170, 170))
    elif kind == "drone":
        draw.ellipse([cx - 14, cy - 6, cx + 14, cy + 6], fill=(60, 60, 60))
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(200, 60, 40))
        for dx, dy in [(-20, -12), (20, -12), (-20, 10), (20, 10)]:
            draw.line([cx, cy, cx + dx, cy + dy], fill=(60, 60, 60), width=2)
            draw.line([cx + dx - 8, cy + dy, cx + dx + 8, cy + dy], fill=(120, 120, 120), width=3)
        draw.rectangle([x + 4, y + h - 12, x + w - 4, y + h - 6], fill=(194, 154, 90))
        draw.polygon([(x + 10, y + h - 12), (x + 26, y + h - 26), (x + 40, y + h - 12)], fill=(150, 110, 60))
    elif kind == "quake":
        draw.polygon([(x + 4, y + h - 8), (x + w // 3, y + 10), (x + w // 2, y + h - 8)], fill=(90, 110, 130))
        draw.polygon([(x + w // 3, y + h - 8), (x + 2 * w // 3, y + 2), (x + w - 6, y + h - 8)], fill=(120, 140, 160))
        draw.polygon([(x + w // 3 - 8, y + 22), (x + w // 3, y + 10), (x + w // 3 + 8, y + 22)], fill=(255, 255, 255))
        pts = []
        for i in range(9):
            pts.append((x + 4 + i * (w - 8) // 8, cy + 12 + (14 if i % 2 else -14)))
        draw.line(pts, fill=(200, 40, 30), width=2)
    elif kind == "gavel":
        draw.rectangle([cx - 4, cy - 18, cx + 4, cy + 16], fill=(120, 80, 40))
        draw.rectangle([cx - 22, cy - 22, cx + 22, cy - 10], fill=(90, 60, 30))
        draw.rectangle([cx - 26, cy - 26, cx + 26, cy - 20], fill=(140, 95, 45))
        draw.ellipse([cx - 24, cy + 14, cx + 24, cy + 22], fill=(90, 60, 30))
        draw.rectangle([x + w - 26, y + 6, x + w - 10, y + h - 10], fill=(250, 250, 245))
        draw.line([x + w - 22, y + 14, x + w - 14, y + 14], fill=(100, 100, 100), width=1)
        draw.line([x + w - 22, y + 20, x + w - 14, y + 20], fill=(100, 100, 100), width=1)
    elif kind == "carrier":
        draw.polygon([(x + 6, y + h - 22), (x + w - 8, y + h - 22), (x + w - 20, y + h - 10), (x + 14, y + h - 10)], fill=(90, 95, 105))
        draw.rectangle([cx - 4, y + h - 38, cx + 14, y + h - 22], fill=(70, 75, 85))
        draw.line([cx + 14, y + h - 38, cx + 14, y + h - 52], fill=(70, 75, 85), width=2)
        draw.polygon([(cx + 14, y + h - 52), (cx + 30, y + h - 46), (cx + 14, y + h - 40)], fill=(200, 40, 30))
        for i in range(3):
            draw.arc([x + i * 16, y + h - 8, x + i * 16 + 22, y + h + 4], 180, 360, fill=(70, 130, 200))
    elif kind == "probe":
        draw.ellipse([cx - 16, cy - 10, cx + 16, cy + 16], fill=(70, 110, 170))
        draw.ellipse([cx - 5, cy - 2, cx + 5, cy + 8], fill=(40, 70, 120))
        draw.rectangle([cx + 12, cy - 16, cx + 26, cy - 6], fill=(200, 200, 190))
        draw.ellipse([cx - 22, cy - 14, cx - 14, cy - 6], fill=(255, 255, 255))
        draw.ellipse([cx - 22, cy + 6, cx - 14, cy + 14], fill=(255, 255, 255))
    elif kind == "gaza":
        for bx, bw, bh in [(x + 6, 20, 40), (x + 30, 16, 28), (x + 50, 22, 48)]:
            draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(70, 70, 78))
            for wy in range(2):
                draw.rectangle([bx + 4, y + h - bh + 6 + wy * 12, bx + 8, y + h - bh + 10 + wy * 12], fill=(255, 220, 120))
        draw.ellipse([cx + 8, y + 2, cx + 20, y + 12], fill=(160, 160, 160))
        draw.ellipse([cx + 16, y + 6, cx + 28, y + 16], fill=(180, 180, 180))
        draw.rectangle([x + w - 24, y + h - 22, x + w - 6, y + h - 6], fill=(255, 255, 255))
        draw.rectangle([x + w - 18, y + h - 20, x + w - 12, y + h - 8], fill=(200, 40, 30))
        draw.rectangle([x + w - 22, y + h - 16, x + w - 8, y + h - 12], fill=(200, 40, 30))
    elif kind == "missile":
        draw.polygon([(cx - 4, cy + 18), (cx + 4, cy + 18), (cx + 2, cy - 18), (cx - 2, cy - 18)], fill=(200, 200, 200))
        draw.polygon([(cx - 2, cy - 18), (cx + 2, cy - 18), (cx, cy - 28)], fill=(200, 40, 30))
        draw.polygon([(cx - 4, cy + 12), (cx - 12, cy + 22), (cx - 4, cy + 18)], fill=(180, 180, 180))
        draw.polygon([(cx + 4, cy + 12), (cx + 12, cy + 22), (cx + 4, cy + 18)], fill=(180, 180, 180))
        for i in range(3):
            draw.ellipse([cx - 8 - i * 4, cy + 24 + i * 6, cx - 2 - i * 4, cy + 30 + i * 6], fill=(255, 160, 40))
    elif kind == "cricket":
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=(80, 160, 80))
        draw.rectangle([cx - 26, y + 4, cx - 18, y + h - 8], fill=(150, 110, 60))
        draw.ellipse([cx + 10, cy - 6, cx + 22, cy + 6], fill=(200, 40, 30))
        if h >= 40:
            draw.text((cx - 6, y + h - 34), "181", font=font(SANS_B, 20), fill=(255, 255, 255))
    elif kind == "t20":
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=(80, 160, 80))
        draw.rectangle([cx - 30, cy - 4, cx + 30, cy + 4], fill=(210, 190, 150))
        for sx in (cx - 24, cx - 18, cx - 12):
            draw.rectangle([sx, cy - 14, sx + 3, cy - 4], fill=(255, 220, 90))
        draw.ellipse([cx + 14, cy - 18, cx + 24, cy - 8], fill=(200, 40, 30))
        if h >= 40:
            draw.text((cx - 8, y + 2), "184/8", font=font(SANS_B, 15), fill=(255, 255, 255))
    elif kind == "jets":
        for jx, jy, s in [(cx - 18, cy - 8, 1), (cx + 10, cy + 8, 1)]:
            draw.polygon([(jx - 14, jy), (jx + 10, jy - 5), (jx + 16, jy), (jx + 10, jy + 5)], fill=(70, 75, 85))
            draw.polygon([(jx - 2, jy - 4), (jx + 6, jy - 12), (jx + 8, jy - 4)], fill=(90, 95, 105))
        draw.arc([x + 6, y + 4, x + w - 6, y + h - 4], 200, 340, fill=(120, 160, 200))
        draw.arc([x + 14, y + 10, x + w - 14, y + h - 10], 200, 340, fill=(150, 180, 210))
    elif kind == "helmet":
        draw.pieslice([cx - 18, cy - 14, cx + 18, cy + 14], 180, 360, fill=(90, 110, 70))
        draw.rectangle([cx - 20, cy + 2, cx + 20, cy + 8], fill=(70, 90, 55))
        draw.rectangle([cx - 3, cy - 18, cx + 3, cy - 12], fill=(70, 90, 55))
        draw.rectangle([x + w - 22, y + 8, x + w - 8, y + h - 8], fill=(255, 255, 255))
        draw.rectangle([x + w - 18, y + h - 22, x + w - 12, y + h - 12], fill=(200, 40, 30))
    elif kind == "crash":
        draw.rectangle([x + 6, cy - 8, x + 40, cy + 10], fill=(30, 110, 160))
        for wx in range(4):
            draw.rectangle([x + 10 + wx * 8, cy - 4, x + 15 + wx * 8, cy + 2], fill=(200, 230, 255))
        draw.rectangle([x + w - 34, cy - 6, x + w - 6, cy + 10], fill=(200, 140, 40))
        draw.ellipse([x + 12, cy + 10, x + 20, cy + 18], fill=(30, 30, 30))
        draw.ellipse([x + 28, cy + 10, x + 36, cy + 18], fill=(30, 30, 30))
        ex, ey = cx + 8, cy - 16
        for ang in range(0, 360, 45):
            import math
            x2 = ex + int(9 * math.cos(math.radians(ang)))
            y2 = ey + int(9 * math.sin(math.radians(ang)))
            draw.line([ex, ey, x2, y2], fill=(255, 180, 0), width=2)
    elif kind == "blast":
        draw.rectangle([x + 8, cy + 2, x + w - 8, cy + 14], fill=(60, 60, 70))
        draw.rectangle([x + 14, cy - 6, x + w - 22, cy + 2], fill=(80, 80, 90))
        draw.ellipse([x + 14, cy + 14, x + 22, cy + 22], fill=(30, 30, 30))
        draw.ellipse([x + w - 24, cy + 14, x + w - 16, cy + 22], fill=(30, 30, 30))
        ex, ey = cx, y + 9
        for ang in range(0, 360, 30):
            import math
            r = 10
            x2 = ex + int(r * math.cos(math.radians(ang)))
            y2 = ey + int(r * math.sin(math.radians(ang)))
            draw.line([ex, ey, x2, y2], fill=(255, 140, 0), width=3)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 200, 40))
    elif kind == "chart":
        base = y + h - 6
        bars = [8, 14, 20, 28]
        bw = (w - 16) // 4
        for i, bh in enumerate(bars):
            bx = x + 8 + i * bw
            draw.rectangle([bx, base - bh, bx + bw - 4, base],
                           fill=(255, 210, 90) if i == 3 else (31, 78, 121))
        draw.line([(x + 8, base - 12), (x + w - 10, base - 30)], fill=(200, 40, 30), width=2)
    elif kind == "syringe":
        draw.line([cx - 16, cy + 14, cx + 14, cy - 16], fill=(200, 200, 200), width=5)
        draw.line([cx - 16, cy + 14, cx + 14, cy - 16], fill=(120, 120, 120), width=2)
        draw.line([cx + 14, cy - 16, cx + 22, cy - 24], fill=(120, 120, 120), width=2)
        draw.rectangle([cx - 22, cy + 8, cx - 12, cy + 20], fill=(70, 130, 200))
        draw.ellipse([cx + 2, cy - 2, cx + 12, cy + 8], fill=(255, 255, 255))
        draw.text((cx + 4, cy + 1), "+", font=font(SANS_B, 12), fill=(200, 40, 30))


# ---------------------------------------------------------------- panels
def draw_panel(img, draw, x, y, w, h, st, big):
    num, region, topic, place, head, deck, src, status, art = st
    rc = REGION_COLORS[region]
    draw.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=PAPER)
    pic_h = 66 if big else 48
    # picture band
    band = (NAVY if art in ("satellite", "probe", "jets") else
            (40, 48, 66) if art in ("strike", "gaza", "missile") else
            (240, 234, 214) if art in ("quake", "gavel", "helmet", "syringe", "chart") else
            (210, 228, 240) if art in ("drone", "carrier", "crash", "blast") else
            (230, 240, 220))
    draw.rectangle([x + 1, y + 1, x + w - 1, y + pic_h], fill=band)
    # number badge
    bx, by = x + 6, y + 6
    draw.ellipse([bx, by, bx + 20, by + 20], fill=RED)
    ns = str(num)
    fnum = font(SANS_B, 12 if num < 10 else 10)
    tw = draw.textlength(ns, font=fnum)
    draw.text((bx + 10 - tw / 2, by + 3), ns, font=fnum, fill=(255, 255, 255))
    # status chip
    sc = STATUS_COLORS[status]
    fstat = font(SANS_B, 8)
    sw = draw.textlength(status, font=fstat) + 8
    draw.rectangle([x + w - sw - 5, y + 7, x + w - 5, y + 20], fill=sc)
    draw.text((x + w - sw - 1, y + 9), status, font=fstat, fill=(255, 255, 255))
    # pictogram (skip where band is light and art is text-free)
    pic(img, draw, art, x + 4, y + 24, w - 8, pic_h - 26)
    ty = y + pic_h + 4
    # region + topic
    ftag = font(SANS_B, 10 if big else 9)
    draw.text((x + 6, ty), region + " - " + topic, font=ftag, fill=RED)
    ty += 13 if big else 12
    fplace = font(SANS_B, 10 if big else 9)
    draw.text((x + 6, ty), place, font=fplace, fill=INK)
    ty += 14 if big else 13
    # headline
    fhead = ImageFont.truetype(SERIF_B, 20 if big else 14)
    lines, fh = fit_lines(draw, head, fhead, w - 12, 2)
    for ln in lines:
        draw.text((x + 6, ty), ln, font=fh, fill=INK)
        ty += fh.size + 2
    # deck
    fdeck = font(SANS, 11 if big else 10)
    max_deck = 3
    dlines = wrap(draw, deck, fdeck, w - 12)[:max_deck]
    for ln in dlines:
        draw.text((x + 6, ty), ln, font=fdeck, fill=(60, 60, 60))
        ty += 13 if big else 12
    # source
    fsrc = font(SANS_I, 9)
    draw.text((x + 6, y + h - 13), src, font=fsrc, fill=GREY)


def draw_numbers(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.text((x + 8, y + 6), "THE DAY IN NUMBERS", font=font(SANS_B, 11), fill=(255, 255, 255))
    yy = y + 26
    for val, lab in NUMBERS:
        draw.text((x + 8, yy), val, font=font(SANS_B, 20), fill=(255, 210, 90))
        vw = draw.textlength(val, font=font(SANS_B, 20))
        draw_wrapped(draw, x + 14 + vw, yy + 4, lab, font(SANS, 10), w - 22 - vw,
                     fill=(230, 230, 230), lh=12)
        yy += 24


# ---------------------------------------------------------------- world map
MAP_ROWS = [
    "                                                    ",
    "      ####   #######                    #######      ",
    "   #########  ######   ######    ################## ",
    "  ###########  ####   ########  ####################",
    "  ##########         #########  ################### ",
    "   ########          ###  ####   ################   ",
    "    ######            ##   ###    ##############     ",
    "     ####            ###    ##     ###########       ",
    "      ##            ####    #      #########         ",
    "      #            #####           #######           ",
    "                  ######           #####            ",
    "                 #######            ###              ",
    "                 ######              #               ",
    "                  ####                               ",
    "                  ###                 #####          ",
    "                   ##                 #######        ",
    "                   #                   ######        ",
    "                                      ####          ",
]
MAP_PINS = [  # (story num, lon, lat)
    (1, 4.4, 50.8), (2, 35.2, 47.8), (3, -107.4, 24.8), (4, 87.9, 27.8),
    (5, 116.4, 39.9), (6, 51.4, 35.7), (7, 20.1, 32.1), (8, 34.5, 31.5),
    (9, 42.9, 14.8), (10, 75.9, 22.7), (11, 153.4, -28.0), (12, 127.0, 37.5),
    (13, 139.7, 35.7), (14, 55.9, 25.8), (15, -73.6, 4.1),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=(238, 240, 244))
    draw.text((x + 8, y + 5), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
    draw.text((x + w - 118, y + 6), "pins = story numbers", font=font(SANS, 9), fill=GREY)
    mx, my = x + 10, y + 24
    cw, ch = (w - 20) / 54.0, (h - 34) / 18.0
    step = min(cw, ch)
    for r, row in enumerate(MAP_ROWS):
        for c, ch2 in enumerate(row):
            if ch2 == "#":
                px = mx + c * step + step / 2
                py = my + r * step + step / 2
                draw.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4], fill=(120, 140, 160))
    PIN_OFF = {5: (9, -7), 12: (11, 5), 6: (-9, -5), 7: (-11, 7), 8: (7, 9),
               9: (3, 11), 14: (11, -3), 15: (0, 0), 10: (-9, -7), 4: (5, -9),
               13: (12, -8)}
    for num, lon, lat in MAP_PINS:
        col = (lon + 180.0) / 360.0 * 54.0
        row = (75.0 - lat) / 130.0 * 18.0
        px = mx + col * step + PIN_OFF.get(num, (0, 0))[0]
        py = my + row * step + PIN_OFF.get(num, (0, 0))[1]
        draw.ellipse([px - 5.5, py - 5.5, px + 5.5, py + 5.5], fill=RED, outline=(255, 255, 255), width=1)
        ns = str(num)
        fnum = font(SANS_B, 7)
        tw = draw.textlength(ns, font=fnum)
        draw.text((px - tw / 2, py - 5), ns, font=fnum, fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    M = 14  # side margin
    y = 0
    # top bar
    draw.rectangle([0, y, W, y + 22], fill=NAVY)
    draw.text((M, y + 5), "THE WORLD IN ONE DAY", font=font(SANS_B, 11), fill=(255, 255, 255))
    right = "37 STORIES - 9 REGIONS - ALL FROM THIS ONE DAY"
    draw.text((W - M - draw.textlength(right, font=font(SANS_B, 11)), y + 5),
              right, font=font(SANS_B, 11), fill=(255, 210, 90))
    y += 22
    # masthead
    title = "Tuesday 24 November 2026"
    size = 72
    while size > 40:
        fhead = ImageFont.truetype(SERIF_B, size)
        if draw.textlength(title, font=fhead) <= W - 2 * M:
            break
        size -= 2
    tw = draw.textlength(title, font=fhead)
    draw.text(((W - tw) / 2, y + 2), title, font=fhead, fill=INK)
    y += 84
    # red sub-headline
    fsub = ImageFont.truetype(SERIF, 19)
    sub = "NATO vows space defence  -  Zaporizhzhia hit overnight  -  US drone helped catch El Chapo Isidro"
    tw = draw.textlength(sub, font=fsub)
    draw.text(((W - tw) / 2, y), sub, font=fsub, fill=RED)
    y += 26
    # region bars
    x = M
    for name, cnt in REGION_COUNTS:
        label = "%s %d" % (name, cnt)
        f = font(SANS_B, 10)
        bw = draw.textlength(label, font=f) + 12
        draw.rectangle([x, y, x + bw, y + 20], fill=REGION_COLORS[name])
        draw.text((x + 6, y + 4), label, font=f, fill=(255, 255, 255))
        x += bw + 5
    y += 26
    # UTC timeline strip
    draw.rectangle([0, y, W, y + 24], fill=DARK)
    draw.text((M, y + 5), "THE DAY IN UTC", font=font(SANS_B, 10), fill=(255, 210, 90))
    tx = M + 108
    ftime = font(SANS_B, 10)
    fitem = font(SANS, 9)
    widths = [draw.textlength(t, font=ftime) + 5 + draw.textlength(ev, font=fitem)
              for t, ev in TIMELINE]
    total = sum(widths)
    avail = W - M - tx
    n = len(TIMELINE)
    gap = 14 + max(0, (avail - total - 14 * (n - 1)) // (n - 1)) if n > 1 else 14
    for (t, ev), w_item in zip(TIMELINE, widths):
        if tx + w_item > W - M:
            break
        draw.text((tx, y + 5), t, font=ftime, fill=(255, 210, 90))
        tx += draw.textlength(t, font=ftime) + 5
        draw.text((tx, y + 5), ev, font=fitem, fill=(235, 235, 235))
        tx += draw.textlength(ev, font=fitem) + gap
    y += 30
    # row 1: 3 big panels + numbers panel
    gap = 8
    colw = (W - 2 * M - 3 * gap) // 4
    rh1 = 190
    for i, st in enumerate(PANELS[0:3]):
        draw_panel(img, draw, M + i * (colw + gap), y, colw, rh1, st, big=True)
    draw_numbers(draw, M + 3 * (colw + gap), y, colw, rh1)
    y += rh1 + gap
    # row 2: 6 panels
    colw6 = (W - 2 * M - 5 * gap) // 6
    rh2 = 160
    for i, st in enumerate(PANELS[3:9]):
        draw_panel(img, draw, M + i * (colw6 + gap), y, colw6, rh2, st, big=False)
    y += rh2 + gap
    # row 3: 6 panels
    for i, st in enumerate(PANELS[9:15]):
        draw_panel(img, draw, M + i * (colw6 + gap), y, colw6, rh2, st, big=False)
    y += rh2 + gap
    # bottom: also-today list + map
    bot_h = 190
    list_w = 640
    draw.text((M, y), "ALSO TODAY", font=font(SANS_B, 12), fill=INK)
    draw.text((M + 96, y + 1), "- 22 more stories from Tuesday 24 November",
              font=font(SANS, 10), fill=GREY)
    # status chips legend in list header
    lx = M + list_w - 210
    for lab in ("REPORTED", "CLAIM", "ONGOING"):
        f = font(SANS_B, 8)
        sw = draw.textlength(lab, font=f) + 8
        draw.rectangle([lx, y + 1, lx + sw, y + 13], fill=STATUS_COLORS[lab])
        draw.text((lx + 4, y + 3), lab, font=f, fill=(255, 255, 255))
        lx += sw + 4
    ly = y + 18
    col2_x = M + list_w // 2 + 6
    fitem = font(SANS, 10)
    fsrc = font(SANS_I, 8)
    for idx, (num, region, txt, src) in enumerate(ALSO):
        cx = M if idx < 11 else col2_x
        cy = ly + (idx % 11) * 15
        draw.text((cx, cy), str(num), font=font(SANS_B, 10), fill=RED)
        tw_max = (list_w // 2 - 6) - 24 - draw.textlength(" - " + src, font=fsrc) - 4
        # truncate story text to fit one line
        s = txt
        while draw.textlength(s, font=fitem) > tw_max and len(s) > 10:
            s = s[:-1]
        if s != txt:
            s = s.rstrip() + ".."
        draw.text((cx + 22, cy), s, font=fitem, fill=INK)
        sx = cx + 22 + draw.textlength(s, font=fitem)
        draw.text((sx, cy + 1), " - " + src, font=fsrc, fill=GREY)
    draw_map(draw, M + list_w + 10, y, W - M - (M + list_w + 10), bot_h)
    y += bot_h + 6
    # date check footer
    draw.rectangle([M, y, W - M, y + 56], outline=RED, width=1)
    draw.rectangle([M, y, M + 108, y + 56], fill=RED)
    draw.text((M + 8, y + 12), "DATE CHECK", font=font(SANS_B, 13), fill=(255, 255, 255))
    draw.text((M + 8, y + 30), "24 NOV ONLY", font=font(SANS_B, 9), fill=(255, 210, 90))
    fx = M + 118
    fdc = font(SANS_B, 11)
    draw.text((fx, y + 4), "Every story here happened, or was first reported, on Tuesday 24 November 2026 (UTC).",
              font=fdc, fill=INK)
    fleft = font(SANS, 10)
    left = "Left out because they happened on an earlier day:  " + "  -  ".join(
        "%s %s" % (t, d) for t, d in LEFT_OUT)
    draw_wrapped(draw, fx, y + 22, left, fleft, W - M - fx - 8, fill=(60, 60, 60), lh=13)
    y += 62
    # legend + footer
    leg = ("HOW SURE:  CONFIRMED = two or more outlets  -  OFFICIAL = on the record  -  "
           "REPORTED = carried by the day's wires or officials  -  CLAIM = one side's account, labelled as such  -  "
           "ONGOING = still unfolding  -  Scenes are drawn illustrations, not photographs.")
    draw_wrapped(draw, M, y, leg, font(SANS, 9), W - 2 * M, fill=GREY, lh=11)
    y += 24
    foot = "24 NOVEMBER 2026  -  THE DAY'S WORLD NEWS, IN ONE IMAGE"
    fw = draw.textlength(foot, font=font(SANS, 9))
    draw.text(((W - fw) / 2, y), foot, font=font(SANS, 9), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
