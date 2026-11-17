## What and why

<!-- One or two sentences. The title must describe the real content: it becomes the squash commit header. -->

Refs: plan <ID>

## Checks run locally before the push (rule R5)

- [ ] `python -m mkdocs build --strict`
- [ ] `python scripts/check_translations.py`
- [ ] Tests (`python scripts/dev.py check`), once the code skeleton exists
- [ ] Commit messages follow Conventional Commits: header of at most 72 characters, body lines of at most 100

## Before the merge

- [ ] The title still describes the content (after a rebase or a change of content: `gh pr edit <n> --title "..."`)
- [ ] A teammate has approved; no bypass of the rules
- [ ] Use of generative AI in this pull request is listed in `docs/ai-usage.md`, or there is none
