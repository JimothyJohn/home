# Advin — Branding Guide

The visual and verbal identity of [advin.io](https://advin.io) and, by
extension, the public face of the workshop's projects. When in doubt, the
live site (`index.html`) is the reference implementation.

## Identity

**Advin** is an independent engineering workshop, and the brand should read
like one: a printed ledger of working projects, not a startup landing page.
The aesthetic is *letterpress field-notes* — warm paper, hard black rules,
one vermillion accent used like a press stamp.

The wordmark is the word **Advin** set in the display face, ending in a
vermillion full stop: **Advin<span style="color:#b3382c">.</span>** The dot
is the logo. No icon, no gradient, no mascot.

## Color

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#f4efe6` | Page background — warm paper |
| `--paper2` | `#ece5d8` | Hover / raised paper |
| `--ink` | `#1c1a16` | Primary text, hard rules |
| `--ink-soft` | `#57524a` | Secondary text |
| `--faint` | `#8d867a` | Tertiary text, numerals |
| `--rule` | `#d8cfbf` | Hairline rules, borders |
| `--mark` | `#b3382c` | Vermillion accent — the press stamp |

Rules of use:

- Vermillion (`--mark`) is **scarce by design**: link hovers, the wordmark
  dot, "live" status, the stamp. If more than ~5% of a view is vermillion,
  it stops being a stamp.
- No other hues. No blues, no greens, no gradients. Status is conveyed with
  vermillion (live) and ink-weight, not a traffic-light palette.
- Text sits on paper, never on vermillion, except selection
  (`::selection` inverts to vermillion/paper).

## Typography

Fonts are the ones the workshop's GitHub Pages sites already use — the home
page inherits from the projects, not the other way around.

| Face | Source | Role |
|---|---|---|
| **Oswald** (500/600/700) | Google Fonts | Display: wordmark, hero, project names. Uppercase, tight leading (~0.9–1.05), slight positive tracking. |
| **IBM Plex Mono** (400/500/600) | Google Fonts | Everything else: body, descriptions, metadata, masthead, colophon. |

Conventions:

- Display type is **UPPERCASE Oswald**; never bold mono as a substitute
  headline.
- Metadata (language · commits · year) is small mono, uppercase, letterspaced
  (`0.06em`+), in `--faint`/`--ink-soft`.
- No third typeface. Ever.

## Layout motifs

- **The ledger.** Content is a ranked list: `№` numeral column, name,
  description, spec column on the right. Rows separated by hairline
  `--rule`, sections opened by a heavy 3px `--ink` rule.
- **Ranked by commits.** The ordering metric is commit count — "the only
  metric that doesn't flatter." Never reorder by vanity metrics.
- **The stamp.** A rotated circular mono-type badge in vermillion, used at
  most once per page.
- **Paper grain.** A faint SVG turbulence texture over `--paper`; subtle
  enough to miss, gone entirely is too flat.

## Voice

- Plain, declarative, a little dry. "No marketing copy on the rows, no
  request-a-quote gates."
- Numbers over adjectives: say *629 commits*, not *battle-tested*.
- Projects are described by what they do, one or two sentences, no
  exclamation points.

## Links

- Every showcased project links to its **GitHub Pages site**
  (`jimothyjohn.github.io/<repo>/` or its custom domain) so visitors land on
  docs or a live demo, not a bare file tree. A repo without a Pages site
  links to its GitHub source until it earns one.
- Correspondence goes to `nick@advin.io`.

## Assets & implementation

- One static `index.html`, no build step, CSS variables as listed above.
- Fonts load from Google Fonts (`Oswald`, `IBM Plex Mono`) with
  `preconnect`.
- Anything new (an error page, a project card, an email footer) starts from
  the tokens in this file.
