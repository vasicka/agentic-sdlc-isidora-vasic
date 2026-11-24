# Agentic Software Development Lifecycle: Building a Software Factory

This repository follows the course **Agentic Software Development Lifecycle: Building a Software Factory**, which covers how to design and build an AI-assisted software development pipeline. Each module introduces a new layer of the factory, from Git automation to full integration.

---

## Course Progress

- [ ] Module 1: Git Workflow Automation *(in progress)*
- [ ] Module 2: Software Architecture
- [ ] Module 3: Software Requirements
- [ ] Module 4: CI/CD
- [ ] Module 5: TDD/BDD
- [ ] Module 6: Final Integration

---

## Git Agent

The Git agent automates the core Git and GitHub workflow tasks that developers perform repeatedly: creating issues, naming branches, writing commit messages, and opening Pull Requests. It enforces project conventions — commit format, branch prefixes, PR structure, and issue linking — so that every change is traceable, consistently documented, and ready for review without manual overhead.

---

## Agent Harnesses

The course supports three agent harnesses: Kiro CLI, Pi, and OpenCode.

This repository uses Kiro CLI for all modules, with agent configurations
stored in `.kiro/agents/`.

OpenCode starter agents are available in the module starter directories.

For more information, see the [OpenCode harness guide](docs/opencode.md).

---

## Keeping the Repository Up to Date

The cohort repository receives fixes and new course materials.
Use cherry-pick instead of merging unrelated repository histories.

1. Add the cohort remote (only once):

   ```bash
   git remote add cohort https://github.com/LabSoft-AI/Agentic-SDLC-Software-Factory-2026-11-16.git
   ```

2. Fetch updates and find the relevant commits:

   ```bash
   git fetch cohort
   git log --oneline cohort/main -10
   ```

3. Create an update branch from the updated main branch:

   ```bash
   git checkout -b chore/cohort-updates
   git cherry-pick -x <sha>
   ```

4. If conflicts occur, preserve existing student work and resolve
   the conflicts before continuing:

   ```bash
   git add <files>
   git cherry-pick --continue
   ```

   To cancel the operation:

   ```bash
   git cherry-pick --abort
   ```

5. Push the branch and open a Pull Request:

   ```bash
   git push -u origin chore/cohort-updates
   ```

Do not push directly to main.
