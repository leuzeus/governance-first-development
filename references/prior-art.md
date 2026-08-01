# Prior art and neighboring work

Status: informative research record

Access date for all web sources: 2026-08-01.

This review is reasonable, not exhaustive. Searches covered the exact phrase "Governance-First Development", hyphenated variants, related governance-first formulations, repository instruction files, decision records, policy and compliance as code, GitOps, specification-driven development, and empirical work on agent context. Search indexes change, and an omitted source may predate every item listed here.

## Findings about the name

The exact phrase has prior public uses. This repository does not claim that the name is exclusive or that its author invented every practice grouped under it.

Observed public examples include:

- Calathea described itself as a "governance-first development system" for agentic workflows, living RFCs, reproducibility, and a policy-aware SDLC in an [initial import dated 2026-04-22](https://github.com/hackelia-micrantha/calathea-community/blob/06f1c085254ed02900d0484cf5d989a72c003c56/README.md#L15-L22).
- Tachi shipped a scaffold labeled a "governance-first development template with SDLC Triad collaboration" in a [release commit dated 2026-07-04](https://github.com/davidmatousek/tachi/blob/5f5fd1c305705e6807c5936a54c19e60ef89e2a3/.aod/scaffold/README.md#L3-L9).
- ContextDevKit called itself a "business-driven, governance-first development platform for coding agents" in a [snapshot dated 2026-07-28](https://github.com/reiTavares/ContextDevKit/blob/bcfa2b07130fe533b1a9ea875ec3f14c8378edcf/README.md#L6-L13).
- SpecSmith used the phrase for teams adopting its governance and evidence tooling in a [snapshot dated 2026-07-29](https://github.com/layer1labs/specsmith/blob/1e8ada569d4dfcb1a1fedddde4bd35c49fbec2a1/docs/editions.md#L20-L27).

Neighboring formulations are older. Xu et al. proposed a "governance-first paradigm" for agent engineering in [From Craft to Constitution](https://arxiv.org/abs/2510.13857), submitted on 2025-10-12. HadleyLab published [Governance First](https://hadleylab.org/blogs/2026-01-05-governance-first) on 2026-01-05 and described governance-first programming as defining constraints before code is trusted.

These sources establish prior terminology and adjacent designs. They do not show that the GFD synthesis in this repository is equivalent to those systems, and this search cannot establish the first use of the phrase.

## What is inherited and what is proposed

GFD inherits versioned decision records, repository documentation, explicit controls, risk management, machine-readable policy, and agent instructions. Its proposed synthesis joins those pieces with four additional concerns:

1. an explicit precedence map for project authorities;
2. a strict separation of intent, decision, implementation, test, and evidence;
3. governance paths selected by change risk, with compensating controls and rollback;
4. measurement of context debt and governance friction as possible failure modes of governance itself.

That integration is a proposal. Its usefulness is an unvalidated hypothesis.

## Comparative view

Abbreviations: `H` means humans are primary actors; `A` means agents are explicit actors; `varies` means the approach leaves the choice to adopters.

| Approach | Primary purpose | Governed unit | Repository role | Humans | Agents | Authorities | Decisions | Evidence | Friction | Risk adaptation | Relation to GFD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| README-driven or documentation-first development | Design use and explanation before implementation | Product or interface description | Primary design artifact | H | Not original focus | Usually implicit | Captured in prose | Examples and docs | Lightweight by design | Informal | Precedent for writing intent early; GFD adds authority, controls, and evidence lifecycle |
| Architecture Decision Records | Preserve significant decisions and rationale | One architectural or project decision | Records live with code | H | Not original focus | Decision owner is local | Central concern | Consequences, not a proof model | Small modular records | Significance-based | Direct source for decision lifecycle and supersession |
| ISO/IEC/IEEE 42010 | Structure architecture descriptions | Architecture description | One possible medium | H | Not explicit | Stakeholders and viewpoints | Architectural concerns | Conformance to description requirements | Not a main measure | Scope-dependent | Formal architecture precedent; GFD covers broader project governance |
| Policy as code and OPA | Express and evaluate policy decisions | Structured input and policy decision | Common policy source | H authors | A may be subject or caller | Policy ownership external to engine | Encoded as rules | Evaluation result | Operational cost can be measured | Policy-specific | Possible executable control; not the complete project method |
| OSCAL and compliance as code | Exchange control and assessment information | Security and privacy control data | Machine-readable artifacts | H and tools | Not a central role | Regulatory and control authorities | Plans and assessments | Core concern | Automation targets manual cost | Baseline/profile based | Strong precedent for structured evidence; GFD is not a compliance framework |
| GitOps | Reconcile declared state into an operational system | Deployed system and configuration | Desired-state source | H approve changes | Automation reconciles | Repository and platform rules | Commit and review history | Reconciliation state | Delivery cost, not method focus | Operational controls | Shares versioned state and audit history; GFD also governs intent and proof |
| NIST SSDF and DevSecOps guidance | Reduce software vulnerability risk across the SDLC | Development practices and software lifecycle | One implementation location | H and automated tools | Generative agents are covered by later profiles | Organizational and security roles | Security requirements and risk decisions | Provenance and practice results | Not a central metric | Risk-based practice selection | Security and lifecycle source; GFD cannot replace it |
| NIST AI RMF and Responsible AI | Manage risks from AI systems | AI system and its context of use | Optional artifact location | H governance | AI is governed subject | Organizational and external authority | Risk treatment | Measurement and monitoring | Tradeoffs acknowledged | Central | Neighboring AI governance; GFD governs the software project and its coding agents |
| Specification-driven development and Spec Kit | Keep intent and specifications ahead of implementation | Feature or product workflow | Stores spec, plan, tasks, and code | H direct | A is an executor | Workflow rules | Often captured in specs and plans | Checks vary by implementation | Process cost not central | Presets and workflows vary | Compatible input to GFD; GFD adds authority precedence and evidence semantics |
| `AGENTS.md` and similar context files | Give coding agents repository instructions | Repository or directory scope | Dedicated instruction source | H author | A is primary consumer | File precedence depends on tool | May point to decisions | Commands may produce evidence | Recent studies measure cost | Usually local and implicit | One delivery mechanism for GFD, not an authority system by itself |
| Empirical context-file research | Measure effects of repository instructions | Agent task execution | Experimental variable | H researchers | A is study subject | Not the main focus | Task outcomes | Benchmarks, time, tokens, steps | Central | Varies by task sample | Warns GFD against large unmeasured instruction files; findings currently conflict |
| Governance-first agent engineering | Constrain probabilistic agent behavior through a governed architecture | Agent runtime and actions | May contain constitutions and controls | H define rules | A is governed subject | Normative core or constitution | Runtime or constitutional decisions | Evaluation and logs | Resource tracking may appear | Progressive controls | Direct terminology neighbor; narrower focus on agent systems |
| Earlier exact-phrase projects | Govern agentic or software delivery workflows | Product-specific repository and runtime | Usually central | H | A explicit in several projects | Product-specific | RFCs, plans, or harness rules | Receipts, logs, or tests | Varies | Often tiered | Prior use of the name; no claim of equivalence with this GFD draft |
| GFD `0.1-draft` | Make project authority, intent, constraints, validation, and proof auditable together | Repository-centered project | Primary transmission and audit unit | H retain authority | A execute and review within bounds | Explicit precedence map | Versioned lifecycle | Claim-specific statuses and limits | First-class measure | Five profiles | Experimental synthesis to be tested |

## Source register

Each entry records what the source can and cannot support.

### Early documentation and decisions

| Source | Author or organization | Published | Type | Relation | Supports | Does not establish |
|---|---|---:|---|---|---|---|
| [Readme Driven Development](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html) | Tom Preston-Werner | 2010-08-23 | Author essay | Documentation before code with a deliberate limit on process | The idea of writing a repository introduction before implementation predates GFD | That README-first work covers authority, agents, controls, or evidence |
| [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Michael Nygard | 2011-11-15 | Author essay and practice record | Short repository records with status and supersession | A documented origin for the widely used ADR format | That ADRs govern a whole project or prove decision quality |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | ISO, IEC, IEEE | 2022-11 | Standard abstract | Architecture description concepts and relationships | Architecture descriptions have formal prior work | The contents of the paywalled standard beyond the public abstract, or GFD conformance |

### Policy, compliance, delivery, and risk

| Source | Author or organization | Published | Type | Relation | Supports | Does not establish |
|---|---|---:|---|---|---|---|
| [Open Policy Agent documentation](https://www.openpolicyagent.org/docs) | Open Policy Agent project, CNCF | Current | Official documentation | Declarative policy decisions over structured data | Policy as code can be versioned and evaluated by an engine | That every governance rule should be code |
| [OSCAL](https://pages.nist.gov/OSCAL/) | NIST and contributors | Current; page updated 2026-06-02 | Official standard project | Machine-readable control and assessment information | Compliance artifacts and assessment results can use open structured formats | The page's promotional time-savings claims as universal outcomes, or GFD validity |
| [OpenGitOps](https://opengitops.dev/about/) | CNCF GitOps Working Group | Current | Official working-group site | Vendor-neutral principles for GitOps | Git-centered declared state and automated reconciliation are established practices | That GitOps governs project intent or agent authority |
| [Secure Software Development Framework 1.1](https://csrc.nist.gov/projects/ssdf) | NIST | 2022 | Government guidance | Risk-based secure development practices, provenance, and tracked decisions | Security requirements and provenance belong across the software lifecycle | That a documentation-only GFD audit satisfies secure development duties |
| [Artificial Intelligence Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1) | Elham Tabassi, NIST | 2023-01-26 | Government framework | Voluntary, use-case-aware AI risk management | AI governance and risk adaptation have established frameworks | That GFD manages product-level AI harms or meets regulatory duties |

### Agent instructions and specification-driven work

| Source | Author or organization | Published | Type | Relation | Supports | Does not establish |
|---|---|---:|---|---|---|---|
| [`AGENTS.md`](https://agents.md/) | Agentic AI Foundation project | Current | Open-format documentation | Predictable repository instructions for coding agents | A cross-tool convention exists for agent-facing instructions and nested scope | That such files always improve agent outcomes |
| [GitHub Spec Kit](https://github.github.io/spec-kit/) | GitHub | Current; page updated 2026-07-16 | Official tool documentation | Specification, plan, tasks, and implementation workflow for agents | Spec-driven agent workflows are active prior work | That its artifacts include GFD's authority or proof model |
| [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) | Thibaud Gloaguen et al. | 2026-02-12 | Research paper; 2026 workshop version | Controlled comparison of context-file strategies | In its samples, generated context increased cost without a significant success gain; developer files had small, non-significant average gains | A universal rule to delete or keep context files |
| [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404) | Jai Lal Lulla et al. | 2026-01-23 | Research paper | Runtime and token comparison across 124 pull requests | Its sample associated `AGENTS.md` with lower median runtime and output-token use | Causality or correctness gains across all repositories |
| [Lost in the Middle](https://arxiv.org/abs/2307.03172) | Nelson F. Liu et al. | 2023-07-06 | Research paper | Limits in using long input context | Relevant-information position and added context can affect model performance | A direct evaluation of coding-agent repository governance |

### Governance-first terminology

| Source | Author or organization | Published | Type | Relation | Supports | Does not establish |
|---|---|---:|---|---|---|---|
| [From Craft to Constitution](https://arxiv.org/abs/2510.13857) | Qiang Xu et al. | 2025-10-12 | Perspective and architecture paper | Governance-first paradigm for agent engineering | The neighboring formulation predates this repository | Validation of GFD or ownership of the exact GFD synthesis |
| [Governance First](https://hadleylab.org/blogs/2026-01-05-governance-first) | HadleyLab | 2026-01-05 | Technical essay and project account | Constraints and validators precede trusted implementation | Public use of "governance-first programming" and repository constitutions | Independent proof of the reported project's outcomes |
| [Calathea snapshot](https://github.com/hackelia-micrantha/calathea-community/blob/06f1c085254ed02900d0484cf5d989a72c003c56/README.md#L15-L22) | hackelia-micrantha | 2026-04-22 | Public source repository | Exact phrase and agentic, RFC-driven system | An observed exact-phrase use before this publication | First use of the phrase or equivalence with GFD |
| [Tachi scaffold snapshot](https://github.com/davidmatousek/tachi/blob/5f5fd1c305705e6807c5936a54c19e60ef89e2a3/.aod/scaffold/README.md#L3-L9) | davidmatousek | 2026-07-04 | Public source repository | Exact phrase and governed SDLC template | Another observed exact-phrase use | A shared definition or a standard |
| [ContextDevKit snapshot](https://github.com/reiTavares/ContextDevKit/blob/bcfa2b07130fe533b1a9ea875ec3f14c8378edcf/README.md#L6-L13) | reiTavares | 2026-07-28 | Public source repository | Exact phrase and coding-agent platform | Another observed exact-phrase use | That GFD's name is unique or exclusive |

## Gaps in this review

The search did not identify a single established specification named "Agent Decision Records." It found several newer agent receipt, audit, and decision-record proposals, but their names and scopes differ. GFD therefore treats agent decision records as an emerging family, not as one settled standard.

No trademark clearance or legal name opinion was performed. Repository and code-search results can miss private, unindexed, renamed, or deleted work. The project name remains usable as a descriptive proposal, but uniqueness is not claimed.
