---
name: feature-campaign
description: Build an advin.io project-update email (one project, three features, a GIF of each, one call to action) from a project's recent commits, and put it in Constant Contact as a draft. Use when asked to announce a project's new features, make a newsletter, or make feature GIFs.
---

# Feature campaign: one project, three features, a GIF of each

Worked example: `campaigns/2026-11-helmsman/` (GIFs, the scripts that made them, `email.html`). Brand rules: the `advin-brand` skill. Read both first.

## 1. Pick the three features

- Read the project's commits since the last campaign (`git log --since=… --merges`). Pick the three a customer would notice; skip refactors, CI, docs-only.
- For each, note what it does, the one number or standard that proves it, and where it can be shown working.
- Check the project's own voice rules (its CLAUDE.md or BRANDING.md) and follow them on top of advin.io's. Every claim must be true of what is built; say "verified against a simulator" when it was, never "tested on a robot".

## 2. Decide how each one is proven (three tiers)

| Tier | When | How | Proof line |
|---|---|---|---|
| Capture | It runs in a browser (playground, site, web UI) | `scripts/record_browser_example.py` pattern: Playwright + Chrome, record video, script the clicks, then `scripts/to_gif.sh` with a crop | `Recorded live from the playground.` |
| Replay | Needs hardware or files | Run the real code on its test fixtures or simulator captures (e.g. `campaigns/…/src/dxf_dump.rs`), dump the output, animate exactly that output in an HTML page with a `render(t)` function, frame it with `scripts/render_frames.py`, then `to_gif.sh` | `… real output, animated.` |
| Illustrate | Nothing can be run | Same HTML route, clearly drawn as a diagram | `Illustration.` |

Rules: never show more than the GIF proves; never mock data in a "capture"; canvas apps (egui, WebGL) need clicks by coordinate, so take a screenshot first and find the control.

Headless WebGL: launch Chrome with `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`.

## 3. GIF specs

600 px wide (shown at 544), 12 fps, 8–14 s, ≤ 600 KB, palette per clip. No titles or captions baked in (the email carries the words). Start on a frame that already shows something. Animations use the project's palette and face (fonts from `google/fonts` on GitHub when the network blocks Google Fonts).

## 4. The email

- Fill `email-template.html`: every `{{…}}` placeholder; repeat the feature block three times (01 without the divider).
- Frame stays advin.io light; the stage takes the project's `STAGE_BG`, `ACCENT`, `STAGE_TEXT`, face. CTA at the top of the stage, lowercase (`see it for yourself`), linking to the place to try it.
- No datasheet links. Sign-off "Thanks," / Nick / advin.io · Dallas, TX / nick@advin.io.
- Render a preview in headless Chrome (route image URLs to local files) and look at it before uploading.

## 5. Constant Contact

1. Host the GIFs publicly first (commit them under `campaigns/<yyyy-mm>-<project>/` and use the raw.githubusercontent.com URL at that commit), then `upload_my_library_file` each one; use the returned `files.constantcontact.com` URLs in the HTML. Large files can't go through the connector as data URLs.
2. The wordmark is already in the library: `https://files.constantcontact.com/ed7f35af901/36c28a0e-f792-4f15-8aa1-cd069c1c02a1.png`.
3. `create_email` (format_type 5, from/reply-to nick@advin.io, `[[trackingImage]]` before `</body>`), or `update_email` on an existing draft. Name it `<Project>: <what's new> (<yyyy-mm>)`.
4. The connector cannot pick a list or send. Sending is Nick's click in Constant Contact (or the browser, once he is signed in). Never send without his explicit go-ahead.
