"""Create or update the GitHub planning objects of the project from files.

Reads .github/labels.json and .github/backlog.json and makes GitHub match them:
labels, milestones with their due dates, one issue per plan step (label,
milestone, assignee), and a project board that holds the issues.

The script can be run again at any time: a label is updated in place, a
milestone is found by its title, an issue is found by the step identifier at
the start of its title ("[A4] ...") and is never created twice.

Requires the GitHub CLI (gh), authenticated with write access to the
repository. The project board also needs the "project" scope:
    gh auth refresh -s project

Usage:
    python scripts/github_setup.py --dry-run     show what would be done
    python scripts/github_setup.py               apply
    python scripts/github_setup.py --skip-project
"""

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def gh(args, dry_run=False, check=True):
    """Run a gh command and return its standard output."""
    if dry_run:
        short = [a.splitlines()[0][:60] + ("..." if len(a) > 60 or "\n" in a else "") for a in args]
        print("  would run: gh " + " ".join(short))
        return ""
    result = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout


def sync_labels(labels, dry_run):
    for label in labels:
        gh(
            ["label", "create", label["name"], "--color", label["color"],
             "--description", label["description"], "--force"],
            dry_run,
        )
    print(f"labels: {len(labels)} created or updated")


def sync_milestones(repo, milestones, dry_run):
    existing = {}
    if not dry_run:
        raw = gh(["api", f"repos/{repo}/milestones?state=all&per_page=100"])
        existing = {m["title"]: m["number"] for m in json.loads(raw)}
    for milestone in milestones:
        fields = ["-f", f"description={milestone['description']}", "-f", f"due_on={milestone['due']}T23:59:59Z"]
        if milestone["title"] in existing:
            number = existing[milestone["title"]]
            gh(["api", "-X", "PATCH", f"repos/{repo}/milestones/{number}", *fields], dry_run)
        else:
            gh(["api", "-X", "POST", f"repos/{repo}/milestones", "-f", f"title={milestone['title']}", *fields], dry_run)
    print(f"milestones: {len(milestones)} created or updated")


def sync_issues(issues, dry_run):
    """Create the missing issues; return {step id: issue url}."""
    known = {}
    if not dry_run:
        raw = gh(["issue", "list", "--state", "all", "--limit", "1000", "--json", "title,url"])
        for issue in json.loads(raw):
            if issue["title"].startswith("[") and "]" in issue["title"]:
                known.setdefault(issue["title"][1:issue["title"].index("]")], issue["url"])
    created = 0
    for issue in issues:
        if issue["id"] in known:
            continue
        args = ["issue", "create", "--title", issue["title"], "--body", issue["body"]]
        args += ["--milestone", issue["milestone"]]
        for label in issue["labels"]:
            args += ["--label", label]
        for login in issue["assignees"]:
            args += ["--assignee", login]
        url = gh(args, dry_run).strip().splitlines()[-1] if not dry_run else gh(args, dry_run)
        created += 1
        if dry_run:
            continue
        known[issue["id"]] = url
        if issue.get("closed_comment"):
            gh(["issue", "close", url, "--reason", "completed", "--comment", issue["closed_comment"]])
    print(f"issues: {created} created, {len(issues) - created} already present")
    return known


def sync_project(owner, title, urls, dry_run):
    number = None
    if not dry_run:
        raw = gh(["project", "list", "--owner", owner, "--format", "json", "--limit", "100"], check=False)
        if not raw:
            print('project: skipped, gh cannot list projects (run "gh auth refresh -s project")')
            return
        for project in json.loads(raw).get("projects", []):
            if project["title"] == title:
                number = project["number"]
    if number is None:
        raw = gh(["project", "create", "--owner", owner, "--title", title, "--format", "json"], dry_run)
        number = json.loads(raw)["number"] if raw else "<new>"
    for url in urls:
        gh(["project", "item-add", str(number), "--owner", owner, "--url", url], dry_run)
    print(f"project: {title} (number {number}), {len(urls)} issues added or already there")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="print the gh commands without running them")
    parser.add_argument("--skip-project", action="store_true", help="do not create or fill the project board")
    args = parser.parse_args()

    labels = json.loads((ROOT / ".github" / "labels.json").read_text(encoding="utf-8"))
    backlog = json.loads((ROOT / ".github" / "backlog.json").read_text(encoding="utf-8"))
    known_labels = {label["name"] for label in labels}
    known_milestones = {m["title"] for m in backlog["milestones"]}
    for issue in backlog["issues"]:
        missing = set(issue["labels"]) - known_labels
        if missing or issue["milestone"] not in known_milestones or not issue["assignees"]:
            raise SystemExit(f"{issue['id']}: unknown label {missing}, unknown milestone or no assignee")

    repo = "<owner>/<repo>"
    if not args.dry_run:
        repo = gh(["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]).strip()
    print(f"repository: {repo}")
    sync_labels(labels, args.dry_run)
    sync_milestones(repo, backlog["milestones"], args.dry_run)
    urls = sync_issues(backlog["issues"], args.dry_run)
    if not args.skip_project:
        sync_project(repo.split("/")[0], backlog["project_title"], list(urls.values()), args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
