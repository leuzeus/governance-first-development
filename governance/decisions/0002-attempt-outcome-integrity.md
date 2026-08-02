# Decision 0002: Separate execution status from product verdict

Status: accepted

Date: 2026-08-02

Authority: project owner and method editor

## Context

GFD `0.1-draft` defines claim-specific evidence but does not distinguish a failed execution from a failed product. It also lacks a gate-progression record, failure classification, append-only outcome correction, causal lineage, and materiality test. The baseline audit records the gap in `governance/audits/attempt-outcome-baseline.md`.

## Options

1. Add only the principle to the manifesto.
2. Add one combined mutable attempt manifest.
3. Add an immutable attempt declaration plus append-only outcome events, schemas, a validator, focused examples, and corresponding skill checks.
4. Adopt a full incident-management and workflow platform.

## Decision

Choose option 3.

An attempt declaration records purpose, authority, governance identity, planned gates, and the target product gate. Outcome events record execution status, gate results, product verdict, failure classification, causal relations, correction state, and materiality assessments.

The two-layer model keeps the contract small while allowing terminal results and later classifications to remain append-only. It also preserves a lightweight boundary for session occurrences that do not justify a product attempt.

The following rule is normative:

> Never blame the product for a test that never ran.

`product_verdict = failed` is valid only when the target product gate was executed and recorded a failed result. `product_verdict = not_executed` cannot, by itself, justify changing product code.

## Consequences

Benefits expected but not yet validated:

- Agents can route corrections to product, procedure, orchestration, or environment using recorded evidence.
- Historical outcomes can be reclassified without rewriting the original record.
- A correction remains unvalidated until a later attempt records the appropriate causal relation.
- Materiality can prevent editorial or observational changes from forcing unrelated expensive work.

Costs and risks:

- Two JSON record types and a validator add maintenance and context.
- Operators may misclassify failures or create records for trivial session occurrences.
- A valid schema cannot prove that the recorded observation is honest.
- Git append-only checks require a declared baseline and cannot protect records stored outside the inspected repository.

## Compatibility

This is an additive draft extension. Existing GFD adopters may migrate prospectively. A project claims conformance with the attempt outcome integrity extension only when it declares the adopted schema version, record location, authority, and migration boundary.

The audit skill keeps its existing read-only default and audit-depth interface. New checks are additive, so the skill receives a minor version increase from an unversioned baseline to `0.2.0`.

## Expected evidence

- Both schemas parse and the deterministic validator accepts all positive examples.
- Negative fixtures fail for the intended reason.
- An append-only Git test detects modified or deleted historical records.
- The repository validator covers schemas, examples, tests, skill metadata, and package inputs.
- Two packages produced from the same commit have identical SHA-256 values.
- Local installed skill copies remain unchanged during this work.

## Rollback

Supersede this decision, stop requiring new records, retain existing records as historical evidence, and revert the validator and documentation in a new commit. Never delete or rewrite records already cited by a decision or release.

## Replacement

superseded_by: none
