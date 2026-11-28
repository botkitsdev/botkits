# botkits-channel-performance-page

Turn one YouTube Studio CSV export into a single visual page: tiles, Shorts "% stayed" bars and long-video CTR bars.

For YouTube creators who want to see a channel's last batch of uploads at a glance, without sharing Studio access.

## Install

```sh
npx skills add botkitsdev/botkits --skill botkits-channel-performance-page
```

To list every skill in the repo: `npx skills add botkitsdev/botkits --list`.

No CLI? Copy this folder into the skills folder your agent uses, and keep `SKILL.md` inside it.

## What it does

- Reads the table CSV from Studio's advanced mode ("Export current view"). Needs a title and a views column; everything else is optional.
- Parses Studio's number formats, including rounded counts like 1.2K, and keeps the raw text next to the number.
- Splits Shorts from long videos by type column or by duration (180 seconds or less).
- Writes one self-contained HTML page: totals tiles, winner and miss chips, Shorts "% stayed" bars in three bands, long-video CTR bars, and a footer that lists every gap.
- One channel and one export at a time. It never signs in to YouTube or changes anything.

## Before and after (example)

Before: `example/studio-export.csv`, 8 rows for a made-up channel, "Tiny Garden Lab". Not real data.

```sh
python3 scripts/csv_page.py example/studio-export.csv --channel "Tiny Garden Lab (sample)" --out sample.html
```

After: a page titled "One Short brought 34% of views", with tiles (18,412 views, 395.4 watch hours, +138 subscribers, 2.8% CTR), two Shorts above 40% stayed, one under 25%, and the long video with the weakest CTR flagged at 1.7%.

## Use it in

- Used daily: none yet. This skill is new.
- Installs with `npx skills add` (tested 18 Nov 2026 for the repo): Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and Grok Build.
- Supports the SKILL.md format (vendor docs): Claude apps (upload), ChatGPT (Business, Enterprise, Edu, Healthcare upload), and the other clients listed at [agentskills.io](https://agentskills.io/clients).
- Other agents that support the Agent Skills format can load it. We have not run it there.
- No direct install yet in ChatGPT dots or Meta Muse. Paste the instructions from [SKILL.md](SKILL.md) into a chat.

| Agent | Put this folder here |
| --- | --- |
| Grok Bot | Paste [SKILL.md](SKILL.md) in a 1:1 chat and ask the Bot to save it as a skill. |
| Claude Code | `.claude/skills/botkits-channel-performance-page/` or `~/.claude/skills/botkits-channel-performance-page/` |
| Codex | `.agents/skills/botkits-channel-performance-page/` or `~/.agents/skills/botkits-channel-performance-page/` |
| Cursor | `.agents/skills/botkits-channel-performance-page/` or `.cursor/skills/botkits-channel-performance-page/` |
| Gemini CLI | `.gemini/skills/botkits-channel-performance-page/` or `.agents/skills/botkits-channel-performance-page/` (one folder deep only) |
| GitHub Copilot | `.github/skills/botkits-channel-performance-page/` or `.agents/skills/botkits-channel-performance-page/` |
| Grok Build | `.grok/skills/botkits-channel-performance-page/` or `~/.grok/skills/botkits-channel-performance-page/` |
| Claude apps | Turn on code execution. ZIP this folder and upload it in Customize, Skills. |

Install tested is not run tested.

## Links

- [botkits.dev](https://botkits.dev)
- Instructions: [SKILL.md](SKILL.md)

License: MIT
