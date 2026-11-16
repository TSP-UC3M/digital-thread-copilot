# Database search of 2026-11-16

Records returned by the queries of the search protocol in `docs/01-state-of-the-art.md`, run by Ferdinand Lacroix on 2026-11-16 after the protocol was merged.

| File | Content | Rows |
| --- | --- | --- |
| `ieee-s1.csv` | IEEE Xplore, string S1 | 1 |
| `ieee-s2.csv` | IEEE Xplore, string S2 | 13 |
| `scopus-s2.csv` | Scopus, string S2 | 50 |
| `records-unique.csv` | The 64 records above after removal of duplicates, with an identifier R01 to R53 and the origin of each record | 53 |
| `screening-decisions.csv` | Decision at the title and abstract stage for each unique record: `id`, `stage`, `decision`, `criterion` (IC = inclusion criterion not met, EC = exclusion criterion met) | 53 |
| `screening-sample.csv` | Decisions of the two screeners on the double screening sample | 11 |

Scopus, string S1, returned no record, so it has no file.

## Why these files are reduced

Each file keeps six fields only: title, year, source, type, DOI and origin. The full exports of the databases, which include the abstracts, are not published here: this repository is public and we have not established that the terms of use of Scopus and IEEE Xplore allow the redistribution of full exports. The full exports are kept by the team and can be shown to the teaching staff on request. This is a deviation from the protocol, which said that the exports would be kept in the repository; it is recorded in `docs/01-state-of-the-art.md`.

The reduced files are enough to recompute the counts of the search record: number of records per query, and number of unique records.

## How duplicates were removed

Two records are the same work when they have the same DOI (case-insensitive) or, failing that, the same title once reduced to lowercase letters and digits. The files are read in the order of the table above, and `records-unique.csv` is sorted by normalised title. Origin lists every query that returned the record.

## Double screening sample

A random 20 % of the unique records (11 of 53) is screened independently by a second member. Drawn with Python `random.seed(20261116)` then `random.sample` on the 53 records in the order of `records-unique.csv`: R01, R14, R21, R22, R26, R33, R37, R41, R42, R48, R53.

## Screening files

`screening-decisions.csv` and `screening-sample.csv` are written by `scripts/screening_flow.py` from the screening sheets of the team, which also computes the counts of the flow and Cohen's kappa reported in `docs/01-state-of-the-art.md`. The sheets themselves hold the abstracts and the screeners' notes and are not published, for the reason given above. The reduced files are enough to recount the exclusions per criterion and to recompute the agreement on the sample. The criterion of R37 is the one counted in the flow (exclusion criterion 1), not the one first written by the first screener (inclusion criterion 1); the page explains why.
