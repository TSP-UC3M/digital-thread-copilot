"""Export the ruleset that protects the default branch into .github/rulesets/ (plan step B4).

    python scripts/export_ruleset.py           write .github/rulesets/<name>.json and print a summary
    python scripts/export_ruleset.py --check   exit 1 if the exported file differs from the live ruleset
                                               or if the rules expected by the plan are missing

Needs the GitHub CLI (`gh`), authenticated with read access to the repository settings.
Fields that change at every read (links, timestamps, node id) and the field that depends on who
asks (current_user_can_bypass) are removed, so that two members export the same file.
"""

import json
import pathlib
import re
import subprocess
import sys

OUT_DIR = pathlib.Path(".github/rulesets")
VOLATILE = ("_links", "created_at", "updated_at", "node_id", "current_user_can_bypass")
# Checks required by the plan (B4, F2, F7): pull request title and messages, documentation build, and the four
# jobs of the ci workflow (pull requests 77 and 78). Add "secrets" and "dependencies" if pr-8 makes them required.
EXPECTED_CHECKS = (
    "commitlint",
    "build",
    "lint",
    "unit (ubuntu-latest)",
    "unit (windows-latest)",
    "functional",
    "Verification matrix (VCRM)",
)


def gh_json(path):
    result = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode != 0:
        raise SystemExit(f"gh api {path} failed:\n{result.stderr.strip()}")
    return json.loads(result.stdout)


def repository():
    return gh_json("repos/{owner}/{repo}")["full_name"]


def targets_default_branch(ruleset):
    include = ruleset.get("conditions", {}).get("ref_name", {}).get("include", [])
    return ruleset.get("target") == "branch" and any(ref in ("~DEFAULT_BRANCH", "refs/heads/main") for ref in include)


def clean(ruleset):
    return {key: value for key, value in ruleset.items() if key not in VOLATILE}


def summary(ruleset):
    """Return (lines, problems): what the ruleset enforces and what the plan expects but is missing."""
    rules = {rule.get("type"): rule.get("parameters", {}) for rule in ruleset.get("rules", [])}
    lines = [f"name: {ruleset.get('name')}", f"enforcement: {ruleset.get('enforcement')}"]
    problems = []
    if ruleset.get("enforcement") != "active":
        problems.append("the ruleset is not active")
    pull_request = rules.get("pull_request")
    if pull_request is None:
        problems.append("no pull_request rule: direct pushes are allowed")
    else:
        approvals = pull_request.get("required_approving_review_count", 0)
        lines.append(f"required approvals: {approvals}")
        lines.append(f"review from code owners required: {pull_request.get('require_code_owner_review', False)}")
        if approvals < 1:
            problems.append("fewer than 1 required approval")
    checks = [c.get("context") for c in rules.get("required_status_checks", {}).get("required_status_checks", [])]
    lines.append("required checks: " + (", ".join(checks) if checks else "none"))
    problems += [f"required check missing: {name}" for name in EXPECTED_CHECKS if name not in checks]
    for rule_type, label in (("non_fast_forward", "force pushes blocked"), ("deletion", "deletion blocked")):
        lines.append(f"{label}: {rule_type in rules}")
        if rule_type not in rules:
            problems.append(f"rule missing: {rule_type}")
    bypass = ruleset.get("bypass_actors", [])
    lines.append(f"bypass actors: {len(bypass)}")
    return lines, problems


def main(argv):
    check = argv == ["--check"]
    if argv and not check:
        print(__doc__)
        return 2
    repo = repository()
    found = []
    for entry in gh_json(f"repos/{repo}/rulesets"):
        detail = gh_json(f"repos/{repo}/rulesets/{entry['id']}")
        if targets_default_branch(detail):
            found.append(detail)
    if not found:
        print("No ruleset targets the default branch.")
        return 1
    status = 0
    for detail in found:
        print(f"current user can bypass: {detail.get('current_user_can_bypass', 'unknown')}")
        name = re.sub(r"[^a-z0-9]+", "-", str(detail.get("name", "ruleset")).lower()).strip("-") or "ruleset"
        path = OUT_DIR / f"{name}.json"
        text = json.dumps(clean(detail), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        lines, problems = summary(detail)
        print("\n".join(lines))
        for problem in problems:
            print(f"PROBLEM: {problem}")
        if check:
            if not path.is_file() or path.read_bytes().decode("utf-8") != text:
                print(f"OUT OF DATE: {path}")
                status = 1
            if problems:
                status = 1
        else:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode("utf-8"))
            print(f"written: {path}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
