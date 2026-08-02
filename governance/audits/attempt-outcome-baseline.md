# Attempt outcome governance baseline audit

Audit profile: `DEEP`

Project context: `personal_agent_driven`

Audited commit: `2c6fe2371fb5cd6ac1eff85bc5a28a33defe4e34`

Audited branch and state: `main`, clean

Audit date: 2026-08-02

Verdict: `non_conformant` for attempt outcome integrity; the repository has no current contract that can prove whether a product gate ran before a product failure is assigned.

## Executive summary

GFD already separates claims from evidence and requires honest `PASS`, `FAIL`, `SKIP`, and `UNAVAILABLE` states. It also rejects documentary evidence as a substitute for material observation. Those controls are useful foundations.

The audited snapshot has no model for an attempt, execution status, product verdict, gate progression, failure classification, causal lineage, append-only reclassification, or materiality. It contains no schemas, tests, fixtures, packaging tool, or installation comparison tool. The reference skill can detect unavailable environmental validation, but it does not prohibit a product correction when the product gate never executed.

The repository remains proportionate for a personal experimental project. The correction should add one small interoperable record model, one append-only outcome model, one validator, and focused fixtures. It should not turn every mistyped read command into a governed product attempt.

## Scope, method, and evidence state

Facts:

- Git identified the current working directory as the repository root.
- `main` was clean at the audited commit and had no remote.
- The repository contained 34 tracked files, 27 Markdown files, no schema files, no test or fixture directories, and no packaging or skill-sync tool.
- `python -X utf8 scripts/validate_repository.py` passed all local checks and reported external links as `SKIP`.
- The official skill validator reported `Skill is valid!`.
- The four functional files in the canonical skill matched the `.codex` installation byte for byte. The repository also contained `README.md` and `PROVENANCE.md`; the `.agents` installation did not exist.

Inference:

- A green repository validation cannot support attempt outcome integrity because the validator has no check for that property.

Unknowns:

- No project using GFD has recorded data showing how often product failures are currently misclassified.
- The cost of the proposed records in long-running material workloads has not been measured.
- No independent reviewer evaluated this baseline.

Commands inspected but not executed include publication, remote configuration, push, release, and local skill synchronization. They are outside this audit and require separate authority.

## Authority map

| Source | Class | Role in this audit |
|---|---|---|
| Explicit project-owner mission dated 2026-08-02 | Human authority | Authorizes this bounded method and skill evolution |
| `METHOD.md` | Canonical normative proposal | Defines evidence, lifecycle, controls, agents, friction, and audit |
| `governance/decisions/0001-initial-method-and-license.md` | Proposed decision | Governs future publication only; it does not authorize public release |
| `AGENTS.md` and `CONTRIBUTING.md` | Operational policy | Require precedence review, proportional changes, validation, and a decision for normative meaning |
| `STATUS.md` and `ROADMAP.md` | Informative status and plan | Preserve experimental limits and missing evidence |
| `skills/audit-project-governance/` | Experimental implementation | Supplies the baseline audit workflow but is also under evaluation |
| Validator output and Git observations | Evidence | Apply only to the audited commit and commands actually run |

No authority conflict was observed. The project-owner mission adds a normative requirement without accepting the still-proposed public-release decision.

## Control inventory

| Control | Source and trigger | Protected risk | Evidence and observed cost | Disposition |
|---|---|---|---|---|
| Claim-specific evidence | `METHOD.md:136-153`, every completion claim | Overbroad proof | Manual record semantics; cost unknown | `keep_as_is` |
| Four proof states | `METHOD.md:147-149`, each evidence result | Hidden skip or unavailable check | Present in prose and validator reports | `keep_as_is` |
| Material evidence boundary | `METHOD.md:151`, material claims | Documentary substitution | Manual review | `keep_as_is` |
| Evidence invalidation | `METHOD.md:166`, changed claim, code, environment, or method | Stale proof | Scope is broad but no materiality test exists | `keep_but_route_conditionally` |
| Agent evidence limits | `METHOD.md:207-218`, agent work | Invented or generalized proof | Manual instructions | `add_compensating_control` |
| Repository validator | `scripts/validate_repository.py`, local and CI runs | Missing files, broken links, private material, stale skill snapshot | Automated and fast in the observed run | `automate` |
| Fixed skill snapshot hashes | `scripts/validate_repository.py:37-58`, every validation | Silent vendor drift | Detects drift but also blocks any intentional skill revision until edited | `keep_but_route_conditionally` |
| Human publication approval | authority map and decision 0001 | Unauthorized public release | Not yet granted | `keep_as_is` |

## Representative paths A to F

### A: editorial clarification

The current path uses `FAST`, a targeted diff review, and repository validation. It is proportionate. No rule currently states that an editorial change preserves prior attempt validity, so an adopting project may still trigger an unnecessary rerun.

### B: local operator mistake

A mistyped path or command can be described as a failed command, but the method does not define a session occurrence or prevent promotion to a product failure. The missing separation is material because an agent may inspect product code without evidence that the product ran.

### C: reusable orchestration defect

The method recognizes controls and workflows but has no primary classification for an encoded pipeline or script error. The correction target may therefore be selected by narrative rather than contract.

### D: public schema or documented verdict

