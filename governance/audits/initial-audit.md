# Initial governance audit

Audit profile: `STANDARD`

Project context: `personal_agent_driven`

Audit date: 2026-08-01

Verdict: ready for owner pre-publication review; not authorized for public push or release.

## Executive summary

The repository has an explicit authority order, one canonical method, visible maturity limits, claim-specific evidence rules, a concise agent router, and a human publication boundary. A later requirement-by-requirement recheck found that two sentences treated the proposed MIT license as already accepted. They were corrected before publication. No remaining contradiction or missing local authority was found that blocks a pre-publication review.

The strict controls around license, skill identity, public status, and publication are justified because those actions affect rights and external state. The largest observed cost is documentary: the pre-release snapshot contained 32 files and 135,474 bytes. Most of that size comes from the user-requested method, research record, and preserved audit skill rather than repeated root instructions. `AGENTS.md` remains 33 lines.

Evidence about GFD's effectiveness is insufficient by design and is labeled as such. The repository can support a claim about what `0.1-draft` proposes. It cannot support a claim that the method improves software projects.

## Scope, method, and evidence state

The audit examined the uncommitted working tree on branch `main` before the first commit. Git had no history and all project files were new. The audit loaded:

1. `governance/authority-map.md`;
2. `METHOD.md`;
3. decision 0001;
4. `LICENSE`;
5. `SECURITY.md`;
6. `AGENTS.md`;
7. `CONTRIBUTING.md`.

It followed their references to `STATUS.md`, `ROADMAP.md`, the prior-art register, release notes, validator, skill provenance, and templates. The commands and results are recorded in [the validation evidence](../evidence/initial-validation.md).

Commands inspected but not executed were the future GitHub repository creation, remote configuration, push, tag, and release commands. They require the owner's pre-publication approval.

## Authority map assessment

The map distinguishes external obligations, owner decisions, contracts, the canonical method, accepted decisions, operational policies, plans, informative documents, the experimental skill, and generated evidence. It states that recency alone does not set precedence and gives a stop rule for conflicts.

`METHOD.md` is the only detailed normative GFD source. The README files summarize it and identify themselves as orientation. The skill is explicitly below the method in precedence and its differences are recorded in `PROVENANCE.md`.

Assessment: no `authority_precedence_gap` or `temporal_authority_conflict` observed.

## Controls examined

| Control | Source | Protected risk | Trigger and effect | Evidence and cost | Disposition |
|---|---|---|---|---|---|
| Authority precedence and conflict stop | Authority map, `AGENTS.md` | Silent rule selection or agent self-authorization | Any conflicting rule; blocks affected work | Manual source review; low per change when routing works | `keep_as_is` |
| Change-profile routing | `METHOD.md`, `AGENTS.md` | Uniform process or weak critical controls | Every change; ceremony varies by risk | Manual classification; cost unknown in real pilots | `requires_more_measurement` |
| Required structure | Validator | Missing publication artifact | Every validation; blocking | Automated `PASS`; negligible observed runtime | `keep_as_is` |
| Internal links | Validator and CI | Broken repository navigation | Every validation; blocking | Automated `PASS`; low observed runtime | `keep_as_is` |
| Bilingual status and shared concepts | Validator plus manual review | Material English/French divergence | Shared meaning changes; blocking for named concepts | Automated and manual `PASS`; full semantic equivalence remains manual | `keep_as_is` |
| CFF fields and schema | Validator plus official schema | Invalid citation metadata | Citation change and release; blocking | One useful block observed and corrected | `keep_as_is` |
| Skill manifest and format | Provenance manifest and official skill validator | Silent skill drift or incomplete copy | Skill change; blocking | Hash and format `PASS`; four exact files | `keep_as_is` |
| Private material scan | Validator | Secret or local-path publication | Every validation; blocking | Automated `PASS`; pattern coverage is limited | `keep_as_is` |
| Publication and writing language scan | Validator plus `avoid-ai-writing` review | Unsupported maturity claim or low-trust prose | Document change; blocking automated subset | One false-positive example; manual second pass `PASS` | `requires_more_measurement` |
| External source links | Optional validator and manual browser review | Dead or misleading citations | Pre-release and source change; informative unless a required source fails | 19 automated responses; two automated `UNAVAILABLE` cases | `keep_but_move_to_integration_boundary` |
| Prior-art and name collision review | Research record, GitHub search | False novelty or name-uniqueness claim | Initial and later name claims; blocking for exclusivity claims | Earlier exact uses found; search is non-exhaustive | `keep_as_is` |
| Human publication approval | Goal, authority map, decision 0001, `AGENTS.md` | Unauthorized public write, visibility, release, or identity choice | First publication and material release; blocking | Approval not yet given | `unsafe_to_relax` |

## Representative paths

### A: editorial correction

Current path: read the scoped document and `AGENTS.md`, confirm no normative meaning changes, apply `FAST`, run the validator, inspect the diff, and revert the commit if needed.

Assessment: pertinent and proportionate. A decision record or full prior-art review is not required.

### D: normative public method change

Current path: read the authority map, `METHOD.md`, accepted decisions, and contribution rules; classify the proposal as normative; record problem, evidence, alternatives, friction, risk, and rollback; update both README files when shared meaning changes; run validation; obtain method-owner approval.

