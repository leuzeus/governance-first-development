# Governance-First Development

[Lire en français](README.fr.md)

> Experimental proposal — tested only on ongoing projects; no completed full-lifecycle reference implementation yet.

Governance-First Development (GFD) is a draft method for software repositories built by humans and AI coding agents. It keeps authority, intent, decisions, constraints, validation requirements, and evidence beside the code and under version control.

This repository publishes a proposal, not a proven standard. Its claims are deliberately narrow, and its open questions are tracked in [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md).

## The problem

AI agents can change a repository faster than a new contributor can reconstruct its history. Important rules often remain scattered across conversations, issue trackers, stale plans, and one agent's private memory. A passing test may then be mistaken for proof of a wider claim. An agent may also change a requirement, test, or document until its own implementation appears compliant.

Adding more instructions does not solve this by itself. Long context files and uniform approval processes can increase cost, hide the rule that matters, and delay small reversible fixes. GFD treats governance friction as something to measure, not as an acceptable side effect.

## Where the proposal came from

The sequence was practical:

1. Problems appeared during AI-assisted work on several ongoing projects: lost context, conflicting documents, agent drift, weak validation, and slow procedures.
2. Existing practices were examined, including Architecture Decision Records (ADRs), repository instructions, policy as code, GitOps, specification-driven development, and versioned documentation.
3. The project owner created and refined `audit-project-governance`, a local audit skill for finding governance failures and proposing risk-proportionate corrections.
4. The skill was used on ongoing projects, including SplatForge, as an experimental tool.
5. The recurring ideas were separated from the skill and shaped into GFD.
6. This repository now exposes the proposal to criticism, counterexamples, and measurement.

Those projects are observation sites. None is a completed validation of GFD.

## Working definition

> Governance-First Development is a repository-centered software development approach in which project authority, intent, decisions, constraints, validation requirements, and evidence evolve alongside the code so that humans and AI agents can develop, understand, verify, and audit the project reliably.

The repository is the main transmission and audit unit. External authorities can still apply, but the repository must identify them, state their scope, and explain their precedence.

## What changes when agents write code

An agent can read rules, edit the implementation, update tests, and rewrite explanations in one run. That compression of roles creates a specific risk: the same actor may alter both a claim and the evidence used to accept it.

GFD responds by separating five things that are often blurred together:

- intent: what outcome is sought;
- decision: which option an authorized person or process selected;
- implementation: what changed in the repository;
- test: which behavior was checked;
- evidence: what result supports a stated claim, on which environment, and with which limits.

This separation helps a new human or a third-party agent check the project without relying on private chat history. It can also make an external audit easier because claims point to authorities and evidence instead of summaries alone. Whether it improves outcomes enough to justify its cost remains an experimental question.

## The proposed method

GFD asks a project to keep only the governance it can explain and maintain:

- an authority map with an explicit precedence rule;
- current intent, non-goals, contracts, and invariants;
- decision records that remain visible when superseded;
- controls selected according to risk;
- evidence records tied to specific claims;
- honest states for unavailable or deferred validation;
- a record of governance friction and false blocks;
- periodic audits of both the project and its governance.

The canonical description is [METHOD.md](METHOD.md). The shorter [MANIFESTO.md](MANIFESTO.md) states the initial principles.

## Risk-proportionate paths

GFD proposes five profiles. They adjust ceremony, not invariants.

| Profile | Intended use |
|---|---|
| `EXPLORE` | Read-only investigation or isolated prototype with no delivery claim |
| `FAST` | Local, low-risk, reversible change with no critical boundary |
| `STANDARD` | Significant internal behavior or an additive public surface |
| `ASSURED` | Persistence, compatibility, permissions, secrets, publication, destructive effects, or required material proof |
| `EMERGENCY` | Time-bounded overlay with compensating controls, rollback, expiry, and later regularization |

## Minimal adoption

A personal project can start without copying this whole repository:

1. Name the current authority for requirements and identify what overrides what.
2. Write one current objective and its non-goals.
3. Record decisions that would be costly to rediscover.
4. State the invariants an agent cannot relax.
5. Select `FAST`, `STANDARD`, or `ASSURED` for each delivered change.
6. Attach evidence to the claims made at completion.
7. Record one friction measure, even if it is only elapsed validation time with a stated collection method.

See [the personal project example](examples/personal-agent-driven-project.md) and the [templates](templates/).

## What GFD is not

GFD is not a replacement for AI governance, Responsible AI, GitOps, DevSecOps, policy as code, compliance as code, ADRs, specification-driven development, or `AGENTS.md`. It can use those practices where they fit.

It is also not a claim that Markdown creates governance. A rule matters only when its authority, scope, lifecycle, enforcement, and evidence are understood. Some rules belong in executable checks. Others require human judgment or material validation.

The phrase "governance-first development" and neighboring "governance-first" formulations have prior public uses. [The prior-art review](references/prior-art.md) records examples and explains how this proposal differs.

## Current maturity

Version `0.1-draft` is an initial research artifact.

- No completed product has used GFD across a full lifecycle.
- No controlled comparison with an equivalent non-GFD project exists.
- Effects on quality, speed, token use, maintenance, and auditability have not been established.
- Results from ongoing projects are observations, not scientific or industrial validation.
- Multi-contributor, operated, regulated, and long-maintenance settings remain untested.

The method may be revised or abandoned if the planned studies do not show enough value.

## Repository map

- [METHOD.md](METHOD.md): canonical `0.1-draft` method
- [STATUS.md](STATUS.md): maturity, evidence gaps, risks, and open questions
- [ROADMAP.md](ROADMAP.md): validation program
- [references/prior-art.md](references/prior-art.md): sources and comparison
- [skills/audit-project-governance/](skills/audit-project-governance/): experimental reference audit implementation
- [CONTRIBUTING.md](CONTRIBUTING.md): corrections, criticism, cases, measurements, and normative changes

## Contributing evidence and counterexamples

A useful contribution may support GFD, narrow it, or show that a practice costs more than it returns. Please state the context, method, result, limits, and provenance of any evidence. Examples are not proof, and an AI audit is not independent merely because a different prompt produced it.

Open a contribution using [CONTRIBUTING.md](CONTRIBUTING.md). Security reports follow [SECURITY.md](SECURITY.md).

## License and citation

The proposed license is MIT. It permits use, modification, redistribution, and commercial use while requiring preservation of the copyright and license notice. See [LICENSE](LICENSE) and [CITATION.cff](CITATION.cff).
