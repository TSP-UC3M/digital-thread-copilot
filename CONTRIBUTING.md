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
    mkdocs build --strict
    python scripts/check_translations.py
    mkdocs serve
    ```

    The preview is at http://127.0.0.1:8000/digital-thread-copilot/.

Leave the environment with `deactivate`.

## Workflow

1. Create an issue linked to a milestone (OE1 to OE5).
2. Create a branch from `main`: `<type>/<short-description>`, for example `feat/graph-ingestion` or `docs/state-of-the-art`.
3. Commit with Conventional Commits messages (see below) and push the branch.
4. Open a pull request to `main`. Its title must also follow Conventional Commits: it becomes the commit message when the pull request is squash-merged.
5. Merge only when the checks pass (`commitlint`, `build`) and the review is approved.

`main` is protected: no direct push, no force push.

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

Rules: English, imperative mood, lowercase first letter, no final period, header of at most 72 characters. Breaking changes use `!` after the type or a `BREAKING CHANGE:` footer.

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
