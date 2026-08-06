# Security policy

GFD `0.1-draft` is documentation and an experimental audit skill. It has no stable supported release yet.

## Reporting a vulnerability

Do not open a public issue for a secret, exploitable path, private data exposure, or a vulnerability in the vendored skill. After the repository is public, use GitHub's private security advisory form:

<https://github.com/leuzeus/governance-first-development/security/advisories/new>

If that form is unavailable, contact the repository owner through the [GitHub profile](https://github.com/leuzeus) without including exploit details in a public message. The owner can then establish a private channel.

Include the affected commit, file, impact, reproduction conditions, and any safe mitigation. Do not access data or systems beyond what is needed to demonstrate the issue.

## Response status

No response-time promise is made for this experimental personal project. The owner will record whether the report is confirmed, rejected, duplicated, or unavailable to reproduce. Publication and disclosure timing require an explicit owner decision.

## Public repository baseline

The public GitHub repository uses a proportionate baseline for a personal experimental project:

- secret scanning and push protection are enabled when GitHub exposes them for the repository;
- dependency vulnerability alerts and automated security updates are enabled;
- private vulnerability reporting is enabled;
- GitHub Actions receives read-only default repository permissions and cannot approve pull requests;
- the default branch rejects deletion and non-fast-forward updates;
- merged branches are deleted automatically.

The baseline does not require pull-request approvals or status checks while there is one cumulative owner and no qualifying CI workflow. Add those controls through a new decision if contributors, protected releases, or material automation make their benefit exceed their friction.

An unavailable platform control is reported as `UNAVAILABLE`; it is never described as enabled without a successful settings query.
