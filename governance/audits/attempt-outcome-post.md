# Attempt outcome governance post-change audit

Audit profile: `DEEP`

Project context: `personal_agent_driven`

Baseline commit: `2c6fe2371fb5cd6ac1eff85bc5a28a33defe4e34`

Audited implementation commit: `c5187ce`

Audited branch and state: `codex/gfd-attempt-outcome-governance`, clean

Audit date: 2026-08-02

Verdict: `conformant` for the repository's internal Attempt Outcome Integrity contract; practical benefit, classification accuracy, and maintenance cost remain unvalidated outside synthetic cases.

## Executive summary

The six baseline findings are addressed at the contract and tooling level. GFD now separates operational execution, gate results, proof status, product verdict, and failure classification. A product failure requires an executed failed product gate. Attempt declarations and outcome events have schemas, terminal gate progression is checked, later classification is append-only, materiality controls proof invalidation, and correction validation requires later evidence.

Eight generic cases exercise product, operator, orchestration, and environment failure; explicit non-applicability; retrospective classification; normative invalidation; and an applied but unvalidated correction. Negative tests reject false product blame, missing progression, premature correction validation, blanket product classification, over-promotion of session occurrences, non-material reruns, missing normative lineage, a wrong retrospective hash, and rewritten history.

The canonical audit skill is version `0.2.0`. Its package has a declared file list, deterministic archive bytes, historical provenance, a non-mutating comparison mode, and an approval-gated apply mode. The personal installation was compared before and after the dry run and remained byte-identical. No installation, publication, remote, or external project was changed.

This is a self-audit of synthetic contracts. It does not show that the model improves a real project, that classifications are honest, or that its record-maintenance cost is acceptable.

## Scope, method, and evidence state

Facts:

- Git identified commit `c5187ce` on branch `codex/gfd-attempt-outcome-governance` with a clean tracked worktree.
- No Git remote is configured.
- The baseline contained 34 tracked files, 27 Markdown files, and 152,660 tracked bytes.
- The audited implementation contains 75 tracked files, 34 Markdown files, and 308,607 tracked bytes: increases of 41 files, 7 Markdown files, and 155,947 bytes.
- The positive corpus contains 9 attempt declarations and 11 outcome events across cases A through H.
- The test suite contains 12 executed tests.
- The canonical package declares 10 files and version `0.2.0`.
- The personal installed copy contained 4 files before and after the dry-run comparison; their relative paths and SHA-256 values were unchanged.
- The repository still states that GFD is an experimental proposal with no completed full-lifecycle reference implementation.

Inference:

- The executable contract closes the baseline representational gap for records that honestly adopt it.
- The session-occurrence boundary and materiality rules reduce two identified false-block mechanisms in the specification, but their net effect in practice is unknown.

Unknowns:

- Frequency of false product blame in live agent work
- Accuracy and inter-reviewer agreement of the five failure classifications
- Classification, reconstruction, and maintenance cost over time
- Whether adopters will record the actual terminal gate honestly
- Portability across projects and agent hosts
- Net effect on product rework, delivery time, and token use

No public release, push, skill installation, or external-project operation was executed. Those actions were outside the authorized repository mutation scope.

## Validation results

| Check | Status | Observed result and limit |
|---|---|---|
| Repository validator | `PASS` | 46 required files; internal links, bilingual status, citation, skill manifest, 27 JSON files, attempt examples, private-material scan, and publication-language scan passed |
| External link network check | `SKIP` | The local validator was run without `--external`; no network availability claim is made |
| Attempt examples and append-only baseline | `PASS` | Verdict `conformant`; 9 attempts, 11 events; all record changes from the baseline were additions |
| Python unit tests | `PASS` | 12 of 12 executed tests passed |
| Official skill structure validator | `PASS` | Reported `Skill is valid!` |
| Deterministic package | `PASS` | Two builds produced SHA-256 `F7CE824922D8A37C8FCA41A43C5D9576E6B79106878714BF4FC7A8557640D463` |
| Installation comparison | `PASS` | Expected drift was reported with dry-run exit code 1; no target file changed |
| Independent agent forward-test | `UNAVAILABLE` | No independent agent execution was available in this audit context; deterministic fixtures were used but are not a substitute for independent review |
| Remote publication and draft PR | `SKIP` | No remote exists and no publication authority was exercised |

