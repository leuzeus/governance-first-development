# Authority map for this repository

Status: current

Owner hats are cumulative and currently held by the GitHub identity `LeuZeuS`: `project_owner`, `method_editor`, `evidence_maintainer`, and `release_authority`.

| Source | Role | Status | Scope | Precedence | Owner | Effective date | Relationship |
|---|---|---|---|---:|---|---|---|
| Applicable law, third-party licenses, and GitHub terms | External obligation | External and current when applicable | Publication, licensing, privacy, platform use | 1 | External authorities; interpreted by project owner | Varies | Cannot be overridden by repository prose |
| Explicit project-owner decision | Human authority | Current within stated scope | Identity, license, publication, security, normative direction | 2 | `project_owner` | Decision date | Must be recorded when it changes durable repository meaning |
| [LICENSE](../LICENSE), [SECURITY.md](../SECURITY.md), public commitments | Accepted contract and policy | Current | Rights, disclosure, and public behavior | 3 | `project_owner` | 2026-08-06 | Constrain public repository and release work under accepted decisions 0001 and 0004 |
| [METHOD.md](../METHOD.md) | Canonical method | Normative proposal | GFD `0.1-draft` | 4 | `method_editor` | 2026-08-01 | Definition and required method behavior |
| Accepted records in `governance/decisions/` | Decision authority | Accepted or superseded as marked | Scope stated in each record | 5 | Named decision authority | Record date | Amend or interpret the method without erasing history |
| [schemas/attempt-record.schema.json](../schemas/attempt-record.schema.json), [schemas/attempt-outcome.schema.json](../schemas/attempt-outcome.schema.json) | Executable contract | Current draft extension | Attempt outcome integrity records | 6 | `method_editor` | 2026-08-02 | Implement METHOD section 7.1 and accepted decision 0002; cannot override either |
| [governance/publication-privacy-policy.json](publication-privacy-policy.json), [scripts/audit_publication_privacy.py](../scripts/audit_publication_privacy.py) | Executable publication control | Current repository policy | Personal data and machine-structure scrub before publication | 7 | `release_authority` | 2026-08-05 | Implement accepted decision 0003; cannot approve an exception or history rewrite |
| [AGENTS.md](../AGENTS.md), [CONTRIBUTING.md](../CONTRIBUTING.md) | Operational policy | Current | Repository work and contribution | 8 | `method_editor` | 2026-08-01 | Implement higher authorities; cannot redefine GFD alone |
| [ROADMAP.md](../ROADMAP.md) and current task plans | Plan | Informative | Future validation and work | 9 | `project_owner` | 2026-08-01 | No authority to claim planned results |
| [README.md](../README.md), [README.fr.md](../README.fr.md), [STATUS.md](../STATUS.md), [GLOSSARY.md](../GLOSSARY.md) | Explanation and status | Informative except exact public status commitments | Orientation and current limits | 10 | `method_editor` | 2026-08-01 | Summarize or contextualize canonical sources |
| `references/`, `examples/`, `templates/` | Research, example, template | Informative | Prior art and adoption aids | 11 | `evidence_maintainer` | Varies | Cannot create a normative requirement |
| `skills/audit-project-governance/` | Experimental implementation | Informative implementation | Governance audit workflow | 12 | Skill author and `method_editor` | Vendored snapshot date | Implements audit checks but does not redefine GFD or its schemas |
| Generated reports, CI logs, GitHub views | Projection or evidence | Non-normative unless a claim cites it | Specific run or view | 13 | Tool and `evidence_maintainer` | Run date | Valid only for the recorded commit and environment |

## Conflict rule

When two applicable sources conflict, the contributor records both sources, stops the affected conclusion or change, and asks the first competent authority in the table. Recency does not create precedence. A scoped lower source can add detail but cannot weaken a higher rule without an accepted decision.

## Replacement rule

A normative change updates the canonical source and adds or amends a decision record. The old decision remains in Git and receives `superseded_by` when replaced. Informative mirrors are updated in the same change or marked temporarily divergent.
