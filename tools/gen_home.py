import math

import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'frontend', 'index.html')

def sun():
    # Vogel's phyllotaxis: 144 seeds (a Fibonacci number) at the golden angle, radius ~ sqrt(n)
    ga = math.pi * (3 - math.sqrt(5))
    N = 144
    dots = ''.join('<circle cx="%.2f" cy="%.2f" r="%.2f"%s/>' % (4.55 * math.sqrt(i) * math.cos(i * ga), 4.55 * math.sqrt(i) * math.sin(i * ga), 0.75 + 1.15 * i / N, '' if i > 60 else ' opacity="1"')
                   for i in range(1, N + 1))
    return f'''<svg class="sun" viewBox="-62 -62 124 124" aria-hidden="true"><g class="r1" id="dots" fill="var(--acc)">{dots}</g></svg>'''

mail_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7.5l8.5 6 8.5-6"/></svg>'
arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
word = '<em>' + ''.join('<span style="--i:%d">%s</span>' % (i, c) for i, c in enumerate('SUN')) + '</em><em>' + ''.join('<span style="--i:%d">%s</span>' % (i + 3, c) for i, c in enumerate('FLOWER')) + '</em>'
import urllib.parse
_g = math.pi * (3 - math.sqrt(5))
_d = ''.join("<circle cx='%.2f' cy='%.2f' r='%.2f'/>" % (1.22 * math.sqrt(i) * math.cos(i * _g), 1.22 * math.sqrt(i) * math.sin(i * _g), .22 + .3 * i / 55) for i in range(1, 56))
fav = "data:image/svg+xml," + urllib.parse.quote("<svg xmlns='http://www.w3.org/2000/svg' viewBox='-10 -10 20 20'><circle r='10' fill='#000'/><g fill='#fff'>" + _d + "</g></svg>")
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
mono = 'abcdefghijklmnopqrstuvwxyz0123456789.@-/ '
grain = "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")"

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Sunflower</title>
<meta name="description" content="delowe projects.">
<meta name="theme-color" content="#f3f2ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#06070a" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@300;500;700&amp;display=swap&amp;text={letters}%20">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&amp;display=swap&amp;text={mono.replace(' ', '%20')}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@800&amp;display=swap&amp;text=SUNFLOWER">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/atropos@2.0.2/atropos.min.css">
<style>
:root{{color-scheme:light dark;
  --bg:#f3f2ee;--ink:#14130f;--soft:#6b6a63;--line:rgba(0,0,0,.11);--acc:#14130f;--stroke:rgba(0,0,0,.05);--run:rgba(0,0,0,.34);
  --gA:rgba(255,255,255,.95);--gB:rgba(0,0,0,.07);--card:rgba(255,255,255,.55);--grain:.05;--fl:rgba(0,0,0,.2);--sh:0 30px 70px -30px rgba(40,30,0,.35)}}