Assessment: pertinent. The manual English/French check cannot be replaced by the current shared-term test.

### F: license, publication, and release

Current path: use `ASSURED`; verify rights, author identity, license, prior terminology, security contact, public status, citation, secrets, skill hashes, links, and release notes; run the initial audit; present the pre-publication summary; wait for owner approval; create and verify the public repository, push, tag, and release.

Assessment: strictness is justified. GitHub state is currently `UNAVAILABLE` because the required approval boundary has not been crossed.

## Classified findings

### F-01: publication boundary is strict and justified

- Category: `strictness_is_justified`
- Evidence: authority-map rows 1 to 3, decision 0001, `AGENTS.md` agent limits, and the unexecuted GitHub operations
- Protected risk: unauthorized publication, wrong visibility, incorrect identity or license, and irreversible external claims
- Cost: one explicit owner review; time unknown
- Confidence: high, because the boundary is stated in several scoped sources with one precedence rule
- Action: `keep_as_is`

### F-02: documentary cost requires measurement

- Category: `necessary_but_expensive`
- Evidence: 32 files, 25 Markdown files, 135,474 bytes before audit artifacts; `METHOD.md` 342 lines; preserved skill source and reference total 22,939 bytes
- Protected risk: missing method coverage, unattributed prior art, unusable templates, and incomplete skill provenance
- Cost: maintenance and context load are estimated from file counts and size; elapsed maintenance cost is unknown
- Confidence: medium; size is observed but burden has not been measured
- Action: `requires_more_measurement`

### F-03: lexical publication gate can false-block cautionary prose

- Category: `false_block_risk`
- Evidence: the first validator pass flagged a sentence warning readers against mistaking the repository for evidence of effectiveness
- Protected risk: unsupported maturity claims
- Cost: one rewording in this run; future frequency unknown
- Consequence of relaxing: an actual maturity claim could pass unnoticed
- Consequence of status quo: contributors may rewrite valid critical prose to satisfy a pattern
- Confidence: high for the observed example, low for future frequency
- Action: `requires_more_measurement`

### F-04: method-effectiveness evidence is absent

- Category: `insufficient_evidence`
- Evidence: `STATUS.md` unknowns and missing cases; no completed lifecycle or controlled baseline
- Protected risk: overclaiming maturity
- Cost of status quo: the project cannot claim effectiveness, which is correct
- Confidence: high
- Action: `requires_more_measurement`

### F-05: semantic review remains a human boundary

- Category: `agent_reasoning_risk`
- Evidence: the validator checks selected terms and links, not claim truth, translation equivalence, or whether evidence supports a broader conclusion
- Protected risk: superficial procedural compliance replacing valid content
- Cost: manual review at normative and release boundaries; time unknown
- Confidence: high
- Action: `keep_as_is`

### F-06: repeated maturity status is intentional duplication

- Category: `strictness_is_justified`
- Evidence: exact status appears in the English README, French README, `STATUS.md`, and planned release notes as required public surfaces
- Protected risk: readers missing the experimental status on entry or release pages
- Cost: synchronized maintenance across four locations; automated checks cover three local surfaces
- Confidence: high
- Action: `keep_as_is`

### F-07: draft licensing language exceeded recorded authority

- Category: `agent_reasoning_risk`
- Evidence: the owner declared authorship of the skill, while the first local draft marked decision 0001 as accepted and said the owner had already selected MIT
- Protected risk: publishing under an unapproved license or attributing a decision the owner did not make
- Cost: one provenance correction, one decision-status correction, and a more explicit approval request
- Confidence: high; the recorded owner message established authorship but did not expressly accept MIT
- Action: `add_compensating_control`; the correction was applied after the read-only audit, and decision 0001 now remains proposed until approval names the public visibility, MIT license, and `LeuZeuS` author identity

## Invariants

The audit found explicit sources for truth about commands, the four evidence states, a source-of-truth order, no implicit publication, secret protection, retained history, provenance and permissions, rollback for critical changes, conclusions limited to evidence, and separation between the method and its skill implementation.

## Friction summary

```yaml
audit_profile: STANDARD
project_context: personal_agent_driven
authorities_loaded: 7
controls_examined: 12
governance_files_implicated: 8
useful_blocks_observed: 2
false_block_risks: 1
deferred_evidence:
  - public repository, description, remote, push, tag, and release verification
  - planned private security advisory URL
  - completed lifecycle and maintenance outcomes
governance_friction: medium
evidence_quality: partial
```

Friction is `medium` because the method and research artifacts are sizable for a personal repository, while the root agent instructions and local validation path remain short. No elapsed maintenance or token baseline exists.

## Exactly one first step recommended

After publication, record a pre-GFD baseline for one pilot before adding or changing that pilot's governance. Use the metric fields in `ROADMAP.md`, keep the pilot change reversible, and stop if the baseline cannot be collected without inventing history.

This step is recommended and has not been executed.

## Limits and final state

The audit covers a new documentation repository, not an operated product. External link automation could not verify the ISO page or the future security-advisory URL. No public write, policy reform, release, migration, production change, or destructive action occurred during the audit.

The working tree remains uncommitted on `main` at the audit boundary. All new files belong to this goal; no pre-existing user changes were present.
