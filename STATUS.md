# Status of GFD

Version: `0.1-draft`

Publication: approved for a public GitHub repository on 2026-08-06 under the MIT License and the public author identity `LeuZeuS`. This approval does not change the experimental maturity status.

> Experimental proposal — tested only on ongoing projects; no completed full-lifecycle reference implementation yet.

This page separates inherited practice, observed experience, proposed synthesis, and missing evidence. The separation prevents an existing technique or a current experiment from being presented as proof of GFD.

## Practices inherited from existing work

GFD uses ideas with substantial prior history: version control, Architecture Decision Records, risk management, policy as code, machine-readable compliance information, GitOps, specification-driven work, repository instruction files, secure development guidance, and auditable evidence records. [The prior-art review](references/prior-art.md) describes the relation and limits of each source.

## Elements taken directly from the audit skill

The first method draft adopts these structures from `audit-project-governance`:

- facts, inferences, and unknowns are reported separately;
- evidence states are `PASS`, `FAIL`, `SKIP`, and `UNAVAILABLE`;
- audit depth is selected as `TARGETED`, `STANDARD`, or `DEEP`;
- change paths are `EXPLORE`, `FAST`, `STANDARD`, and `ASSURED`, with an `EMERGENCY` overlay;
- controls are assessed with both protected risk and observed cost;
- recommendations require rollback, escalation conditions, and residual-risk disclosure.

The skill is an experimental reference implementation. It is not the normative definition of GFD.

## Synthesis proposed by GFD

The proposal combines repository authority mapping, decision lifecycle, human and agent limits, claim-specific evidence, proportional controls, context debt, and governance-friction measurement in one method. The combination is the proposed contribution. Each component has predecessors.

The attempt outcome integrity extension adds schemas and deterministic checks that separate execution from product verdict, preserve outcome lineage, and require a materiality assessment before invalidating evidence. The examples and tests establish only that the current contracts behave as specified on synthetic cases. No live pilot has yet established better diagnosis, lower rework, or acceptable maintenance cost.

## Observations from ongoing projects

The project owner reports recurring losses of context, contradictory documents, agent drift, weak validation, and governance processes that sometimes cost more than the risk they address. SplatForge and other unfinished projects informed the proposal.

These are experience reports without a controlled baseline. They identify questions; they do not establish causal effects.

## Experimental session audit

The optional [`audit-session-progress`](skills/audit-session-progress/README.md) skill is an additional experimental implementation. It diagnoses a bounded work episode and proposes the next discriminating observation. It does not replace `audit-project-governance`, change `METHOD.md`, mandate periodic audits, or install itself in an agent host.

The initial skill, transfer-analysis guidance, and [evaluation protocol](skills/audit-session-progress/references/evaluation.md) are available. No independent behavioral evaluation or prospective pilot has established diagnostic accuracy, fewer repeated corrections, faster resolution, or acceptable net cost. Package and repository validation concern artifact consistency only. Raw private chat histories are not part of the distribution.

## Unvalidated hypotheses

- An explicit authority map may reduce contradictions and unauthorized rule changes.
- Separating claims from evidence may improve audit accuracy.
- Risk-based paths may preserve critical controls while reducing delay for local reversible work.
- Short, routed context may help agents more than large static instruction files.
- Recording friction may expose controls that should be changed or removed.
- A targeted session audit may identify missing questions or a wrong correction layer without introducing false blocks or disproportionate audit cost.
- Separating execution failures from product verdicts may reduce misdirected product changes.
- Append-only outcome lineage may improve later reconstruction without creating excessive record maintenance.
- Materiality decisions may avoid unrelated reruns without retaining stale proof.

## Unknowns

- Net effect on defect rate, delivery time, token use, and maintenance cost
- Behavior after a product enters long-term maintenance
- Fit for multi-contributor and professional operations
- Portability across agent vendors and models
- Minimum useful set of artifacts for different project types
- Whether the proposed profiles are understandable without expert guidance
- Frequency and severity of false blocks introduced by the method

## Missing evidence and needed cases

No pilot has a recorded pre-GFD baseline. No equivalent project has been run with and without GFD under controlled conditions. Independent human review, cross-vendor trials, completed lifecycle cases, maintenance-period data, and documented counterexamples are still needed.

The attempt outcome model additionally needs prospective pilot evidence for classification accuracy, rate of temporary `unclassified` outcomes, retrospective reclassification cost, false product-failure attribution, false invalidation, rerun cost, and the number of trivial session occurrences correctly left unpromoted.

## Risks created by the method

GFD can fail through bureaucracy, overdocumentation, excessive context, conflicting rules, superficial compliance, false evidence, slower corrections, dependence on one agent, self-justifying governance, weak measurement, or premature transfer of enterprise practices into a personal project.

The method has no exemption from its own scrutiny. A control whose value cannot be observed should be measured, narrowed, or removed after a recorded decision.

## Limits of the initial audit

The initial repository audit covers a new documentation-only project. It cannot test software delivery, production operation, migrations, security boundaries, hardware evidence, or long-term document drift. Link checks and document consistency are useful controls here, but they are not evidence that GFD improves another project.

## Open questions

1. Which governance fields are required for a personal project before the cost exceeds the benefit?
2. Which materiality decisions preserve valid evidence without concealing a changed acceptance boundary?
3. Which agent instructions belong in a root file, and which should be loaded only for a task?
4. How can avoided drift be recorded without inventing a counterfactual?
5. When does a different AI agent count as an independent reviewer?
6. Which additional parts of GFD justify schemas or executable tests without turning ordinary work into record maintenance?
7. When does an operational occurrence justify promotion to a durable attempt record?

The validation program in [ROADMAP.md](ROADMAP.md) is designed to challenge these hypotheses.
