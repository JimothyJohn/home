# advin.io — Branding Guide

The brand for **advin.io** and anything published under it. These are the
owner's choices, not derived conventions — when a project page and this file
disagree, this file wins. The live site (`index.html`) is the reference
implementation.

## Identity

**Advin** is an independent engineering workshop. The brand is deliberately
plain: near-pure white, near-pure black, one rounded typeface. No gradients,
no icon set, no mascot.

The wordmark is lowercase **advin.** set in Comfortaa Bold, matching the
domain. The trailing full stop is part of the mark.

## Color

Monochrome by decree. Two anchors, with grays mixed from them as needed.

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#fcfcfc` | Background — near-pure white |
| `--ink` | `#0d0d0d` | Text, rules, accents — near-pure black |
| `--paper2` | `#f4f4f4` | Hover / raised surfaces |
| `--ink-soft` | `#3d3d3d` | Secondary text |
| `--faint` | `#8a8a8a` | Tertiary text, numerals |
| `--rule` | `#e4e4e4` | Hairline rules, borders |

Rules of use:

- **No hues.** Emphasis comes from weight, size, and spacing — never color.
  Status ("live") is bold ink, not green.
- Never pure `#ffffff` on `#000000`; the near-pure pair is the brand.
- Selection inverts: ink background, paper text.
- Interactive affordances are structural (underline, background shift,
  motion), not color changes.

## Typography

One typeface: **[Comfortaa](https://fonts.google.com/specimen/Comfortaa)**
(Google Fonts, variable 300–700). No secondary face, no mono fallback for
metadata — Comfortaa everywhere.

| Use | Weight | Treatment |
|---|---|---|
| Wordmark / hero | 700 | lowercase, tight (-0.02em), line-height ~1 |
| Headings / project names | 700 | lowercase |
| Body | 400 | sentence case, line-height ~1.55 |
| Labels / metadata | 400–500 | uppercase, letterspaced (0.06em+), small |

- Display type is **lowercase** — Comfortaa's rounded forms are the brand's
  personality; uppercase display headlines fight it.
- Small labels may be uppercase for legibility at size.

## Layout motifs

- **The ledger.** Content is a ranked list: `№` numeral column, name,
  description, spec column. Rows separated by hairline `--rule`; sections
  opened and closed by heavy 3px `--ink` rules.
- **Ranked by commits.** The ordering metric is commit count — the only
  metric that doesn't flatter. Never reorder by vanity metrics.
- **Flat surfaces.** No shadows, no grain, no texture. Depth is expressed
  with rules and the two background tones.

## Voice

- Plain, declarative, a little dry. No marketing copy, no exclamation
  points.
- Numbers over adjectives: say *629 commits*, not *battle-tested*.
- Projects are described by what they do, in one or two sentences.

## Links

- Every showcased project links to its **GitHub Pages site**
  (`jimothyjohn.github.io/<repo>/` or its custom domain) so visitors land on
  docs or a live demo, not a bare file tree. A repo without a Pages site
  links to its GitHub source until it earns one.
- Correspondence goes to `nick@advin.io`.

## Assets & implementation

- One static `index.html`, no build step, CSS variables as listed above.
- Comfortaa loads from Google Fonts with `preconnect`.
- Anything new (an error page, a project card, an email footer) starts from
  the tokens in this file.
