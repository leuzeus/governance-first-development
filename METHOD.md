# Governance-First Development method

Status: normative proposal for GFD `0.1-draft`

This document defines the first public draft of Governance-First Development. It is normative only for projects that adopt it, and only within the scope those projects declare. The method is experimental and may change through the process in [CONTRIBUTING.md](CONTRIBUTING.md).

GFD uses the key words `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` to distinguish requirements from advice. A project may adopt only part of the draft, but it must identify omissions instead of claiming full conformance.

## 1. Context before ceremony

A project begins by describing the context that determines useful governance:

- project type and purpose;
- number and relationship of contributors;
- roles assigned to agents;
- users, deployment, and operational responsibilities;
- safety, security, financial, legal, or availability impact;
- hardware, platform, data, and network constraints;
- applicable regulation or contractual duties;
- current maturity, from exploration through maintenance.

The context classification is descriptive. It does not grant authority. A personal project with one owner SHOULD use cumulative hats instead of inventing committees or a separation of duties that does not exist. A project with real operational or regulatory obligations MUST record those boundaries.

Context changes over time. The project MUST review its classification when contributors, users, deployment, criticality, or external duties change.

## 2. Authorities and precedence

An authority map identifies every source that can constrain or approve work. Each entry records its role, status, scope, owner, effective date, precedence, and relationship to other sources.

Common classes include:

- canonical project authorities;
- public contracts and validated schemas;
- accepted decision records;
- domain policies;
- roadmaps and plans;
- historical or superseded documents;
- evidence records;
- external law, regulation, contract, or platform rule;
- generated projections and mirrors;
- operational files and caches.

The project MUST state a precedence rule. A useful default is:

1. applicable external legal, contractual, safety, and security obligations;
2. explicit decisions of the project authority within their scope;
3. public contracts and non-negotiable invariants;
4. the canonical method or project specification;
5. accepted, current decision records and scoped policies;
6. current plans and operational instructions;
7. informative documents, examples, generated views, and historical records.

This default is not automatic. An adopting project MUST confirm or replace it. A newer file does not win merely because it is newer, and a more specific rule cannot bypass a higher invariant unless an authorized decision permits that exception.

When two authorities conflict, work on the affected conclusion or change MUST pause. The conflict record identifies both sources, their scopes, the unresolved point, and the authority that can decide. An agent MUST NOT choose a preferred source silently.

External authority MAY remain outside Git when copying it would be illegal, unstable, or misleading. The repository records a stable citation, access date, scope, owner, and local consequence.

## 3. Intent and objectives

Current intent tells contributors why work exists before it tells them how to implement it. An objective records:

- the desired outcome;
- current non-goals;
- boundaries and constraints;
- success criteria;
- known assumptions;
- authority and owner;
- start, review, and expiry dates when relevant.

An agent MAY clarify or restate an objective. It MUST NOT broaden the objective, promote an assumption to a requirement, or remove a non-goal without the required authority.

Plans and task lists are subordinate to current intent. Completion of a plan does not prove that the outcome is valid.

## 4. Decisions

A decision record is required when a choice would be costly or unsafe to rediscover, reverse, or reinterpret. It includes:

- context and problem;
- considered options;
- decision and rationale;
- consequences, including costs and rejected benefits;
- status and date;
- deciding authority;
- affected contracts, implementation, and evidence;
- replacement link when superseded.

Decision states SHOULD include `proposed`, `accepted`, `rejected`, `deprecated`, and `superseded`. Replacing a decision creates a new record or an explicit amendment. The previous record remains available and points to its replacement.

Minor editorial choices and low-cost implementation details do not need decision records. Recording every choice would hide the decisions that matter.

## 5. Contracts and invariants

Contracts describe observable commitments. Invariants describe properties that must remain true within a declared scope. They may cover:

- technical interfaces and behavior;
- domain rules;
- security and permissions;
- compatibility and migration;
- determinism and reproducibility;
- data ownership, retention, and integrity;
- performance envelopes;
- environment or hardware requirements.

Every invariant identifies its source, scope, rationale, owner, and verification method. An invariant without a feasible check may still be necessary, but its evidence status must remain honest.

Governance profiles MAY change the amount, timing, or location of a check. They MUST NOT silently weaken an invariant. If an invariant changes, an authorized decision records the old rule, new rule, migration or compatibility effect, and evidence required.

