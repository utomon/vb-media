"""Virtual Binder carousel builder. 1080x1350, dark theme, purple glow.

Usage: python3 vbslides.py spec.json outdir
spec.json = {"footer": "...", "slides": [ {type: hook|detail|point|cta, ...}, ... ]}
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, M = 1080, 1350, 72
BG = (10, 10, 16)
PURPLE = (86, 43, 244)
LAV = (150, 120, 255)
WHITE = (255, 255, 255)
MUTE = (130, 130, 150)
GREEN = (61, 220, 132)
RED = (255, 92, 108)


def F(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


XB, CSB, SEMI, MED = ("BarlowCondensed-ExtraBold.ttf", "BarlowCondensed-SemiBold.ttf",
                      "Barlow-SemiBold.ttf", "Barlow-Medium.ttf")


def tw(font, text, spacing=0):
    return font.getlength(text) + spacing * max(len(text) - 1, 0)


def text(im, xy, s, font, fill, spacing=0, anchor="ls"):
    d = ImageDraw.Draw(im)
    x, y = xy
    if anchor[0] == "r":
        x -= tw(font, s, spacing)
    elif anchor[0] == "m":
        x -= tw(font, s, spacing) / 2
    if spacing == 0:
        d.text((x, y), s, font=font, fill=fill, anchor="l" + anchor[1])
        return
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill, anchor="l" + anchor[1])
        x += font.getlength(ch) + spacing


def canvas():
    im = Image.new("RGBA", (W, H), BG + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((-300, 900, 700, 1700), fill=PURPLE + (110,))
    g.ellipse((300, 1050, 1400, 1800), fill=PURPLE + (60,))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    return Image.alpha_composite(im, glow)


def fit(name, s, size, maxw):
    while size > 40 and F(name, size).getlength(s) > maxw:
        size -= 6
    return F(name, size)


def grad_text(im, xy, s, font, c1=(190, 170, 255), c2=PURPLE, spacing=0):
    mask = Image.new("L", (W, H), 0)
    text(mask, xy, s, font, 255, spacing)
    bbox = mask.getbbox()
    if not bbox:
        return
    x0, _, x1, _ = bbox
    grad = Image.new("RGBA", (W, H))
    gd = ImageDraw.Draw(grad)
    for x in range(x0, x1 + 1):
        t = (x - x0) / max(x1 - x0, 1)
        gd.line((x, 0, x, H), fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,))
    im.paste(grad, (0, 0), mask)


def chrome(im, idx, total):
    logo = Image.open(os.path.join(HERE, "assets", "logo.png")).convert("RGBA")
    logo.thumbnail((200, 80))
    im.alpha_composite(logo, (M, 62))
    text(im, (W - M, 112), f"{idx} / {total}", F(SEMI, 28), MUTE, 3, "rs")


def pill(im, xy, s, font=None, fill=(30, 24, 70), line=LAV, color=LAV):
    font = font or F(SEMI, 26)
    x, y = xy
    w = tw(font, s, 4) + 56
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + w, y + 56), 28, fill=fill, outline=(106, 80, 220), width=2)
    text(im, (x + 28, y + 28 + 2), s, font, color, 4, "lm")
    return w


def footer(im, s):
    text(im, (M, H - 62), s, F(MED, 24), (110, 110, 130))


def wrap(s, font, maxw):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if tw(font, t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def hook(sp, idx, total, ft):
    im = canvas(); chrome(im, idx, total)
    pill(im, (M, 190), sp["kicker"].upper())
    y = 440
    for ln in sp["lines"]:
        text(im, (M, y), ln.upper(), F(XB, 130), WHITE); y += 122
    if sp.get("big"):
        grad_text(im, (M, 960), sp["big"].upper(), fit(XB, sp["big"].upper(), 330, W - 2 * M))
    chips = sp.get("chips", [])
    if chips:
        cw = (W - 2 * M - 30 * (len(chips) - 1)) / len(chips)
        d = ImageDraw.Draw(im)
        for i, (a, b) in enumerate(chips):
            x = M + i * (cw + 30)
            d.rounded_rectangle((x, 1010, x + cw, 1160), 22, fill=(32, 22, 100), outline=(106, 80, 220), width=2)
            text(im, (x + cw / 2, 1082), a.upper(), F(XB, 62), WHITE, 0, "mm")
            text(im, (x + cw / 2, 1128), b.upper(), F(SEMI, 22), LAV, 4, "mm")
    if sp.get("swipe"):
        text(im, (M, 1236), sp["swipe"].upper(), F(SEMI, 28), LAV, 4)
        d = ImageDraw.Draw(im)
        d.line((W - M - 64, 1226, W - M, 1226), fill=LAV, width=4)
        d.line((W - M - 22, 1210, W - M, 1226), fill=LAV, width=4)
        d.line((W - M - 22, 1242, W - M, 1226), fill=LAV, width=4)
    footer(im, ft); return im


def detail(sp, idx, total, ft):
    im = canvas(); chrome(im, idx, total)
    pill(im, (M, 190), sp["kicker"].upper())
    grad_text(im, (M, 640), sp["big"].upper(), F(XB, 290))
    y = 770
    for ln in wrap(sp["title"].upper(), F(XB, 92), W - 2 * M)[:2]:
        text(im, (M, y), ln, F(XB, 92), WHITE); y += 94
    rows = sp.get("rows", [])[:5]
    top = 1260 - 82 * len(rows)
    d = ImageDraw.Draw(im)
    for i, (a, b) in enumerate(rows):
        yy = top + i * 82
        d.line((M, yy, W - M, yy), fill=(60, 55, 90), width=2)
        text(im, (M, yy + 52), a.upper(), F(SEMI, 27), MUTE, 6)
        text(im, (W - M, yy + 52), b, F(SEMI, 36), WHITE, 0, "rs")
    if rows:
        d.line((M, top + 82 * len(rows), W - M, top + 82 * len(rows)), fill=(60, 55, 90), width=2)
    footer(im, ft); return im


def point(sp, idx, total, ft):
    """Headline + short body paragraphs, optional stat line (label, value, 'up'|'down')."""
    im = canvas(); chrome(im, idx, total)
    pill(im, (M, 190), sp["kicker"].upper())
    y = 400
    for ln in sp["lines"]:
        text(im, (M, y), ln.upper(), F(XB, 120), WHITE); y += 112
    if sp.get("stat"):
        lab, val, tone = sp["stat"]
        col = GREEN if tone == "up" else RED if tone == "down" else LAV
        y += 30
        grad_text(im, (M, y + 200), val.upper(), F(XB, 230), (190, 170, 255) if col == LAV else col, col)
        text(im, (M, y + 250), lab.upper(), F(SEMI, 28), MUTE, 6)
        y += 300
    body_font = F(MED, 38)
    y += 40
    for para in sp.get("body", []):
        for ln in wrap(para, body_font, W - 2 * M):
            text(im, (M, y), ln, body_font, (205, 205, 220)); y += 54
        y += 22
    footer(im, ft); return im


def cta(sp, idx, total, ft):
    im = canvas(); chrome(im, idx, total)
    y = 330
    for ln in sp.get("lines", ["Know what", "yours is"]):
        text(im, (M, y), ln.upper(), F(XB, 128), WHITE); y += 108
    grad_text(im, (M, y), sp.get("accent", "worth.").upper(), F(XB, 128))
    text(im, (M, 628), sp.get("sub", "Scan your binder. Track its value over time."), F(MED, 36), MUTE)
    badge = Image.open(os.path.join(HERE, "assets", "badge_blk.png")).convert("RGBA")
    bw = 340; bh = int(badge.height * bw / badge.width)
    badge = badge.resize((bw, bh), Image.LANCZOS)
    by = 660
    im.alpha_composite(badge, (M, by))
    text(im, (M + bw + 40, by + bh / 2 + 4), "LINK IN BIO", F(SEMI, 34), WHITE, 4, "lm")
    text(im, (M, by + bh + 52), "OR FOLLOW  @VIRTUALBINDER.APP", F(SEMI, 26), LAV, 4)
    for name, x, y0, rot in (("phone_scan.png", 20, 880, 6), ("phone_shelf.png", 520, 850, -6)):
        p = Image.open(os.path.join(HERE, "assets", name)).convert("RGBA")
        p.thumbnail((520, 900))
        p = p.rotate(rot, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(p, (x, y0))
    return im


BUILDERS = {"hook": hook, "detail": detail, "point": point, "cta": cta}


def build(spec, out):
    os.makedirs(out, exist_ok=True)
    slides = spec["slides"]; paths = []
    for i, sp in enumerate(slides, 1):
        im = BUILDERS[sp["type"]](sp, i, len(slides), spec.get("footer", "")).convert("RGB")
        p = os.path.join(out, f"slide_{i}.png"); im.save(p, optimize=True); paths.append(p)
    return paths


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    for p in build(spec, sys.argv[2]):
        print(p)
