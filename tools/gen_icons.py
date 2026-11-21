"""Draws the sunflower.co.zw icon set from one piece of geometry.

The shape is the old Project Sunflower flower (two layers of petals around a serrated disc, see
BACKUP/sunflower-before-linc.git frontend/assets/sunflower.png) as a single-colour silhouette with NO background:
front petals are separated from the back layer by a thin gap, the serrated disc floats in a ring of space.

Run:  python tools/gen_icons.py      (needs Pillow)
Writes into frontend/: favicon.svg (turns light on dark tabs), favicon.ico, icon-192.png, icon-512.png (transparent),
icon-maskable-512.png, apple-touch-icon.png (opaque, the OS needs that), social-preview.png, site.webmanifest
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'frontend')
INK, PAPER = (20, 19, 15), (243, 242, 238)   # the site's own light-theme colours
INK_HEX, PAPER_HEX = '#14130f', '#f3f2ee'

# geometry in a 1000 x 1000 box centred on 0,0
FRONT = dict(n=14, r0=205, r1=470, w=58, rot=0.0)
BACK = dict(n=14, r0=205, r1=425, w=56, rot=math.pi / 14)
DISC_R = 172
RING = 52        # empty ring between disc and petals
GAP = 11         # empty line between front and back petals
TEETH = 44


def bez(p0, p1, p2, p3, k=28):
    out = []
    for i in range(k + 1):
        t = i / k
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def petal(a, r0, r1, w, lean=0.05):
    L = r1 - r0
    loc = [((r0, 0), (r0 + .22 * L, -w * 1.55), (r0 + .72 * L, -w * 1.2), (r1, 0)),
           ((r1, 0), (r0 + .72 * L, w * 1.2), (r0 + .22 * L, w * 1.55), (r0, 0))]
    c, s = math.cos(a + lean), math.sin(a + lean)
    return [tuple((c * x - s * y, s * x + c * y) for x, y in seg) for seg in loc]


def petals(cfg):
    return [petal(cfg['rot'] + i * 2 * math.pi / cfg['n'], cfg['r0'], cfg['r1'], cfg['w']) for i in range(cfg['n'])]


def disc_pts():
    return [((DISC_R + (13 if i % 2 == 0 else -4)) * math.cos(i * math.pi / TEETH),
             (DISC_R + (13 if i % 2 == 0 else -4)) * math.sin(i * math.pi / TEETH)) for i in range(TEETH * 2)]


def path_d(a, b):
    f = lambda p: '%.1f,%.1f' % p
    return 'M%s C%s %s %s C%s %s %s Z' % (f(a[0]), f(a[1]), f(a[2]), f(a[3]), f(b[1]), f(b[2]), f(b[3]))


# ---------- SVG: one mask, one colour that follows the browser theme ----------
def svg():
    back = ''.join('<path d="%s"/>' % path_d(*p) for p in petals(BACK))
    front = ''.join('<path d="%s"/>' % path_d(*p) for p in petals(FRONT))
    disc = 'M' + ' L'.join('%.1f,%.1f' % p for p in disc_pts()) + 'Z'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 1000 1000">'
            '<style>.f{fill:%s}@media(prefers-color-scheme:dark){.f{fill:#f4f4f2}}</style>'
            '<mask id="m" maskUnits="userSpaceOnUse" x="-500" y="-500" width="1000" height="1000">'
            '<g fill="#fff">%s</g>'
            '<g fill="#fff" stroke="#000" stroke-width="%d" stroke-linejoin="round" paint-order="stroke">%s</g>'
            '<circle r="%d" fill="#000"/><path d="%s" fill="#fff"/></mask>'
            '<rect class="f" x="-500" y="-500" width="1000" height="1000" mask="url(#m)"/></svg>'
            ) % (INK_HEX, back, GAP * 2, front, DISC_R + RING, disc)


# ---------- PNG: same geometry as an alpha mask, supersampled ----------
def mask(size, scale=1.0, ss=4):
    S = size * ss
    m = Image.new('L', (S, S), 0)
    dr = ImageDraw.Draw(m)
    k = S / 1000 * scale
    T = lambda p: (S / 2 + p[0] * k, S / 2 + p[1] * k)
    poly = lambda p: [T(q) for q in bez(*p[0])] + [T(q) for q in bez(*p[1])]
    for p in petals(BACK):
        dr.polygon(poly(p), fill=255)
    for p in petals(FRONT):
        pts = poly(p)
        dr.line(pts + [pts[0]], fill=0, width=max(1, round(GAP * 2 * k)), joint='curve')
        dr.polygon(pts, fill=255)
    r = (DISC_R + RING) * k
    dr.ellipse([S / 2 - r, S / 2 - r, S / 2 + r, S / 2 + r], fill=0)
    dr.polygon([T(p) for p in disc_pts()], fill=255)
    return m.resize((size, size), Image.LANCZOS)


def colourise(m, ink=INK, bg=None):
    base = Image.new('RGBA', m.size, (0, 0, 0, 0) if bg is None else bg + (255,))
    base.paste(Image.new('RGBA', m.size, ink + (255,)), (0, 0), m)
    return base


def font(size, bold=False):
    for name in (['segoeuib.ttf', 'arialbd.ttf'] if bold else ['segoeuil.ttf', 'segoeui.ttf', 'arial.ttf']):
        try:
            return ImageFont.truetype(os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', name), size)
        except OSError:
            pass
    return ImageFont.load_default()


def social():
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), PAPER)
    fl = colourise(mask(540, .98), bg=PAPER)
    im.paste(fl.convert('RGB'), (65, 45))
    dr = ImageDraw.Draw(im)
    dr.text((640, 215), 'delowe', font=font(84), fill=INK)
    dr.text((640, 305), 'projects', font=font(84, True), fill=INK)
    dr.text((644, 430), 'sunflower.co.zw', font=font(34), fill=(107, 106, 99))
    return im


def main():
    open(os.path.join(OUT, 'favicon.svg'), 'w', encoding='utf-8').write(svg())
    colourise(mask(512, .98)).save(os.path.join(OUT, 'icon-512.png'))
    colourise(mask(192, .98)).save(os.path.join(OUT, 'icon-192.png'))
    colourise(mask(180, .84), bg=PAPER).save(os.path.join(OUT, 'apple-touch-icon.png'))    # OS needs an opaque square
    colourise(mask(512, .68), bg=PAPER).save(os.path.join(OUT, 'icon-maskable-512.png'))   # inside the 80% safe zone
    ico = [colourise(mask(s, .98, ss=8)) for s in (16, 32, 48)]
    ico[2].save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    social().save(os.path.join(OUT, 'social-preview.png'), optimize=True)
    open(os.path.join(OUT, 'site.webmanifest'), 'w', encoding='utf-8').write(json.dumps({
        'name': 'Sunflower', 'short_name': 'Sunflower', 'start_url': '/', 'display': 'standalone',
        'background_color': PAPER_HEX, 'theme_color': PAPER_HEX,
        'icons': [{'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': '/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}, indent=2))
    print('icons written to', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