Tests that reproduce the implementation algorithm are weak evidence for observable behavior. A project SHOULD prefer checks at the contract boundary.

## 6. Controls

A control exists to reduce a named risk. Its record includes:

- source and protected risk;
- trigger and scope;
- owner or authority hat;
- automatic or manual operation;
- blocking or informative effect;
- result and retained evidence;
- environmental dependency;
- observable cost;
- fallback and rollback;
- exception path and expiry;
- overlap with other controls;
- risk of false blocking.

Projects SHOULD begin with the smallest control that can detect the failure at the right boundary. A targeted check runs before a wider suite. Expensive integration checks SHOULD move to the integration boundary when local execution adds no useful signal.

Human review is a control only when the reviewer has a defined question, relevant access, and enough evidence. A nominal approval does not replace testing or material observation.

Controls that never find defects are not automatically useless, and controls that once found a defect are not automatically permanent. Their value and cost require periodic review.

## 7. Evidence

Evidence is claim-specific. Every evidence record states:

- the claim supported;
- evidence type;
- environment and relevant configuration;
- method or command;
- observed result;
- date and provenance;
- limits and missing observations;
- reproducibility conditions;
- validity period or invalidation trigger;
- one status: `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE`.

`PASS` means the recorded method supported the named claim in the recorded environment. It does not support a broader claim. `FAIL` means the observation contradicted the acceptance condition. `SKIP` means a declared rule permitted an applicable check not to run. `UNAVAILABLE` means the required environment, dependency, permission, or observation could not be obtained.

A document can prove that a decision was recorded. It cannot prove GPU behavior, visual quality, a migration on real data, or production availability. Material claims require material evidence.

An AI-generated summary is not independent evidence. A review by another agent may reduce some shared reasoning errors, but model family, prompts, shared context, and common tests can preserve the same bias. Independence MUST be described, not assumed.

## 8. Time and lifecycle

Every normative artifact declares enough status to distinguish current rules from history, proposals, and projections. The repository SHOULD make these states easy to find:

- current and effective;
- proposed or planned;
- superseded or deprecated;
- historical and non-normative;
- generated projection;
- expired or pending review.

A document does not become authoritative through recency alone. A decision does not disappear when superseded. Evidence expires when its claim, relevant code, environment, method, or validity period changes.

Projects SHOULD detect drift between code and documentation at the narrowest useful boundary. Generated views identify their source and must not be edited as separate truth.

## 9. Context debt

Context debt appears when needed information is absent, duplicated, stale, oversized, badly routed, or available only through private conversation. It affects humans and agents differently, so the project records the consumer and task involved.

Repository instructions SHOULD route readers to stable authorities instead of copying those authorities. Root instructions remain short. Specialized rules live near their domain and declare their scope.

More context is not assumed to be better. The project MAY measure instruction length, loaded files, agent steps, elapsed time, token use, or task success. Metrics require a defined collection method and cannot be reconstructed from memory.

Private conversational memory MAY help an active task, but it cannot be the only source for a durable rule, decision, or completion claim.

## 10. Document governance

Each document has one clear responsibility. Normative truth SHOULD have one maintained source; other documents link to it or summarize it with an explicit status.

The repository records:

- normative and informative documents;
- examples and templates;
- generated views;
- historical records;
- translation relationships;
- archive and replacement rules;
- owners and review triggers.

Translations identify the canonical source and are updated together when meaning changes. If they diverge, the canonical source governs until the difference is resolved and documented.

A new document is justified by a distinct consumer or responsibility. Empty templates, duplicated principles, and enterprise policies without a matching risk SHOULD be removed.

## 11. Agent governance

An agent receives a bounded action scope, permissions, and explicit escalation conditions. Project instructions identify:

- actions the agent may take without a new decision;
- actions that require human authority;
- prohibited changes and protected data;
- required validations and evidence;
- publication, migration, permission, and destructive boundaries;
- how contradictions and missing authority are handled;
- what must remain traceable.

An agent MUST NOT:

- invent evidence, commands, results, identities, or authority;
- change a contract or oracle solely to accept its implementation;
- present absence of failure as positive proof;
- generalize from one environment without stating the limit;
- expose secrets or private machine data;
- expand scope silently;
- publish, migrate, delete, or make an irreversible change without authority.

