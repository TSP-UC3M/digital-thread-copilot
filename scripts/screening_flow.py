"""Compute the selection flow of the state of the art from the screening files.

Inputs
  --search-dir   folder of the reduced exports (ieee-s1.csv, ieee-s2.csv,
                 scopus-s2.csv, records-unique.csv)
  --screening    decisions of the first screener on all unique records
  --sample-1     frozen decisions of the first screener on the sample
  --sample-2     frozen decisions of the second screener on the sample
Outputs (in --out-dir)
  screening-decisions.csv  id, stage, decision, criterion (no notes, no abstracts)
  screening-sample.csv     decisions of both screeners on the sample
  screening-flow.md        counts of the flow and agreement on the sample

The script takes no decision: it checks the files, counts, and applies the
documented overrides of OVERRIDES, each of which changes the criterion counted,
never an include or exclude decision.

The screening files hold the abstracts exported from the databases and are kept
outside the repository (see references/search-2026-11-16/README.md). The two
CSV outputs are their published, reduced form.

Usage:
  python screening_flow.py --search-dir references/search-2026-11-16
      --screening <file> --sample-1 <file> --sample-2 <file> --out-dir <dir>
      [--allow-incomplete]
"""

import argparse
import csv
import pathlib
import sys
from collections import Counter

DECISION = "decision (include/exclude)"
CRITERION = "criterion not met (IC1-IC3) or met (EC1-EC4)"
CRITERIA = ("IC1", "IC2", "IC3", "EC1", "EC2", "EC3", "EC4")
STAGE = "title-abstract"

# Criterion counted in the flow when it differs from the one written by the
# first screener. Clarification decided on 2026-11-16 after the double
# screening: a literature review without its own evaluation is counted under
# exclusion criterion 1.
OVERRIDES = {"R37": "EC1"}


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def decisions(rows):
    return {
        row["id"]: (row[DECISION].strip().lower(), row[CRITERION].strip().upper())
        for row in rows
    }


def check(all_rows, unique, sample_1, allow_incomplete):
    """Return (errors, warnings) found in the first screener's file."""
    errors, warnings = [], []
    ids = [row["id"] for row in all_rows]
    if sorted(ids) != sorted(row["id"] for row in unique):
        errors.append("identifiers differ from records-unique.csv")
    for row in all_rows:
        rid = row["id"]
        decision = row[DECISION].strip().lower()
        criterion = row[CRITERION].strip().upper()
        if not decision:
            if not allow_incomplete:
                errors.append(f"{rid}: no decision")
            continue
        if decision not in ("include", "exclude"):
            errors.append(f"{rid}: decision '{decision}'")
        elif decision == "exclude" and criterion not in CRITERIA:
            errors.append(f"{rid}: exclude without a valid criterion ('{criterion}')")
        elif decision == "include" and criterion:
            errors.append(f"{rid}: include with a criterion ('{criterion}')")
        volume = row["type"].strip() == "Conference review"
        # Step 1 of the procedure: a whole proceedings volume is excluded under
        # EC1 before the year is looked at, so a volume dated 2027 counts as EC1.
        if volume and (decision, criterion) != ("exclude", "EC1"):
            warnings.append(f"{rid}: whole proceedings volume, expected exclude EC1")
        if row["year"].strip() == "2027" and not volume and (decision, criterion) != ("exclude", "IC3"):
            warnings.append(f"{rid}: dated 2027, expected exclude IC3")
    full = decisions(all_rows)
    for rid, value in decisions(sample_1).items():
        if full.get(rid) != value:
            errors.append(f"{rid}: differs from the frozen sample file")
    return errors, warnings


