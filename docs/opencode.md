# OpenCode Harness

OpenCode is the third supported harness, next to Kiro CLI and Pi. Agent files are
Markdown files in `.opencode/agents/`. The system prompt is the file body. YAML
frontmatter sets the description, mode, model, and permissions.

## Install

```bash
curl -fsSL https://opencode.ai/v2/install | bash
```

Alternatives: `brew install anomalyco/tap/opencode-v2` or
`npm install -g @opencode/cli`. Verify:

```bash
opencode --version
```

## Agent file format

```markdown
---
description: What the agent does
mode: primary
permissions:
  - action: edit
    resource: "*"
    effect: allow
---

System prompt goes here.
```

Start OpenCode from your repository and pick the agent with `/agents`, `Ctrl+X`
then `A`, or cycle with `Shift+Tab`. For one-off runs:

```bash
opencode run --agent git-agent "Create an issue for the README"
```

## What maps from Kiro

| Kiro | OpenCode |
|------|----------|
| `.kiro/agents/<name>.json` | `.opencode/agents/<name>.md` |
| `prompt` (inline or `file://`) | Markdown body. OpenCode has no `file://` prompt, so inline it. |
| `tools` | Built-in tools plus `permissions` rules. Common actions: `read`, `glob`, `grep`, `edit`, `shell`. |
| `resources` | No per-agent auto-load. List files in the prompt and tell the agent to read them. |
| `hooks.postToolUse` | No per-agent hook. Put the rule in the prompt, or write an OpenCode plugin. |
| `mcpServers` | `mcp.servers` in `opencode.jsonc`. Server config is project-wide. |

## Module starters

Each module has an OpenCode starter next to the Kiro JSON:

| Module | OpenCode starter |
|--------|------------------|
| 1 Git | `modules/module-1-git/starter/git-agent.md` |
| 2 Architecture | `modules/module-2-architecture/starter/architecture-agent.md` |
| 3 Requirements | `modules/module-3-requirements/starter/requirements-agent.md` |
| 4 CI/CD | `modules/module-4-cicd/starter/cicd-agent.md` |
| 5 TDD/BDD | `modules/module-5-tdd-bdd/starter/tdd-bdd-agent.md` |

Copy the starter into your own repository:

```bash
mkdir -p .opencode/agents
cp modules/module-1-git/starter/git-agent.md .opencode/agents/
```

Then start OpenCode and select the agent:

```bash
opencode
> /agents
```

Use the same prompts as the Kiro instructions. The agent, tools, and task are
the same. Only the file format changes.

## Differences to keep in mind

- OpenCode loads `AGENTS.md` automatically. Kiro resources are not automatic, so
  the starters tell the agent which files to read.
- The OpenCode permission model is allow by default. Add `effect: deny` rules to
  remove a capability. The starters list the tools they use.
- Kiro `postToolUse` hooks have no per-agent equivalent. For a deterministic
  "run tests after write" sensor, use an OpenCode plugin or a git pre-commit
  hook. Module 5 asks you to add the test rule to the prompt.
- MCP servers are project-wide in OpenCode. Add them under `mcp.servers` in
  `opencode.jsonc`.

## References

- [OpenCode documentation](https://opencode.ai/docs/)
- [OpenCode agents](https://opencode.ai/docs/agents/)
- [OpenCode configuration](https://opencode.ai/docs/config/)
