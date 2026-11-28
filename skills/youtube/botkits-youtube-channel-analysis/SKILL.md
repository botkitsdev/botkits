---
name: botkits-youtube-channel-analysis
description: >-
  Use this to analyse one YouTube channel, yours or a competitor's, from
  public data. Give a handle or URL. It scores every video against the
  channel's own median, reads upload cadence, length mix, title and thumbnail
  patterns, Shorts versus long-form, the likely search or browse lane and a
  rough RPM band, then ends with 3 to 5 ideas. Needs yt-dlp. It reads public
  numbers only and cannot see impressions, CTR or retention.
compatibility: Needs Python 3.9+, yt-dlp and network access to YouTube. Pillow is optional (thumbnail sheet). Run it on a machine that can reach YouTube.
---

# YouTube channel analysis

One channel in. One repeatable report out. The report says what works on that channel, why it may work, and what you can make from it.

## When to use

- To learn from one peer: study one competitor in depth.
- When your own channel stalls: compare your last 60 videos with your own median.
- Before you plan a batch: find which lane, length and packaging a channel wins with.

Skip it for a whole niche. Use `botkits-youtube-niche-report` for that. This skill goes deep on one channel.

## Inputs

Ask for these. If the user cannot answer, use the default and say so.

1. The channel handle or URL.
2. Whose channel it is: the user's own, or a competitor's.
3. The niche, in one word from `data/rpm-bands.json` (default: skip the money step).
4. The goal: "next 5 videos", "why views dropped", "should we start this format".
5. Sample size. Default 60 long-form and 60 Shorts. Raise `--long` until the sample covers at least 180 days.

## Step 1. Pull the data

Check for a `YOUTUBE_API_KEY`. If it exists, use the API route in [references/method.md](references/method.md). If not, run the helper. It needs no key.

```sh
python3 scripts/channel_scan.py @handle --niche education --long 120 --out scan/handle
```

It writes `report.md`, `videos.csv`, `summary.json` and a thumbnail sheet. It reads only public pages. It never signs in.

If the run finds no videos, check the handle. If `yt-dlp "ytsearch1:test"` fails, YouTube blocks this machine. Run it elsewhere.

## Step 2. Cadence

Read the cadence block. Write down:

- Uploads in the last 30 and 90 days, for long-form and Shorts apart.
- The usual gap and the longest gap.
- Days since the last upload. A gap of 180 days or more is a warning.

A channel that posts daily and a channel that posts monthly need different reads. Do not call a score "normal" before you know which one you study.

## Step 3. Outliers

The score is views divided by the channel's own median, same format only. Use the bands in [references/method.md](references/method.md).

1. List every video at 3 or more. List the flops too.
2. A video that is still young has a provisional score. Mark it. Do not build on it.
3. One outlier is luck. Three outliers with the same structure are a format. Look for the repeat.
4. For each outlier, ask: did it win on packaging or on access (a guest, a leak, a news event)? Skip access wins.
5. Check size. A pattern from a channel 0.2 to 10 times your size transfers. A pattern from a giant often does not.

## Step 4. Packaging

Open `thumbs/sheet.jpg`. TOP tiles are the best scores. LOW tiles are the worst.

For each tile, write one line: the promise, the tension, the proof object, the split of work between title and thumbnail, and the distance from the channel's normal video. Then compare TOP with LOW.

Use the title feature table as a pointer only. A feature with 3 or more videos on both sides and a clear gap in median score is worth a test. Do not turn one table row into a rule.

Never copy a title or a thumbnail. Copy the structure of the promise.

## Step 5. Length and format

- Read the length mix table. Which length bucket has the best median score?
- Score Shorts and long-form apart. Never add or compare their views.
- Note any format the channel stopped doing after a flop.
- For your own Shorts, ask the user for "viewed vs swiped away" from Studio.

## Step 6. Lane: search or browse

The helper labels titles as search-style or browse-style. This is a guess.

- A search video answers a typed query. It starts slow and climbs. Check it at 28 and 90 days.
- A browse video wins the feed. It spikes early. Check it at 7 days.
- For the user's own channel, replace the guess with fact: Studio, then Reach, then "How viewers find this video".
- For a search video, write the query first. Keep the title close to it. Keep each search video clearly different from the others.
- Upload to a search lane at least once every 6 months.

