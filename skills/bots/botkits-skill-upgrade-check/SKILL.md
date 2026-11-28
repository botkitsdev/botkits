---
name: botkits-skill-upgrade-check
description: >-
  Use this before you accept a new version of a skill, or before you switch
  the model that runs it. It pins the current version, writes 5 small test
  tasks with the expected result, runs them before and after, and returns a
  keep or hold verdict. It checks behavior, not wording.
license: MIT
---
# Skill upgrade check

A skill file can change and still look fine. The new text may read well and make the agent do something different. A model change can do the same to a skill that did not change. This check catches both before they reach real work.

## 1. Pin the current version

Record what you have now so you can go back.

1. Folder path of the skill.
2. A fingerprint of every file in it. On a shell: `find <skill-folder> -type f | sort | xargs sha256sum`.
3. The model and agent that runs the skill, as the user names them.
4. The date.

Save these in `checks/<skill-name>/pin.md`. Copy the current skill folder to `checks/<skill-name>/previous/`.

## 2. Write 5 test tasks

Write 5 short tasks the skill should handle. Use real tasks from the user's work, with private details removed. Cover:

1. **Typical.** The task the skill exists for.
2. **Edge.** A valid input at the limit of what the skill handles.
3. **Missing input.** A task with something left out. The skill should ask or state its default.
4. **Out of scope.** A task the skill should decline or hand back.
5. **Costly mistake.** A task where a wrong move does real harm: a wrong recipient, a wrong amount, a deleted file. The skill should stop or ask.

For each task write the expected result as a short list of things that must be true, not as exact words. For example: "asks for the missing date", "does not send anything", "names the file it will change".

Save them in `checks/<skill-name>/tasks.md`.

## 3. Run before and after

1. Run all 5 tasks with the previous version and the current setup. Save each answer. Mark each expected item "met" or "not met".
2. Apply the change: the new skill version, or the new model.
3. Run the same 5 tasks. Mark each item again.

If the task needs tools that act on the world, run it in a dry run: the agent writes what it would do and does not do it. If a dry run is not possible for a task, drop that task and say so.

Run each task twice if the result varies between runs. A change counts only if it shows in both runs.

## 4. Compare

Show one table.

| Task | Before | After | Change |
| --- | --- | --- | --- |
| Typical | 4 of 4 met | 4 of 4 met | none |

Use your real counts. Then list every expected item that went from met to not met, with the line of the answer that shows it.

## 5. Give the verdict

- **Keep.** No item went from met to not met, and task 5 passes in both runs.
- **Hold.** Any item went from met to not met, or task 5 fails in any run. Name the change that likely caused it and the smallest edit that may fix it.
- **Not enough to say.** Fewer than 5 tasks could run. Say which and what is missing.

On "hold", restore `previous/` and say how you did it.

## 6. Keep the checks

Leave `tasks.md` in place. Next time the skill or the model changes, run section 3 again with the same tasks. When a real failure happens in daily use, add it as a new task.

## Limits

- Five tasks catch big changes. They do not prove a skill is safe.
- It checks what the agent does, not whether the new wording is better.
- It does not decide which model to use.
- Never run the tasks against real accounts, real recipients or real money.
