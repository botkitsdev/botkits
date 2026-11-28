---
name: botkits-channel-performance-page
description: >-
  Use this when you want one channel's recent YouTube results on a single
  visual page. Turns a YouTube Studio CSV export into a self-contained HTML
  page: totals tiles, winner and miss chips, Shorts "% stayed" bars and
  long-video CTR bars. One channel, one export, no browser automation and no
  login.
license: MIT
compatibility: Needs Python 3.9+ (standard library only) and a CSV exported from YouTube Studio.
---

# Channel performance page

A Studio export is a wall of numbers. This skill turns it into a page you can
read in ten seconds: tiles, bars and short labels, no paragraphs. The title is
the finding, not the channel name.

It works from a file the owner downloads. It never signs in, opens Studio or
changes anything on the channel.

## When to use

- After a batch of uploads, to see which Shorts held viewers and which long
  videos got clicked.
- Before planning the next batch, to pick what to repeat and what to drop.
- To share one channel's week with a collaborator without sharing Studio access.

Skip it for a single video (Studio's own video page is better) or for many
channels at once (this reads one export at a time).

## Inputs

1. **The CSV.** In YouTube Studio: Analytics, Content, then "See more" to open
   advanced mode. Pick the date range, then "Export current view" as
   comma-separated values. Use the table file (often `Table data.csv`). Add the
   columns you want first: impressions, impressions click-through rate,
   average percentage viewed and, for Shorts, "Stayed to watch" if your Studio
   offers it.
2. **Channel name** to show on the page. Ask; default "Your channel".
3. **The finding**, a few words for the title. Write it after reading the data
   (step 3 below). Without it the script makes a plain one.

## Steps

1. Check the file opens and has a header row with at least a title column and
   a views column. If headers are not English, ask the owner to switch Studio
   to English for the export, or add their header names to `ALIASES` in
   `scripts/csv_page.py`.
2. Run a first pass and keep the data:

   ```sh
   python3 scripts/csv_page.py "Table data.csv" --channel "My channel" \
     --out channel-page.html --json channel-page.json
   ```

3. Read `channel-page.json`. Pick the one thing the owner should notice, in
   six words or fewer, and use it as the title. Good: "Plant Shorts held 50%+".
   Bad: "Channel performance report".
4. Run again with `--title "<finding>"`. Open the page at phone width and at
   desktop width. Check that no bar runs past its track and that the footer
   names every gap.
5. Hand over the HTML file. It has no server and no tracking. Fonts come from
   Google Fonts when online and fall back to system fonts offline.

## What the page shows

| Block | From | Notes |
| --- | --- | --- |
| Tiles | the Total row, or the sum of rows | Views, watch hours, subscribers, CTR, uploads, best % stayed |
| Winner and miss chips | top 2 by views; Shorts under 25% stayed; long videos under 2% CTR | Up to 5 chips |
| Shorts: % stayed | "Stayed to watch" column | Bands: 40%+, 25 to 40%, under 25%. ★ marks uploads from the last 7 days (`--new-days`) |
| Long videos: CTR | impressions click-through rate | Bands: 4%+, 2 to 4%, under 2% |
| Footer | file name, rows read, gaps | Lists missing columns and rounded counts |

A row is a Short when a type column says so, or else when its duration is 180
seconds or less (`--short-max-s`).

## Rules

- Read only. Never ask for the owner's Studio password, cookies or API keys.
- Keep the page visual: no paragraphs, labels of a few words.
- Do not invent a number. If a column is missing, the block says so and the
  footer lists the gap.
- Studio rounds big counts (1.2K). The script parses them and the footer says
  totals are close, not exact.
- Bands are rules of thumb, not YouTube benchmarks. Say so if the owner asks.

## Files

| Path | Use |
| --- | --- |
| `scripts/csv_page.py` | CSV to page. Standard library only. `--help` lists options. |
| `scripts/template.html` | Page layout, BotKits light and dark tokens. |
| `scripts/test_csv_page.py` | `python3 -m pytest -q scripts` |
| `example/studio-export.csv` | A made-up channel ("Tiny Garden Lab") to try it on. Not real data. |

Try it: `python3 scripts/csv_page.py example/studio-export.csv --channel "Tiny Garden Lab (sample)" --out sample.html`
