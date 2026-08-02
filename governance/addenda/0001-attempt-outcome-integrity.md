# Addendum 0001: Attempt outcome integrity

Date: 2026-08-02

Status: accepted for implementation in GFD `0.1-draft`

Authority: project owner and method editor

Impact: high

Breaking change: no for existing adopters; yes for future claims of conformance with the attempt outcome integrity extension

## Summary

Add a minimal attempt model that separates operational execution from the verdict about the product. Preserve historical records through append-only outcome events, record gate progression and causal lineage, and require a materiality decision before invalidating evidence or forcing an expensive rerun.

The governing invariant is:

> Never blame the product for a test that never ran.

French formulation:

> Ne jamais attribuer au produit l’échec d’un test qui n’a pas été exécuté.

## Motivation

The current method describes claim-specific evidence but cannot represent whether a product-evaluating gate actually ran. A failed command, pipeline, environment, or session action can therefore be narrated as a product failure without the required observation. The correction target may then move to product code even when the product was never evaluated.

This addendum addresses the gap without making every failed read command a full attempt. A session occurrence becomes a governed attempt only when it was intentionally started to obtain a bounded product result, evidence item, or gate verdict, or when an authority promotes the occurrence because its impact, recurrence, or causal significance requires durable tracking.

## Assumptions

New assumptions:

- Attempt records and outcome events can be stored as small JSON documents.
- A repository can identify which gates evaluate the product.
- Git history or another immutable store remains available for append-only verification.

Removed assumption:

- A single evidence status is sufficient to explain an interrupted multi-gate execution.

## Requirements mapping

| Old requirement | Action | New requirement | Notes |
|---|---|---|---|
| Evidence is claim-specific (`METHOD.md` section 7) | keep | `AOI-REQ-001` | Attempt evidence remains claim-specific |
| Evidence uses `PASS`, `FAIL`, `SKIP`, `UNAVAILABLE` | keep | `AOI-REQ-002` | Proof status remains separate from execution and product verdict |
| Evidence expires when claim, code, environment, method, or validity changes | revise | `AOI-REQ-003` | Expiry requires a materiality decision tied to the affected proof |
| Historical and superseded decisions remain visible | split | `AOI-REQ-004`, `AOI-REQ-005` | Apply append-only history to outcomes and retrospective classifications |
| Agent conclusions remain limited to evidence | revise | `AOI-REQ-006` | A product correction cannot follow solely from `not_executed` |
| Controls identify source, trigger, result, and evidence | split | `AOI-REQ-007`, `AOI-REQ-008` | Gates also identify authority, type, progression, and terminal result |
| Governance friction is measured | keep | `AOI-REQ-009` | Record rerun and classification cost only when observed |
| No current requirement for failure classes | add | `AOI-REQ-010` | Add four primary classes plus temporary `unclassified` |
| No current causal lineage requirement | add | `AOI-REQ-011` | Represent cause, correction, retry, supersession, and validation |
| No current session occurrence boundary | add | `AOI-REQ-012` | Keep ad hoc operational mistakes lightweight unless promoted |

## New requirements

- `AOI-REQ-001`: An attempt is a bounded execution intended to produce evidence, a product result, or a gate verdict.
- `AOI-REQ-002`: Execution status, proof status, gate result, and product verdict are distinct fields and MUST NOT be inferred from one another without an explicit rule.
- `AOI-REQ-003`: Evidence invalidation MUST identify the changed input and explain why the change is material to the claim or gate.
- `AOI-REQ-004`: Terminal outcomes and later classifications MUST be append-only records with stable identifiers.
- `AOI-REQ-005`: A retrospective classification MUST reference the original attempt and prior outcome, state author, date, evidence, confidence, and preserve the original record.
- `AOI-REQ-006`: `product_verdict = failed` requires an executed product-evaluating gate whose recorded result is `failed`. `not_executed` MUST NOT authorize a product correction by itself.
- `AOI-REQ-007`: Each planned gate records a stable identifier, sequence, type, and authority.
- `AOI-REQ-008`: Each terminal outcome records the last successful gate, terminal gate, target product gate execution, result, and evidence.
- `AOI-REQ-009`: Rerun, reconstruction, classification, and governance costs remain measured or unknown; they are never reconstructed from memory.
- `AOI-REQ-010`: Primary failure classification is one of `product_failure`, `operator_error`, `orchestration_error`, `environment_failure`, or temporarily `unclassified`.
- `AOI-REQ-011`: Outcome relations support `retries`, `supersedes`, `caused_by`, `corrects`, `validates_correction_for`, and `invalidated_by`.
- `AOI-REQ-012`: A session occurrence is promoted only when it belongs to a declared attempt or an authority records material impact, recurrence, or causal significance.

## Validation mapping

| Requirement | Test or evidence |
|---|---|
| `AOI-REQ-001` to `AOI-REQ-002` | Attempt and outcome schemas plus positive fixtures |
| `AOI-REQ-003` | Editorial, observational, normative, and material-environment fixture tests |
| `AOI-REQ-004` to `AOI-REQ-005` | Outcome supersession validation and Git append-only test |
| `AOI-REQ-006` | Negative fixture forbidding product failure when the product gate did not run |
| `AOI-REQ-007` to `AOI-REQ-008` | Gate sequence, last-successful-gate, and terminal-gate validator tests |
| `AOI-REQ-009` | Manual status review; no quantitative benefit claim is accepted without data |
| `AOI-REQ-010` | Classification enum and routing tests |
| `AOI-REQ-011` | Causal-lineage examples and reference-integrity tests |
| `AOI-REQ-012` | Synthetic governance fixture that over-promotes trivial session occurrences |

## Migration

Existing projects do not rewrite historical manifests. They may begin at a declared adoption date and add classification sidecars only when an old attempt is material to a current conclusion. A sidecar cites the old record, preserves its original bytes, states confidence, and remains `unclassified` when evidence is insufficient.

No old result becomes conformant merely because a sidecar exists. No prior product verdict is changed without an append-only superseding outcome and supporting evidence.

## Rollback and supersession

If the model proves too costly or ambiguous, supersede this addendum and decision 0002. Preserve existing records and schemas as historical contracts, stop requiring them for new attempts, and publish the migration status. Do not delete outcome history already used to support a claim.
