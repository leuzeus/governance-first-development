# audit-session-progress

Experimental session audit, version `0.1.0-draft`. Optional, informative implementation; behavioral effectiveness has not been evaluated. The skill entrypoint is written in French. The GFD method remains `0.1-draft`.

## Purpose and boundaries

Use the skill to examine a bounded work episode when corrections repeat, a selected method is contested, or useful observations stop. It identifies a material anomaly, a question that changes a decision, and a test or other bounded next action. A long investigation that produces new evidence is not automatically stalled.

Session diagnosis complements the repository-level `audit-project-governance` skill. Rules and gates remain governed by the project's adopted authorities. The audit is read-only and does not grant implementation, publication, or installation authority.

## Invoke

Ask an agent to use `$audit-session-progress`, name the outcome and blockage, and identify the relevant chat or authorized export. It reads a useful segment and its accessible evidence, not the entire private history by default. Its output distinguishes observations, causal hypotheses, missing evidence, and proposals.

The [diagnostic guidance](references/diagnostic.md) covers reference transfer and implicit expert knowledge. The [evaluation protocol](references/evaluation.md) includes counterexamples and prospective measurement. Format checks and deterministic packaging do not establish diagnostic accuracy or faster resolution.

## Distribution

`PACKAGE_MANIFEST.json` declares the portable files. From the repository root:

```powershell
python -X utf8 tools/package_skill.py --skill-dir skills/audit-session-progress
```

The existing sync tool supports this source. Compare against an explicitly chosen target first:

```powershell
python -X utf8 tools/sync_skill.py --source skills/audit-session-progress --target <reviewed-target>
```

This comparison writes nothing. Applying a reviewed sync requires `--apply` and the exact approval phrase `sync audit-session-progress 0.1.0-draft`. This repository addition does not perform that installation. A host may need different discovery metadata; `agents/openai.yaml` is Codex-specific.

## Provenance and maturity

See [PROVENANCE.md](PROVENANCE.md) for the initial draft and its declared adaptations. No private transcripts, machine configuration, or personal paths are included. The package includes the repository's [MIT license notice](LICENSE); preserve it when redistributing. No automatic audit schedule, hook, or mandatory session gate is introduced.
