# Repository instructions

This is a personal, documentation-first experimental project. One person may hold the cumulative hats `project_owner`, `method_editor`, `evidence_maintainer`, and `release_authority`.

## Authorities and precedence

Read [governance/authority-map.md](governance/authority-map.md) first for any normative change. Applicable external obligations and the explicit project owner's decision take precedence. Within the repository, [METHOD.md](METHOD.md) is the canonical GFD `0.1-draft` method, followed by accepted records in `governance/decisions/`, then scoped policies and current plans. Examples, templates, research notes, generated output, and historical records are informative.

If two applicable sources conflict, cite both and stop the affected work. Do not resolve the conflict by recency or convenience.

## Validation

Run from the repository root:

```powershell
python -X utf8 scripts/validate_repository.py
python -X utf8 scripts/validate_attempt_governance.py
python -X utf8 -m unittest discover -s tests -v
```

Report each check as `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE`. Never claim that an unrun or unavailable check passed.

Before any first public push, release, or publication-oriented history rewrite, also run:

```powershell
python -X utf8 scripts/audit_publication_privacy.py --history
```

`FAIL` or `UNAVAILABLE` blocks publication. Automated `PASS` does not replace the manual identity, filename, commit-message, contextual-data, and binary-metadata review in [privacy addendum 0002](governance/addenda/0002-publication-privacy-scrub.md). Never copy a matched private value into an issue, commit message, audit report, or chat summary.

## Agent limits

- Separate observed facts, inferences, hypotheses, and proposals.
- Do not invent evidence, commands, results, sources, identities, dates, or authority.
- Do not change acceptance criteria merely to approve an implementation.
- Do not expose secrets, private paths, chat history, or machine-specific configuration.
- Do not publish, push, release, change visibility, alter licensing, or revise authorship without the required human decision.
- Keep `README.md` and `README.fr.md` aligned when their meaning changes.
- Treat changes to `METHOD.md`, `MANIFESTO.md`, authority, precedence, profiles, evidence semantics, license, skill provenance, or public status as `STANDARD` or `ASSURED`, never as an editorial shortcut.
- Never attribute a product failure unless an executed product gate recorded a failed result. Preserve attempt and outcome history through append-only records.
- Treat personal information, secrets, local paths, host and network topology, device identifiers, and unreviewed binary metadata as publication blockers unless the release authority explicitly approved the public value.

## Proposing method changes

Follow [CONTRIBUTING.md](CONTRIBUTING.md). A normative proposal identifies the problem, evidence, alternatives, expected benefit, added friction, risks, and rollback. Preserve the replaced text in Git history and add a decision record when meaning changes.