The measured local durations for one post-change run were: repository validation 647 ms, attempt validation 386 ms, unit tests 1,988 ms, official skill validation 132 ms, and one package build 145 ms. These are single-machine observations, not performance guarantees or historical baselines.

## Authority map

| Source | Class | Role in this audit |
|---|---|---|
| Explicit project-owner mission dated 2026-08-02 | Human authority | Authorized the bounded method and canonical skill evolution |
| `METHOD.md` section 7.1 | Canonical normative proposal | States the attempt outcome invariant and materiality rules |
| `governance/addenda/0001-attempt-outcome-integrity.md` | Accepted normative addendum | Maps prior evidence requirements to AOI requirements |
| `governance/decisions/0002-attempt-outcome-integrity.md` | Accepted decision | Selects immutable attempts, append-only outcomes, schemas, validator, and skill version |
| `schemas/attempt-*.schema.json` | Executable contract | Defines adopted record syntax below the method and decision |
| `AGENTS.md` and `CONTRIBUTING.md` | Operational policy | Route validation and prohibit false product blame |
| `skills/audit-project-governance/` | Experimental implementation | Audits adopted attempt models without redefining GFD |
| Validator, test, package, and Git outputs | Evidence | Apply only to the recorded commit, environment, and commands |

No conflict was observed among applicable authorities. The schemas remain subordinate to the method and accepted decision. Public-release authority remains separate and unexercised.

## Control inventory

| Control | Protected risk | Evidence and observed cost | Disposition |
|---|---|---|---|
| Product-blame invariant | Product changes based on a test that did not run | METHOD, manifesto, skill, semantic validator, negative fixture | `keep_as_is` |
| Attempt declaration schema | Missing purpose, authority, gate identity, or product target | JSON schema and positive corpus | `keep_as_is` |
| Append-only outcome schema | Mutable history and conflated result types | JSON schema, retrospective case F, Git rewrite test | `keep_as_is` |
| Terminal progression validator | Unsupported last-successful or terminal gate | Semantic checks and negative test | `keep_as_is` |
| Failure routing | Wrong correction layer | Four primary classes plus temporary `unclassified`; live accuracy unknown | `requires_more_measurement` |
| Materiality decision | False invalidation or stale proof | Cases and negative tests for editorial and normative changes | `requires_more_measurement` |
| Session-occurrence boundary | Bureaucracy from recording every tool action | Policy heuristic and anti-pattern fixture | `keep_but_route_conditionally` |
| Correction validation lineage | Applied change presented as verified | Case H and premature-validation test | `keep_as_is` |
| Dynamic skill manifest | Intentional evolution blocked by historical fixed hashes | Versioned 10-file manifest and repository check | `replace_with_executable_test` |
| Deterministic package | Non-reproducible manual copy | Two identical builds; 150 ms observed for one build | `keep_as_is` |
| Dry-run sync with exact approval | Accidental installation overwrite | Drift report, explicit phrase, no deletion, installed bytes unchanged | `keep_as_is` |

## Representative paths A to F

### A: editorial clarification

The materiality model keeps existing proof by default. A new attempt requires an explicit decision identifying a material effect. The negative test detects an editorial rerun imposed without that decision. This is internally conformant; no live false-block rate has been measured.

### B: local operator mistake

Case B records a failed preparatory gate, an unexecuted product gate, `product_verdict = not_executed`, and `operator_error`. The false-product-blame fixture is rejected with `AOI-PRODUCT-BLAME`.

### C: reusable orchestration defect

Case C routes failure to `orchestration_error` before the product gate. The product remains `not_executed`, preserving the actual correction target.

### D: public schema or documented verdict

The additive schemas are governed by an accepted decision, compatibility boundary, templates, examples, and tests. Case D shows an executed but inconclusive product gate when the environment prevents a valid verdict.

### E: evidence identity and canonical skill

Case F binds retrospective classification to the SHA-256 of the original outcome. Case G identifies a normative criteria change, affected gate, invalidated proof, decision, and new attempt. Skill package identity is separate from the historical source snapshot and from any installed copy.