Multiple agents MAY divide work or review one another. The task record states what was delegated, which evidence each agent obtained, and where shared assumptions limit independence. A human keeps the responsibilities assigned by the project.

## 12. Friction

Governance friction includes elapsed time, loaded context, tokens, validations, coordination, document maintenance, false blocks, delays, and the cost of obtaining evidence. Benefits may include defects found, contradictions exposed, drift corrected, risky actions stopped, or audit time reduced.

Every reported value is marked as:

- measured;
- estimated from named observable proxies;
- unknown.

The project MUST NOT invent historical baselines, avoided incidents, token counts, frequencies, or savings. A qualitative result is acceptable when its basis is stated.

Friction is evaluated with the protected risk. A five-minute check may be excessive for a typo and inadequate for a destructive migration. No universal threshold applies.

## 13. Audit and improvement

Audit depth matches the question:

- `TARGETED` examines a named contradiction, control, risk, or source of friction;
- `STANDARD` samples significant domains and at least three representative change paths, including the most critical applicable path;
- `DEEP` inventories the system and replays all relevant paths when high assurance or a major reform justifies the cost.

An audit separates facts, inferences, and unknowns. It records the commit, branch, Git state, authorities consulted, commands run, commands only inspected, unavailable dependencies, and project context.

Findings describe exact evidence, protected risk, observed cost, confidence, consequence of change, consequence of the status quo, and a bounded recommendation. Reform is not automatic. The authorized owner selects and implements it through the appropriate profile.

After a change, the project checks the predicted signal, residual risk, and friction. A control that does not produce enough value becomes a candidate for narrowing, replacement, or removal through a recorded decision.

## 14. Governance profiles

Profiles select ceremony for a change. Projects may tune them, but each local profile must retain the fields below and name its escalation triggers. `EMERGENCY` is an overlay, not a lower assurance class.

### 14.1 `EXPLORE`

- Objective: learn, reproduce, or test an idea without making a delivery claim.
- Use: read-only diagnosis, disposable analysis, or an isolated prototype.
- Acceptable risk: local and reversible effects confined to a disposable environment.
- Forbidden changes: production writes, publication, persistent migration, real secrets, permission changes, destructive actions, or edits to canonical authority.
- Minimum reading: task objective, safety boundaries, relevant local instructions, and data-handling limits.
- Minimum controls: isolation, target verification, no-secret check, and cleanup or retention decision.
- Expected evidence: observations, reproduction steps, environment, and explicit statement that no delivery claim is made.
- Required authority: task owner within a pre-authorized experimental boundary.
- Escalation: any public surface, persistence, shared state, critical data, or request to ship.
- Compensating controls: sandbox, copy of data, disabled network or writes, and disposable branch where useful.
- Rollback: delete or abandon only the isolated artifacts after confirming their exact scope.
- Regularization: if retained, reclassify the work under `FAST`, `STANDARD`, or `ASSURED` and obtain their evidence.

### 14.2 `FAST`

- Objective: deliver a small reversible change without unnecessary ceremony.
- Use: typo, local documentation correction, narrow internal bug, or additive low-risk configuration.
- Acceptable risk: bounded local regression with an immediate rollback and no critical boundary.
- Forbidden changes: incompatible public behavior, persistence, permission or secret handling, publication, destructive operation, weakened invariant, or unresolved authority conflict.
- Minimum reading: scoped instructions, affected contract or document, and the relevant invariant.
- Minimum controls: targeted check, diff review, secret and private-path scan when content changes, and rollback confirmation.
- Expected evidence: exact change, targeted result, limits, and Git diff.
- Required authority: owner of the affected local scope.
- Escalation: wider behavior, uncertain compatibility, failed targeted check, shared data, or a critical boundary.
- Compensating controls: feature flag, additive change, warning instead of block, or deferred broad suite at integration when justified.
- Rollback: revert the bounded commit or restore the prior local artifact.
- Regularization: no extra document is required unless the change created a decision that would be costly to rediscover.

### 14.3 `STANDARD`

