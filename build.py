#!/usr/bin/env python3
"""Seyaa Jewels Inc. - Trade Catalogue 2026 (A4 PDF)"""
import json, os, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

W, H = A4
INK      = HexColor('#1C1C1C')
PAPER    = HexColor('#FFFFFF')
ACCENT   = HexColor('#DD611C')
MUTED    = HexColor('#9A9A9A')
HAIRLINE = HexColor('#3A3A3A')
PANEL    = HexColor('#242424')

ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, 'fonts')
for n, f in [('Mont', 'Montserrat-Regular'), ('Mont-B', 'Montserrat-Bold'),
             ('Mont-L', 'Montserrat-Light'), ('Mont-SB', 'Montserrat-SemiBold'),
             ('Allura', 'Allura-Regular')]:
    pdfmetrics.registerFont(TTFont(n, f'{F}/{f}.ttf'))

EMBLEM = os.path.join(ROOT, 'assets', 'mark_white.png')
QR     = os.path.join(ROOT, 'assets', 'wa_qr.png')
IMGDIR = os.path.join(ROOT, 'renders')

DATA = json.load(open(os.path.join(ROOT, 'catalogue_data.json')))

ORDER = ['Round Tennis Bracelet', 'All Mix Fancy Bracelet',
         'Straight Line Tennis Necklace', 'Graduated Tennis Necklace',
         'Round Studs - Basket Setting', 'Round Studs - Martini Setting',
         'Eternity Bands']

BLURB = {
 'Round Tennis Bracelet':
   'The classic four-prong line bracelet. Uniform round brilliants set edge to edge, '
   'on a flexible link that sits flat on the wrist.',
 'All Mix Fancy Bracelet':
   'Alternating fancy shapes — pear, oval, emerald, marquise and cushion — set in a '
   'continuous line for a bracelet with more movement and light return than a round line.',
 'Straight Line Tennis Necklace':
   'A single uniform line of round brilliants carried right around the neck, '
   'finished with a concealed box clasp and safety catch.',
 'Graduated Tennis Necklace':
   'Stones graduate from the clasp down to the largest centre stones at the front, '
   'giving the line a tapered, settled drape.',
 'Round Studs - Basket Setting':
   'Round brilliants held in an open four-prong basket. The lifted gallery lets light '
   'through the pavilion and sits slightly proud of the lobe.',
 'Round Studs - Martini Setting':
   'A low three-prong martini mount that sets the stone close to the ear. '
   'Lighter in gold weight than the basket, with a cleaner profile from the side.',
 'Eternity Bands':
   'Round brilliants set in a continuous shared-prong circuit. '
   'Supplied in US size 7 as standard.',
}

SPEC = {  # extra fixed line per section
 'Round Tennis Bracelet': '7 inch · Box clasp with safety catch',
 'All Mix Fancy Bracelet': '7 inch · Box clasp with safety catch',
 'Straight Line Tennis Necklace': '16.5 inch · Box clasp with safety catch',
 'Graduated Tennis Necklace': '16.5 inch · Box clasp with safety catch',
 'Round Studs - Basket Setting': 'Four-prong basket · Push back',
 'Round Studs - Martini Setting': 'Three-prong martini · Push back',
 'Eternity Bands': 'US size 7 · Shared prong',
}


def ct_of(title):
    m = re.match(r'([\d.]+)', title)
    return m.group(1) if m else ''


def clean(t):
    """Short variant label, e.g. '2 CT'."""
    return f'{ct_of(t)} CT'


