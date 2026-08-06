# Decision 0004: Apply a proportionate public repository security baseline

Status: accepted

Date: 2026-08-06

Authority: project owner and release authority

Change path: `ASSURED`

## Context

The project owner authorized creation of a public GitHub repository after the first-publication privacy review. Public visibility exposes repository history, enables unsolicited contributions, and makes platform configuration part of the project's security boundary.

The repository is a personal, documentation-first experimental project. It currently has one cumulative owner, no production service, no package publishing workflow, and no qualifying CI status check.

## Evidence and limits

The repository validators can check committed content, Git history, schemas, tests, and configured privacy patterns. They cannot prove GitHub settings. Each platform control therefore requires a successful post-creation API query before it is reported as enabled.

Secret scanning does not prove that no secret exists. Dependency alerts do not cover every vendored or external component. Branch protection cannot prevent an authorized administrator from changing repository settings. The security policy makes no response-time promise.

## Options

1. Keep GitHub defaults and rely on manual care.
2. Enable every available restriction, including mandatory pull requests, approvals, signatures, and status checks.
3. Enable secret, dependency, disclosure, workflow-permission, and history-protection controls without imposing checks or approvals that the project cannot currently satisfy.

## Decision

Choose option 3. After creating the public repository:

- enable GitHub secret scanning and push protection when available;
- enable dependency vulnerability alerts and automated security updates;
- enable private vulnerability reporting;
- set default GitHub Actions repository permissions to read-only and prevent workflows from approving pull requests;
- protect the default branch from deletion and non-fast-forward updates;
- delete merged head branches automatically;
- query each setting after mutation and report `PASS`, `FAIL`, or `UNAVAILABLE` without overstating platform coverage.

Do not require pull-request approvals, commit signatures, or status checks until a later decision identifies contributors, release risk, or executable checks that justify the added friction.

## Expected benefit and friction

The baseline reduces accidental secret publication, dependency-notification gaps, workflow privilege, silent security-report disclosure, and destructive default-branch updates. It adds several platform settings and verification queries but no recurring approval step for the sole owner.

Residual risk includes administrator override, undetected contextual data, unsupported secret patterns, supply-chain issues outside GitHub's dependency model, and future configuration drift.

## Rollback and escalation

Rollback individual GitHub settings only through an explicit project-owner decision and record the resulting exposure. Reassess the baseline when the repository gains another contributor, publishes executable artifacts, adds privileged workflows, or declares a supported release.

## Replacement

superseded_by: none
