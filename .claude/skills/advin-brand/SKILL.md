---
name: advin-brand
description: advin.io brand guide (and its hidden creative side ADVINIO). Use for anything made for advin.io or its projects: web pages, emails and Constant Contact campaigns, social posts, decks, docs, copy.
---

# advin.io brand guide

Full design system with live previews, tokens and logo files: https://claude.ai/artifact/J8czVPWQFHVLdtgi2kkTPR
Website source of truth: github.com/JimothyJohn/home (`BRANDING.md`, `index.html`, `brand/`).

## 1. Identity

- **advin.io**: the business. An AI research lab in **Dallas, TX**. Handcrafted, exclusive, small on purpose. **Light mode.**
- **ADVINIO**: the creative outlet, a hidden Easter egg beneath the technology. **Dark mode.** Never announced or linked from business surfaces (email, legal, documents, proposals). Dark-mode visitors to advin.io land in it; a device that turns dark with the page open sees advin.io fade into it.
- **Legal entity:** `advin.io LLC` (registration lapsed; owner will reinstate before revenue). Use it once in legal contexts and footers, then "advin.io".
- **Projects incubate** on advin.io subdomains (`helmsman.advin.io`). A project that graduates gets its own domain, like Apache or Eclipse incubators. Docs, privacy and data policies live on advin.io and are shared by all projects. **Each project keeps its own brand and colors.**
- "Boutique" reads cheesy. Avoid it. The hero dek is due for new copy.
- Parked idea: an older blue eye logo. Not in use.

## 2. Names and marks

| Write | Never |
|---|---|
| advin.io (always lowercase, always `.io`, even at sentence start) | Advin, ADVIN.IO, Advin.io |
| ADVINIO (always uppercase, no dot) | Advinio, aDVINIO |

If "advin.io" starting a sentence reads badly, rewrite the sentence.

