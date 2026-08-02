# Glossary

The definitions below apply to GFD `0.1-draft`. [METHOD.md](METHOD.md) is authoritative when a shorter glossary entry loses necessary detail.

## Agent

A software system that can inspect, reason about, or change project artifacts. An agent has no authority beyond the permissions and decisions granted by the project.

## Attempt

A bounded execution intentionally started to produce evidence, a product result, or a gate verdict. It is declared before the bounded evaluation and retains immutable identity.

## Authority

A person, document, contract, external rule, or controlled process empowered to make a specific decision. Authority has a scope, owner, status, and place in the precedence order.

## Claim

A statement presented as true, such as "the migration preserves version 1 data" or "the release passed its security gate."

## Constraint

A condition that narrows acceptable choices. A constraint may come from an invariant, public contract, environment, policy, decision, or external authority.

## Context debt

The cost and risk created when project context is missing, duplicated, stale, too large, poorly routed, or trapped in private conversation.

## Control

A test, review, gate, approval, observation, or material check intended to reduce a named risk.

## Decision record

A versioned record of a choice, its context, considered options, consequences, authority, status, and replacement history.

## Execution status

The operational state of an attempt or gate, such as prepared, running, completed, failed, cancelled, or superseded. It does not by itself establish a product verdict.

## Failure classification

An evidence-bounded attribution to `product_failure`, `operator_error`, `orchestration_error`, `environment_failure`, or temporarily `unclassified`.

## Evidence

An observed result linked to a claim. Evidence records its environment, method, date, provenance, limits, reproducibility, validity period, and status.

## Friction

The cost introduced by governance, including time, context, tokens, approvals, coordination, document maintenance, false blocks, and delayed evidence.

## Governance profile

One of `EXPLORE`, `FAST`, `STANDARD`, `ASSURED`, or `EMERGENCY`. A profile selects proportionate ceremony for a change without weakening applicable invariants.

## Gate

An ordered control with a stable identifier, type, authority, and declared acceptance condition. A product gate evaluates the product; a preparatory gate does not.

## Inference

A conclusion drawn from facts but not directly observed. It must be labeled and limited by the evidence used.

## Invariant

A property that must remain true across applicable changes. A profile may change how an invariant is checked, but cannot silently remove it.

## Materiality assessment

A recorded decision about whether a changed claim, rule, implementation, method, or environment affects named evidence or gates and therefore requires invalidation or a new attempt.

## Normative

Binding within its declared scope. A normative source can contain requirements; an informative source explains, illustrates, or records without creating authority.

## Proof status

One of `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE`. `SKIP` means an applicable process deliberately did not run under a stated rule. `UNAVAILABLE` means the needed environment, dependency, or observation could not be obtained.

## Product verdict

One of `passed`, `failed`, `not_executed`, `not_applicable`, or `inconclusive`. `failed` requires an executed product gate that recorded a failed result.

## Repository-centered

The repository is the primary unit for transmitting and auditing governance. The phrase does not imply that every authority or evidence artifact must physically live in Git.

## Session occurrence

An operational event such as a read, lookup, command, or path error. It becomes a governed attempt only when declared as one or promoted by an authority for material impact, recurrence, or causal significance.

## Outcome event

An append-only record of a terminal outcome, retrospective classification, materiality assessment, or correction update linked to an immutable attempt.

## Superseded

No longer current because another identified decision or rule replaced it. A superseded artifact remains available as history and cannot be treated as current authority.
