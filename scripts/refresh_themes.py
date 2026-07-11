#!/usr/bin/env python3
"""Keep each showcase entry's --pbg in sync with its project page.

For every `.entry` in index.html, fetch the page its name links to and
extract the page's default background color (inline `--bg` custom property,
`body { background }`, `<meta name="theme-color">`, or a one-hop same-origin
stylesheet — in that order). Rewrite the entry's `--pbg` when it drifts, and
nudge `--pink` only when the new background would make the current ink
unreadable (contrast < 3:1). Fonts, bars, and accents stay hand-curated.

Stdlib only. Usage: refresh_themes.py [--check] [path/to/index.html]
  --check  report drift, exit 1 if any, write nothing
"""

import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

UA = {"User-Agent": "advin-theme-refresh/1.0 (+https://advin.io)"}
TIMEOUT = 15

NAMED = {
    "white": "#ffffff", "black": "#000000", "ivory": "#fffff0",
    "snow": "#fffafa", "whitesmoke": "#f5f5f5", "transparent": None,
}


def fetch(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read(512_000).decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 — report-and-continue per page
        print(f"    fetch failed: {exc}")
        return None


def normalize(color: str) -> str | None:
    color = color.strip().strip(";").strip()
    if color.lower() in NAMED:
        return NAMED[color.lower()]
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", color)
    if m:
        return "#" + "".join(c * 2 for c in m.group(1)).lower()
    if re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        return color.lower()
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)[^)]*\)", color)
    if m:
        r, g, b = (min(255, int(v)) for v in m.groups())
        return f"#{r:02x}{g:02x}{b:02x}"
    return None  # gradients, var() refs, oklch, etc. — leave curation alone


def custom_props(css: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;}]+)", css)}


def resolve(value: str, props: dict[str, str], depth: int = 3) -> str | None:
    """Normalize a CSS color value, following var(--x[, fallback]) references."""
    value = value.strip()
    m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)", value)
    if m:
        if depth == 0:
            return None
        target = props.get(m.group(1)) or m.group(2)
        return resolve(target, props, depth - 1) if target else None
    return normalize(value)


def bg_from_css(css: str) -> str | None:
    props = custom_props(css)
    # :root --bg token first — the page's own declared background token
    for name in ("--bg", "--background"):
        if name in props and (c := resolve(props[name], props)):
            return c
    # body/html { ... background(-color): X } with var() resolution
    for sel in ("body", "html"):
        for block in re.finditer(r"(?:^|[}\s])" + sel + r"\s*(?:,[^{]*)?\{([^}]*)\}", css):
            m = re.search(r"background(?:-color)?\s*:\s*([^;}]+)", block.group(1))
            if m and (c := resolve(m.group(1).split()[0], props)):
                return c
    return None


def page_background(url: str) -> str | None:
    html = fetch(url)
    if html is None:
        return None
    for style in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S | re.I):
        if c := bg_from_css(style.group(1)):
            return c
    m = re.search(r'<meta[^>]+name=["\']theme-color["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m and (c := normalize(m.group(1))):
        return c
    # one hop into same-origin stylesheets
    origin = urlparse(url).netloc
    for link in re.finditer(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', html, re.I):
        href = urljoin(url, link.group(1))
        if urlparse(href).netloc != origin:
            continue
        css = fetch(href)
        if css and (c := bg_from_css(css)):
            return c
    return None


def luminance(hexcolor: str) -> float:
    r, g, b = (int(hexcolor[i : i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main() -> int:
    check_only = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = Path(args[0]) if args else Path(__file__).resolve().parent.parent / "index.html"
    html = path.read_text()

    entry_re = re.compile(
        r'(<div class="entry[^"]*" style=")([^"]*)("[^>]*>.*?<a class="name" href="([^"]+)")',
        re.S,
    )
    drift = 0
    out = []
    last = 0
    for m in entry_re.finditer(html):
        out.append(html[last : m.start()])
        last = m.end()
        style, url = m.group(2), m.group(4)
        name = re.sub(r"https?://(www\.)?", "", url).rstrip("/")
        print(f"  {name}")

        if "github.com" in urlparse(url).netloc:
            print("    repo link, not a themed page — skipped")
            out.append(m.group(0))
            continue

        live = page_background(url)
        if live is None:
            print("    no extractable background — kept curated value")
            out.append(m.group(0))
            continue

        cur = re.search(r"--pbg:\s*([^;]+);?", style)
        cur_bg = normalize(cur.group(1)) if cur else None
        if cur_bg == live:
            print(f"    in sync ({live})")
            out.append(m.group(0))
            continue

        drift += 1
        print(f"    drift: --pbg {cur_bg or 'unset'} -> {live}")
        new_style = (
            re.sub(r"--pbg:\s*[^;]+;?", f"--pbg:{live};", style)
            if cur
            else style.rstrip("; ") + f"; --pbg:{live};"
        )
        ink = re.search(r"--pink:\s*([^;]+);?", new_style)
        ink_hex = normalize(ink.group(1)) if ink else None
        if ink_hex and contrast(ink_hex, live) < 3.0:
            fixed = "#1a1a1a" if luminance(live) > 0.5 else "#f2f2f2"
            print(f"    ink unreadable on new bg -> --pink {fixed}")
            new_style = re.sub(r"--pink:\s*[^;]+;?", f"--pink:{fixed};", new_style)
        out.append(m.group(1) + new_style + m.group(3))

    out.append(html[last:])
    if drift and not check_only:
        path.write_text("".join(out))
        print(f"\nupdated {drift} entr{'y' if drift == 1 else 'ies'} in {path}")
    elif drift:
        print(f"\n{drift} entr{'y' if drift == 1 else 'ies'} drifted (check mode, nothing written)")
        return 1
    else:
        print("\nall themes in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
