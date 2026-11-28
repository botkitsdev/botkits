<picture><source media="(prefers-color-scheme: dark)" srcset="../../assets/bots/header-botkits-youtube-growth-coach-dark.png 1x, ../../assets/bots/header-botkits-youtube-growth-coach-dark@2x.png 2x"><img src="../../assets/bots/header-botkits-youtube-growth-coach-light.png" srcset="../../assets/bots/header-botkits-youtube-growth-coach-light.png 1x, ../../assets/bots/header-botkits-youtube-growth-coach-light@2x.png 2x" width="800" alt="BotKits botkits-youtube-growth-coach bot header"></picture>

# botkits-youtube-growth-coach

A YouTube growth coach bot: it studies what wins in a niche, writes an honest pace plan to the Partner Program thresholds, and picks a title and thumbnail pair for one video.

Use this when you want one bot for those three jobs, instead of loading the skills one by one.

## Install

Copy this folder and the skill folders it names. Then paste [PACK.md](PACK.md) into your bot and ask it to take this job, or point an agent at the folder.

The pack names these skills, already in this repo:

- [botkits-youtube-niche-report](../../skills/youtube/botkits-youtube-niche-report/)
- [botkits-youtube-monetization-plan](../../skills/youtube/botkits-youtube-monetization-plan/)
- [botkits-youtube-title-thumbnail-set](../../skills/youtube/botkits-youtube-title-thumbnail-set/)
- [botkits-shorts-reframe](../../skills/video/botkits-shorts-reframe/)

To install one skill: `npx skills add botkitsdev/botkits --skill <skill-name>`.

## What it does

- Studies the niche with a report scored against each channel's own median, then plans topics from that.
- Sizes the gap to the official Partner Program thresholds, checks the pace against your weekly hours, and writes a week-by-week plan. It does not promise a date or an income.
- Writes 10 honest titles and 3 thumbnail concepts for one video, scores them, and asks you to pick a pair on a card.
- Reframes a 16:9 video to a 1080×1920 Short when that is part of the plan.
- Optional Monday review of the four pace numbers. It stays silent when you are on track and nothing new showed up.
- It does not upload, buy views, run ads, post on other networks, write a full script or edit the film.

## Before / after (example)

### Before

You have 120 subscribers, 300 watch hours and 5 hours a week. The plan so far is "post more", and titles are written at upload time.

### After

The bot writes a pace plan that says what each video would need to earn, marks the result as a stretch or not in this window, and waits for you to pick a route on a card. For the next video it returns a ranked title and thumbnail set and asks you to pick a pair. This is a made-up example.

## Use it in

- Built in Grok Bot. Not in daily use yet. Not run on a real channel yet.
- Installs with `npx skills add` for the skills it lists (tested 18 Nov 2026): Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and Grok Build. The pack itself is a `PACK.md` you load as the bot's job. We have not shipped it as a Grok Bot template.
- Other agents that support a persona plus skills can load it. We have not run the pack there.

Tappable approval cards need a bot that can show them (Grok Bot does). Without cards, the bot still presents real options and waits for a clear pick. It must not invent a letter menu as a substitute for a card when cards are available.

| Agent | How to load it |
| --- | --- |
| Grok Bot | Paste [PACK.md](PACK.md) in a 1:1 chat and ask the Bot to take this job and save the listed skills. |
| Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Grok Build | Install the listed skills with `npx skills add`, then add `PACK.md` as the agent's instructions. |

Install tested is not run tested.

## Links

- [botkits.dev](https://botkits.dev)
- Pack: [PACK.md](PACK.md)

License: MIT
