#!/usr/bin/env python3
"""Keep each showcase entry's --pbg in sync with its project page.

For every `.entry` in index.html, fetch the page its name links to and work
out the background a first-time visitor on a light-scheme device sees: the
page's inline styles and same-origin stylesheets, cascaded over `:root` /
`html` / `body` as served. Preference and print media blocks
(`prefers-color-scheme: dark`) and theme selectors the served markup doesn't
match (`:root[data-theme="dark"]`) are not the default and are skipped.
`body { background }` wins, then `html` / `:root`, then a `--bg` /
`--background` token, and `<meta name="theme-color">` only as a last resort —
it colours the browser chrome, which is often not the page.

Rewrite the entry's `--pbg` when it drifts, and nudge `--pink` only when the
new background would make the current ink unreadable (contrast < 3:1). Fonts,
bars, and accents stay hand-curated. An entry carrying `data-pbg-pin` keeps
its curated background and is not fetched — for pages whose theme is chosen
by script at runtime, which a static scrape cannot see.

Stdlib only. Usage: refresh_themes.py [--check] [path/to/index.html]
  --check  report drift, exit 1 if any, write nothing
Exits 2 when index.html has no entries, or an entry it cannot read — never a
quiet "all in sync" over nothing.
"""

import html.parser
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

UA = {
    "User-Agent": "advin-theme-refresh/1.0 (+https://advin.io)",
    # ask the way a browser does: amr-emulator.com answers anything else with its API index
    "Accept": "text/html,text/css;q=0.9,*/*;q=0.8",
}
TIMEOUT = 15
MAX_SHEETS = 8

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


def resolve(value: str, props: dict[str, str], depth: int = 8) -> str | None:
    """Normalize a CSS color value, following var(--x[, fallback]) references."""
    value = value.strip()
    m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,(.+))?\)", value, re.DOTALL)
    if m:
        if depth == 0:
            return None
        target = props.get(m.group(1)) or m.group(2)
        return resolve(target, props, depth - 1) if target else None
    return normalize(value)


def first_color(value: str, props: dict[str, str]) -> str | None:
    """The color in a `background` value: the whole value, else its first color token."""
    if c := resolve(value, props):
        return c
    token, depth = "", 0
    for ch in value + " ":
        if ch.isspace() and depth == 0:
            if token and (c := resolve(token, props)):
                return c
            token = ""
            continue
        depth += (ch == "(") - (ch == ")" and depth > 0)
        token += ch
    return None


def blocks(css: str):
    """Yield (prelude, body) for each top-level `prelude { body }`, minding quotes and nesting."""
    depth, start, opened, quote = 0, 0, 0, None
    i, n = 0, len(css)
    while i < n:
        ch = css[i]
        if quote:
            if ch == "\\":
                i += 1
            elif ch == quote or ch == "\n":
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "{":
            if depth == 0:
                opened = i
            depth += 1
        elif ch == "}":
            if depth:
                depth -= 1
                if depth == 0:
                    yield css[start:opened], css[opened + 1 : i]
            if depth == 0:
                start = i + 1
        i += 1


CONDITION = r"\[[^\]]*\]|:not\(\s*\[[^\]]*\]\s*\)|\.[\w-]+"
ROOT_SELECTOR = re.compile(rf"(:root|html|body)((?:{CONDITION})*)", re.IGNORECASE)
ATTR_TEST = re.compile(r"""\[\s*([\w-]+)\s*(?:=\s*(["']?)([^"'\]]*)\2\s*)?\]""")


def target(selector: str, root: dict[str, str], body: dict[str, str]) -> tuple[str, int] | None:
    """("root" | "body", specificity) when the selector matches that element as served."""
    m = ROOT_SELECTOR.fullmatch(selector.strip())
    if not m:
        return None  # descendants, pseudo-elements, anything not the page itself
    which = "body" if m.group(1).lower() == "body" else "root"
    attrs = body if which == "body" else root
    conditions = re.findall(CONDITION, m.group(2))
    for cond in conditions:
        if cond.startswith("."):
            hit = cond[1:] in attrs.get("class", "").split()
        else:
            test = ATTR_TEST.search(cond)
            if not test:
                return None  # ^=, ~= and friends: not worth guessing at
            name, has_value, want = test.group(1).lower(), "=" in test.group(0), test.group(3)
            hit = name in attrs and (not has_value or attrs[name] == want)
        if hit == cond.startswith(":not"):
            return None
    return which, len(conditions)


