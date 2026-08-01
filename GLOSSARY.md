# Glossary

The definitions below apply to GFD `0.1-draft`. [METHOD.md](METHOD.md) is authoritative when a shorter glossary entry loses necessary detail.

## Agent

A software system that can inspect, reason about, or change project artifacts. An agent has no authority beyond the permissions and decisions granted by the project.

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

## Evidence

An observed result linked to a claim. Evidence records its environment, method, date, provenance, limits, reproducibility, validity period, and status.

## Friction

The cost introduced by governance, including time, context, tokens, approvals, coordination, document maintenance, false blocks, and delayed evidence.

## Governance profile

One of `EXPLORE`, `FAST`, `STANDARD`, `ASSURED`, or `EMERGENCY`. A profile selects proportionate ceremony for a change without weakening applicable invariants.

## Inference

A conclusion drawn from facts but not directly observed. It must be labeled and limited by the evidence used.

## Invariant

A property that must remain true across applicable changes. A profile may change how an invariant is checked, but cannot silently remove it.

## Normative

Binding within its declared scope. A normative source can contain requirements; an informative source explains, illustrates, or records without creating authority.

## Proof status

One of `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE`. `SKIP` means an applicable process deliberately did not run under a stated rule. `UNAVAILABLE` means the needed environment, dependency, or observation could not be obtained.

## Repository-centered

The repository is the primary unit for transmitting and auditing governance. The phrase does not imply that every authority or evidence artifact must physically live in Git.

## Superseded

No longer current because another identified decision or rule replaced it. A superseded artifact remains available as history and cannot be treated as current authority.
