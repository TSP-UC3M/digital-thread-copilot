# Contributing

## Development setup (Windows, PowerShell)

Each member works in a virtual environment local to the repository (`.venv/`, ignored by Git).

1. Create it once, from the repository folder:

    ```powershell
    python -m venv .venv
    ```

2. Activate it at the start of each PowerShell session:

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

    If PowerShell refuses to run the script, allow local scripts once for your user:
    `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

3. Install the pinned tools:

    ```powershell
    python -m pip install --upgrade pip
    python -m pip install -r requirements-docs.txt
    ```

4. Check the documentation before pushing:

    ```powershell
    python -m mkdocs build --strict
    python scripts/check_translations.py
    python -m mkdocs serve
    ```

    The preview is at http://127.0.0.1:8000/digital-thread-copilot/.

    The commands call `python -m mkdocs` rather than `mkdocs`, because a Windows application control policy can block `mkdocs.exe`.

Leave the environment with `deactivate`.

## Workflow

One task, one issue, one branch, one pull request.

1. Create an issue linked to a milestone (OE1 to OE5).
2. Start every working session by reading the state of the repository:

    ```powershell
    git fetch origin
    git status
    gh pr status
    ```

    If the current branch has a merged or closed pull request, clean up first:

    ```powershell
    git switch main
    git pull
    git branch -D <branch>
    git fetch --prune
    ```

3. Create a branch from an up-to-date `main`: `<type>/<short-description>`, for example `feat/graph-ingestion` or `docs/state-of-the-art`.
4. Commit with Conventional Commits messages (see below) and push the branch. Never commit on a branch whose pull request is merged: the push would recreate the branch and conflict with the squash commit on `main`.
5. Leave no uncommitted change outside the current pull request: either it gets its own commit, or it stays out of the repository until the current pull request is merged.
6. Before opening a pull request, check that none exists for the branch:

    ```powershell
    gh pr list
    ```

7. Open a pull request to `main`. Its title must also follow Conventional Commits: it becomes the header of the commit when the pull request is squash-merged (default message "Pull request title and commit details").
8. Before the merge, check that the title of the pull request describes what it actually contains, in particular after a rebase or a change of content. Correct it if needed:

    ```powershell
    gh pr edit <number> --title "<type>(<scope>): <description>"
    ```

9. Merge only when the checks pass (`commitlint`, `build`) and a teammate has approved the pull request. This holds for every member, including those whom the ruleset allows to bypass the review.

`main` is protected: no direct push, no force push. Its history is never rewritten: a wrong commit title on `main` is recorded, not amended.

## Commit messages

Format, following [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<optional scope>): <description>
```

| Type | Use |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Tests only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `style` | Formatting only |
| `perf` | Performance improvement |
| `build` | Build system or dependencies |
| `ci` | Continuous integration |
| `chore` | Maintenance |
| `revert` | Revert a previous commit |

Rules: English, imperative mood, lowercase first letter, no final period, header of at most 72 characters, body lines of at most 100 characters. Do not use the verb "fix" in a description whose type is not `fix`. Breaking changes use `!` after the type or a `BREAKING CHANGE:` footer.

Examples: `feat(ingest): import ReqIF requirements`, `docs(planteamiento): add Spanish translation`.

## Check a message locally (PowerShell, needs Node.js)

Install commitlint once, globally:

```powershell
npm install -g @commitlint/cli@19 @commitlint/config-conventional@19
```

Then, from the repository folder:

```powershell
"docs: add contributing guide" | commitlint
```

No output means the message is valid.
