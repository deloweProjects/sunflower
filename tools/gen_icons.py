"""Draws the sunflower.co.zw icon set from one piece of geometry.

The shape is the old Project Sunflower flower (two layers of outlined petals around a serrated disc, white on black,
see BACKUP/sunflower-before-linc.git frontend/assets/sunflower.png), redrawn as clean vectors.

Run:  python tools/gen_icons.py      (needs Pillow)
Writes into frontend/: favicon.svg, favicon.ico, icon-192.png, icon-512.png, icon-maskable-512.png,
apple-touch-icon.png, social-preview.png, site.webmanifest
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'frontend')
BG, FG = '#000000', '#ffffff'

# ---------- geometry, in a 1000 x 1000 box centred on 0,0 (flower radius ~ 470) ----------
FRONT = dict(n=14, r0=205, r1=470, w=58, rot=0.0)       # long petals in front
BACK = dict(n=14, r0=205, r1=420, w=52, rot=math.pi / 14)  # shorter petals between them, behind
DISC_R = 178
TEETH = 44
STROKE = 15


def bez(p0, p1, p2, p3, k=24):
    pts = []
    for i in range(k + 1):
        t = i / k
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def petal(a, r0, r1, w, lean=0.05):
    """Control points of one pointed petal pointing along angle a (slight lean so it feels drawn, not stamped)."""
    L = r1 - r0
    loc = [((r0, 0), (r0 + .22 * L, -w * 1.55), (r0 + .72 * L, -w * 1.2), (r1, 0)),
           ((r1, 0), (r0 + .72 * L, w * 1.2), (r0 + .22 * L, w * 1.55), (r0, 0))]
    c, s = math.cos(a + lean), math.sin(a + lean)
    return [tuple((c * x - s * y, s * x + c * y) for x, y in seg) for seg in loc]


def petals(cfg):
    return [petal(cfg['rot'] + i * 2 * math.pi / cfg['n'], cfg['r0'], cfg['r1'], cfg['w']) for i in range(cfg['n'])]


def disc_pts():
    pts = []
    for i in range(TEETH * 2):
        a = i * math.pi / TEETH
        r = DISC_R + (13 if i % 2 == 0 else -4)
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def flicks():
    """Short tick marks between disc and petals, like the little flicks in the old drawing."""
    out = []
    n = 28
    for i in range(n):
        a = i * 2 * math.pi / n + .06
        out.append(((DISC_R + 42) * math.cos(a), (DISC_R + 42) * math.sin(a), (DISC_R + 66) * math.cos(a), (DISC_R + 66) * math.sin(a)))
    return out


# ---------- SVG ----------
def svg_flower(bg=None, size=1000, scale=1.0, rx=None):
    f = lambda v: '%.1f' % v
    d = []
    for layer in (BACK, FRONT):
        for a_seg, b_seg in petals(layer):
            d.append('<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z"/>' % (
                f(a_seg[0][0]), f(a_seg[0][1]), f(a_seg[1][0]), f(a_seg[1][1]), f(a_seg[2][0]), f(a_seg[2][1]), f(a_seg[3][0]), f(a_seg[3][1]),
                f(b_seg[1][0]), f(b_seg[1][1]), f(b_seg[2][0]), f(b_seg[2][1]), f(b_seg[3][0]), f(b_seg[3][1])))
    petals_svg = ''.join(d)
    disc = 'M' + ' L'.join('%s,%s' % (f(x), f(y)) for x, y in disc_pts()) + 'Z'
    ticks = ''.join('M%s,%sL%s,%s' % (f(x0), f(y0), f(x1), f(y1)) for x0, y0, x1, y1 in flicks())
    bgel = ''
    if bg == 'circle':
        bgel = '<circle r="500" fill="%s"/>' % BG
    elif bg == 'square':
        bgel = '<rect x="-500" y="-500" width="1000" height="1000" fill="%s"/>' % BG
    elif bg == 'round':
        bgel = '<rect x="-500" y="-500" width="1000" height="1000" rx="%d" fill="%s"/>' % (rx or 220, BG)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 1000 1000">%s'
            '<g transform="scale(%s)" fill="%s" stroke="%s" stroke-width="%d" stroke-linejoin="round" stroke-linecap="round">%s'
            '<path d="%s" fill="%s" stroke="none"/><path d="%s" fill="none"/></g></svg>') % (bgel, scale, BG, FG, STROKE, petals_svg, disc, FG, ticks)


# ---------- PNG (same geometry, supersampled) ----------
def flower_png(size, scale=1.0, pad_bg=BG, ss=4):
    S = size * ss
    im = Image.new('RGB', (S, S), pad_bg)
    dr = ImageDraw.Draw(im)
    k = S / 1000 * scale
    T = lambda p: (S / 2 + p[0] * k, S / 2 + p[1] * k)
    sw = max(1, round(STROKE * k))
    for layer in (BACK, FRONT):
        for a_seg, b_seg in petals(layer):
            poly = [T(p) for p in bez(*a_seg)] + [T(p) for p in bez(*b_seg)]
            dr.polygon(poly, fill=BG, outline=FG, width=sw)
    dr.polygon([T(p) for p in disc_pts()], fill=FG)
    for x0, y0, x1, y1 in flicks():
        dr.line([T((x0, y0)), T((x1, y1))], fill=FG, width=sw)
    return im.resize((size, size), Image.LANCZOS)


def font(size, bold=False):
    for name in (['segoeuib.ttf', 'arialbd.ttf'] if bold else ['segoeuil.ttf', 'segoeui.ttf', 'arial.ttf']):
        try:
            return ImageFont.truetype(os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', name), size)
        except OSError:
            pass
    return ImageFont.load_default()


def social():
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), BG)
    fl = flower_png(520, scale=.98)
    im.paste(fl, (70, 55))
    dr = ImageDraw.Draw(im)
    dr.text((640, 215), 'delowe', font=font(84), fill=FG)
    dr.text((640, 305), 'projects', font=font(84, True), fill=FG)
    dr.text((644, 430), 'sunflower.co.zw', font=font(34), fill='#8b8d93')
    return im


def main():
    w = lambda name, data, mode='w': open(os.path.join(OUT, name), mode, **({'encoding': 'utf-8'} if mode == 'w' else {})).write(data)
    w('favicon.svg', svg_flower(bg='circle', scale=.9))
    big = flower_png(512, scale=.98)
    big.save(os.path.join(OUT, 'icon-512.png'))
    flower_png(192, scale=.98).save(os.path.join(OUT, 'icon-192.png'))
    flower_png(180, scale=.86).save(os.path.join(OUT, 'apple-touch-icon.png'))   # iOS rounds the corners itself, keep some air
    flower_png(512, scale=.7).save(os.path.join(OUT, 'icon-maskable-512.png'))    # inside the 80% safe zone
    ico = [flower_png(s, scale=.98, ss=8) for s in (16, 32, 48)]
    ico[2].save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    social().save(os.path.join(OUT, 'social-preview.png'), optimize=True)
    w('site.webmanifest', json.dumps({
        'name': 'Sunflower', 'short_name': 'Sunflower', 'start_url': '/', 'display': 'standalone',
        'background_color': BG, 'theme_color': BG,
        'icons': [{'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': '/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}, indent=2))
    print('icons written to', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