def cascade(css: str, root: dict[str, str], body: dict[str, str]) -> dict[str, dict[str, str]]:
    """The declarations that land on the served root and body, last-declared last."""
    out = {"root": {}, "body": {}}
    rank = {"root": {}, "body": {}}

    def walk(text: str) -> None:
        for prelude, block in blocks(text):
            prelude = prelude.rsplit(";", 1)[-1].strip()  # shed @import / @charset statements
            if prelude.startswith("@"):
                at = prelude.lower()
                if at.startswith("@media"):
                    if "prefers-" not in at and "print" not in at:
                        walk(block)
                elif at.startswith(("@supports", "@layer")):
                    walk(block)
                continue
            for selector in prelude.split(","):
                hit = target(selector, root, body)
                if not hit:
                    continue
                which, spec = hit
                for decl in block.split(";"):
                    name, sep, value = decl.partition(":")
                    name = name.strip() if name.strip().startswith("--") else name.strip().lower()
                    value = re.sub(r"\s*!important\s*$", "", value.strip(), flags=re.IGNORECASE)
                    if not sep or not value or spec < rank[which].get(name, 0):
                        continue
                    out[which].pop(name, None)  # re-insert: a later declaration sorts last
                    out[which][name] = value
                    rank[which][name] = spec

    walk(re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL))
    return out


def bg_from_css(css: str, root: dict | None = None, body: dict | None = None) -> str | None:
    decls = cascade(css, root or {}, body or {})
    props = {k: v for which in ("root", "body") for k, v in decls[which].items() if k.startswith("--")}
    for which in ("body", "root"):
        for name, value in reversed(decls[which].items()):
            if name in ("background", "background-color") and (c := first_color(value, props)):
                return c
    for name in ("--bg", "--background"):
        if name in props and (c := resolve(props[name], props)):
            return c
    return None


class Page(html.parser.HTMLParser):
    """The parts of a served page that decide its background."""

    def __init__(self) -> None:
        super().__init__()
        self.root: dict[str, str] = {}
        self.body: dict[str, str] = {}
        self.css: list[tuple[str, str]] = []  # ("inline", text) | ("link", href), in document order
        self.theme_color: str | None = None
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.root = self.root or a
        elif tag == "body":
            self.body = self.body or a
        elif tag == "style":
            self._in_style = True
            self.css.append(("inline", ""))
        elif tag == "link" and "stylesheet" in a.get("rel", "").lower().split() and a.get("href"):
            self.css.append(("link", a["href"]))
        elif tag == "meta" and a.get("name", "").lower() == "theme-color" and self.theme_color is None:
            self.theme_color = a.get("content", "")

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.css[-1] = ("inline", self.css[-1][1] + data)


def page_background(url: str) -> str | None:
    text = fetch(url)
    if text is None:
        return None
    page = Page()
    page.feed(text)
    page.close()
    origin = urlparse(url).netloc
    sheets, linked = [], 0
    for kind, value in page.css:
        if kind == "inline":
            sheets.append(value)
            continue
        href = urljoin(url, value)
        if urlparse(href).netloc != origin or linked == MAX_SHEETS:
            continue  # same-origin only, one hop, bounded
        linked += 1
        if css := fetch(href):
            sheets.append(css)
    if c := bg_from_css("\n".join(sheets), page.root, page.body):
        return c
    return normalize(page.theme_color) if page.theme_color else None


