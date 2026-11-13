(function () {
  var TAU = Math.PI * 2, GA = Math.PI * (3 - Math.sqrt(5));
  function heart(x, y) { var a = x * x + y * y - 1; return a * a * a - x * x * y * y * y <= 0; }
  function hex(R, step, fn) {
    var h = step * 0.866, nj = Math.ceil(R / h), ni = Math.ceil(R / step) + 1;
    for (var j = -nj; j <= nj; j++) for (var i = -ni; i <= ni; i++) fn(i * step + (j & 1 ? step / 2 : 0), j * h);
  }
  var V = [];

  // 0 - the reference, in halftone dots: heart petals alternating with ovals around a dotted disc
  V.push(function () {
    var d = [];
    hex(24, 4.3, function (x, y) { var r = Math.hypot(x, y); if (r < 23.5) d.push([x, y, 1.85 - 1.05 * r / 23.5]); });
    for (var k = 0; k < 12; k++) {
      var a = k * TAU / 12 - Math.PI / 2, c = Math.cos(a), s = Math.sin(a), big = k % 2 === 0, cu = 43;
      hex(16, 2.9, function (px, py) {
        var du = px, tv = py, ok, t;
        if (big) { var sc = 8.4; ok = heart(tv / sc, du / sc + 0.12); t = (du + sc) / (sc * 2.3); }
        else { ok = (du * du) / 144 + (tv * tv) / 20 <= 1; t = (du + 12) / 24; }
        if (!ok) return;
        var rad = cu + du, ox = c * rad - s * tv, oy = s * rad + c * tv;
        d.push([ox, oy, 1.45 - 0.6 * Math.min(1, Math.max(0, t))]);
      });
    }
    return d;
  });

  // 1 - phyllotaxis head: seeds at the golden angle
  V.push(function () {
    var d = [];
    for (var i = 1; i <= 240; i++) { var r = 3.6 * Math.sqrt(i), a = i * GA; d.push([r * Math.cos(a), r * Math.sin(a), 0.7 + 1.15 * i / 240]); }
    return d;
  });

  // 2 - concentric rings, like a sun dial
  V.push(function () {
    var d = [[0, 0, 1.7]];
    for (var k = 1; k <= 7; k++) { var R = k * 7.9, n = Math.round(6 * k * 1.08 + 1); for (var i = 0; i < n; i++) { var a = i * TAU / n + (k % 2) * 0.12; d.push([R * Math.cos(a), R * Math.sin(a), 0.75 + 0.1 * k]); } }
    return d;
  });

  // 3 - sixteen rays of growing dots
  V.push(function () {
    var d = [[0, 0, 1.6]];
    for (var k = 0; k < 16; k++) { var a = k * TAU / 16, long = k % 2 === 0; for (var j = 0; j < (long ? 12 : 8); j++) { var R = 12 + j * (long ? 3.9 : 3.8); d.push([R * Math.cos(a), R * Math.sin(a), 0.55 + 0.1 * j]); } }
    return d;
  });

  // 4 - halftone disc: big dots in the middle, fading outward
  V.push(function () {
    var d = [];
    hex(56, 5.1, function (x, y) { var r = Math.hypot(x, y); if (r <= 55) d.push([x, y, 2.0 * (1 - r / 58) + 0.35]); });
    return d;
  });

  function build() {
    var sets = V.map(function (f) { return f(); }), N = 0;
    sets.forEach(function (s) { N = Math.max(N, s.length); });
    sets = sets.map(function (s) {
      s = s.map(function (p) { var a = Math.atan2(p[1], p[0]) + Math.PI; return [p[0], p[1], p[2], Math.floor(a / (TAU / 28)) * 1000 + Math.hypot(p[0], p[1])]; });
      s.sort(function (a, b) { return a[3] - b[3]; });
      var out = [];
      for (var i = 0; i < N; i++) out.push(i < s.length ? s[Math.floor(i * s.length / Math.min(N, s.length))] : [0, 0, 0]);
      return out;
    });
    return { sets: sets, N: N };
  }

  var g = document.getElementById('dots');
  if (!g || !('transition' in g.style)) return;
  var B = build(), NS = 'http://www.w3.org/2000/svg', dots = [], cur = 0;
  g.textContent = '';
  for (var i = 0; i < B.N; i++) { var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', 1); c.style.setProperty('--i', i); g.appendChild(c); dots.push(c); }
  function show(k) {
    var s = B.sets[k];
    for (var i = 0; i < dots.length; i++) dots[i].style.transform = 'translate(' + s[i][0].toFixed(2) + 'px,' + s[i][1].toFixed(2) + 'px) scale(' + s[i][2].toFixed(2) + ')';
  }
  show(0);
  if (!matchMedia('(prefers-reduced-motion:reduce)').matches) {
    setInterval(function () { if (document.hidden) return; cur = (cur + 1) % B.sets.length; show(cur); }, 5000);
  }
  window.__logo = { B: B, show: show };
})();