## Step 7. Money, with caveats

If you gave a niche, the report shows an RPM band and a value for one typical video.

- Say "rough band". Never say "this channel earns".
- Name the source and its date. Two public sources can differ by 5 times for the same niche.
- Kids content made for kids pays far less than other niches. Say so for any kids channel.
- Shorts pay a small fraction of long-form per view.

## Step 8. Ideas

Write 3 to 5 ideas. Each idea has these lines:

- Pattern: the finding it comes from, with n and one example video.
- Our angle: one sentence that is true and not obvious. If you have none, drop the idea (the take gate).
- Format: long or Short, and the length bucket.
- Lane: search or browse, and the check date (7 days, or 28 and 90 days).
- Title: three options. Lead with the best.
- Thumbnail: two concepts in one sentence each.
- Risk: what could make it fail.

Order the ideas by strength of evidence, not by taste.

## Output

Save in the scan folder:

- `report.md` from the helper.
- `analysis.md` with your patterns and gaps. Use the template in [references/method.md](references/method.md).
- `ideas.md` with the 3 to 5 ideas.

Lead the final message with the verdict and the first idea.

## Limits

- Views are lifetime views today. A young video looks weak next to an old one.
- Public data has no impressions, CTR or retention. Say so when a finding needs them.
- Lane and RPM are estimates. Mark them as estimates every time.
- A sample under 5 matured videos gives no score.
- The channel's audience country can change RPM by a large factor.
- Study what works. Do not copy titles, scripts or thumbnails one to one. Keep downloaded thumbnails for analysis only. Do not republish them.

## Use with other skills

- `botkits-youtube-niche-report`: run it first to pick channels, then run this skill on the two or three best.
- `botkits-storytelling-hooks`: use it to write the opening of each idea.
- If you keep a 90-day outlier audit and a seven-day scorecard, feed this report into the audit and log each new video with its lane, so the scorecard reads search videos at 28 and 90 days.

## Inspired by

Rewritten in my own words from these sources. No text is copied.

- 1of10, [How to Find Competitor YouTube Channels in 2026](https://1of10.com/blog/find-youtube-competitors/). It gives three tests for a real competitor and compares each video with the channel median. It misses cadence, lane, money and a Shorts split, and it relies on a weekly manual sheet. This skill adds a one-command scan and a lane and RPM read.
- Bomx, [OUTLIER_PLAYBOOK.md](https://github.com/Bomx/viral-agent-1of10/blob/main/OUTLIER_PLAYBOOK.md). It gives score bands, four honesty questions and a "what is missing" pass. It is tied to one tool's feed and ignores search, cadence and money. This skill adds those, plus a check date by lane. The repo license was not checked, so I took ideas only.
- YouTube Help, [Decoding CTR and impressions](https://support.google.com/youtube/answer/16767369). It explains why CTR falls as reach grows and why CTR differs by surface. It covers only your own channel. This skill adds a way to read other channels from public data.
- YouTube Help, [Understand your video reach](https://support.google.com/youtubecreatorstudio/answer/9314355). It defines every traffic source. It is private data. This skill adds a title-based guess and a check against Studio for your own channel.
- ReachMath, [YouTube RPM by niche](https://reachmath.com/data/youtube-rpm-by-niche/), built on AIR Media-Tech data. It gives measured RPM by niche. It has no channel method and thin samples in some niches. This skill ties the band to one channel's median views and adds caveats.
- Autonolab, [YouTube packaging](https://blog.autonolab.com/blog/2025-07-06-the-packaging-doctrine-thumbnail-title-systems-used-by-viral-operators/). It treats title and thumbnail as one pair and warns against universal rules. It has no numbers. This skill pairs the idea with a TOP and LOW sheet scored against the channel.
- Google for Developers, [YouTube Data API quota costs](https://developers.google.com/youtube/data/determine_quota_cost). It lists what each call costs. It has no analysis. This skill adds scoring and a yt-dlp path that needs no key.
- ViewStats, [Competitors tool](https://viewstats.zendesk.com/hc/en-us/articles/28242057319707-Competitors-Tool). It shows a competitor feed and side-by-side numbers. It is a paid, closed tool with no idea gate. This skill is open and ends in ideas with a take gate.
