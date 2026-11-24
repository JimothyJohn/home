# advin.io — Branding Guide

The brand for **advin.io** and anything published under it. These are the
owner's choices, not derived conventions — when a project page and this file
disagree, this file wins. The live site (`index.html`) is the reference
implementation.

## Identity

**advin.io** is an AI research lab in **Dallas, TX** — handcrafted,
exclusive, small on purpose. The legal entity is **advin.io LLC**. The location is part of the story: a
cutting-edge lab in a metroplex with few if any others. State it plainly
(hero, footer, bios); never bury it. The brand is deliberately plain:
near-pure white, near-pure black, one rounded typeface. No gradients, no
icon set, no mascot.

The name is **advin.io**, written exactly that way — **always lowercase,
always with the `.io`** — in headings, body copy, the wordmark, everywhere.
Never "Advin", never "ADVIN.IO".

The wordmark is the name set in Comfortaa Bold. Outlined SVGs live in
`brand/`.

**Two faces.** advin.io is the business and lives in **light mode**.
**ADVINIO** — always uppercase, no dot, set in **Comfortaa Light** — is the
creative outlet, the hidden Easter egg beneath the technology, and lives in
**dark mode**. A visitor whose device is dark lands in ADVINIO; one whose
device turns dark while the page is open watches advin.io fade into it (the
dimension shift). ADVINIO is never announced or linked from business
surfaces; legal pages, email and documents are always advin.io light.

**The mark** is a capital **A** in Comfortaa Light — ADVINIO's letter on
loan to the business. Anything circular or square-cropped (favicon,
avatars, social profiles) uses the A. The lowercase "a" exists only inside
the name advin.io. (A small eye logo from earlier projects is parked as a
possible future idea.)

## Color

Monochrome by decree. Two anchors, with grays mixed from them as needed.

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#fcfcfc` | Background — near-pure white |
| `--ink` | `#0d0d0d` | Text, rules, accents — near-pure black |
| `--paper2` | `#f4f4f4` | Hover / raised surfaces |
| `--ink-soft` | `#3d3d3d` | Secondary text |
| `--faint` | `#8a8a8a` | Icons and marks only (3.36:1 fails for text) |
| `--faint-text` | `#6b6b6b` | Tertiary text — colophon, meta (5.19:1) |
| `--rule` | `#e4e4e4` | Hairline rules, borders |

Rules of use:

- **No hues** in the frame — emphasis comes from weight, size, spacing and
  depth. Subtle background gradients within the near-pure range are welcome.
- ADVINIO mirrors the palette: `paper` `#0d0d0d`, `paper2` `#181818`, `ink`
  `#fcfcfc`, `ink-soft` `#c2c2c2`, `faint-text` `#8a8a8a`, `faint` `#6b6b6b`,
  `rule` `#262626`.
- Never pure `#ffffff` on `#000000`; the near-pure pair is the brand.
- Selection inverts: ink background, paper text.
- **The one exception: project gallery entries.** Each showcased project may
  carry its own site's fonts and colors (accent bar, title face, hover
  surface) so the entry previews the thing it links to. The project's
  palette stays inside its entry; the page frame stays monochrome.

## Typography

One typeface for the frame:
**[Comfortaa](https://fonts.google.com/specimen/Comfortaa)** (Google Fonts,
variable 300–700).

| Use | Weight | Treatment |
|---|---|---|
| Wordmark / hero | 700 | lowercase, tight (-0.02em) |
| Body | 400 | sentence case, line-height ~1.55 |
| Labels / buttons | 600–700 | lowercase, small |

- Display type is **lowercase** — Comfortaa's rounded forms are the brand's
  personality.
- Gallery entry titles are the exception: they render in their project's
  own display face (see Color, above).

## Layout motifs

- **The gallery.** Projects are rows: title with a source link beside it,
  one- or two-sentence description, nothing else. No rank numbers, no
  column headers, no language/commit/date metadata.
- **Accent bars.** Each entry carries a thin left bar in its project's
  accent color.
- **Project surfaces.** Each row wears its project's own live page
  background at rest — the gallery is a quilt of the projects' actual
  surfaces. `scripts/refresh_themes.py` re-scrapes every page weekly (the
  `Theme refresh` workflow) and PRs any drift, so the quilt never goes
  stale.
- **Soul shards.** Each entry casts one small fragment of its project's
  world into the row's white space — a spec row, an API response, a fleet
  status, a stamp — set in the project's own type and palette, tilted,
  straightening on hover. One shard per project, never
  more; the shard is evidence, not decoration. The hero carries a
  shard index, one tick per gallery entry in its project's accent, linking
  down the page (a tick that vanishes on the dark ground carries a `--cd`
  from its project's own palette).
- **Motion is quiet and mostly interactive.** If the visitor isn't moving
  the page, the page doesn't move: no idle loops or drift. A single
  staggered rise on load, scroll reveals on rows, hover responses, and the
  dimension shift — all disabled under `prefers-reduced-motion`.
- **Heavy rules.** Sections open with a 3px ink rule; entries separate with
  hairlines.
- **Depth, not decoration.** Shadows are welcome when they render smooth:
  two layers (tight contact + wide ambient), low alpha, ink-tinted, blur
  ≤ 56px; in ADVINIO add a 1px top rim. Never transition `box-shadow` —
  fade a pseudo-element that carries it. No grain or texture.

## Voice

- Plain, declarative, a little dry. Handcrafted and exclusive — never
  salesy. No exclamation points, no emoji. Dry, not cute.
- Adjectives are fine when data backs them up. Purpose lines stay general
  and memorable; datasheets and specs carry the specific numbers.
- Projects are described by what they do, in one or two sentences.
- Simple words over marketing words. Emails sign off with "Thanks,".

## Links

- Every gallery entry links **twice**: the title to the project's site
  (GitHub Pages or its custom domain), and a GitHub mark beside the title
  to the source repository. A project without a site links its title to
  the source until it earns one.
- Deployed models live on
  [replicate.com/jimothyjohn](https://replicate.com/jimothyjohn) — linked
  from the hero.
- Contact is a single pill button, top right, opening mail to
  `nick@advin.io`. No other contact affordances.
- The footer is one centered line: `© 2026 advin.io LLC · Dallas, TX` and
  the privacy and terms links (ADVINIO: `© 2026 ADVINIO · an advin.io LLC
  endeavor`).
- Projects incubate on advin.io subdomains; one that graduates gets its own
  domain, like an Apache or Eclipse incubator. Documentation, privacy and
  data policies live on advin.io and are shared across projects.

## Assets & implementation

- One static `index.html`, no build step, CSS variables as listed above.
- Fonts load from Google Fonts with `preconnect`; project-entry faces load
  only the weights the entries use.
- Anything new (an error page, a project card, an email footer) starts from
  the tokens in this file. The full brand book — voice, email, social,
  imagery, ADVINIO, live previews — is the advin.io design system:
  https://claude.ai/artifact/J8czVPWQFHVLdtgi2kkTPR
- `brand/` holds the outlined wordmarks (advin.io, ADVINIO), the A mark,
  avatars and the email wordmark; the root holds the favicons and `og.png`.