def luminance(hexcolor: str) -> float:
    r, g, b = (int(hexcolor[i : i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


OPEN_TAG = re.compile(r"<(div|a)\b[^>]*>", re.IGNORECASE)
TAG_ATTR = re.compile(r"""([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+)))?""")
STYLE_ATTR = re.compile(r"""((?<![\w-])style\s*=\s*)(["'])(.*?)\2""", re.DOTALL | re.IGNORECASE)


def tag_attrs(tag: str) -> dict[str, str]:
    inner = re.sub(r"^<\s*[\w-]+|/?>$", "", tag)
    return {
        m.group(1).lower(): next((g for g in m.groups()[1:] if g is not None), "")
        for m in TAG_ATTR.finditer(inner)
    }


def entries(text: str) -> list[dict]:
    """Each `.entry` opening tag — whatever order its attributes come in — and its name link."""
    found = []
    for m in OPEN_TAG.finditer(text):
        attrs = tag_attrs(m.group(0))
        classes = attrs.get("class", "").split()
        if m.group(1).lower() == "div" and "entry" in classes:
            found.append({"start": m.start(), "end": m.end(), "attrs": attrs, "url": None})
        elif m.group(1).lower() == "a" and "name" in classes and found and found[-1]["url"] is None:
            found[-1]["url"] = attrs.get("href") or None
    return found


def restyle(tag: str, style: str, live: str) -> str:
    """The entry's opening tag with --pbg set to `live`, and --pink fixed if it stopped being readable."""
    if re.search(r"--pbg:\s*[^;]+;?", style):
        new_style = re.sub(r"--pbg:\s*[^;]+;?", f"--pbg:{live};", style)
    else:
        new_style = style.rstrip("; ") + f"; --pbg:{live};"
    ink = re.search(r"--pink:\s*([^;]+);?", new_style)
    ink_hex = normalize(ink.group(1)) if ink else None
    if ink_hex and contrast(ink_hex, live) < 3.0:
        fixed = "#1a1a1a" if luminance(live) > 0.5 else "#f2f2f2"
        print(f"    ink unreadable on new bg -> --pink {fixed}")
        new_style = re.sub(r"--pink:\s*[^;]+;?", f"--pink:{fixed};", new_style)
    if STYLE_ATTR.search(tag):
        return STYLE_ATTR.sub(lambda m: m.group(1) + m.group(2) + new_style + m.group(2), tag, count=1)
    return tag[:-1].rstrip() + f' style="{new_style.lstrip("; ")}">'


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    check_only = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]
    path = Path(args[0]) if args else Path(__file__).resolve().parent.parent / "index.html"
    text = path.read_text()

    found = entries(text)
    if not found:
        print(f"error: no .entry rows found in {path} — nothing was checked")
        return 2
    nameless = [e["attrs"].get("id", "?") for e in found if not e["url"]]
    if nameless:
        print(f"error: no .name link in entr{'y' if len(nameless) == 1 else 'ies'}: {', '.join(nameless)}")
        return 2

    drift = 0
    out = []
    last = 0
    for e in found:
        tag, url = text[e["start"] : e["end"]], e["url"]
        print(f"  {re.sub(r'https?://(www[.])?', '', url).rstrip('/')}")

        if "data-pbg-pin" in e["attrs"]:
            print("    pinned (data-pbg-pin) — kept curated value")
            continue
        if "github.com" in urlparse(url).netloc:
            print("    repo link, not a themed page — skipped")
            continue

        live = page_background(url)
        if live is None:
            print("    no extractable background — kept curated value")
            continue

        style_attr = STYLE_ATTR.search(tag)
        style = style_attr.group(3) if style_attr else ""
        cur = re.search(r"--pbg:\s*([^;]+);?", style)
        cur_bg = normalize(cur.group(1)) if cur else None
        if cur_bg == live:
            print(f"    in sync ({live})")
            continue

        drift += 1
        print(f"    drift: --pbg {cur_bg or 'unset'} -> {live}")
        out.append(text[last : e["start"]])
        out.append(restyle(tag, style, live))
        last = e["end"]

    out.append(text[last:])
    if drift and not check_only:
        path.write_text("".join(out))
        print(f"\nupdated {drift} entr{'y' if drift == 1 else 'ies'} in {path}")
    elif drift:
        print(f"\n{drift} entr{'y' if drift == 1 else 'ies'} drifted (check mode, nothing written)")
        return 1
    else:
        print(f"\nall themes in sync ({len(found)} entries read)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
