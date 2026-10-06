"""Contract tests for scripts/refresh_themes.py.

The CLI runs as a subprocess against fixture project pages served over real
HTTP on localhost — no patched urllib, no network. Each fixture page is a
small copy of a shape a live project page actually ships.

Run: python3 -m unittest discover -s tests -v
"""

import http.server
import random
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "refresh_themes.py"

TOGGLE_CSS = """
:root { /* light is the default */ --paper: #e9e7e1; --ink: #15140f; }
:root[data-theme="dark"] { --paper: #141310; --ink: #eae7df; }
body { margin: 0; background: var(--paper); color: var(--ink); }
"""

# path under the served root -> content
PAGES = {
    # inline token + body background
    "plain/index.html": "<html><head><style>:root{--bg:#f6f7f8}"
    "body{background:var(--bg)}</style></head><body></body></html>",
    # perceptronics: a dark-scheme media block redefines the token later on
    "darkmedia/index.html": """<!DOCTYPE html><html lang="en"><head><style>
      :root { --bg: #f6f7f8; --ink: #14181d; }
      @media (prefers-color-scheme: dark) { :root { --bg: #101316; --ink: #e9edf0; } }
      body { color: var(--ink); background: var(--bg); }
    </style></head><body></body></html>""",
    # tensor-factory: a theme toggle the served markup has not switched on
    "toggle/index.html": '<!doctype html><html lang="en"><head>'
    '<link rel="stylesheet" href="style.css" /></head><body></body></html>',
    "toggle/style.css": TOGGLE_CSS,
    # the same stylesheet, served with the dark theme switched on
    "served-dark/index.html": '<!doctype html><html lang="en" data-theme="dark"><head>'
    '<link rel="stylesheet" href="style.css" /></head><body></body></html>',
    "served-dark/style.css": TOGGLE_CSS,
    # specodex: theme-color is the browser chrome, the page is in the stylesheet
    "chrome/index.html": '<!DOCTYPE html><html lang="en"><head>'
    '<meta name="theme-color" content="#3b4a2a" />'
    '<link rel="stylesheet" crossorigin href="/chrome/assets/app.css">'
    '</head><body><div id="root"></div></body></html>',
    "chrome/assets/app.css": ":root[data-theme=light]{--bg-primary:#e8e2c9}"
    ":root[data-theme=dark],:root{--bg-primary:#251d14}"
    "body{font-family:monospace;background-color:var(--bg-primary)}"
    "@media (prefers-color-scheme:dark){:root{--bg-primary:#000}}",
    # nothing but a theme-color to go on
    "metaonly/index.html": '<html><head><meta content="#123456" name="theme-color">'
    "</head><body></body></html>",
    # uServer: href before rel
    "hreffirst/index.html": '<html><head><link href="./style.css" rel="stylesheet">'
    "</head><body></body></html>",
    "hreffirst/style.css": "body { background-color: #abcdef; }",
    # no background anywhere
    "nobg/index.html": "<html><head><style>p{color:red}</style></head><body></body></html>",
    # braces and a quote in strings and comments must not derail the scan
    "tricky/index.html": """<html><head><style>
      /* } body { background: #ff0000 } it's a comment */
      .x::before { content: "}"; }
      .y::after { content: '{ body { background: #00ff00 }'; }
      body { background: #0a0b0c url("img}.png") no-repeat !important; }
    </style></head><body></body></html>""",
    # not a page at all
    "garbage/index.html": b"\xff\xfe<style>body{{{background:\x00#zz;}}}}}<html <body '\"",
}

ROW = """  <div class="entry reveal" id="{id}"{extra} style="--pfont:'Oswald',sans-serif; --pbar:#A88A1C; --pbg:{pbg}; --pink:{pink}; --pacc:#7A1F1F; --tilt:-2.5deg;">
    <div>
      <div class="head">
        <a class="name" href="{url}">{id}</a>
        <a class="src" href="https://github.com/example/{id}" aria-label="{id} source on GitHub">src</a>
      </div>
      <p class="desc">A row.</p>
    </div>
    <div class="shard" aria-hidden="true" style="background:#E8E2C9; --dd:.0s;">shard</div>
  </div>
"""


