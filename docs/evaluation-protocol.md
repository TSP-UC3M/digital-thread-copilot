# Evaluation protocol

!!! warning "Draft, to be frozen before any measurement"
    This protocol is a draft. It is frozen by a tag before the first evaluation run; after the freeze, any change is a dated deviation recorded on this page. Items marked "To decide" are open. No measurement has been made.

## 1. Purpose

Decide on the hypothesis of the project: the answers of an LLM copilot restricted to deterministic tools over a knowledge graph of the artifacts cite the correct artifacts with a recall and a precision of at least 0.90 and a hallucination rate of at most 5 %, and with a significantly higher recall than the same LLM given all the artifacts as text in its context, without graph or tools. Secondary, indicative observation: engineers using the copilot answer faster than by manual search.

The hypothesis has two criteria (decision record ADR-0001):

- Primary criterion, automated. The copilot meets absolute thresholds and has a significantly higher recall than the same model given all the artifacts in its context (configuration R2 of section 3).
- Secondary criterion, indicative. Time and correctness against a manual search by participants outside the group.

## 2. Material

| Item | Definition | Frozen by |
| --- | --- | --- |
| Case study | Digital thread of the GPCA infusion pump: 12 requirements, the SysML v2 model, 12 test cases, their links | Tag on the data, before the questions are written |
| Reference links | Every satisfies, verifies and depends-on link, reviewed by a member who is not the author | Same tag |
| Questions | 20 questions: at least 6 on traceability, 6 on impact, 6 on coverage | Tag before any copilot run |
| Reference answers | For each question, the set of required identifiers and the set of acceptable identifiers | Same tag as the questions |

Rules for the questions:

1. Each question is answered by a set of artifact identifiers. A required identifier must be cited; an acceptable identifier may be cited without penalty (for example an intermediate model element on the path); any other identifier is an error.
2. Reference answers are derived from the reference links by a script where possible, and checked by a member who did not write the question.
3. Questions are written before any copilot answer is seen by their author, and they are never changed after the freeze. A question found to be wrong after the freeze is reported and excluded from all configurations, with the reason.
4. A script confirms that every identifier of the reference answers exists in the graph.

## 3. Configurations

All three use the same model, version, provider, reasoning setting and SDK version.

| Configuration | Input given to the model | Tools | Role |
| --- | --- | --- | --- |
| C: copilot | Question | Our tools only | System under evaluation |
| R1: question only | Question | None | Lower bound, reported |
| R2: artifacts in context | Question and the text of all artifacts of the case study | None | Reference of the primary criterion |

- Model: To decide (decision record ADR-0015). The page names the model, its version or digest, the provider and the reasoning setting before the freeze. Reasoning is off unless decided otherwise.
- Repetitions: each question is run 3 times in each configuration, in separate sessions: 20 x 3 x 3 = 180 runs.
- The SDK exposes no temperature or seed. Run-to-run variability is therefore measured by the repetitions and reported; it is not controlled.
- Every measurement comes from a live run. Replayed responses are used for tests and demonstration only and are never measured.
- Order: the 180 runs are executed in an order drawn at random with a recorded seed, so that a drift of the provider does not favour a configuration.

## 4. Metrics

For one run, let C be the set of identifiers cited in the answer, Q the required identifiers, A the acceptable identifiers and G the identifiers that exist in the graph.

| Metric | Definition | Convention |
| --- | --- | --- |
| Recall | \|C ∩ Q\| / \|Q\| | Every question has at least one required identifier |
| Precision | \|C ∩ (Q ∪ A)\| / \|C\| | 0 when C is empty and Q is not |
| Hallucination rate | \|C \ G\| / \|C\|, share of cited identifiers that do not exist | 0 when C is empty; reported per run and pooled over all cited identifiers |
| Time | Seconds from the question to the complete answer | Reported, no threshold in the primary criterion |

- Identifiers are extracted from the answer by a fixed pattern defined with the identifier scheme of the case study; the extraction is unit tested on hand-written examples.
- Precision and hallucination rate are computed twice for the copilot: on the raw answer of the agent, and on the answer returned to the user after the guardrail. Otherwise the metric would measure the guardrail and not the approach. An answer replaced by the fixed reply "no supporting artifact" has an empty C.
- Per question and configuration, each metric is the mean of the 3 repetitions. This gives 20 values per configuration; the question is the unit of analysis.

## 5. Primary criterion

Primary metric: recall, the single metric tested for the comparison (decision of Ferdinand Lacroix, 2026-11-22). The comparison of the primary criterion is C against R2 on recall.

The primary criterion is met when all the following hold:

1. Mean recall of C over the 20 questions is at least 0.90.
2. Mean precision of C, on the raw answer of the agent, is at least 0.90.
3. Pooled hallucination rate of C, on the raw answer of the agent, is at most 5 %.
4. Recall of C is higher than recall of R2, and the difference is significant at the 0.05 level in the paired test of section 6.

Verdict: "accepted" when 1 to 4 hold; "rejected" when 4 fails or when recall is under its threshold; "partially supported" in the other cases, with the list of what holds and what does not. The verdict is stated per threshold, with the measured value.

Thresholds 2 and 3 are read on the raw answer of the agent, before the guardrail; precision and hallucination rate after the guardrail are reported next to them (decision of Ferdinand Lacroix, 2026-11-22). Reason: the guardrail removes identifiers that do not exist in the graph, so a threshold read after it would measure the guardrail and not the approach.

## 6. Statistical analysis

Analysis by the member in charge of statistics (Elio Bonnenfant), written as a script before the runs and run on the frozen result files.

