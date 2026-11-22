#!/usr/bin/env python3
"""Compose the 22 November 2026 world-news front page (1024x1024).

Five generated editorial panels + masthead + caption bars + an
"ALSO TODAY" text column, all type set with PIL so every letter is
crisp. Output is JPEG bytes in a file named entry.png (allowed by
the competition: PNG or JPEG, told apart by first bytes).
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

ASSETS = os.path.expanduser('~/workspace/makefun/news-image-assets')
OUT = os.path.join(ASSETS, 'entry.png')

CREAM = (243, 235, 216)
PAPER = (250, 246, 236)
NAVY = (20, 32, 46)
INK = (24, 28, 34)
RED = (178, 44, 32)
TEAL = (159, 216, 210)
GREY = (96, 100, 104)

BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF_B = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

def fit(img, w, h):
    return ImageOps.fit(img, (w, h), Image.LANCZOS)

def load(name):
    return Image.open(os.path.join(ASSETS, name)).convert('RGB')

def fit_size(draw, text, size, max_w, min_size=14):
    while size > min_size and draw.textlength(text, font=font(BOLD, size)) > max_w:
        size -= 1
    return size

def panel(canvas, draw, x, y, w, h, img, headline, sub, head_size=25, sub_size=18):
    cap_h = 74 if sub else 52
    img_h = h - cap_h
    canvas.paste(fit(img, w, img_h), (x, y))
    draw.rectangle([x, y + img_h, x + w, y + h], fill=NAVY)
    hs = fit_size(draw, headline, head_size, w - 26)
    draw.text((x + 14, y + img_h + 10), headline, font=font(BOLD, hs), fill=CREAM)
    if sub:
        ss = fit_size(draw, sub, sub_size, w - 26)
        draw.text((x + 14, y + img_h + 44), sub, font=font(BOLD, ss), fill=TEAL)
    draw.rectangle([x, y, x + w, y + h], outline=NAVY, width=3)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def main():
    W = H = 1024
    canvas = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ---- masthead ----
    d.text((28, 14), 'T H E   W O R L D   I N   O N E   D A Y', font=font(BOLD, 25), fill=RED)
    d.text((26, 46), 'SUNDAY · 22 NOVEMBER 2026', font=font(SERIF_B, 55), fill=NAVY)
    d.text((28, 112), 'The day’s biggest stories, in a single picture', font=font(SERIF, 21), fill=GREY)
    d.line([24, 140, 1000, 140], fill=NAVY, width=4)

    lead = load('media-generation-news-lead-bahrain-0-1c99713a-e31b-4f3b-9559-4c71f830c203.webp')
    mexico = load('media-generation-news-mexico-cartel-0-a4e965f1-863f-4fad-a19b-3b80f5a5db50.webp')
    cop31 = load('media-generation-news-cop31-0-3ebb863a-c531-49de-a919-e14a2179efbc.webp')
    baltic = load('media-generation-news-baltic-ship-0-1b41eba0-80d2-441f-95f7-9802118d69c4.webp')
    markets = load('media-generation-news-markets-0-8be63ed0-766f-490b-a3f9-4cd59d5b0466.webp')

    # ---- lead + right column ----
    panel(canvas, d, 24, 156, 604, 452, lead,
          'IRAN STRIKES BAHRAIN', 'Industrial site hit · tankers struck in Hormuz', 31, 20)
    panel(canvas, d, 644, 156, 356, 218, mexico,
          'CARTEL BOSS CAPTURED', '11 killed in Sinaloa raid')
    panel(canvas, d, 644, 390, 356, 218, cop31,
          'COP31 TALKS STALL', 'Overtime over fossil fuels')

    # ---- bottom row ----
    panel(canvas, d, 24, 624, 317, 284, baltic,
          'DRONE HITS RUSSIAN SHIP', 'Baltic crew evacuated', 21, 17)
    panel(canvas, d, 353, 624, 317, 284, markets,
          'AI SELL-OFF SINKS STOCKS', 'Wall Street in correction', 21, 17)

    # ALSO TODAY text panel
    x, y, w, h = 682, 624, 318, 284
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=NAVY, width=3)
    d.text((x + 16, y + 12), 'ALSO TODAY', font=font(BOLD, 24), fill=RED)
    briefs = [
        'EU–Indonesia trade deal sealed after 10 years',
        'Missile hits Kryvyi Rih, Zelensky’s hometown',
        'UN draft rules on autonomous weapons agreed',
        'Alcaraz v Zverev in ATP Finals decider',
    ]
    cy = y + 50
    bf = font(BOLD, 17)
    for b in briefs:
        d.ellipse([x + 16, cy + 6, x + 24, cy + 14], fill=RED)
        for ln in wrap(d, b, bf, w - 52):
            d.text((x + 34, cy), ln, font=bf, fill=INK)
            cy += 22
        cy += 9

    # ---- footer ----
    d.line([24, 930, 1000, 930], fill=NAVY, width=3)
    foot = 'One day · one picture · 22 November 2026'
    fnt = font(SERIF_B, 24)
    tw = d.textlength(foot, font=fnt)
    d.text(((W - tw) / 2, 948), foot, font=fnt, fill=NAVY)

    canvas.save(OUT, 'JPEG', quality=88)
    print('wrote', OUT, os.path.getsize(OUT), 'bytes, size', canvas.size)

if __name__ == '__main__':
    main()
