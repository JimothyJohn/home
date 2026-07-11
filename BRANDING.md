# advin.io — Branding Guide

The brand for **advin.io** and anything published under it. These are the
owner's choices, not derived conventions — when a project page and this file
disagree, this file wins. The live site (`index.html`) is the reference
implementation.

## Identity

**advin.io** is a boutique AI research lab in **Dallas, TX** — handcrafted,
exclusive, small on purpose. The location is part of the story: a
cutting-edge lab in a metroplex with few if any others. State it plainly
(hero, footer, bios); never bury it. The brand is deliberately plain:
near-pure white, near-pure black, one rounded typeface. No gradients, no
icon set, no mascot.

The name is **advin.io**, written exactly that way — **always lowercase,
always with the `.io`** — in headings, body copy, the wordmark, everywhere.
Never "Advin", never "ADVIN.IO".

The wordmark is the name set in Comfortaa Bold.

## Color

Monochrome by decree. Two anchors, with grays mixed from them as needed.

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#fcfcfc` | Background — near-pure white |
| `--ink` | `#0d0d0d` | Text, rules, accents — near-pure black |
| `--paper2` | `#f4f4f4` | Hover / raised surfaces |
| `--ink-soft` | `#3d3d3d` | Secondary text |
| `--faint` | `#8a8a8a` | Tertiary text |
| `--rule` | `#e4e4e4` | Hairline rules, borders |

Rules of use:

- **No hues** in the frame — emphasis comes from weight, size, and spacing.
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
  status, a stamp — set in the project's own type and palette, tilted and
  gently adrift, straightening on hover. One shard per project, never
  more; the shard is evidence, not decoration. The hero carries a
  seven-tick shard index, one accent per project, linking down the page.
- **Motion is quiet.** A single staggered rise on load, scroll reveals on
  rows, the shards' slow drift — all disabled under
  `prefers-reduced-motion`. Nothing blinks, nothing loops loudly.
- **Heavy rules.** Sections open with a 3px ink rule; entries separate with
  hairlines.
- **Flat surfaces.** No shadows, no grain, no texture.

## Voice

- Plain, declarative, a little dry. Handcrafted and exclusive — never
  salesy. No exclamation points.
- Numbers over adjectives; projects are described by what they do, in one
  or two sentences.

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
- The footer is a single centered copyright line — nothing else.

## Assets & implementation

- One static `index.html`, no build step, CSS variables as listed above.
- Fonts load from Google Fonts with `preconnect`; project-entry faces load
  only the weights the entries use.
- Anything new (an error page, a project card, an email footer) starts from
  the tokens in this file.
