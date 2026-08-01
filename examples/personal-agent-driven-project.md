# Example: a personal offline photo organizer

Status: fictional adoption example, not evidence for GFD

One owner maintains a desktop tool that indexes personal photos without uploading them. Coding agents may implement and review changes. The example shows a small GFD adoption; it does not import the governance of another project.

## Minimal authority map

| Source | Role | Precedence | Owner |
|---|---|---:|---|
| Owner's explicit decision | Product and release authority | 1 | Project owner |
| Public file-format contract | Compatibility invariant | 2 | Project owner |
| Accepted decision records | Design choices | 3 | Project owner |
| Root agent instructions | Work commands and limits | 4 | Project owner |
| Roadmap and issues | Plans | 5 | Project owner |

Conflict rule: the agent stops the affected work and asks the owner. A newer issue cannot override the file-format contract.

## Objective and non-goals

Objective: add duplicate-photo detection for the owner's local library.

Success means the tool identifies byte-identical files and reports them without deleting or uploading anything.

Non-goals: perceptual similarity, cloud sync, automatic deletion, and mobile support.

## Decision

Decision: hash file contents with SHA-256 and store only the hash, size, and local identifier in the existing index.

Rejected option: perceptual hashing. It would widen the objective and create a threshold the owner has not defined.

Consequence: the first scan reads every file and may take longer. The owner accepts that cost for exact duplicate detection.

## Invariant

The application never deletes, modifies, or uploads a photo during indexing. A coding agent cannot relax this invariant or change the test oracle to allow writes.

## `FAST` change

Change: correct the help text from "similar photos" to "byte-identical photos."

Controls: inspect the canonical feature description, change one string, run the documentation link check, and review the diff. Rollback is one commit revert.

Escalation: any change to detection behavior moves to `STANDARD`.

## `STANDARD` change

Change: implement duplicate grouping in the existing index.

Controls: review the objective and invariant, add behavior tests with known duplicate and non-duplicate fixtures, run the index integration test, inspect the database diff, and confirm that no upload or delete path is called.

Evidence: test results support exact grouping only. They do not support performance on the owner's full library.

Rollback: revert the feature commit and rebuild the derived index.

## `ASSURED` change

Change: migrate the persistent index to store hashes.

Controls: back up a copy of the index, run a read-only preflight, test upgrade and downgrade on representative copied data, verify the real application opens the migrated copy, and obtain owner approval before touching the live index.

Evidence must identify the application version, schema versions, copied dataset, commands, results, and limits. A unit test alone cannot prove the live migration path.

## Evidence record

Claim: version 2 opens an index migrated from version 1 and preserves its 120 fixture records.

Status: `PASS` in this fictional example.

Method: copy the version 1 fixture database, record its checksum and row count, run the migration, open it with version 2, and compare the 120 expected records.

Limit: the fixture does not cover corrupted databases or the owner's full library. This record is invalidated by a schema or migration change.

## Exception

During an active data-loss incident, the owner may apply an `EMERGENCY` overlay that disables indexing through a configuration flag. The record names the incident, skipped checks, owner approval, expiry after 24 hours, rollback, and follow-up test. The overlay cannot authorize deleting user photos.

## Targeted audit

Question: can an agent change the duplicate definition without owner authority?

The auditor reads the authority map, objective, decision, invariant, and tests. It reports facts, inferences, and unknowns separately. It proposes a correction only if a concrete path can bypass the owner decision.

## Friction measure

Metric: elapsed governance time for the `STANDARD` change.

Collection: the owner starts a timer for required document reading, evidence writing, and review, then records validation time separately from implementation.

Period: one change.

Limits: timer accuracy depends on manual pauses, the owner already knows the repository, and one change cannot establish an average. The example contains no fabricated duration.