- **advin.io wordmark:** Comfortaa Bold (700), letter-spacing −0.02em, lowercase.
- **ADVINIO wordmark:** Comfortaa Light (300), capitals, +0.04em. Dark ground only.
- **The mark:** a capital **A** in Comfortaa Light, ADVINIO's letter. **Anything circular or square-cropped uses the A**: favicon, avatars, social profiles, app icons. The default avatar is the paper A on an ink square. The lowercase "a" is never a mark.
- Never add a symbol beside a wordmark, recolor it with a project accent, stretch it, outline it, or put ADVINIO on light or advin.io on dark.
- Hosted files (after PR #40 deploys): `https://advin.io/brand/` has `advin-wordmark-ink.svg`, `advin-wordmark-paper.svg`, `advinio-wordmark-paper.svg`, `advinio-wordmark-ink.svg`, `a-mark-paper.svg`, `a-mark-ink.svg`, `avatar-400-dark.png`, `avatar-400-light.png`, and `wordmark-email-400.png`. Favicons and `og.png` sit at the site root.

## 3. Color

Monochrome. **No hues in the frame.** Color belongs to the projects, inside their own blocks. Near-pure, never `#ffffff` or `#000000`. Subtle near-pure background gradients are welcome (e.g. paper → paper2); never hue gradients in the frame.

| Token | advin.io (light) | ADVINIO (dark) | Use |
|---|---|---|---|
| paper | #fcfcfc | #0d0d0d | Ground |
| paper2 | #f4f4f4 | #181818 | Raised, hover, email canvas |
| ink | #0d0d0d | #fcfcfc | Text, heavy rules, borders, button fill |
| ink-soft | #3d3d3d | #c2c2c2 | Secondary/body text |
| faint-text | #6b6b6b | #8a8a8a | Tertiary text: footers, meta |
| faint | #8a8a8a | #6b6b6b | Icons/marks only (fails as text) |
| rule | #e4e4e4 | #262626 | Hairlines only |

Selection inverts (ink fill, paper text). Prefer higher contrast.

**Project palettes** (inside their own entries only): helmsman #FFC20E on #141414, Saira Stencil One · specodex #A88A1C / #7A1F1F on #E8E2C9, Oswald · perceptronics #157a45 · amr emulator #1a76bc · supervictor #f97316 · tensor factory #e1261c · uServer #0d6efd · ophanim #050505 (dark-mode tick #a0a0a0) · colmapper #8a8a8a. A project block may use its background, a 4px left accent bar and its title color and face.

## 4. Typography

One face: **Comfortaa** (Google Fonts, variable 300–700). IBM Plex Mono only for "shards" (small code/spec fragments).

| Style | Size | Weight | Case |
|---|---|---|---|
| Hero wordmark | clamp(3.2rem, 10vw, 7rem) | 700 (ADVINIO 300) | lowercase (ADVINIO caps) |
| Headline | 28–36px | 700 | lowercase |
| Section label | 13px, +0.14em | 700, ink-soft | lowercase |
| Body | 15–16px, line-height 1.55 (docs 1.7) | 400; emphasis 600 in ink | sentence case |
| Button | 13–14px | 600 | lowercase |
| Footer | 12px, +0.08em | 400, faint-text | sentence case |

Measure: dek 54ch, body 60ch, documents 42rem. No italics in the frame.

## 5. Layout, depth, motion

- **Structure is rules, not boxes.** A section opens with a **3px ink rule** and a lowercase label; items separate with 1px `rule` hairlines.
- **Masthead:** wordmark left, one contact pill right (`mailto:nick@advin.io`), 3px rule beneath. **Footer:** 3px rule, one centered line: `© 2026 advin.io LLC · Dallas, TX` plus privacy and terms links (ADVINIO: `© 2026 ADVINIO · an advin.io LLC endeavor`).
- **Project gallery rows:** title links to the site, a GitHub mark links to the source, then one or two sentences and one "shard". The row wears the project's own background and accent bar. No ranks, dates or stats.
- **Depth:** shadows welcome if smooth. Use two layers (tight contact plus wide ambient), low alpha, ink-tinted, blur ≤ 56px.
  - Light: `0 1px 2px rgba(13,13,13,.06), 0 4px 12px rgba(13,13,13,.08)` (rest) and `0 2px 4px rgba(13,13,13,.06), 0 10px 28px rgba(13,13,13,.14)` (raised).
  - ADVINIO: add `inset 0 1px 0 rgba(252,252,252,.06)` and step the surface to #181818.
  - Never transition `box-shadow`: fade an `::after` that carries it. No `backdrop-filter` or large `drop-shadow`.
- **Motion is quiet and interactive.** If the visitor isn't moving the page, the page doesn't move: no idle loops or drift. Hover responses, scroll reveals, a single short rise on load. Prompted fades are welcome; never a fade on first load (reads as loading). Respect `prefers-reduced-motion`.
- No grain, no texture, no icon set (only the GitHub mark and the A).

## 6. Voice

Plain, declarative, a little dry. Handcrafted and exclusive, never salesy. Dry, not cute.

- **Two registers.** The **purpose line** is general and memorable, adjectives welcome ("The soft PLC you program by describing the machine."). The **spec line** is specific, with numbers and standards ("IEC 61131-3 Structured Text, EtherNet/IP and Modbus TCP, fixed scan."). Adjectives must be backed by data; if nothing backs one, cut it.
- What it does first. One or two sentences per project; the rest belongs on a datasheet.
- **No exclamation points. No emoji.** No urgency ("limited time", "don't miss").
- Lowercase headings, labels and buttons (`contact`, `see it`, `try the playground`). Sentence case for body and subject lines.
- Use: lab, system, build, handcrafted, simple, runs, finds, writes. Avoid: solution, platform, ecosystem, world-class, revolutionary, leverage, empower, unlock, book a demo, "we're thrilled".
- Emails sign off **"Thanks,"** then: `Nick` / `advin.io · Dallas, TX` / `nick@advin.io`. No logo, social icons or quotes in signatures.
- **Project voice rules stack on top.** Helmsman: written for controls and plant engineers. Never "agent" or "agentic" on marketing. No status, roadmap or "early release". Never name the implementation language, Raspberry Pi or the model vendor. The edge node is "the Skipper". Headline: "Say what it should do. See it work." Claims must be true of what's built.

## 7. Content model: video leads

A project update starts as a **video** (YouTube) showing the thing running with real people. Its **transcript** becomes the copy. **Stills** from it become thumbnails and post and email images. Make it **interactive** where possible (playground, live demo).

## 8. Imagery

- Real things and real people only. No stock.
- **Generated images are fine for graphics, never for people or for products presented as real.**
- Until real photos exist, use **labeled placeholders** (paper2 block, 1px rule border, a label like `[PHOTO] engineer at the bench with a Skipper`). Never stand-ins.
- Screenshots come from real runs, never mocked data.
- Diagrams are monochrome line work with lowercase labels; a project's accent may color the one path that matters.

## 9. Email (Constant Contact)

- **The frame never changes; the stage does.** advin.io light frame (masthead with wordmark image, lowercase headline, intro, "Thanks," sign-off, `© 2026 advin.io LLC · Dallas, TX` footer) around a full-width **project stage** in that project's own palette and face. No per-email brand guide.
- **Format: one project, three features, proof of each, one call to action.** The CTA (`see it for yourself`, in the project's accent) sits at the **top** of the stage, right under the project name. No datasheet links.
- Each feature: number (`01`), title in the project's face, purpose line, GIF (544 px, ≤ 600 KB, no title baked in, first frame not empty because Outlook shows only that), spec line in mono, and a small proof line: *recorded live*, *real output, animated*, or *illustration*.
- Single column, 600 px, table layout, hex inlined, page background #fcfcfc edge to edge (Constant Contact appends a white footer with the address and unsubscribe; don't add your own).
- Fonts: `'Comfortaa', Arial, Helvetica, sans-serif`; the wordmark is an image. No shadows. Subject: short, specific, sentence case, no emoji. Preheader: one sentence that adds a fact.
- Never ADVINIO in email. Never emoji or "!".
- Template and workflow: the `feature-campaign` skill.

## 10. Social

- Live: Replicate (`jimothyjohn`), GitHub (`JimothyJohn`), YouTube. LinkedIn company page to create; Instagram maybe later. Every avatar is the inverted A.
- Bio: one line, no emoji, no "boutique". Link `https://advin.io`, no link-in-bio pages.
- Posts are 1080×1080 or 1200×630. A paper frame, 3px rule and wordmark, plus one project or one fact in that project's colors. Write a purpose line, a spec line, a link, and at most two lowercase hashtags for real communities. No engagement bait or countdowns.

## 11. Decks and documents

- 16:9 on a paper ground. The title slide is the hero: shard ticks, wordmark, dek.
- Each content slide opens with a 3px rule and a lowercase label. One idea per slide; slide number in faint-text, bottom right.
- Documents: Comfortaa throughout, lowercase headings, hairline tables with no fills, and the footer `advin.io · Dallas, TX`.

## 12. ADVINIO in full

- Comfortaa Light capitals on #0d0d0d. The same rules and restraint.
- Shadows get a top rim, and motion eases a little longer.
- Generated, abstract or motion imagery is fine here, one image per surface.
- May link back to advin.io; never the reverse. Never on email, legal pages or proposals.
