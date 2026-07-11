# home

The static home page of [advin.io](https://advin.io) — a showcase of the
most-developed projects on github.com/JimothyJohn, ranked by commit count.
The list is curated: uplink, uptime-visuals, and big-canyon-band-page are
deliberately excluded. Visual identity lives in [BRANDING.md](BRANDING.md).

Plain HTML/CSS, no build step. `Deploy advin.io` publishes `master` to AWS
(S3 + CloudFront behind https://advin.io, stack `advin-home` in us-east-1);
work lands via PRs into `dev`, and `dev → master` is a manual merge. CI/CD
identity is the `advin-home-github-oidc` stack (`deploy/github-oidc.yaml`),
scoped to this repo's master branch. Per-repo GitHub Pages remain the
project-overview layer; this domain is served from AWS.

Regenerating the ranking: commit counts come from the GitHub API
(`/repos/<owner>/<repo>/commits?per_page=1`, last-page number of the `Link`
header) — update `index.html` when the order shifts.