def page(rows):
    return "<!DOCTYPE html>\n<html><body>\n<main>\n" + "\n".join(rows) + "</main>\n</body></html>\n"


def closed_port():
    """A port nothing listens on: bound, then released."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        self.server.hits.append(self.path)


def serve(directory):
    handler = lambda *a, **kw: Handler(*a, directory=directory, **kw)  # noqa: E731
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.hits = []
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


class RefreshThemes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        rng = random.Random(0)
        alphabet = ["{", "}", ":root", "body", "html", "--bg", ":", ";", "#fff", "var(", ")",
                    "@media", "(prefers-color-scheme: dark)", '"', "'", "/*", "*/", "\\", "\n",
                    "background", "[data-theme=", "]", ",", " ", "\x00", "é", "url(", "!important"]
        cls.fuzz = [f"fuzz{i}" for i in range(25)]
        pages = dict(PAGES)
        for name in cls.fuzz:
            css = "".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 400)))
            pages[f"{name}/index.html"] = f"<html><head><style>{css}</style></head><body></body></html>"
        for rel, content in pages.items():
            f = root / "site" / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(content if isinstance(content, bytes) else content.encode())
        (root / "other").mkdir()
        (root / "other" / "style.css").write_text("body { background: #bada55; }")
        cls.server = serve(str(root / "site"))
        cls.other = serve(str(root / "other"))
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        for s in (cls.server, cls.other):
            s.shutdown()
            s.server_close()
        cls.tmp.cleanup()

    def setUp(self):
        self.server.hits.clear()
        self.other.hits.clear()
        self.index = Path(self.tmp.name) / f"{self.id().rsplit('.', 1)[-1]}.html"

    def row(self, site, pbg="#ffffff", pink="#111111", extra="", url=None):
        return ROW.format(id=site, pbg=pbg, pink=pink, extra=extra, url=url or f"{self.base}/{site}/")

    def run_cli(self, rows, *flags):
        """Write an index of `rows`, run the CLI on it, return (result, text before, text after)."""
        before = rows if isinstance(rows, str) else page(rows)
        self.index.write_text(before)
        r = subprocess.run([sys.executable, str(SCRIPT), *flags, str(self.index)],
                           capture_output=True, text=True, timeout=120)
        self.assertNotIn("Traceback", r.stderr, r.stdout + r.stderr)
        return r, before, self.index.read_text()

    def assert_synced_to(self, site, expected, **row):
        """A row curated as white ends up with exactly `expected`, and nothing else moves."""
        r, before, after = self.run_cli([self.row(site, **row)])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(after, before.replace("--pbg:#ffffff;", f"--pbg:{expected};"), r.stdout)

    # --- the rows are found -------------------------------------------------

    def test_row_with_id_between_class_and_style_is_synced(self):
        # the shape every row in index.html has had since the shard index
        self.assert_synced_to("plain", "#f6f7f8")

    def test_row_attribute_order_does_not_matter(self):
        row = self.row("plain").replace('class="entry reveal" id="plain"', 'id="plain" data-x="1"')
        row = row.replace(';">\n    <div>', ';" class="reveal entry">\n    <div>', 1)
        r, before, after = self.run_cli([row])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(after, before.replace("--pbg:#ffffff;", "--pbg:#f6f7f8;"), r.stdout)

    def test_no_rows_is_an_error_not_in_sync(self):
        r, before, after = self.run_cli("<html><body><main><p>no gallery</p></main></body></html>")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertNotIn("in sync", r.stdout)
        self.assertEqual(after, before)

    def test_row_without_a_name_link_is_an_error(self):
        broken = self.row("plain").replace('class="name"', 'class="title"')
        for flags in ((), ("--check",)):
            r, before, after = self.run_cli([self.row("darkmedia"), broken], *flags)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertEqual(after, before)

    def test_missing_index_is_an_error(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(self.index) + ".absent"],
                           capture_output=True, text=True, timeout=120)
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)

    # --- which background counts ---------------------------------------------

    def test_dark_scheme_media_block_is_not_the_default(self):
        self.assert_synced_to("darkmedia", "#f6f7f8")

    def test_theme_selector_the_markup_does_not_match_is_ignored(self):
        self.assert_synced_to("toggle", "#e9e7e1")

    def test_theme_selector_the_markup_matches_applies(self):
        self.assert_synced_to("served-dark", "#141310", pink="#eeeeee")

    def test_stylesheet_outranks_theme_color(self):
        self.assert_synced_to("chrome", "#251d14", pink="#eeeeee")

    def test_theme_color_is_the_last_resort(self):
        self.assert_synced_to("metaonly", "#123456", pink="#eeeeee")

    def test_stylesheet_link_with_href_before_rel(self):
        self.assert_synced_to("hreffirst", "#abcdef")

    def test_braces_and_quotes_in_strings_and_comments(self):
        self.assert_synced_to("tricky", "#0a0b0c", pink="#eeeeee")

    # --- what gets written ----------------------------------------------------

    def test_check_reports_drift_and_writes_nothing(self):
        r, before, after = self.run_cli([self.row("plain")], "--check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("#f6f7f8", r.stdout)
        self.assertEqual(after, before)

    def test_in_sync_row_is_left_alone_and_a_second_run_is_a_no_op(self):
        r, before, after = self.run_cli([self.row("plain"), self.row("toggle")])
        self.assertNotEqual(after, before)
        r2, before2, after2 = self.run_cli(after, "--check")
        self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)
        self.assertEqual(after2, after)

    def test_only_the_drifted_row_changes(self):
        rows = [self.row("plain", pbg="#f6f7f8"), self.row("toggle"), self.row("nobg", pbg="#010203")]
        r, before, after = self.run_cli(rows)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(after, before.replace("--pbg:#ffffff;", "--pbg:#e9e7e1;"))

    def test_unreadable_ink_is_nudged_and_readable_ink_is_kept(self):
        r, before, after = self.run_cli([self.row("served-dark", pink="#111111")])
        self.assertIn("--pbg:#141310; --pink:#f2f2f2;", after, r.stdout)
        r, before, after = self.run_cli([self.row("plain", pink="#333333")])
        self.assertIn("--pbg:#f6f7f8; --pink:#333333;", after, r.stdout)

    def test_pinned_row_is_neither_fetched_nor_changed(self):
        rows = [self.row("plain", extra=" data-pbg-pin"), self.row("toggle", pbg="#e9e7e1")]
        r, before, after = self.run_cli(rows, "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(after, before)
        self.assertFalse([h for h in self.server.hits if "/plain/" in h], self.server.hits)
        self.assertTrue([h for h in self.server.hits if "/toggle/" in h], self.server.hits)

    # --- pages that give nothing, or lie ---------------------------------------

    def test_pages_without_an_answer_keep_the_curated_value(self):
        dead = f"http://127.0.0.1:{closed_port()}/"
        rows = [self.row("nobg"), self.row("missing"), self.row("garbage"), self.row("dead", url=dead),
                self.row("repo", url="https://github.com/example/repo")]
        for flags in ((), ("--check",)):
            r, before, after = self.run_cli(rows, *flags)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(after, before)

    def test_stylesheet_on_another_origin_is_never_fetched(self):
        other = f"http://127.0.0.1:{self.other.server_address[1]}/style.css"
        site = Path(self.tmp.name) / "site" / "offorigin"
        site.mkdir(exist_ok=True)
        (site / "index.html").write_text(
            f'<html><head><link rel="stylesheet" href="{other}">'
            f'<link rel="stylesheet" href="//127.0.0.1:{self.other.server_address[1]}/style.css">'
            "</head><body></body></html>")
        r, before, after = self.run_cli([self.row("offorigin")])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(after, before)
        self.assertEqual(self.other.hits, [])

    def test_hostile_css_never_crashes_or_writes_a_non_colour(self):
        r, before, after = self.run_cli([self.row(name) for name in self.fuzz])
        self.assertIn(r.returncode, (0, 1), r.stdout + r.stderr)
        for line in after.splitlines():
            if 'class="entry' in line:
                self.assertRegex(line, r"--pbg:#[0-9a-f]{6}; --pink:#[0-9a-f]{6}; --pacc:#7A1F1F;")
        self.assertEqual(after.count("\n"), before.count("\n"))


if __name__ == "__main__":
    unittest.main()