def kappa(sample_1, sample_2):
    first, second = decisions(sample_1), decisions(sample_2)
    if sorted(first) != sorted(second):
        raise SystemExit("the two sample files do not hold the same records")
    n = len(first)
    table = Counter((first[r][0], second[r][0]) for r in first)
    observed = (table["include", "include"] + table["exclude", "exclude"]) / n
    p1 = sum(1 for r in first if first[r][0] == "include") / n
    p2 = sum(1 for r in second if second[r][0] == "include") / n
    expected = p1 * p2 + (1 - p1) * (1 - p2)
    value = (observed - expected) / (1 - expected) if expected != 1 else float("nan")
    differing = sorted(
        r for r in first if first[r][0] == second[r][0] and first[r][1] != second[r][1]
    )
    return n, table, observed, expected, value, differing


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for name in ("--search-dir", "--screening", "--sample-1", "--sample-2", "--out-dir"):
        parser.add_argument(name, required=True, type=pathlib.Path)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()

    unique = read(args.search_dir / "records-unique.csv")
    queries = [
        ("IEEE Xplore", "S1", "ieee-s1.csv"),
        ("IEEE Xplore", "S2", "ieee-s2.csv"),
        ("Scopus", "S2", "scopus-s2.csv"),
    ]
    identified = [(db, s, len(read(args.search_dir / f))) for db, s, f in queries]
    identified.insert(2, ("Scopus", "S1", 0))
    total = sum(count for _, _, count in identified)

    all_rows = read(args.screening)
    sample_1, sample_2 = read(args.sample_1), read(args.sample_2)
    errors, warnings = check(all_rows, unique, sample_1, args.allow_incomplete)
    for message in warnings:
        print("warning:", message)
    for message in errors:
        print("error:", message)
    if errors:
        return 1

    final = {}
    for rid, (decision, criterion) in decisions(all_rows).items():
        if decision == "exclude" and rid in OVERRIDES:
            criterion = OVERRIDES[rid]
        final[rid] = (decision, criterion)
    decided = {rid: v for rid, v in final.items() if v[0]}
    excluded = Counter(c for d, c in decided.values() if d == "exclude")
    included = sum(1 for d, _ in decided.values() if d == "include")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with open(args.out_dir / "screening-decisions.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["id", "stage", "decision", "criterion"])
        for rid in sorted(decided):
            writer.writerow([rid, STAGE, *decided[rid]])

    first, second = decisions(sample_1), decisions(sample_2)
    with open(args.out_dir / "screening-sample.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            ["id", "screener_1_decision", "screener_1_criterion", "screener_2_decision", "screener_2_criterion"]
        )
        for rid in sorted(first):
            writer.writerow([rid, *first[rid], *second[rid]])

    n, table, observed, expected, value, differing = kappa(sample_1, sample_2)
    lines = ["# Selection flow, databases (generated by scripts/screening_flow.py)", ""]
    if len(decided) < len(final):
        lines += [f"INCOMPLETE: {len(decided)} of {len(final)} records have a decision.", ""]
    lines += ["| Stage | Count |", "| --- | --- |"]
    lines += [f"| Records identified, {db}, string {s} | {count} |" for db, s, count in identified]
    lines += [
        f"| Records identified, total | {total} |",
        f"| Duplicates removed | {total - len(unique)} |",
        f"| Records screened (title and abstract) | {len(decided)} |",
        f"| Records excluded | {sum(excluded.values())} |",
    ]
    lines += [f"| Excluded under {c} | {excluded[c]} |" for c in CRITERIA if excluded[c]]
    lines += [f"| Records sent to full-text assessment | {included} |", ""]
    lines += [
        f"## Agreement on the double screening sample ({n} records)",
        "",
        "| | Screener 2: include | Screener 2: exclude |",
        "| --- | --- | --- |",
        f"| Screener 1: include | {table['include', 'include']} | {table['include', 'exclude']} |",
        f"| Screener 1: exclude | {table['exclude', 'include']} | {table['exclude', 'exclude']} |",
        "",
        f"Observed agreement {observed:.3f}, expected agreement {expected:.3f}, Cohen's kappa {value:.3f}.",
        f"Same decision under a different criterion: {', '.join(differing) or 'none'}.",
        f"Criterion counted differently from the first screener's file: {', '.join(f'{k} as {v}' for k, v in OVERRIDES.items())}.",
        "",
    ]
    (args.out_dir / "screening-flow.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
