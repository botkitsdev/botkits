# Method notes

Read these when you need the reason behind a number in `SKILL.md`.

## Score bands

Score = a video's views divided by the median views of the same channel and the same format (long-form or Shorts). Use only videos older than 14 days for the median. Mark newer videos as young.

| Score | Read it as | Action |
| --- | --- | --- |
| Under 0.5 | Flop | Note what the channel tried. Flops teach too. |
| 0.5 to 1.5 | Normal | Ignore. |
| 1.5 to 3 | Mild lift | Note it only if it repeats. |
| 3 to 10 | Outlier | Study the packaging and the opening. |
| 10 and up | Breakout | Check the subscriber count first. Then study it closely. |

Two checks before you trust a score:

1. Is the median stable? Fewer than 5 matured videos means no score. Read raw views instead.
2. Did the video win on access or on packaging? A guest, a leak or a news event is access. You cannot copy access.

Use `score_roll` (the median of the 10 videos before it) when the channel changed a lot over time. Use `score` (whole sample) for a steady channel.

## Own videos versus other channels

- Your own video: judge it with the seven-day scorecard rule (win at 2 or more) if it is in the browse lane. Judge it at 28 and 90 days if it is in the search lane.
- A competitor video: use 3 or more as "study this". The bar is higher because you cannot see its impressions.

## Lane rules

The script labels each title as search-style, browse-style, mixed or unclear. This is a guess from words only.

- Search-style words: how to, tutorial, guide, vs, best, review, explained, for beginners, what is, setup, install, fix, template, a year.
- Browse-style words: I, my, we, tested, tried, built, spent, quit, never, worst, secret, truth, why, a question mark.

Confirm a guess with evidence:

- Old videos that still earn views each day point to search.
- A sharp spike in the first days, then a flat line, points to browse.
- For your own channel, open YouTube Studio, then the video, then Analytics, then Reach. Read "How viewers find this video". Pick the lane with the most absolute views in one date range. Percentages alone mislead on small samples.
- Open "YouTube search" terms on the same card. The real query often differs from your title.

CTR differs by lane. Search CTR is often higher on fewer impressions. Home CTR is often lower on many impressions. Never compare CTR across lanes. When a video reaches more people, its CTR often drops. That can mean it reached new viewers. It is often a good sign.

## Check dates by lane

| Lane | Check at | Why |
| --- | --- | --- |
| Browse | 7 days | The feed decides early. |
| Search | 28 days and 90 days | Search videos start slow and climb. |
| Suggested | 28 days | It needs time to link to other videos. |

A search video that looks like a flop at 7 days is not a flop yet.

## Guardrails for a search lane

- Upload at least once every 6 months, or the channel looks dead to a new viewer.
- Make each search video clearly different from the last. Two videos for the same query compete with each other.
- Keep the title close to the real query. Write the query first, then the hook.

## Packaging read

Read the title and thumbnail as one pair. For each TOP and LOW video on the sheet, write one line:

- Promise: what does the viewer expect to get?
- Tension: what question or risk does the image show?
- Proof: what object, number or result is visible?
- Split: what does the thumbnail say, and what does the title add?
- Distance: how far is it from the channel's normal video?

Compare the TOP row with the LOW row. A pattern needs three or more videos. Treat every pattern as a test, never as a law.

## Shorts

- Never compare Shorts views with long-form views. Score them apart.
- For your own Shorts, pull "viewed vs swiped away" in Studio. A low viewed rate means a weak opening. A low shown-in-feed count means weak reach.
- Shorts pay far less per 1,000 views than long-form. The helper uses USD 0.07 to 0.20.

## RPM and money

- RPM is what the creator receives per 1,000 views, after YouTube's share, across all views, including views that showed no ad.
- CPM is what advertisers pay per 1,000 ad impressions. It is higher than RPM.
- The helper multiplies the channel's median long-form views by the niche RPM band. The result is one typical video, not a month.
- Treat the result as an order of magnitude. Audience country, ad load and made-for-kids status move it a lot.
- Two public RPM sources can differ by a factor of 5 or more for the same niche. One measures real Studio data. Others estimate from the outside. Say which one you used.

## YouTube Data API route

Use this when `YOUTUBE_API_KEY` is set. It is faster and gives exact dates. The helper script does not call it yet, so write a short loop yourself.

1. `channels.list` with `part=contentDetails` and the channel id. Read `relatedPlaylists.uploads`.
2. `playlistItems.list` on that playlist, `maxResults=50`, and follow `nextPageToken`.
3. `videos.list` with `part=snippet,contentDetails,statistics` and up to 50 ids per call.

Each call costs 1 quota unit. The default daily quota is 10,000 units. `search.list` has its own small bucket, so do not use it to list a channel's videos.

## Report template

1. One-line verdict: what this channel does that works, in plain words.
2. Numbers: median views, uploads per 30 days, outlier count, lane guess, RPM band.
3. Patterns: three at most, each with its n and one example video.
4. Gaps: what the channel does not do that its audience may want.
5. Ideas: 3 to 5, each in the idea format of `SKILL.md`.
6. Limits: sample size, young videos, anything you could not read.
