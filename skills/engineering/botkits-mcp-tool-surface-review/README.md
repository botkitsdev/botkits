<picture><source media="(prefers-color-scheme: dark)" srcset="../../../assets/skills/header-botkits-mcp-tool-surface-review-dark.png 1x, ../../../assets/skills/header-botkits-mcp-tool-surface-review-dark@2x.png 2x"><img src="../../../assets/skills/header-botkits-mcp-tool-surface-review-light.png" srcset="../../../assets/skills/header-botkits-mcp-tool-surface-review-light.png 1x, ../../../assets/skills/header-botkits-mcp-tool-surface-review-light@2x.png 2x" width="800" alt="BotKits botkits-mcp-tool-surface-review skill header"></picture>

# botkits-mcp-tool-surface-review

Review an MCP server's tool list: one table of findings, a fix for each, and a rewrite of the two worst tools.

Use this when you build or adopt an MCP server and want its design checked before an agent uses it.

## Install

```sh
npx skills add botkitsdev/botkits --skill botkits-mcp-tool-surface-review
```

To list every skill in the repo: `npx skills add botkitsdev/botkits --list`.

No CLI? Copy this folder into the skills folder your agent uses, and keep `SKILL.md` inside it. Copy the skill folder itself, not the category folder.

## What it does

- Takes the `tools/list` JSON, the source where tools are registered, or a plain list of names. Thinner input means more checks are marked "not checked".
- Reads the current MCP tools page first and notes the version, so the checks match the spec.
- Scores each tool on ten checks: size of the job, name, description, input schema, output schema, result size, read or write, read-only mode, errors and repeat safety.
- Checks the server as a whole: sign-in and token scope, limits, text written by other people, feedback, discovery and tool count.
- Returns the top 3 problems, the per-tool table, and full rewrites for the two worst tools.
- It does not call the tools, so nothing can change real data. It reviews design, not speed or uptime.

## Before / after (example)

### Before

Your server has one tool, `ask_assistant`, that takes a sentence and returns a paragraph. Agents get long text back and cannot combine results.

### After

The report marks that tool "fix" on size of the job and output schema. It proposes four smaller tools with typed inputs and outputs, and writes two of them out in full. This is a made-up example.

## Use it in

- Built in Grok Bot. Not in daily use yet. Not run on a real project yet.
- Installs with `npx skills add` (tested 18 Nov 2026): Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and Grok Build.
- Supports the SKILL.md format (vendor docs): Claude apps (upload), ChatGPT (Business, Enterprise, Edu, Healthcare upload), and the other clients listed at [agentskills.io](https://agentskills.io/clients).
- Other agents that support the Agent Skills format can load it. We have not run it there.
- No direct install yet in ChatGPT dots or Meta Muse. Paste the instructions from [SKILL.md](SKILL.md) into a chat.

The agent needs the tool definitions or the source. It reads the spec page if it has web access. It does not need a connection to the server.

| Agent | Put this folder here |
| --- | --- |
| Grok Bot | Paste [SKILL.md](SKILL.md) in a 1:1 chat and ask the Bot to save it as a skill. |
| Claude Code | `.claude/skills/botkits-mcp-tool-surface-review/` or `~/.claude/skills/botkits-mcp-tool-surface-review/` |
| Codex | `.agents/skills/botkits-mcp-tool-surface-review/` or `~/.agents/skills/botkits-mcp-tool-surface-review/` |
| Cursor | `.agents/skills/botkits-mcp-tool-surface-review/` or `.cursor/skills/botkits-mcp-tool-surface-review/` |
| Gemini CLI | `.gemini/skills/botkits-mcp-tool-surface-review/` or `.agents/skills/botkits-mcp-tool-surface-review/` (one folder deep only) |
| GitHub Copilot | `.github/skills/botkits-mcp-tool-surface-review/` or `.agents/skills/botkits-mcp-tool-surface-review/` |
| Grok Build | `.grok/skills/botkits-mcp-tool-surface-review/` or `~/.grok/skills/botkits-mcp-tool-surface-review/` |
| Claude apps | Turn on code execution. ZIP this folder and upload in Customize, Skills. |

Install tested is not run tested.

## Links

- [botkits.dev](https://botkits.dev)
- Instructions: [SKILL.md](SKILL.md)

License: MIT
