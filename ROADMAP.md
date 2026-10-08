# Validation roadmap

Status: informative plan for testing GFD `0.1-draft`

This roadmap is organized around questions that could weaken, revise, or reject the method. Adding documents is not progress unless it improves a measured decision, control, or audit.

## Phase 0: establish the publication baseline

Before the first public release:

- record the repository commit, authority map, method version, and initial audit;
- validate internal links, source metadata, translations, citation metadata, licence, and vendored-skill provenance;
- run the redacting current-surface and full-history privacy scans, then review intended public identities, filenames, contextual personal data, and binary metadata;
- record unresolved findings in [STATUS.md](STATUS.md);
- publish no performance or quality claim that lacks a recorded method.

Exit condition: a third-party reader can distinguish normative text, observations, hypotheses, examples, and evidence gaps.

## Phase 1: instrument pilot projects

For each pilot, establish a baseline before changing its governance. Record the project context, current authorities, existing controls, typical change paths, known false blocks, available timing or token data, and gaps in historical measurement.

Do not reconstruct missing history. The baseline begins when collection begins.

Each governance change receives a dated log entry with:

- reason and hypothesis;
- affected path and risk;
- previous and new control;
- expected benefit and added friction;
- rollback and review date;
- observed outcome.

For attempt outcome integrity pilots, also record:

- declared attempt and target product gate;
- last successful and terminal gate;
- product-gate execution and product verdict;
- initial and retrospective failure classification;
- correction state and the later attempt, if any, that validates it;
- materiality decision, affected proof, and rerun choice;
- time spent recording, classifying, reconstructing, and rerunning;
- session occurrences intentionally not promoted to attempts.

## Phase 2: run bounded comparisons

Where safe and affordable, compare periods, tasks, or matched projects with different governance treatments. Candidate experiments include:

- short routed agent instructions versus a larger static context file;
- targeted checks before full suites versus full suites on every change;
- explicit claim-to-evidence records versus unstructured completion summaries;
- `FAST` and `STANDARD` routing versus one uniform process;
- same-agent review versus a different agent and human review.
- targeted session diagnosis with `audit-session-progress` versus an ordinary continuation, where the tasks and available evidence are sufficiently comparable.

Comparisons must state assignment method, sample size, model and version, task type, environment, exclusions, and stopping rule. An exploratory result remains exploratory.

The [session-audit protocol](skills/audit-session-progress/references/evaluation.md) starts with dated episodes read at a fixed cutoff, with later outcomes hidden. Include repeated corrections, failed reference transfers, external dependencies, incomplete histories, and productive long investigations. Record confirmed and rejected findings, questions that change a decision, false blocks, and audit cost. Historical replay tests diagnosis; a prospective baseline is needed before making a claim about time saved or resolution. Keep raw private traces in their authorized location and review any shareable summary before publication.

## Phase 3: complete a lifecycle and maintenance period

After the first pilot release, review the method at two boundaries:

1. after the first complete product delivery;
2. after a declared maintenance period long enough to observe stale context, superseded decisions, and evidence expiry.

The review asks which controls prevented a named failure, which created false blocks, which documents drifted, and which decisions remained understandable to a new contributor.

## Phase 4: test portability

Run equivalent tasks with several agent providers and models. Preserve prompts, available tools, repository state, and evaluation criteria. A different provider does not make a review independent when both agents share the same incorrect authority or test oracle.

Add a collaborative pilot only when real contributors participate. Add a professional or regulated pilot only when its operators and authorities approve the evidence plan.

## Phase 5: revise or abandon

Collect counterexamples throughout the program. A principle or control becomes a candidate for revision or removal when it repeatedly adds cost without protecting an observed risk, cannot be applied consistently, or creates worse failure modes than the one it targets.

Publish negative and unavailable results. GFD should be abandoned or narrowed if its core synthesis does not produce enough value relative to its friction.

## Required observations

The program will track, when observable:

1. initial state for each pilot;
2. governance changes;
3. friction introduced;
4. useful blocks;
5. false blocks;
6. contradictions detected;
7. drift prevented or corrected, without invented counterfactuals;
8. context and token use when direct data exists;
9. audits by an agent other than the implementer;
10. human review of agent conclusions;
11. comparison with non-GFD periods or projects when feasible;
12. results after first complete delivery;
13. results after maintenance;
14. trials across agent providers;
15. counterexamples;
16. revisions, rejected claims, and abandoned principles.

