# Decision 0003: Require a privacy scrub before publication

Status: accepted

Date: 2026-08-05

Authority: project owner and release authority

## Context

The project owner requested an explicit cleaning step for personal information and details that reveal the structure of the author's computer. The current validator checks several text patterns but does not cover the complete Git publication surface or binary metadata.

## Options

1. Keep the existing current-file regex scan.
2. Add only a manual checklist.
3. Add a redacting current-surface scanner, a full-history mode, an explicit public-identity policy, binary review by hash, tests, and a final human review.
4. Automatically delete or rewrite every match.

## Decision

Choose option 3. Apply [privacy addendum 0002](../addenda/0002-publication-privacy-scrub.md) to this repository's first-publication and release workflow.

The regular repository validator runs the current-surface scan. Before the first public push or release, the release authority runs:

```powershell
python -X utf8 scripts/audit_publication_privacy.py --history
```

A `FAIL` or `UNAVAILABLE` result blocks publication. Automated `PASS` is followed by the manual review in the addendum. The scanner reports categories and locations without printing matched values.

## Consequences

The control can find personal data in the index, working tree, Git metadata, or deleted but reachable history. It also makes binary metadata an explicit review boundary.

The scanner may false-block synthetic paths, private-address examples, or intended public contact details. Such content must be replaced with a reserved example, moved to non-public evidence, or approved through a narrow documented policy entry. A pattern exception must never contain a real secret.

Full-history scanning is slower than a current-tree check and cannot prove that contextual personal information is absent. The manual review remains necessary.

## Expected evidence

- A safe synthetic repository passes current and history modes.
- A sensitive current path fails without echoing its value.
- Removed sensitive content passes the current scan but fails the history scan.
- An unapproved Git identity fails without echoing its email.
- An unreviewed binary blob fails.
- The standard repository validator invokes the current-surface scanner.

## Rollback

Supersede this decision, retain the audit history, and remove or narrow the control through a new reviewed commit. Do not publish real matched values as evidence for the rollback.

## Replacement

superseded_by: none