class Cat:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.c.setTitle('Seyaa Jewels Inc. — Trade Catalogue 2026')
        self.c.setAuthor('Seyaa Jewels Inc.')
        self.page = 0

    # ---------- primitives ----------
    def ground(self):
        self.c.setFillColor(INK)
        self.c.rect(0, 0, W, H, stroke=0, fill=1)

    def emblem(self, cx, top_y, h):
        im = Image.open(EMBLEM)
        w = h * im.width / im.height
        self.c.drawImage(EMBLEM, cx - w / 2, top_y - h, w, h,
                         mask='auto', preserveAspectRatio=True)

    def script(self, text, cx, y, size, color=PAPER):
        self.c.setFont('Allura', size)
        self.c.setFillColor(color)
        self.c.drawCentredString(cx - size * 0.075, y, text)

    def tracked(self, text, x, y, size, tracking=2.6, font='Mont',
                color=PAPER, center=None):
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        s = ' '.join(text)  # visual letter-spacing via spaces is unreliable; use charSpace
        self.c.setFont(font, size)
        obj = self.c.beginText()
        tw = self.c.stringWidth(text, font, size) + tracking * (len(text) - 1)
        obj.setTextOrigin((W - tw) / 2 if center else x, y)
        obj.setCharSpace(tracking)
        obj.setFillColor(color)
        obj.setFont(font, size)
        obj.textOut(text)
        obj.setCharSpace(0)
        self.c.drawText(obj)
        self.c._charSpace = 0
        return tw

    def rule(self, x1, x2, y, color=HAIRLINE, w=0.6):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(w)
        self.c.line(x1, y, x2, y)

    def footer(self, left='', right=True):
        self.c.setFont('Mont-L', 6.6)
        self.c.setFillColor(MUTED)
        if left:
            self.c.drawString(18 * mm, 12 * mm, left)
        self.c.setFillColor(HexColor('#6E6E6E'))
        self.c.drawRightString(W - 18 * mm, 12 * mm, 'Price on request')
        self.rule(18 * mm, W - 18 * mm, 16 * mm, HexColor('#2E2E2E'))

    def newpage(self):
        self.c.showPage()
        self.page += 1

    # ---------- image / placeholder ----------
    def plate(self, path, x, y, w, h, label):
        """Draw a render inside a panel, or a labelled placeholder frame."""
        self.c.setFillColor(PANEL)
        self.c.setStrokeColor(HexColor('#333333'))
        self.c.setLineWidth(0.6)
        self.c.roundRect(x, y, w, h, 3, stroke=1, fill=1)
        if path and os.path.exists(path):
            im = Image.open(path)
            pad = 6
            bw, bh = w - 2 * pad, h - 2 * pad
            sc = min(bw / im.width, bh / im.height)
            dw, dh = im.width * sc, im.height * sc
            self.c.drawImage(path, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh,
                             mask='auto', preserveAspectRatio=True)
        else:
            self.c.setFillColor(HexColor('#4A4A4A'))
            self.c.setFont('Mont-L', 7)
            self.c.drawCentredString(x + w / 2, y + h / 2 + 4, 'IMAGE')
            self.c.setFont('Mont-L', 6)
            self.c.drawCentredString(x + w / 2, y + h / 2 - 7, label)
        # caption strip
        self.c.setFillColor(ACCENT)
        self.c.setFont('Mont-SB', 6.4)
        obj = self.c.beginText()
        tw = self.c.stringWidth(label, 'Mont-SB', 6.4) + 1.8 * (len(label) - 1)
        obj.setTextOrigin(x + w / 2 - tw / 2, y - 11)
        obj.setCharSpace(1.8)
        obj.setFillColor(ACCENT)
        obj.setFont('Mont-SB', 6.4)
        obj.textOut(label)
        obj.setCharSpace(0)
        self.c.drawText(obj)
        self.c._charSpace = 0

    # ---------- pages ----------
    def cover(self):
        self.ground()
        self.c.setFillColor(ACCENT)
        self.c.rect(0, H - 4, W, 4, stroke=0, fill=1)
        self.emblem(W / 2, H - 52 * mm, 46 * mm)
        self.script('Seyaa Jewels', W / 2, H - 116 * mm, 56)
        self.tracked('LAB GROWN DIAMOND JEWELLERY', 0, H - 129 * mm, 8,
                     3.4, 'Mont-L', PAPER, center=True)
        self.rule(W / 2 - 24 * mm, W / 2 + 24 * mm, H - 142 * mm, ACCENT, 0.9)
        self.tracked('TRADE CATALOGUE', 0, H - 162 * mm, 13, 5.5, 'Mont', PAPER, center=True)
        self.script('2026', W / 2, H - 182 * mm, 44, ACCENT)
        self.rule(W / 2 - 40 * mm, W / 2 + 40 * mm, 48 * mm, HexColor('#2E2E2E'))
        self.tracked('14K GOLD  ·  E-F  ·  VS-SI  ·  IGI CERTIFIED', 0, 38 * mm, 7,
                     3.0, 'Mont-L', MUTED, center=True)
        self.tracked('PRICES ON REQUEST', 0, 26 * mm, 6.4, 3.0, 'Mont-L', HexColor('#6E6E6E'), center=True)
        self.newpage()

    def about(self, paras):
        self.ground()
        self.c.setFillColor(ACCENT)
        self.c.rect(0, H - 4, W, 4, stroke=0, fill=1)
        self.emblem(W / 2, H - 32 * mm, 26 * mm)
        self.script('About Seyaa Jewels', W / 2, H - 78 * mm, 32)
        self.rule(W / 2 - 16 * mm, W / 2 + 16 * mm, H - 88 * mm, ACCENT, 0.9)

        y = H - 108 * mm
        ml, mr = 28 * mm, W - 28 * mm
        for p in paras:
            y = self.wrap(p, ml, y, mr - ml, 'Mont-L', 9.6, 17, PAPER)
            y -= 9 * mm

        # standards block
        top = min(y - 16 * mm, 128 * mm)
        self.rule(ml, mr, top, HexColor('#2E2E2E'))
        self.tracked('HOUSE STANDARDS', 0, top - 10 * mm, 6.4, 3.0, 'Mont-SB', MUTED, center=True)
        y = top - 24 * mm
        cols = [('METAL', '14K Gold'), ('COLOURS', 'Yellow · White'),
                ('DIAMONDS', 'Lab Grown'), ('COLOUR', 'E-F'),
                ('CLARITY', 'VS-SI'), ('CERTIFICATION', 'IGI')]
        cw = (mr - ml) / 3
        for i, (k, v) in enumerate(cols):
            cx = ml + cw * (i % 3) + cw / 2
            ry = y - (i // 3) * 20 * mm
            self.c.setFillColor(ACCENT)
            self.c.setFont('Mont-SB', 6.2)
            obj = self.c.beginText()
            tw = self.c.stringWidth(k, 'Mont-SB', 6.2) + 1.8 * (len(k) - 1)
            obj.setTextOrigin(cx - tw / 2, ry)
            obj.setCharSpace(1.8); obj.setFillColor(ACCENT); obj.setFont('Mont-SB', 6.2)
            obj.textOut(k); obj.setCharSpace(0); self.c.drawText(obj); self.c._charSpace = 0
            self.c.setFillColor(PAPER)
            self.c.setFont('Mont', 10)
            self.c.drawCentredString(cx, ry - 14, v)
        self.rule(ml, mr, 42 * mm, HexColor('#2E2E2E'))
        self.tracked('PRICES ON REQUEST', 0, 32 * mm, 6.4, 3.0, 'Mont-L', HexColor('#6E6E6E'), center=True)
        self.newpage()

    def wrap(self, text, x, y, width, font, size, lead, color):
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        words, line = text.split(), ''
        for wd in words:
            t = (line + ' ' + wd).strip()
            if self.c.stringWidth(t, font, size) <= width:
                line = t
            else:
                self.c.drawString(x, y, line)
                y -= lead
                line = wd
        if line:
            self.c.drawString(x, y, line)
            y -= lead
        return y

    def wrapc(self, text, cx, y, width, font, size, lead, color):
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        words, line, lines = text.split(), '', []
        for wd in words:
            t = (line + ' ' + wd).strip()
            if self.c.stringWidth(t, font, size) <= width:
                line = t
            else:
                lines.append(line); line = wd
        if line:
            lines.append(line)
        for ln in lines:
            self.c.drawCentredString(cx, y, ln)
            y -= lead
        return y

    def opener(self, name, items):
        self.ground()
        self.c.setFillColor(ACCENT)
        self.c.rect(0, H - 4, W, 4, stroke=0, fill=1)

        title, sub = name, ''
        if ' - ' in name:
            title, sub = name.split(' - ')
        self.tracked('COLLECTION', 0, H - 56 * mm, 6.6, 3.4, 'Mont-L', MUTED, center=True)
        self.script(title, W / 2, H - 74 * mm, 36)
        if sub:
            self.tracked(sub.upper(), 0, H - 84 * mm, 8, 3.2, 'Mont-L', ACCENT, center=True)
        self.rule(W / 2 - 16 * mm, W / 2 + 16 * mm, H - 94 * mm, ACCENT, 0.9)

        y = self.wrapc(BLURB[name], W / 2, H - 108 * mm, W - 74 * mm,
                       'Mont-L', 9, 15, HexColor('#CFCFCF'))
        self.tracked(SPEC[name].upper(), 0, y - 7 * mm, 6.6, 2.6, 'Mont', MUTED, center=True)

        # ---- spec table
        ml, mr = 22 * mm, W - 22 * mm
        ty = y - 26 * mm
        headers = ['CT WT', 'STONES', 'GOLD WT', 'SIZE', 'SKU · WHITE', 'SKU · YELLOW']
        wts = [0.13, 0.13, 0.14, 0.14, 0.23, 0.23]
        tw = mr - ml
        xs, acc = [], ml
        for f in wts:
            xs.append(acc); acc += tw * f

        self.c.setFillColor(HexColor('#2A2A2A'))
        self.c.rect(ml, ty - 5, tw, 18, stroke=0, fill=1)
        for i, h in enumerate(headers):
            cx = xs[i] + tw * wts[i] / 2
            obj = self.c.beginText()
            w_ = self.c.stringWidth(h, 'Mont-SB', 6.2) + 1.6 * (len(h) - 1)
            obj.setTextOrigin(cx - w_ / 2, ty + 1.8)
            obj.setCharSpace(1.6); obj.setFillColor(ACCENT); obj.setFont('Mont-SB', 6.2)
            obj.textOut(h); obj.setCharSpace(0); self.c.drawText(obj); self.c._charSpace = 0

        ry = ty - 5
        for n, it in enumerate(items):
            rh = 19
            ry -= rh
            if n % 2 == 0:
                self.c.setFillColor(HexColor('#212121'))
                self.c.rect(ml, ry, tw, rh, stroke=0, fill=1)
            vals = [f"{ct_of(it['title'])} ct",
                    str(int(float(it['stones']))) if it['stones'] else '—',
                    f"{it['gold']} g",
                    str(it['size']).replace('INCH', 'in').strip() if it['size'] not in (None, 'NA') else '—',
                    it.get('sku_W', '—'), it.get('sku_Y', '—')]
            for i, v in enumerate(vals):
                cx = xs[i] + tw * wts[i] / 2
                self.c.setFont('Mont' if i < 4 else 'Mont-L', 7.6 if i < 4 else 7.2)
                self.c.setFillColor(PAPER if i < 4 else HexColor('#C9C9C9'))
                self.c.drawCentredString(cx, ry + 6.5, v)
        self.rule(ml, mr, ry, HexColor('#2E2E2E'))

        self.c.setFont('Mont-L', 6.6)
        self.c.setFillColor(MUTED)
        self.c.drawCentredString(W / 2, ry - 16,
                                 'All diamonds lab grown · E-F colour · VS-SI clarity · 14K gold, yellow or white')
        self.footer(title.upper())
        self.newpage()

    def variant(self, section, it):
        self.ground()
        self.c.setFillColor(ACCENT)
        self.c.rect(0, H - 4, W, 4, stroke=0, fill=1)

        title = section.split(' - ')[0]
        sub = section.split(' - ')[1] if ' - ' in section else ''
        self.tracked(title.upper() + (f'  ·  {sub.upper()}' if sub else ''),
                     0, H - 30 * mm, 6.4, 3.0, 'Mont-L', MUTED, center=True)
        self.script(f'{ct_of(it["title"])} Carat', W / 2, H - 48 * mm, 34)
        self.rule(W / 2 - 14 * mm, W / 2 + 14 * mm, H - 57 * mm, ACCENT, 0.9)

        # two plates
        gap = 7 * mm
        mg = 18 * mm
        pw = (W - 2 * mg - gap) / 2
        ph = pw * 1.22
        py = H - 70 * mm - ph
        self.plate(f'{IMGDIR}/{it.get("sku_W","")}.jpg', mg, py, pw, ph,
                   f'{it.get("sku_W","—")}  ·  14K WHITE')
        self.plate(f'{IMGDIR}/{it.get("sku_Y","")}.jpg', mg + pw + gap, py, pw, ph,
                   f'{it.get("sku_Y","—")}  ·  14K YELLOW')

        # spec strip
        ml, mr = mg, W - mg
        sy = 94 * mm
        self.c.setFillColor(HexColor('#232323'))
        self.c.roundRect(ml, sy - 32 * mm, mr - ml, 36 * mm, 3, stroke=0, fill=1)

        size = str(it['size']).replace('INCH', 'in').strip() if it['size'] not in (None, 'NA') else '—'
        cells = [('TOTAL CARAT WEIGHT', f"{it['tcw']} ct"),
                 ('DIAMONDS', str(int(float(it['stones']))) if it['stones'] else '—'),
                 ('SHAPE', str(it['shape']).strip().title()),
                 ('GOLD WEIGHT', f"{it['gold']} g"),
                 ('LENGTH / SIZE', size),
                 ('COLOUR · CLARITY', f"{it['color']} · {it['clarity']}")]
        cw = (mr - ml) / 3
        for i, (k, v) in enumerate(cells):
            cx = ml + cw * (i % 3) + cw / 2
            ry = sy - 10 * mm - (i // 3) * 16 * mm
            obj = self.c.beginText()
            w_ = self.c.stringWidth(k, 'Mont-SB', 5.8) + 1.5 * (len(k) - 1)
            obj.setTextOrigin(cx - w_ / 2, ry)
            obj.setCharSpace(1.5); obj.setFillColor(ACCENT); obj.setFont('Mont-SB', 5.8)
            obj.textOut(k); obj.setCharSpace(0); self.c.drawText(obj); self.c._charSpace = 0
            self.c.setFillColor(PAPER)
            self.c.setFont('Mont', 9.4)
            self.c.drawCentredString(cx, ry - 13, v)

        self.c.setFont('Mont-L', 6.6)
        self.c.setFillColor(MUTED)
        self.c.drawCentredString(W / 2, sy - 42 * mm,
                                 f'14K Gold, yellow or white · Lab grown diamonds · IGI certified · {SPEC[section]}')
        self.footer(f'{title.upper()}  ·  {ct_of(it["title"])} CT')
        self.newpage()

    def contact(self):
        self.ground()
        self.c.setFillColor(ACCENT)
        self.c.rect(0, H - 4, W, 4, stroke=0, fill=1)
        self.emblem(W / 2, H - 34 * mm, 30 * mm)
        self.script('Seyaa Jewels', W / 2, H - 80 * mm, 40)
        self.tracked('LAB GROWN DIAMOND JEWELLERY', 0, H - 90 * mm, 7,
                     3.2, 'Mont-L', MUTED, center=True)
        self.rule(W / 2 - 18 * mm, W / 2 + 18 * mm, H - 102 * mm, ACCENT, 0.9)

        y = H - 120 * mm
        blocks = [('SEYAA JEWELS INC.',
                   ['42 West 48th Street, Suite #600',
                    'New York, NY 10036',
                    'United States']),
                  ('CONTACT',
                   ['Rahul Shah', '+1 917 801 6060', 'seyaajewels@gmail.com'])]
        for k, lines in blocks:
            self.tracked(k, 0, y, 6.4, 3.0, 'Mont-SB', ACCENT, center=True)
            y -= 16
            for ln in lines:
                self.c.setFont('Mont-L', 10)
                self.c.setFillColor(PAPER)
                self.c.drawCentredString(W / 2, y, ln)
                y -= 15
            y -= 10 * mm

        # QR
        qs = 32 * mm
        qy = y - qs
        self.c.setFillColor(PAPER)
        self.c.roundRect(W / 2 - qs / 2 - 4, qy - 4, qs + 8, qs + 8, 3, stroke=0, fill=1)
        self.c.drawImage(QR, W / 2 - qs / 2, qy, qs, qs, mask='auto')
        self.tracked('SCAN TO CHAT ON WHATSAPP', 0, qy - 16, 6.2, 2.8,
                     'Mont-L', MUTED, center=True)

        self.rule(W / 2 - 40 * mm, W / 2 + 40 * mm, 42 * mm, HexColor('#2E2E2E'))
        self.tracked('PRICES ON REQUEST', 0, 32 * mm, 7, 3.4, 'Mont', ACCENT, center=True)
        self.newpage()

    def build(self):
        self.cover()
        self.about([
            'Seyaa Jewels Inc. manufactures fine jewellery set exclusively with IGI-certified '
            'lab grown diamonds. Every piece in this catalogue is produced in-house, from stone '
            'selection and setting through to final polish, giving us direct control over quality, '
            'consistency and delivery timelines.',
            'Our range is built for the trade: classic silhouettes in tennis bracelets, necklaces, '
            'studs and eternity bands, offered across a full spread of carat weights in 14K yellow '
            'and white gold. Specifications are standardised so repeat orders match the first.',
            'All diamonds are E-F colour, VS-SI clarity. Prices are available on request.',
        ])
        for sec in ORDER:
            items = DATA[sec]
            self.opener(sec, items)
            for it in items:
                self.variant(sec, it)
        self.contact()
        self.c.save()
        return self.page


if __name__ == '__main__':
    out = os.path.join(ROOT, 'Seyaa_Jewels_Trade_Catalogue_2026.pdf')
    n = Cat(out).build()
    print('pages:', n, '->', out)