- Unit: the question. Paired values: mean recall of C and of R2 for each of the 20 questions.
- Test: Wilcoxon signed-rank test on the 20 differences, two-sided, level 0.05, exact p-value. Reason: the values are bounded proportions with many ties at 1 and no reason to assume a normal distribution, and the design is paired. Questions with a zero difference are dropped by the test; their number is reported. Sensitivity analysis: a sign-flip permutation test on the mean difference, with the same data; both p-values are reported, and the Wilcoxon result decides.
- Effect size: matched-pairs rank-biserial correlation, and the median of the differences with a bootstrap 95 % interval (10 000 resamples of the questions, recorded seed).
- Several metrics and comparisons: only the test of the primary metric decides the criterion. The other comparisons (precision and hallucination rate of C against R2; the three metrics of C against R1) are secondary: they are reported with p-values adjusted by the Holm procedure and are described as exploratory.
- Variability: for each configuration, the range of the 3 repetitions per question and the number of questions whose 3 answers differ.

Power, computed before any measurement. With 20 paired questions and a two-sided level of 0.05, a power of 0.80 needs a standardized mean difference of about 0.66 for a paired t-test (noncentral t distribution) and about 0.68 for the Wilcoxon test (simulation with normal differences, 4 000 replications: power 0.78 at 0.66 and 0.83 at 0.70). Only large effects can be detected. In addition, the exact test cannot reach 0.05 unless at least 6 questions have a non-zero difference, all in the same direction. If the copilot and R2 both answer most questions perfectly, the test will not be significant whatever the quality of the copilot: a non-significant result is then reported as inconclusive, not as evidence of no difference.

## 7. Secondary criterion: manual baseline

Indicative only; the verdict on the hypothesis does not depend on it.

- 3 participants outside the group, each answering 10 questions: 5 by manual search in the artifacts and 5 with the copilot, in crossed order (the questions and the order are balanced between participants).
- Measured: time per question and correctness against the reference answers. Reported: per participant and per condition, with no test of significance.
- Threshold of the problem statement, read as indicative: time reduced by at least 50 % with the copilot.
- To write before the first session (plan step I3): profile asked of the participants, briefing text, consent to the anonymous use of the timings, what is recorded. Raw data are stored without names.
- If fewer than 3 participants are confirmed on 2026-11-27, the baseline is not run and the secondary criterion is reported as not measured.

## 8. Threats to validity

Classified after Wohlin et al. (conclusion, internal, construct, external).

| Type | Threat | Handling |
| --- | --- | --- |
| Conclusion | 20 questions give low power; ceiling effects reduce it further | Power stated in section 6; effect size and interval reported; a non-significant result is called inconclusive |
| Conclusion | Several metrics and comparisons | One primary metric; Holm adjustment for the others |
| Conclusion | Answers vary from run to run and generation settings cannot be fixed | 3 repetitions per question; variability reported |
| Internal | Questions and reference answers are written by the team that builds the copilot | Frozen before any run; reviewed by a non-author; derived from the reference links by script where possible |
| Internal | The tools may be tuned on the evaluation questions | Smoke questions used in development are separate from the 20 evaluation questions |
| Internal | Provider drift during the runs | Random order of the runs with a recorded seed; dates recorded |
| Construct | Citing the right identifiers is not the same as a useful answer | Stated as a limit; the manual baseline gives a second, indicative view |
| Construct | The guardrail changes precision and the hallucination rate | Thresholds read on the raw answer; values after the guardrail reported |
| Construct | The small case study fits entirely in the context of R2, so the difference with the copilot may be small | Stated; the scaling argument belongs to the discussion, not to the criterion |
| External | One small case study, written in part by the team (model, reference model for the tests) | Stated; no claim beyond this case |
| External | One model and one provider | A replication with another model is reported if the team runs it; otherwise stated as a limit |
| External | 3 participants in the manual baseline | Indicative only |

## 9. Data and reproducibility

- Every run is stored under `eval/` with: question identifier, configuration, repetition, raw answer, answer after the guardrail, tool calls, tokens, duration, model and version, SDK version, date and commit of the code.
- One command recomputes every table of the results page from these files; a unit test checks each metric on a hand-computed example.
- The freeze of this protocol, of the data and of the questions is a tag; the results page cites the tag and lists every deviation.

## 10. Methodological references

Checked under rule R1 by Ferdinand Lacroix on 2026-11-22 against the publisher or JSTOR pages, except where stated. Entries in `docs/references.bib`.

| Use | Reference | Identifier |
| --- | --- | --- |
| Paired test | F. Wilcoxon, "Individual comparisons by ranking methods," *Biometrics Bulletin*, vol. 1, no. 6, pp. 80-83, 1945 | doi:10.2307/3001968 |
| Multiple comparisons | S. Holm, "A simple sequentially rejective multiple test procedure," *Scandinavian Journal of Statistics*, vol. 6, no. 2, pp. 65-70, 1979 | JSTOR 4615733 |
| Effect size | D. S. Kerby, "The simple difference formula: an approach to teaching nonparametric correlation," *Comprehensive Psychology*, vol. 3, article 1, 2014 | doi:10.2466/11.IT.3.1 |
| Experiment design and threats | C. Wohlin et al., *Experimentation in Software Engineering*, Springer, 2012 (1st edition; a 2nd edition exists, 2024) | doi:10.1007/978-3-642-29044-2 |
| Case study method | P. Runeson and M. Höst, "Guidelines for conducting and reporting case study research in software engineering," *Empirical Software Engineering*, vol. 14, no. 2, pp. 131-164, 2009 | doi:10.1007/s10664-008-9102-8 |
| Power | J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed., Lawrence Erlbaum Associates, 1988 | ISBN 0-8058-0283-5 |
