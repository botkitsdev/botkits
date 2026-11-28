---
name: botkits-mcp-tool-surface-review
description: >-
  Use this when you build or adopt an MCP server and want its tool list
  reviewed. It reads the tool definitions, checks each tool against a fixed
  list (size of the job, typed input and output, read and write split, auth,
  result size), and returns a findings table with a fix for each. It reviews
  design. It does not run the server's tools.
license: MIT
---
# MCP tool surface review

An MCP server is only as good as the tools a model sees. This skill reviews that list: the names, the descriptions, the schemas and the results. It works on your own server before release, or on someone else's server before you connect it to an agent.

## 1. Get the tool list

Ask for one of these, in this order:

1. The `tools/list` response as JSON.
2. The source file or folder where the tools are registered.
3. A list of tool names with one-line descriptions. Say in the report that this is a thin input and the checks that need schemas are marked "not checked".

Also ask for the server's auth setup in one or two lines (who signs in, what the token can do) and whether the server has a read-only mode. If the user does not know, mark those checks "unknown".

Do not call the server's tools. A review needs no live calls, and a write tool could change real data.

## 2. Check the spec you are reviewing against

Open the current tools page of the MCP specification before you start and note which version you read:

- https://modelcontextprotocol.io/specification/2025-06-18/server/tools

On that version, a tool has `inputSchema`, an optional `outputSchema`, and optional `annotations`. A result can carry `structuredContent`, and a tool that returns it should also return the same data as text for older clients. If an output schema exists, the server must return data that matches it. Clients must treat annotations as untrusted unless the server is trusted. If a newer version exists, read it and use it.

## 3. Review each tool

Score each tool "pass", "fix" or "unknown" on every check. Show the result as one table, one row per tool.

| # | Check | Pass when |
| --- | --- | --- |
| 1 | Size of the job | The tool does one clear job that an agent can combine with others. It is not one `ask` or `do_anything` tool that hides the whole product behind a sentence. |
| 2 | Name | Verb and noun, unique, readable without the description. |
| 3 | Description | Says what it does, when to use it, and what it does not do, in a few lines. No instructions aimed at the model's behavior elsewhere. |
| 4 | Input schema | Every field has a type and a short description. Required fields are marked. Enums replace free text where the set is small. |
| 5 | Output schema | An `outputSchema` exists, the fields are named, and the server returns `structuredContent` that matches it. |
| 6 | Result size | The tool returns what the next step needs. Large lists are paged or filtered. It does not return a whole record when the caller needs two fields. |
| 7 | Read or write | The tool is clearly a read or a write. Write tools say what they change, and can be undone or are marked as not undoable. |
| 8 | Read-only mode | If a read-only mode exists, write tools are not registered in it. A line in a description that says "do not edit" is not a boundary. |
| 9 | Errors | Failures return a clear message with `isError` set, and say what the caller can change. |
| 10 | Repeat safety | Running a write twice does not do the damage twice, or the tool takes an idempotency key. |

## 4. Review the server

After the tools, check the server as a whole. Use "pass", "fix" or "unknown".

1. **Identity.** Each user signs in as themselves, and the token is scoped to what the tool set needs. A shared long-lived key is a "fix".
2. **Limits.** Inputs are validated, calls are rate limited and outputs are cleaned. The spec lists these as server duties.
3. **Untrusted text.** Any tool that returns text written by other people (tickets, emails, web pages) says so in its description, so the client can treat the text as data.
4. **Intent and feedback.** The server has a way to learn why a tool was called, or a feedback tool, so failed calls can be fixed. This is nice to have, not a "fix".
5. **Discovery.** There is one clear place to find the server and its auth details.
6. **Tool count.** If the list is long, say which tools could be merged, split or removed. Name the ones an agent is least likely to need.

## 5. Write the report

Return, in this order:

1. The spec version you read and the date.
2. The top 3 problems, each with the tool name and a one-line fix.
3. The per-tool table.
4. The server checks.
5. A rewrite for the two worst tools: the new name, description and schemas, written out in full.
6. What you could not check and what you need to check it.

## Limits

- It reviews design from definitions. It does not test behavior, speed or uptime.
- It does not call tools, connect to the server or change files unless the user asks for the rewrite to be applied.
- A passing review does not make a server safe. Say so in the report.
