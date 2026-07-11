# home

The static home page of [advin.io](https://advin.io) — a project gallery
for the lab. Each entry links to the project's site (GitHub Pages or custom
domain) and its source repo, styled with that project's own fonts and
colors. Entries are ordered by commit count (not shown on the page); the
list is curated — uplink, uptime-visuals, and big-canyon-band-page are
deliberately excluded. Visual identity lives in [BRANDING.md](BRANDING.md).

Plain HTML/CSS, no build step. `Deploy Pages` publishes `master` to GitHub
Pages; work lands via PRs into `dev`, and `dev → master` is a manual merge.

Regenerating the ranking: commit counts come from the GitHub API
(`/repos/<owner>/<repo>/commits?per_page=1`, last-page number of the `Link`
header) — update `index.html` when the order shifts.
