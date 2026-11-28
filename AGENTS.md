# AGENTS.md

Instructions for any coding agent working in this repo: Grok Bot, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Muse Code and others.

## Read first

1. [BRAND.md](BRAND.md): the name (always **BotKits** in prose), what we may claim, voice, links and the skill page shape.
2. [DESIGN.md](DESIGN.md): grid, type scale, light and dark tokens, spark, image sizes, alt text, file names and the image check.

Both are required. If a task conflicts with them, stop and ask the owner instead of guessing.

This repo has no `CLAUDE.md` on purpose. Claude Code reads `AGENTS.md` when no `CLAUDE.md` or `CLAUDE.local.md` exists ([Claude Code docs](https://code.claude.com/docs/en/memory)). Adding a `CLAUDE.md` would stop that. Do not add one.

## Repo layout

```
skills/<category>/<skill-name>/SKILL.md   instructions the bot loads
skills/<category>/<skill-name>/README.md  optional, for humans (shape in BRAND.md section 8)
skills/<category>/<skill-name>/...        optional scripts, templates, references
bots/<bot-name>/PACK.md                   the pack an agent loads (persona, skills, routines)
bots/<bot-name>/README.md                 optional, for humans (same page shape as a skill README)
assets/                                   shared README images
docs/credits.md                           source credits
THIRD_PARTY_NOTICES.md                    license notices
.agents/skills/<skill-name>               symlink to skills/<category>/<skill-name>/ (generated)
.claude/skills                            symlink to .agents/skills (generated)
GEMINI.md                                 symlink to this file, for Gemini CLI
```

The folders under `skills/` are the only real copies. `.agents/skills/` gives one flat folder per skill, which Codex, Cursor, Gemini CLI, GitHub Copilot and Muse Code read, and `.claude/skills` points Claude Code at the same folder. Do not edit through a link and do not add files there by hand. After you add, rename or move a skill, run `bash .github/scripts/skill-links.sh` and commit the links. CI runs it with `--check`. Skill folder names must be unique across categories.

Categories today: ads, bots, design, engineering, images, seo, video, writing, youtube.

## Skill format

Every skill follows the open [Agent Skills spec](https://agentskills.io/specification):

- `SKILL.md` starts with YAML frontmatter on line 1. Nothing (not a title, not a blank line) comes before the opening `---`.
- Frontmatter uses only the six spec keys: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. claude.ai uploads and the Skills API accept only these keys ([Claude Code docs](https://code.claude.com/docs/en/skills)). Do not add bot-specific keys such as `disable-model-invocation`, `paths` or `argument-hint`.
- `name`: lowercase letters, digits and single hyphens, at most 64 characters, and the same as the folder name.
- `description`: at most 1024 characters, aim for under 300. Start with the trigger ("Use this when ..."), then the output, then one key limit. Some bots shorten long descriptions.
- `compatibility` (optional, at most 500 characters): the environment a skill needs, for example "Needs Grok Bot (routines, approval cards)".
- Keep `SKILL.md` under 500 lines. Move long reference material to files next to it and link them with relative paths, one level deep.
- One skill, one job.

When you add a skill, also add it to the skill list and the count in `README.md`, run `bash .github/scripts/skill-links.sh`, and put it in a bot pack (see [Bot packs](#bot-packs)).

### Grok Bot-only skills

A skill that uses Grok Bot-only tools (routines, tap or approval cards, `SendToUser`, `CreateAgent`, `CloudAgent`, the box, `/home/box/agent-data/` or `/workspace/` paths, and similar) must:

- start its `description` with **"Needs Grok Bot."**,
- set `compatibility: Needs Grok Bot (<the tools it uses>)`,
- and say "Needs Grok Bot. Uses routines and approval cards." (or the tools it uses) on the first line of its README.


## Bot packs

This repo ships bots, not only skills. A bot is a pack: a persona, the skills it uses, optional routines, and a short getting-started chat.

```
bots/<bot-name>/PACK.md    the pack an agent loads
bots/<bot-name>/README.md  for humans (same page shape as a skill README)
```

The skill folders stay the source of each skill. A pack names them. It does not copy them.

### Split test

A pack author must pass this check before adding a pack. If any check fails, make two packs, not one.

- If the one-job sentence needs "and", split.
- If a fix to one step would never change the other, split.
- A step with its own approvals and failure modes (posting, sending or spending) is its own bot.

### PACK.md format

- Starts with YAML frontmatter on line 1. Nothing comes before the opening `---`.
- Required keys: `name` (the same as the folder), `description` (trigger, then the job, then one limit), `license`, `skills` (a list of skill folder names already in this repo).
- Optional keys: `compatibility`, `routines` (a list of objects with `name`, `schedule`, `skill` and `quiet_when`).
- Pack frontmatter may use `skills` and `routines`. Those keys are not part of the Agent Skills spec, and a pack is not a skill. Do not put them on a `SKILL.md`.

The body, in this order:

1. **Job.** One sentence: what it does each time it wakes.
2. **Not its job.** The nearby things it refuses, even when asked.
3. **Voice.** A few words. Never "helpful assistant".
4. **Wake.** Chat, a routine, an event, or a mix. Silent when there is nothing worth saying.
5. **Approvals.** If the bot ever needs the user to approve, pick or confirm, it asks with a tappable card of real, checked options. No letter menus and no "waiting for your tap" without a card. One card ends the turn. If a tool shows its own approval UI, use that instead.
6. **Skills.** Why each listed skill is in the pack, in one line.
7. **Routines.** If any, the schedule and when they stay quiet.
8. **Getting started.** The first questions, asked one at a time, and what to do with the answers.
9. **Probe set.** Four fixed test asks: a typical ask, an anti-job ask, a decision that needs a card, and a quiet case. A rewrite of the persona must pass at least as many of these as the current text.
10. **Corrections.** Where the shared corrections log lives, and the three steps the bot follows when the user corrects it: update its own instructions and the task SOP; add one dated line to the log (date, bot, what was wrong, the new rule); tell the user in one line which SOP changed. The work is done only when this is in a shared place other bots can read.

When you add a skill, put it in a bot pack as well as the skill list. Prefer an existing pack whose job already covers it. If none fits, add a new pack only after it passes the split test, with a refuse case, a card rule, quiet behaviour and a corrections section. When you add a pack, add it to the bot list in `README.md`.

## Portable skills

To keep a skill usable outside one bot:

- Describe the action, not one bot's tool name: "ask the user to approve" instead of `SendToUser`, "hand the coding to a cloud agent" instead of `CloudAgent`.
- Put bot-specific mappings in a reference file inside the skill, for example `references/grok-bot.md`.
- Use relative paths or a path the user picks, not fixed paths on one machine.
- Scripts must state their dependencies and fail with a clear message.
- No secrets, tokens or personal account IDs in any file.
- Do not claim a skill works on a bot unless someone ran it there. Use the wording in BRAND.md section 7.

## Use a skill in other bots

What we can say today (checked 18 Nov 2026):

| Status | Bots |
| --- | --- |
| Used daily | Grok Bot only |
| `npx skills add` install tested | Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Grok Build. The CLI wrote the files. Nobody has run the skills there yet. |
| Upload supported (vendor docs) | Claude apps; ChatGPT on Business, Enterprise, Edu and Healthcare plans |
| Paste only | ChatGPT dots, Meta Muse |

Install with the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add botkitsdev/botkits --skill <skill-name>
```

Or copy one skill folder by hand. Copy the skill folder itself (`skills/<category>/<skill-name>/`), not the category folder, because some bots look only one folder deep.

| Bot | How | Source |
| --- | --- | --- |
| Grok Bot | Paste the `SKILL.md` in chat and ask the Bot to save it as a skill. Saved skills are one library shared by all your Bots. No documented install from GitHub. | [docs](https://docs.x.ai/grok-bot/skills-routines-and-automations) |
| Claude Code | `.claude/skills/<skill-name>/` or `~/.claude/skills/` | [docs](https://code.claude.com/docs/en/skills) |
| Claude apps | ZIP the skill folder, upload in Customize > Skills. Needs code execution on. | [help](https://support.claude.com/en/articles/12512180-use-skills-in-claude) |
| Codex | `.agents/skills/<skill-name>/` or `~/.agents/skills/` | [docs](https://learn.chatgpt.com/docs/build-skills) |
| ChatGPT | Skills > Create > Upload from your computer (Business, Enterprise, Edu, Healthcare) | [help](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) |
| ChatGPT dots | OpenAI's always-on agents in ChatGPT. A dot can use plugins installed and enabled on your account, and plugins can carry skills. Local skills need a connected computer. No direct SKILL.md install is documented for a dot, so for now paste the instructions. | [dots](https://learn.chatgpt.com/docs/dots), [plugins](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) |
| Cursor | `.agents/skills/` or `.cursor/skills/` (also reads `.claude/skills/`) | [docs](https://cursor.com/docs/skills) |
| Gemini CLI | `.gemini/skills/<skill-name>/` or `.agents/skills/`, one level deep only | [docs](https://geminicli.com/docs/cli/tutorials/skills-getting-started/) |
| GitHub Copilot | `.github/skills/` or `.agents/skills/`, personal `~/.copilot/skills/` | [docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Grok Build | `.grok/skills/` or `~/.grok/skills/` (this is xAI's coding CLI, not Grok Bot) | [Skills CLI agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) |
| Meta Muse | No custom skill install. Paste the instructions into a chat. | [Meta help](https://www.meta.com/help/superintelligence/2797651547267109/) |
| Muse Code | `.agents/skills/<skill-name>/`. Its docs site is not confirmed as an official Meta site. | [docs](https://meta-models.github.io/muse-code-sdk/next/guides/extend/skills/) |

`.agents/skills/` is the shared folder that Codex, Cursor, Gemini CLI, GitHub Copilot and Muse Code all read.

## Outside sources

- Rewrite outside skills in our own words. Do not copy any run of 8 or more words from the source.
- End the skill (or its README) with an `## Inspired by` section that names and links each source.
- Add the source to `docs/credits.md`. If its license needs a notice, add it to `THIRD_PARTY_NOTICES.md`.
- Do not copy from sources that have no reuse license, such as marketplace templates.
- Exception (Dani rule, Nov 2026): when a skill only takes an idea from someone's social post (no text, code or images reused), make it our own: a new name, our own structure, defaults and wording. Do not name or link the post or its author anywhere, with no `## Inspired by` section and no `docs/credits.md` row.

## Git and pull requests

- Branch from `main`. Bot branches start with the bot's prefix, for example `grok-<topic>`.
- One topic per PR. For README upgrades, about 5 skills per PR.
- Never force-push and never rebase a shared branch. Add a new commit instead.
- Do not merge your own PR. A reviewer merges.
- Do not change `assets/` or `README.md` in a PR whose topic is something else.
- PR body: what changed, why, and links to any sources. No Gumroad links in PR bodies.
- Never add paid kit files to this repo. Run `bash .github/scripts/paid-guard.sh` before you push (BRAND.md section 9).

## Before you open a PR

- [ ] Prose says BotKits, never botskills or Botkits.
- [ ] Frontmatter is on line 1, uses only the six spec keys, and `name` matches the folder.
- [ ] Grok Bot-only skills start their description with "Needs Grok Bot."
- [ ] No lime `#C8FF3D` in new images or badges.
- [ ] Every image has real alt text.
- [ ] Every number has a source.
- [ ] New outside ideas are credited.
- [ ] Public text passed [botkits-no-ai-slop](skills/writing/botkits-no-ai-slop/).
- [ ] `bash .github/scripts/skill-links.sh --check` passes.
- [ ] New skills land in a bot pack, and new packs are on the README bot list.
- [ ] New packs pass the split test and include a Corrections section.