## Metric records

Every metric record includes: definition, collection method, period, provenance, limitations, missing data, and confounders. The following set is a starting point, not a mandatory dashboard.

| Metric | Definition | Collection method | Period | Provenance | Main limits, missing data, and confounders |
|---|---|---|---|---|---|
| Governance elapsed time | Time spent reading, recording, approving, and validating due to governance | Timer or timestamped task log with included activities | Per change and release | Human log plus tool timestamps | Multitasking, learning effects, incomplete logs |
| Context loaded | Bytes, lines, files, or tokens loaded because of project governance | Agent trace or deterministic file count; tokens only from provider telemetry | Per task | Trace and repository commit | Provider tokenization, cached prompts, hidden system context |
| Validation time | Elapsed time for required checks | Timed command wrapper or CI timestamps | Per check and change | Command log or CI run | Queue time, cold caches, shared runners |
| Useful block | A control stopped a change with a confirmed defect or unauthorized effect | Finding linked to failed control and later disposition | Per change, summarized quarterly | Gate result, diff, reviewer decision | Confirmation bias; defects found later may be missed |
| False block | A control stopped acceptable work for a reason unrelated to the protected risk | Block record plus authorized resolution | Per change, summarized quarterly | Gate log and decision record | "Acceptable" can change after review |
| Contradiction detected | Two applicable sources made incompatible claims | Audit finding citing both sources and scope | Per audit | Immutable commit references | Search coverage and interpretation |
| Corrected drift | A current artifact was brought back into agreement with its authority | Before and after diff plus authority citation | Per correction | Commit and finding | Does not prove future drift was avoided |
| Rework | Work repeated because intent, authority, or acceptance criteria were wrong or missing | Issue or task log linked to replaced change | Per milestone | Git and task history | Attribution to governance is often uncertain |
| Audit reconstruction time | Time for a new reviewer to locate authority, decisions, and evidence for a sampled claim | Timed audit protocol on a fixed commit | Per sampled claim | Reviewer log | Reviewer skill, repository familiarity, model differences |
| Evidence coverage | Accepted claims with evidence records divided by accepted claims sampled | Audit sample with explicit denominator | Per release | Release claims and evidence index | Claim selection can bias the ratio |
| Agent task outcome | Result against predeclared acceptance criteria | Gold test, human rubric, or material observation | Per task and experiment | Test output and review record | Benchmark validity, model drift, task difficulty |
| Maintenance burden | Time and edits required to keep governance artifacts current | Git diff classification and timer | Monthly or milestone | Git history and maintainer log | Mixed editorial and normative changes |
| False product blame | Outcome records assigning product failure without an executed failed product gate | Schema and semantic validator plus sampled source evidence | Per attempt, summarized per pilot | Immutable attempt and outcome events | Honest recording still requires review |
| Classification latency | Time from terminal outcome to supported primary classification | Event timestamps with a stated clock source | Per classified failure | Append-only outcome lineage | Queuing and reviewer availability |
| Retrospective classification cost | Work needed to classify a preserved historical outcome | Timer and changed-file count | Per addendum | Review log and Git diff | Reviewer familiarity and evidence quality |
| Rerun avoided or required | Materiality decisions retaining or invalidating named proof | Decision sample with affected gates and subsequent attempts | Per change | Materiality event and attempt lineage | Avoided work is not a benefit unless the retained proof remains valid |
| Attempt promotion rate | Session occurrences promoted to governed attempts | Declared occurrences and promotion bases within a predeclared sample | Per task sample | Session log and attempt records | Hidden tool actions and inconsistent occurrence boundaries |

## Audit independence record

An audit claiming independence states:

- implementer and reviewer identities or agent configurations;
- shared prompts, models, tools, tests, and context;
- whether the reviewer could alter the acceptance oracle;
- human review performed;
- unresolved common-mode risks.

The label "different agent" by itself is insufficient.

## First planned study

The first study will compare the repository's concise root `AGENTS.md` with a deliberately expanded variant in isolated runs. It will measure task success, steps, loaded context, elapsed time, and instruction compliance on a small predeclared task set. The expanded variant will not replace the root file unless results justify that decision.
