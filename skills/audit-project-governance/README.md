# `audit-project-governance`

This directory contains the experimental reference audit skill that preceded the public formulation of GFD. The skill helped shape the method, but [METHOD.md](../../METHOD.md) is the normative GFD `0.1-draft` source.

The copied `SKILL.md`, `agents/openai.yaml`, `assets/icon.svg`, and `references/audit-reference.md` are preserved byte for byte from the author's active local snapshot on 2026-08-01. See [PROVENANCE.md](PROVENANCE.md) for hashes, licensing, known divergences, and portability notes.

## Install for Codex

Copy this directory to the personal Codex skills directory as `audit-project-governance`, then restart or reload skill discovery. Keep the whole directory so the reference, agent metadata, and icon remain available.

Do not overwrite an existing installation without first comparing versions and preserving a rollback copy.

## Invoke

Ask the agent to use `$audit-project-governance` and state the audit question. The skill selects the minimum sufficient `TARGETED`, `STANDARD`, or `DEEP` audit depth. It audits in read-only mode and does not authorize a governance reform.

## Other agents

The main `SKILL.md` follows the Agent Skills format, but `agents/openai.yaml` contains Codex-specific interface metadata. Another host may need different discovery metadata, tool names, or permission controls. Preserve the audit contract, evidence states, read-only boundary, and reference links when adapting it.

Report a material difference between the skill and GFD as a documented divergence. Do not edit history to make the two appear identical.
