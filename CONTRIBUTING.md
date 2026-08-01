# Contributing

GFD is open to corrections, criticism, cases, failed experiments, and proposals that reduce its scope. Agreement with the method is not a contribution requirement.

## Ways to contribute

You may submit:

- a correction or clearer explanation;
- an earlier or more relevant source;
- a use case or counterexample;
- a measurement with its raw method and limits;
- a critique of a principle or profile;
- a smaller template;
- an adaptation for another agent or tool;
- a change to the reference audit skill;
- a normative change to the method.

Do not include secrets, private repository material, personal chat logs, or claims about projects you cannot document publicly.

## Classify the change

Every contribution chooses one class:

- `editorial`: wording, spelling, formatting, or a link with no change of meaning;
- `informative`: research, example, explanation, or status data that does not change the method;
- `experimental`: a tool, template, profile trial, or measurement awaiting evaluation;
- `normative`: a change to required behavior, authority, evidence semantics, or the canonical method.

If classification is uncertain, use the stronger class and explain why.

## Evidence contributions

State the claim, project context, environment, method, result, date, provenance, limitations, missing data, confounders, and reproduction conditions. Use `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE` only for a named check.

Examples and impressions are welcome when labeled. Do not turn them into measurements after the fact.

## Normative proposals

A normative proposal includes:

1. the problem and affected authority;
2. evidence and its limits;
3. alternatives considered;
4. expected benefit;
5. friction added or removed;
6. new risks and residual risk;
7. migration or compatibility effect;
8. rollback or supersession path;
9. a proposed decision record.

The project owner or delegated method editor must accept the decision before merge. A different agent may review the proposal, but that review does not replace human authority.

## Pull request checks

- Keep the change within its declared class and scope.
- Update both README languages when shared meaning changes.
- Cite direct, stable sources for historical or quantitative claims.
- Preserve skill provenance and license notices.
- Run `python -X utf8 scripts/validate_repository.py`.
- Report unrun checks honestly.

## Reference skill changes

The vendored skill preserves a historical implementation line that predates public GFD. Do not silently rewrite it to match `METHOD.md`. Describe a material divergence in the skill provenance notes, propose the skill change separately, and identify whether it is a limit, debt, or candidate evolution.
