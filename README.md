# ptea08.github.io

Personal GitHub Pages site. One landing page per project, each in its own
subfolder, so the site root stays free for future projects.

| Path | Served at |
|---|---|
| `bw-watershed/` | <https://ptea08.github.io/bw-watershed/> |

The root itself has no `index.html`, so <https://ptea08.github.io> currently
returns a 404. That is deliberate — nothing links there. Add a root
`index.html` if you ever want a personal index.

## Files

| File | Purpose |
|---|---|
| `.nojekyll` | Site-wide. Skips Jekyll processing, so what Pages serves matches what you see locally. Must stay at the repo root. |
| `bw-watershed/index.html` | The whole page. One file, inline CSS, no JS, no build step. |
| `bw-watershed/pipeline.png` | The three-stage figure. Copied from the paper repo's `assets/pipeline_figure.png`; also the Open Graph preview image. |
| `bw-watershed/tools/make_chart.py` | Regenerates the results bar chart inside `index.html`. Not part of the site. |

Edit and push; Pages redeploys in a minute or two.

## Why a subfolder and not the site root

`ptea08.github.io` is the *user* site and there is only one per account. Putting
the page at the root would mean overwriting it to publish a second project — and
the conference poster's QR code points at
<https://ptea08.github.io/bw-watershed/>, which is printed and cannot be
changed. The subfolder makes that URL permanent.

Serving the page from the `bw-watershed` code repo's `docs/` folder would give
the same URL, but couples it to that repo staying public. Keeping it here does
not.

Two absolute URLs in `index.html` encode this path — `og:image` and `og:url`.
Moving the folder means updating both.

## Previewing before you push

Open `bw-watershed/index.html` directly in a browser — `file://` rendering is
accurate here because there is no build step and no server-side includes.

To check dark mode, toggle your OS theme; the page follows
`prefers-color-scheme`. To check the phone layout, use the browser's responsive
mode at ~390 px wide — the results chart and table both scroll sideways rather
than squashing, and the pipeline figure is a link to the full-size PNG because
it is too wide to read at that width.

## The results chart

The two-panel bar chart is inline SVG written straight into `index.html`. It has
no JS and makes no extra request, and because it fills with `var(--accent)` and
friends it follows dark mode without a second asset.

The bar geometry is generated, not hand-typed. If a number changes, edit `ROWS`
in `tools/make_chart.py` and re-run it:

```bash
python3 tools/make_chart.py     # stdlib only, rewrites index.html in place
```

Do not nudge the SVG coordinates by hand. Every width derives from `ROWS`, so a
hand-edited bar would silently put the chart out of step with the table
underneath it — and the next run of the generator would overwrite it anyway.

## Links

- **Code** — live, pointing at `github.com/ptea08/bw-watershed`.
- **Poster** — live, pointing at `assets/poster.pdf` in that same repo.
- **Paper** — still `aria-disabled` and pointing at `#`. It needs the OpenReview
  URL and is the only remaining `PLACEHOLDER` in the file.

To enable the Paper link: delete its `aria-disabled="true"` attribute and set
the real URL. The Code and Poster links resolve only once
`ptea08/bw-watershed` is public — until then they 404 for everyone except you,
which is exactly the failure a logged-in browser will not show you. Test from a
private window.