### F: publication and local installation writes

The sync tool is non-mutating by default and requires both `--apply` and the exact versioned approval phrase. The apply path was tested only against a disposable temporary target. The real installed copy was compared, not modified. Publication and push remain skipped.

## Baseline finding disposition

| Baseline finding | Post-change state | Evidence | Residual risk |
|---|---|---|---|
| AOI-01 product failure without product execution | Addressed | Normative invariant plus `AOI-PRODUCT-BLAME` test | Dishonest source records remain possible |
| AOI-02 missing gate progression and classification | Addressed | Schemas, cases A–E, semantic validator | Classification accuracy unmeasured |
| AOI-03 no append-only retrospective classification | Addressed | Case F hash binding and rewrite test | Store outside Git may lack append-only enforcement |
| AOI-04 no materiality rule | Addressed at contract level | Case G and editorial/normative negative tests | Live invalidation decisions unmeasured |
| AOI-05 unreproducible skill delivery | Addressed | Version, manifest, deterministic package, dry-run sync | User must review overlapping local customization |
| AOI-06 proportional personal governance | Preserved with added friction | Session-occurrence boundary and no organizational roles added | Repository size increased materially |

## Attempt Outcome Integrity

Verdict: `conformant` for the audited repository records and executable contract.

The validator accepts the eight required generic scenarios, rejects the specified false-attribution and lineage failures, and confirms that all tracked record changes from the pre-extension baseline are additions. This verdict does not evaluate a production product, a real pilot attempt, or the truth of synthetic evidence references.

## Friction summary

```yaml
audit_profile: DEEP
project_context: personal_agent_driven
authorities_loaded: 8
controls_examined: 11
governance_files_implicated: 41
useful_blocks_observed: 10
false_block_risks: 2
deferred_evidence:
  - live classification accuracy and agreement
  - long-term record maintenance cost
  - material workload rerun cost
  - independent agent and human review
governance_friction: medium
evidence_quality: sufficient_for_internal_contract_only
```

The 10 useful blocks are distinct negative behaviors asserted by the tests, not production defects found. Friction remains `medium`: the local checks complete in seconds, but the audited snapshot has 41 more tracked files and 155,947 more bytes than the baseline, and no pilot has measured ongoing record maintenance. The two false-block risks are over-promotion of session occurrences and over-broad evidence invalidation; both now have controls, but their field behavior is unknown.

## Residual findings

### POST-01: schema conformity cannot prove honest observation

- Category: `insufficient_evidence`
- Severity: high
- Confidence: high
- Evidence: validators compare internal fields and file history; they do not observe the product or execution environment
- Recommendation: require material evidence at the product gate and sample source logs during pilot review
- Action: `requires_more_measurement`

### POST-02: maintenance and classification friction are unmeasured

- Category: `necessary_but_expensive`
- Severity: medium
- Confidence: high
- Evidence: one local run measured seconds, but no prospective pilot or maintenance period exists
- Recommendation: collect declared attempt, classification latency, reclassification, rerun, and unpromoted-occurrence data prospectively
- Action: `requires_more_measurement`

### POST-03: independent forward-test is unavailable

- Category: `insufficient_evidence`
- Severity: medium
- Confidence: high
- Evidence: no independent agent or human report accompanies commit `c5187ce`
- Recommendation: obtain a review whose shared model, prompts, context, tests, and oracle are disclosed
- Action: `requires_more_measurement`

## Exactly one first step recommended

Select one non-critical consenting pilot and predeclare a single bounded attempt, its product gate, collection timing, and stop condition before execution; rollback by ending the pilot without changing the project's existing acceptance criteria. This step is recommended and was not executed in this audit.

## Limits and final state

This audit is authored in the same implementation effort and is not independent. Synthetic references such as `evidence://` and `decision://` demonstrate structure only. The external link check was skipped. The package archive is an ignored local build artifact, not a published release.

The audited implementation commit was clean. No remote is configured. No public release, draft pull request, license decision, installed skill, `.agents` skill copy, SplatForge repository, pilot repository, or external project was changed.
