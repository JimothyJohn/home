# home

The static home page of [advin.io](https://advin.io) — a project gallery
for the lab. Each entry links to the project's site (GitHub Pages or custom
domain) and its source repo, styled with that project's own fonts and
colors. Entries are ordered by commit count as a baseline (not shown on the
page), with hand-placed overrides; the list is curated — uplink,
uptime-visuals, and big-canyon-band-page are deliberately excluded. Visual
identity lives in [BRANDING.md](BRANDING.md).

Plain HTML/CSS, no build step. `Deploy advin.io` publishes `master` to AWS
(S3 + CloudFront behind https://advin.io, stack `advin-home` in us-east-1);
work lands via PRs into `dev`, and `dev → master` is a manual merge. CI/CD
identity is the `advin-home-github-oidc` stack (`deploy/github-oidc.yaml`),
scoped to this repo's master branch. Per-repo GitHub Pages remain the
project-overview layer; this domain is served from AWS.

Regenerating the ranking: commit counts come from the GitHub API
(`/repos/<owner>/<repo>/commits?per_page=1`, last-page number of the `Link`
header) — update `index.html` when the order shifts.

Commit count is the baseline, not a law. An entry whose `.entry` div
carries `data-pin` was placed by hand and keeps its position; re-rank only
the unpinned entries around it, and never add or drop a pin without the
owner asking. The hero's shard index follows the gallery order.

Row backgrounds (`--pbg`) are synced weekly from each project's live page
by `scripts/refresh_themes.py` — the background a first-time visitor on a
light-scheme device gets, as far as the served HTML and CSS say. An entry
carrying `data-pbg-pin` keeps its hand-picked background instead. Two are
pinned: Specodex to its light theme, because its script opens first-time
visitors in dark; and AMR Emulator to the MiR brand palette of its MiR
console (`/console`) — blue, the owner's choice — though its title links to
the site's home page. Tests: `python3 -m unittest discover -s tests -v`.
