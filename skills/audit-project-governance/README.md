# `audit-project-governance`

This directory contains version `0.2.0` of the experimental reference audit skill that preceded the public formulation of GFD. The skill helped shape the method, but [METHOD.md](../../METHOD.md) is the normative GFD `0.1-draft` source.

The original four-file snapshot remains identified by byte size and SHA-256 in [PROVENANCE.md](PROVENANCE.md). Version `0.2.0` is an explicit repository evolution governed by [decision 0002](../../governance/decisions/0002-attempt-outcome-integrity.md); it adds attempt/outcome integrity checks, schemas-aware validation, and deterministic distribution controls without rewriting the historical snapshot record.

## Package

`PACKAGE_MANIFEST.json` defines the portable files. Build the archive from the repository root:

```powershell
python -X utf8 tools/package_skill.py
```

The tool writes a deterministic ZIP under `dist/` and reports its SHA-256. Two builds from unchanged bytes must be identical.

## Install for Codex

Compare the canonical version with a personal Codex installation before copying anything:

```powershell
python -X utf8 tools/sync_skill.py --target "$env:USERPROFILE\.codex\skills\audit-project-governance"
```

Exit code `0` means the declared package files match. Exit code `1` means drift was found and no file was changed. The tool does not remove unrelated target files.

Applying the sync requires both the mutation flag and an exact versioned approval phrase:

```powershell
python -X utf8 tools/sync_skill.py --target "$env:USERPROFILE\.codex\skills\audit-project-governance" --apply --approve "sync audit-project-governance 0.2.0"
```

Do not run the apply command without reviewing the reported differences and preserving any local customization that overlaps the declared package files.

## Invoke

Ask the agent to use `$audit-project-governance` and state the audit question. The skill selects the minimum sufficient `TARGETED`, `STANDARD`, or `DEEP` audit depth. It audits in read-only mode and does not authorize a governance reform. When attempts or product verdicts are in scope, it also reports the **Attempt Outcome Integrity** dimension.

## Other agents

The main `SKILL.md` follows the Agent Skills format, but `agents/openai.yaml` contains Codex-specific interface metadata. Another host may need different discovery metadata, tool names, or permission controls. Preserve the audit contract, evidence states, read-only boundary, and reference links when adapting it.

Report a material difference between the skill and GFD as a documented divergence. Do not edit history to make the two appear identical.