Adding attempt and outcome schemas changes a public contract and requires a normative decision, migration notes, fixtures, and versioned validation. Those controls are pertinent.

### E: evidence identity and canonical skill

The method knows that evidence can expire, but it has no test for whether a changed document, schema, product artifact, or environment is material to a specific proof. The canonical skill and installed copies also have no deterministic compare, dry-run, or explicit sync mechanism.

### F: publication and local installation writes

Both remain prohibited without explicit approval. The current task authorizes changes only inside the repository. No remote, public release, or installed skill may be modified.

## Classified findings

### AOI-01: product failure can be assigned without product execution

- Category: `agent_reasoning_risk`
- Severity: high
- Confidence: high
- Evidence: `METHOD.md:136-153` defines evidence states but no execution status or product verdict; the skill contains no `not_executed` rule
- Protected risk: agents changing product code in response to an operator, orchestration, or environment failure
- Cost of status quo: wrong correction target and repeated work; frequency is unknown
- Recommendation: add an invariant that `product_verdict = failed` requires an executed product-evaluating gate with failed evidence
- Action: `add_compensating_control`

### AOI-02: gate progression and failure classification are absent

- Category: `validation_debt`
- Severity: high
- Confidence: high
- Evidence: no tracked schema, fixture, or method field records last completed gate, terminal gate, target gate execution, or the four requested primary failure classes
- Protected risk: ambiguous terminal state and unsupported causal claims
- Cost of status quo: manual reconstruction; time and frequency are unknown
- Recommendation: add a minimal record contract and validator
- Action: `replace_with_executable_test`

### AOI-03: retrospective classification has no append-only contract

- Category: `documentation_debt`
- Severity: medium
- Confidence: high
- Evidence: `METHOD.md:166` preserves superseded decisions, but no equivalent mechanism exists for historical attempt outcomes
- Protected risk: silent history rewriting
- Cost of status quo: provenance depends on Git archaeology and narrative
- Recommendation: introduce outcome sidecars that identify author, date, evidence, confidence, and target attempt
- Action: `add_compensating_control`

### AOI-04: evidence invalidation lacks materiality

- Category: `false_block_risk`
- Severity: medium
- Confidence: high
- Evidence: `METHOD.md:166` expires evidence when its claim, code, environment, method, or validity period changes without stating whether the change affects the proof
- Protected risk: stale evidence
- Consequence of status quo: editorial or observational changes may force expensive reruns
- Recommendation: require a materiality decision before invalidation or rebuild
- Action: `keep_but_route_conditionally`

### AOI-05: canonical skill delivery is not reproducible

- Category: `manual_but_automatable`
- Severity: medium
- Confidence: high
- Evidence: no tracked package, package manifest, comparison tool, dry-run, or sync command exists
- Protected risk: local installation drift and accidental overwrite
- Cost of status quo: manual copying and hash comparison
- Recommendation: add deterministic packaging and an approval-gated compare/sync tool
- Action: `automate`

### AOI-06: current governance remains proportionate

- Category: `strictness_is_justified`
- Severity: informational
- Confidence: high
- Evidence: concise root instructions, one canonical method, one validator, cumulative owner hats, and no committee or service-level machinery
- Protected risk: organizational overreach
- Recommendation: keep the new required fields minimal and allow session occurrences to remain lightweight
- Action: `keep_as_is`

## Attempt Outcome Integrity

Verdict: `non_conformant`.

The audited snapshot cannot represent or validate the distinction between pipeline failure, interrupted execution, product failure, product not executed, and gate not applicable. No evidence contradicts that conclusion. The existing proof vocabulary remains useful but applies at a different layer.

## Friction summary

```yaml
audit_profile: DEEP
project_context: personal_agent_driven
authorities_loaded: 7
controls_examined: 8
governance_files_implicated: 9
useful_blocks_observed: 0
false_block_risks: 1
deferred_evidence:
  - frequency of attempt misclassification in pilot projects
  - material workload rerun cost
  - independent skill review
governance_friction: medium
evidence_quality: partial
```

Friction is `medium` because the current repository is small and routed clearly, but the proposed change spans normative prose, executable contracts, tests, and a distributed skill. No elapsed time or token cost was measured.

## Incremental and reversible plan

1. Add a requirements delta and accepted decision scoped to attempt outcome integrity. Rollback: supersede the decision and remove the new contract before adoption.
2. Add the minimal schemas, examples, validator, and deterministic fixtures. Stop if the contract cannot express the eight required cases without project-specific fields.
3. Update the canonical method and explanatory mirrors. Stop if the experimental status or authority order becomes ambiguous.
4. Extend and version the skill without changing its read-only default. Stop if official skill validation or deterministic tests fail.
5. Package the canonical skill, compare installations without writing them, and run a post-change self-audit. Stop before publication or installation sync.

## Exactly one first step recommended

Create a requirements delta that maps the current evidence and lifecycle requirements to a minimal attempt outcome contract, with rollback by superseding the addendum before any adopter relies on it. This step is recommended here and was not executed within the baseline audit.

## Limits and final state

This audit evaluates the GFD documentation repository, not SplatForge or any product attempt. It does not establish that the proposed model will reduce errors in practice. The auditing skill is not an independent reviewer of its own repository. No policy, gate, workflow, schema, product code, public repository, installed skill, or external project was modified while producing the audited conclusions.
