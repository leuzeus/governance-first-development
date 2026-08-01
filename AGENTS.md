# Repository instructions

This is a personal, documentation-first experimental project. One person may hold the cumulative hats `project_owner`, `method_editor`, `evidence_maintainer`, and `release_authority`.

## Authorities and precedence

Read [governance/authority-map.md](governance/authority-map.md) first for any normative change. Applicable external obligations and the explicit project owner's decision take precedence. Within the repository, [METHOD.md](METHOD.md) is the canonical GFD `0.1-draft` method, followed by accepted records in `governance/decisions/`, then scoped policies and current plans. Examples, templates, research notes, generated output, and historical records are informative.

If two applicable sources conflict, cite both and stop the affected work. Do not resolve the conflict by recency or convenience.

## Validation

Run from the repository root:

```powershell
python -X utf8 scripts/validate_repository.py
```

Report each check as `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE`. Never claim that an unrun or unavailable check passed.

## Agent limits

- Separate observed facts, inferences, hypotheses, and proposals.
- Do not invent evidence, commands, results, sources, identities, dates, or authority.
- Do not change acceptance criteria merely to approve an implementation.
- Do not expose secrets, private paths, chat history, or machine-specific configuration.
- Do not publish, push, release, change visibility, alter licensing, or revise authorship without the required human decision.
- Keep `README.md` and `README.fr.md` aligned when their meaning changes.
- Treat changes to `METHOD.md`, `MANIFESTO.md`, authority, precedence, profiles, evidence semantics, license, skill provenance, or public status as `STANDARD` or `ASSURED`, never as an editorial shortcut.

## Proposing method changes

Follow [CONTRIBUTING.md](CONTRIBUTING.md). A normative proposal identifies the problem, evidence, alternatives, expected benefit, added friction, risks, and rollback. Preserve the replaced text in Git history and add a decision record when meaning changes.
