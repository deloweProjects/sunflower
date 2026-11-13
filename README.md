# sunflower.co.zw

The home page of **delowe projects** and the home of the Linc landing page. Static HTML, no build step,
deployed by Vercel on every push to `main`.

| Address | Shows |
|---|---|
| https://sunflower.co.zw (and `www.`) | `frontend/index.html`: the home page, with Linc pinned as a project |
| https://linc.sunflower.co.zw | `frontend/linc/`: the Linc landing page (Windows download, Android closed-test sign-up) |
| https://sunflower.co.zw/linc/ | the same landing page, by path |

## How it connects

```
sunflower.co.zw  --click the Linc card-->  linc.sunflower.co.zw/#in   (the "#in" plays the entry reveal once)
        \                                        |
         \__ both are ONE Vercel project         +-- Windows button  -> github.com/deloweProjects/LincApp/releases/latest
             (root directory: frontend/)         +-- Android button  -> Google Form (closed-test sign-up) -> Google Play
                                                 +-- same page also lives at deloweprojects.github.io/LincApp (GitHub Pages)
```

`frontend/vercel.json` sends any request whose host is `linc.sunflower.co.zw` to `frontend/linc/`
(`routes`, not `rewrites`, so it beats the home page's own `/`). The root `vercel.json` is the same
thing plus `"outputDirectory": "frontend"` in case the Vercel root directory is ever changed.

## Layout

```
frontend/index.html       home page (generated, see tools/)
frontend/linc-icon-sm.webp
frontend/linc/            the Linc landing page: index.html, privacy.html, img/ (screenshots, video, wallpaper)
frontend/vercel.json      host routing
vercel.json               same routing + outputDirectory
tools/gen_home.py         writes frontend/index.html (python tools/gen_home.py)
tools/logo.js             the morphing dot-logo code (a copy is embedded by the generator)
```

## Working on it

- **Home page:** edit `tools/gen_home.py`, run it, commit the new `frontend/index.html`. Black and white
  only, light/dark by the browser. The logo morphs through five dot designs every 5 s; the big
  background word is an SVG of running outlines; the Linc card is a 3D card (Atropos 2.0.2 from
  jsDelivr); clicking it plays a full-screen transition into the Linc page.
- **Linc landing page:** it is a copy of `LincApp/index.html` (deloweProjects/LincApp, GitHub Pages).
  Change it there, copy it here, and change the one `og:image` line to the `linc.sunflower.co.zw` URL.
  Keep both copies identical.
- **Domain:** `linc.sunflower.co.zw` must be listed under the Vercel project, Settings, Domains, and DNS
  must point at Vercel. Both are done.
- **Vercel root directory is `frontend`.** Do not rename that folder without changing the setting.

## History

This repository used to be "Project Sunflower" (a Node backend and a static front end). It was
replaced on 2026-11-12 with ordinary commits, so the old site is still in the history (last commit
`e7d1548`). A complete mirror is kept at `D:\deloweProjects\BACKUP\sunflower-before-linc.git` on the
owner's PC.

The full write-up (all pages, the screenshot pipeline, the Google Form, the CI clean-up) is
`Vibe/distribution/WEBSITES.md` in the private Linc code repository.