- Objective: deliver significant behavior with reviewable intent, contracts, and evidence.
- Use: internal feature, meaningful refactor, additive public surface, or multi-file documentation change with normative effect.
- Acceptable risk: understood and reversible product risk without critical persistence, permission, secrecy, or destructive effects.
- Forbidden changes: unreviewed incompatibility, uncontrolled migration, secret exposure, silent authority change, destructive action without stronger assurance, or unsupported material claim.
- Minimum reading: objective, affected authorities, decisions, contracts, invariants, and validation instructions.
- Minimum controls: targeted tests, affected integration checks, contract or documentation review, diff review, and stated evidence limits.
- Expected evidence: claim-to-check mapping, commands and results, environment, review outcome, and rollback.
- Required authority: technical or method owner for the affected surface; human approval where the local map requires it.
- Escalation: persistence, compatibility break, permission, security boundary, public release, hardware-only claim, or irreversible effect.
- Compensating controls: staged rollout, feature flag, shadow check, added observability, or time-bounded deferred evidence.
- Rollback: revert or disable the change without data loss; the plan identifies any residual cleanup.
- Regularization: close deferred checks at the stated integration boundary and update affected decisions or contracts.

### 14.4 `ASSURED`

- Objective: make a critical or hard-to-reverse change with evidence at the actual risk boundary.
- Use: persistence, migration, compatibility break, secrets, permissions, security, public release, destructive effects, unsafe or foreign-function code, or required material validation.
- Acceptable risk: only residual risk explicitly accepted by the authorized owner after required controls.
- Forbidden changes: implicit write or publication, missing rollback for a reversible operation, invented proof, unresolved authority conflict, or bypassed safety invariant.
- Minimum reading: all affected authorities, contracts, invariants, threat or failure model, rollback, evidence requirements, and external obligations.
- Minimum controls: preflight, targeted and integration checks, independent or human review where justified, real-environment validation, backup or recovery test, and explicit approval.
- Expected evidence: complete claim mapping, environment identity, commands or procedure, results, limitations, review, approval, rollback readiness, and validity period.
- Required authority: the project hat responsible for the critical boundary, such as release authority, data owner, or security owner.
- Escalation: failed precondition, changed target, unavailable material evidence, rollback uncertainty, or risk beyond the accepted scope.
- Compensating controls: staged execution, dual confirmation, read-only dry run, backup, canary, rate limit, feature flag, audit log, and smaller blast radius.
- Rollback: rehearsed or otherwise supported by evidence appropriate to the effect. Irreversible actions require an explicit acceptance of that fact.
- Regularization: close deferred evidence, reconcile external records, review outcomes, and update the decision when assumptions changed.

### 14.5 `EMERGENCY`

- Objective: reduce immediate harm when the normal path cannot complete in time.
- Use: active incident or urgent exposure with a documented time constraint.
- Acceptable risk: temporary residual risk accepted by the emergency authority because delay is more harmful.
- Forbidden changes: secret exposure, fabricated proof, hidden authority change, unbounded exception, or omission of rollback and expiry without explicit acknowledgment of impossibility.
- Minimum reading: incident scope, critical invariants, target verification, authority, and rollback.
- Minimum controls: two-person or equivalent confirmation when available, smallest blast radius, contemporaneous log, and post-action verification.
- Expected evidence: reason for urgency, skipped controls, compensating controls, exact action, result, residual risk, authority, expiry, and regularization deadline.
- Required authority: the named emergency or release authority. An agent cannot self-declare an emergency.
- Escalation: uncertainty about the target, authority, data loss, safety effect, or inability to observe the result.
- Compensating controls: isolation, temporary disablement, traffic reduction, manual monitoring, backup, and short expiry.
- Rollback: immediate documented route where technically possible.
- Regularization: mandatory review, restoration of normal controls, closure of deferred evidence, and removal or renewal of the exception before expiry.

## 15. Adoption and conformance

A project may begin with an authority map, one objective, applicable invariants, profile selection, and one evidence record. It SHOULD add artifacts only after a recurring risk or consumer justifies them.

A project claiming conformance with GFD `0.1-draft` identifies:

- adopted sections and local adaptations;
- canonical authorities and precedence;
- profile definitions and escalation triggers;
- evidence status vocabulary;
- known omissions and their risk;
- method version and review date.

GFD does not certify the project. Conformance to a process cannot establish the validity, safety, or quality of the resulting software.