@media (prefers-color-scheme:dark){{:root{{
  --bg:#06070a;--ink:#ecebe6;--soft:#8b8d93;--line:rgba(255,255,255,.1);--acc:#f4f4f2;--stroke:rgba(255,255,255,.05);--run:rgba(255,255,255,.34);
  --gA:rgba(255,255,255,.07);--gB:rgba(255,255,255,.06);--card:rgba(255,255,255,.04);--grain:.07;--fl:rgba(255,255,255,.22);--sh:0 30px 80px -30px #000}}}}
*{{box-sizing:border-box;margin:0}}
html,body{{height:100%}}
body{{background:var(--bg);color:var(--ink);font:15px/1.5 "JetBrains Mono",ui-monospace,Consolas,monospace;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100svh}}
.disp{{font-family:"Unbounded","Arial Black",system-ui,sans-serif}}
a{{color:inherit}}

/* ambient */
.amb{{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}}
.amb i{{position:absolute;border-radius:50%;filter:blur(80px);opacity:0;animation:fade 3s forwards}}
.a1{{width:60vmax;height:60vmax;left:-20vmax;top:-30vmax;background:radial-gradient(closest-side,var(--gA),transparent);animation:fade 3s .1s forwards,d1 30s ease-in-out infinite alternate}}
.a2{{width:50vmax;height:50vmax;right:-18vmax;bottom:-26vmax;background:radial-gradient(closest-side,var(--gB),transparent);animation:fade 3s .5s forwards,d2 36s ease-in-out infinite alternate}}
#spot{{position:absolute;inset:0;background:radial-gradient(420px circle at var(--mx,50%) var(--my,40%),var(--gA),transparent 70%);opacity:0;animation:fade 2s 1s forwards}}
.floor{{position:absolute;left:-60%;right:-60%;bottom:-6vh;height:66vh;transform:perspective(560px) rotateX(66deg);transform-origin:50% 100%;opacity:0;animation:fade 3s .3s forwards;
  background-image:linear-gradient(var(--fl) 1.6px,transparent 1.6px),linear-gradient(90deg,var(--fl) 1.6px,transparent 1.6px);background-size:72px 72px;
  -webkit-mask-image:linear-gradient(to top,#000 5%,transparent 80%);mask-image:linear-gradient(to top,#000 10%,transparent 85%)}}
.floor:after{{content:"";position:absolute;inset:0;background-image:inherit;background-size:inherit;animation:fl 3.2s linear infinite}}
@keyframes fl{{to{{background-position:0 72px}}}}
.hud{{position:fixed;inset:14px;z-index:4;pointer-events:none;opacity:0;animation:fade 2s 1.6s forwards}}
.hud i{{position:absolute;width:22px;height:22px;border:0 solid var(--ink);opacity:.35}}
.hud i:nth-child(1){{left:0;top:0;border-width:1.5px 0 0 1.5px}}.hud i:nth-child(2){{right:0;top:0;border-width:1.5px 1.5px 0 0}}
.hud i:nth-child(3){{left:0;bottom:0;border-width:0 0 1.5px 1.5px}}.hud i:nth-child(4){{right:0;bottom:0;border-width:0 1.5px 1.5px 0}}
.noise{{position:fixed;inset:0;z-index:5;pointer-events:none;opacity:var(--grain);background-image:{grain}}}
@keyframes d1{{to{{transform:translate(8vmax,6vmax)}}}}
@keyframes d2{{to{{transform:translate(-8vmax,-5vmax)}}}}
@keyframes fade{{to{{opacity:1}}}}

/* giant outlined wordmark */
.word{{position:fixed;inset:0;z-index:1;pointer-events:none;user-select:none;overflow:hidden;
  -webkit-mask-image:radial-gradient(75% 70% at 50% 50%,#000 35%,transparent 100%);mask-image:radial-gradient(75% 70% at 50% 50%,#000 35%,transparent 100%)}}
.word .px{{position:absolute;left:50%;top:50%;width:min(140vw,175vh);transform:translate3d(calc(-50% + var(--px,0)*-22px),calc(-50% + var(--py,0)*-14px),0);transition:transform .6s cubic-bezier(.2,.7,.2,1);opacity:0;animation:fade 2.6s .4s forwards}}
.word svg{{display:block;width:100%;height:auto;overflow:visible}}
.word text{{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro",Inter,system-ui,sans-serif;font-weight:800;text-anchor:middle;letter-spacing:-.04em}}
.word .base{{fill:none;stroke:var(--stroke);stroke-width:1.1}}
.word .run{{fill:none;stroke:var(--run);stroke-width:1.5;stroke-linecap:round;stroke-dasharray:120 780;animation:dash 26s linear infinite}}
.word .run.b{{stroke-dasharray:60 1040;animation-duration:40s;animation-direction:reverse}}
@keyframes dash{{to{{stroke-dashoffset:-900}}}}
@keyframes dash2{{to{{stroke-dashoffset:-1100}}}}
.word .run.b{{animation-name:dash2}}

/* foreground */
main{{position:relative;z-index:2;min-height:100svh;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:clamp(22px,5vh,48px) 22px clamp(24px,5vh,44px);text-align:center}}
.top{{display:flex;flex-direction:column;align-items:center;gap:clamp(12px,2.4vh,22px)}}
.sun{{width:clamp(110px,19vmin,170px);height:auto;opacity:0;transform:scale(.7) rotate(-30deg);animation:bloom 1.8s .3s cubic-bezier(.2,.8,.2,1) forwards}}
#dots circle{{transition:transform 1.9s cubic-bezier(.7,0,.2,1) calc(var(--i)*1.6ms)}}.r2{{animation:spin 110s linear infinite reverse}}.sd{{animation:spin 200s linear infinite}}
.r1,.r2,.sd,.orb,.orb2{{transform-origin:0 0}}.orb{{animation:spin 24s linear infinite}}.orb2{{animation:spin 24s linear infinite reverse}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes bloom{{to{{opacity:1;transform:none}}}}
h1{{font-weight:300;font-size:clamp(20px,3.4vw,34px);letter-spacing:.02em;line-height:1.15}}
h1 b{{font-weight:700}}

.mid{{display:flex;flex-direction:column;align-items:center;gap:14px;width:100%}}
.label{{color:var(--soft);font-size:12px;letter-spacing:.3em;text-transform:uppercase}}

/* the deep card (Atropos: 3D parallax layers) */
.linccard{{width:min(100%,420px);height:230px;text-decoration:none;color:inherit;display:block;-webkit-tap-highlight-color:transparent}}
.linccard .atropos-inner{{border-radius:26px;border:1px solid var(--line);background:var(--card);-webkit-backdrop-filter:blur(18px) saturate(1.3);backdrop-filter:blur(18px) saturate(1.3);box-shadow:var(--sh);text-align:left;overflow:hidden}}
.linccard .cg{{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:26px 26px;opacity:.7;-webkit-mask-image:radial-gradient(80% 90% at 85% 0%,#000,transparent);mask-image:radial-gradient(80% 90% at 85% 0%,#000,transparent)}}
.linccard .ic{{position:absolute;left:26px;top:26px;width:64px;height:64px;border-radius:18px;box-shadow:0 14px 30px -8px rgba(0,0,0,.55)}}
.linccard .nm{{position:absolute;left:26px;bottom:62px;font-size:44px;font-weight:700;letter-spacing:-.02em;line-height:1}}
.linccard .url{{position:absolute;left:26px;bottom:26px;color:var(--soft);font-size:13px}}
.linccard .go{{position:absolute;right:24px;bottom:22px;width:46px;height:46px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;color:var(--acc)}}
.linccard .go svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}
.linccard .scan{{position:absolute;left:0;right:0;top:-70px;height:70px;background:linear-gradient(transparent,var(--gB),transparent);animation:scan 4.5s ease-in-out infinite}}
@keyframes scan{{to{{transform:translateY(320px)}}}}
.linccard .tk{{position:absolute;width:12px;height:12px;border:0 solid var(--acc);opacity:.8}}
.linccard .tk.a{{left:12px;top:12px;border-width:1.5px 0 0 1.5px}}.linccard .tk.b{{right:12px;top:12px;border-width:1.5px 1.5px 0 0}}.linccard .tk.c{{left:12px;bottom:12px;border-width:0 0 1.5px 1.5px}}.linccard .tk.d{{right:12px;bottom:12px;border-width:0 1.5px 1.5px 0}}
.linccard .lbl{{position:absolute;right:56px;top:25px;color:var(--soft);font-size:11px;letter-spacing:.26em;text-transform:uppercase}}
.linccard .pin{{position:absolute;right:20px;top:20px;width:24px;height:24px;color:var(--acc);transform:rotate(32deg);filter:drop-shadow(0 0 8px var(--acc))}}
.linccard .pin svg{{width:24px;height:24px;fill:currentColor;fill-opacity:.18;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.linccard .dot{{position:absolute;right:26px;top:28px;width:9px;height:9px;border-radius:50%;background:var(--acc);box-shadow:0 0 18px 2px var(--acc)}}

.mail{{display:inline-flex;align-items:center;gap:10px;color:var(--soft);text-decoration:none;font-size:14px;padding:10px 4px;border-bottom:1px solid var(--line);transition:color .25s,border-color .25s}}
.mail:hover{{color:var(--ink);border-color:var(--acc)}}
.mail svg{{width:17px;height:17px;fill:none;stroke:var(--acc);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}

/* the shelf: lots of projects, only Linc is in focus */
.shelf{{position:relative;width:min(100%,420px);margin:0 auto;perspective:1400px}}
.shelf .linccard{{position:relative;z-index:3}}
.ghost{{position:absolute;top:0;left:0;width:100%;height:230px;border-radius:26px;border:1px solid var(--line);background:var(--card);overflow:hidden;pointer-events:none;z-index:1;
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);opacity:0;transform:translateX(0) scale(.9);animation:gin 1.6s var(--gd,1.6s) cubic-bezier(.2,.8,.2,1) forwards}}
.ghost:before{{content:"";position:absolute;left:26px;top:26px;width:64px;height:64px;border-radius:18px;background:var(--line)}}
.ghost:after{{content:"";position:absolute;left:26px;bottom:62px;width:46%;height:30px;border-radius:9px;background:var(--line);box-shadow:0 44px 0 -10px var(--line)}}
.ghost i{{position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,var(--gA),transparent 70%);transform:translateX(-120%);animation:sh 2.6s var(--sd,0s) ease-in-out infinite}}
@keyframes sh{{to{{transform:translateX(120%)}}}}
@keyframes gin{{to{{opacity:var(--go);transform:translateX(var(--gx)) rotateY(var(--gr)) scale(var(--gs));filter:blur(var(--gb))}}}}
.g1{{--gx:-108%;--gr:16deg;--gs:.9;--gb:5px;--go:.6;--gd:1.6s}}
.g2{{--gx:-206%;--gr:24deg;--gs:.8;--gb:9px;--go:.34;--gd:1.8s;--sd:.5s}}
.g3{{--gx:108%;--gr:-16deg;--gs:.9;--gb:5px;--go:.6;--gd:1.7s;--sd:1s}}
.g4{{--gx:206%;--gr:-24deg;--gs:.8;--gb:9px;--go:.34;--gd:1.9s;--sd:1.5s}}
@media (max-width:760px){{.g2,.g4{{display:none}}.g1{{--gx:-94%}}.g3{{--gx:94%}}}}
@media (prefers-reduced-motion:reduce){{.ghost i{{animation:none}}}}

/* leaving for Linc: the card opens into a full-screen circle, the rest falls away */
#go{{position:fixed;inset:0;z-index:100;pointer-events:none;background:#0a110a;clip-path:circle(0 at var(--gx,50%) var(--gy,50%));transition:clip-path .85s cubic-bezier(.7,0,.2,1)}}
#go.on{{clip-path:circle(150vmax at var(--gx,50%) var(--gy,50%))}}
#go img{{position:absolute;left:var(--gx,50%);top:var(--gy,50%);width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:24px;opacity:0;transform:scale(.7);transition:opacity .4s .35s,transform .6s .35s cubic-bezier(.2,.8,.2,1);box-shadow:0 20px 50px -10px rgba(0,0,0,.7)}}
#go.on img{{opacity:1;transform:scale(1)}}
body.leaving main,body.leaving .word,body.leaving .amb,body.leaving .hud{{transition:opacity .6s,transform .8s cubic-bezier(.7,0,.2,1),filter .6s;opacity:0;transform:scale(.94);filter:blur(10px)}}

.rise{{opacity:0;transform:translateY(24px);filter:blur(8px);animation:rise 1.2s var(--d,0s) cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes rise{{to{{opacity:1;transform:none;filter:none}}}}
@media (max-width:560px){{.word p{{font-size:27vw}}.linccard{{height:210px}}.linccard .nm{{font-size:38px}}}}
@media (prefers-reduced-motion:reduce){{*{{animation-duration:.01s!important;animation-delay:0s!important}}.r1,.r2,.sd,.orb,.orb2,.amb i,.floor:after,.scan,.run{{animation:none!important}}}}
</style>
</head>
<body>
<div class="amb" aria-hidden="true"><div class="floor"></div><i class="a1"></i><i class="a2"></i><div id="spot"></div></div>
<div class="noise" aria-hidden="true"></div>
<div class="hud" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div class="word" aria-hidden="true"><div class="px"><svg viewBox="0 0 1000 640">
<defs><g id="w"><text x="500" y="300" font-size="330" text-anchor="middle">SUN</text><text x="500" y="590" font-size="330" text-anchor="middle">FLOWER</text></g></defs>
<use href="#w" class="base"/><use href="#w" class="run"/><use href="#w" class="run b"/>
</svg></div></div>
<main>
  <div class="top">
    {sun()}
    <h1 class="disp rise" style="--d:.9s">delowe <b>projects</b></h1>
  </div>
  <div class="mid">
    <div class="rise" style="--d:1.4s;width:100%;display:flex;justify-content:center">
      <div class="shelf">
        <div class="ghost g2" aria-hidden="true"><i></i></div><div class="ghost g1" aria-hidden="true"><i></i></div><div class="ghost g3" aria-hidden="true"><i></i></div><div class="ghost g4" aria-hidden="true"><i></i></div>
      <a class="atropos linccard" href="https://linc.sunflower.co.zw" aria-label="Linc, linc.sunflower.co.zw">
        <span class="atropos-scale"><span class="atropos-rotate"><span class="atropos-inner">
          <span class="cg" data-atropos-offset="-4"></span><span class="scan" data-atropos-offset="-2"></span><span class="tk a" data-atropos-offset="4"></span><span class="tk b" data-atropos-offset="4"></span><span class="tk c" data-atropos-offset="4"></span><span class="tk d" data-atropos-offset="4"></span>
          <img class="ic" data-atropos-offset="9" src="linc-icon-sm.webp" alt="" width="64" height="64" decoding="async">
          <span class="pin" data-atropos-offset="12"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3.5h6l-1 5.5 3 3.2V14H7v-1.8L10 9z"/><path d="M12 14v6.5"/></svg></span>
          <span class="nm disp" data-atropos-offset="7">Linc</span>
          <span class="url" data-atropos-offset="3">linc.sunflower.co.zw</span>
          <span class="go" data-atropos-offset="10">{arrow}</span>
        </span></span></span>
      </a>
      </div>
    </div>
  </div>
  <a class="mail rise" style="--d:1.7s" href="mailto:deloweprojects@gmail.com">{mail_icon}deloweprojects@gmail.com</a>
</main>
<script src="https://cdn.jsdelivr.net/npm/atropos@2.0.2/atropos.min.js" defer></script>
<script>
(function () {{
  var TAU = Math.PI * 2, GA = Math.PI * (3 - Math.sqrt(5));
  function heart(x, y) {{ var a = x * x + y * y - 1; return a * a * a - x * x * y * y * y <= 0; }}
  function hex(R, step, fn) {{
    var h = step * 0.866, nj = Math.ceil(R / h), ni = Math.ceil(R / step) + 1;
    for (var j = -nj; j <= nj; j++) for (var i = -ni; i <= ni; i++) fn(i * step + (j & 1 ? step / 2 : 0), j * h);
  }}
  var V = [];

  // 0 - the reference, in halftone dots: heart petals alternating with ovals around a dotted disc
  V.push(function () {{
    var d = [];
    hex(24, 4.3, function (x, y) {{ var r = Math.hypot(x, y); if (r < 23.5) d.push([x, y, 1.85 - 1.05 * r / 23.5]); }});
    for (var k = 0; k < 12; k++) {{
      var a = k * TAU / 12 - Math.PI / 2, c = Math.cos(a), s = Math.sin(a), big = k % 2 === 0, cu = 43;
      hex(16, 2.9, function (px, py) {{
        var du = px, tv = py, ok, t;
        if (big) {{ var sc = 8.4; ok = heart(tv / sc, du / sc + 0.12); t = (du + sc) / (sc * 2.3); }}
        else {{ ok = (du * du) / 144 + (tv * tv) / 20 <= 1; t = (du + 12) / 24; }}
        if (!ok) return;
        var rad = cu + du, ox = c * rad - s * tv, oy = s * rad + c * tv;
        d.push([ox, oy, 1.45 - 0.6 * Math.min(1, Math.max(0, t))]);
      }});
    }}
    return d;
  }});

  // 1 - phyllotaxis head: seeds at the golden angle
  V.push(function () {{
    var d = [];
    for (var i = 1; i <= 240; i++) {{ var r = 3.6 * Math.sqrt(i), a = i * GA; d.push([r * Math.cos(a), r * Math.sin(a), 0.7 + 1.15 * i / 240]); }}
    return d;
  }});

  // 2 - concentric rings, like a sun dial
  V.push(function () {{
    var d = [[0, 0, 1.7]];
    for (var k = 1; k <= 7; k++) {{ var R = k * 7.9, n = Math.round(6 * k * 1.08 + 1); for (var i = 0; i < n; i++) {{ var a = i * TAU / n + (k % 2) * 0.12; d.push([R * Math.cos(a), R * Math.sin(a), 0.75 + 0.1 * k]); }} }}
    return d;
  }});

  // 3 - sixteen rays of growing dots
  V.push(function () {{
    var d = [[0, 0, 1.6]];
    for (var k = 0; k < 16; k++) {{ var a = k * TAU / 16, long = k % 2 === 0; for (var j = 0; j < (long ? 12 : 8); j++) {{ var R = 12 + j * (long ? 3.9 : 3.8); d.push([R * Math.cos(a), R * Math.sin(a), 0.55 + 0.1 * j]); }} }}
    return d;
  }});

  // 4 - halftone disc: big dots in the middle, fading outward
  V.push(function () {{
    var d = [];
    hex(56, 5.1, function (x, y) {{ var r = Math.hypot(x, y); if (r <= 55) d.push([x, y, 2.0 * (1 - r / 58) + 0.35]); }});
    return d;
  }});

  function build() {{
    var sets = V.map(function (f) {{ return f(); }}), N = 0;
    sets.forEach(function (s) {{ N = Math.max(N, s.length); }});
    sets = sets.map(function (s) {{
      s = s.map(function (p) {{ var a = Math.atan2(p[1], p[0]) + Math.PI; return [p[0], p[1], p[2], Math.floor(a / (TAU / 28)) * 1000 + Math.hypot(p[0], p[1])]; }});
      s.sort(function (a, b) {{ return a[3] - b[3]; }});
      var out = [];
      for (var i = 0; i < N; i++) out.push(i < s.length ? s[Math.floor(i * s.length / Math.min(N, s.length))] : [0, 0, 0]);
      return out;
    }});
    return {{ sets: sets, N: N }};
  }}

  var g = document.getElementById('dots');
  if (!g || !('transition' in g.style)) return;
  var B = build(), NS = 'http://www.w3.org/2000/svg', dots = [], cur = 0;
  g.textContent = '';
  for (var i = 0; i < B.N; i++) {{ var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', 1); c.style.setProperty('--i', i); g.appendChild(c); dots.push(c); }}
  function show(k) {{
    var s = B.sets[k];
    for (var i = 0; i < dots.length; i++) dots[i].style.transform = 'translate(' + s[i][0].toFixed(2) + 'px,' + s[i][1].toFixed(2) + 'px) scale(' + s[i][2].toFixed(2) + ')';
  }}
  show(0);
  if (!matchMedia('(prefers-reduced-motion:reduce)').matches) {{
    setInterval(function () {{ if (document.hidden) return; cur = (cur + 1) % B.sets.length; show(cur); }}, 5000);
  }}
  window.__logo = {{ B: B, show: show }};
}})();
</script>
<script>
(function(){{
  var r=document.documentElement,q=0,x=0,y=0;
  addEventListener('pointermove',function(e){{x=e.clientX;y=e.clientY;if(!q){{q=requestAnimationFrame(function(){{q=0;r.style.setProperty('--mx',x+'px');r.style.setProperty('--my',y+'px');r.style.setProperty('--px',(x/innerWidth-.5).toFixed(3));r.style.setProperty('--py',(y/innerHeight-.5).toFixed(3))}})}}}},{{passive:true}});
  addEventListener('load',function(){{
    if(window.Atropos&&!matchMedia('(prefers-reduced-motion:reduce)').matches)
      Atropos({{el:'.linccard',activeOffset:34,shadowScale:1.02,rotateXMax:11,rotateYMax:11,highlight:true,shadow:true}});
  }});
}})();
</script>
<script>
(function () {{
  var link = document.querySelector('.linccard');
  function reset() {{ document.body.classList.remove('leaving'); var g = document.getElementById('go'); if (g) g.remove(); }}
  addEventListener('pageshow', function (e) {{ if (e.persisted) reset(); }});
  if (!link) return;
  link.addEventListener('click', function (e) {{
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
    e.preventDefault();
    var url = link.href + (link.href.indexOf('#') < 0 ? '#in' : '');
    if (matchMedia('(prefers-reduced-motion:reduce)').matches) {{ location.href = url; return; }}
    var r = link.getBoundingClientRect(), go = document.createElement('div');
    go.id = 'go'; go.style.setProperty('--gx', (r.left + r.width / 2) + 'px'); go.style.setProperty('--gy', (r.top + r.height / 2) + 'px');
    go.innerHTML = '<img src="linc-icon-sm.webp" alt="">';
    document.body.appendChild(go); document.body.classList.add('leaving');
    requestAnimationFrame(function () {{ requestAnimationFrame(function () {{ go.classList.add('on'); }}); }});
    setTimeout(function () {{ location.href = url; }}, 950);
  }});
}})();
</script>
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8').write(html)
print(len(html) // 1024, 'KB')
