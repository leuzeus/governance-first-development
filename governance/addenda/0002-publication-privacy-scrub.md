# Addendum 0002: Publication privacy scrub

Date: 2026-08-05

Status: accepted for this repository's publication workflow

Authority: project owner and release authority

Impact: high

Breaking change: no for the GFD method; yes for this repository's first-publication gate

## Summary

Add a privacy scrub before the first public push, every public release, and any history rewrite intended for publication. The scrub covers personal identifiers, secrets, local paths, host and network topology, device identifiers, Git identities, commit messages, reachable historical blobs, and binary metadata.

This is a repository publication control. It does not add a universal GFD requirement for adopters.

## Motivation

The existing `private-material` check scans current text for a small set of patterns. It does not prove that deleted content is absent from Git history, that commit metadata uses an intended public identity, or that binary files lack personal metadata. A public push exposes reachable history as well as current files.

The automated scan must not repeat a matched secret or identifier in its output. A path, identity, or network value that needs removal should be located by category and repository position, then reviewed locally.

## Requirements mapping

| Old requirement | Action | New requirement | Notes |
|---|---|---|---|
| Agent must not expose secrets or private machine data | revise | `PPS-REQ-001`, `PPS-REQ-002` | Add an executable publication-surface check |
| Current `private-material` text scan | revise | `PPS-REQ-003` | Route it through the new scanner |
| Human approval before public release | split | `PPS-REQ-004`, `PPS-REQ-005` | Require automated history scan and contextual review |
| No binary metadata rule | add | `PPS-REQ-006` | Unreviewed binary content blocks the automated gate |
| No history-cleaning rule | add | `PPS-REQ-007` | History rewrite remains a separate destructive decision |

## New requirements

- `PPS-REQ-001`: The current index, tracked working-tree content, tracked paths, and nonignored untracked paths and content MUST be scanned before a change is accepted for publication.
- `PPS-REQ-002`: The scan MUST detect configured personal identifiers, non-public email addresses, secrets, absolute local paths, user-profile paths, private network addresses, host or device identifiers, and Codex-local artifact paths.
- `PPS-REQ-003`: The repository validator MUST execute the current-surface scan and report `PASS`, `FAIL`, `SKIP`, or `UNAVAILABLE` honestly.
- `PPS-REQ-004`: Before the first public push or any release, all reachable commits, identities, messages, paths, and blobs MUST pass the history scan.
- `PPS-REQ-005`: An authorized human MUST review contextual identifiers, filenames, intended public attribution, and the limits of automated detection before publication.
- `PPS-REQ-006`: A tracked or historical binary blob MUST have a reviewed SHA-256 entry and reason in the privacy policy or the automated gate fails.
- `PPS-REQ-007`: A history finding MUST NOT be hidden by deleting only the current file. Rewriting unpublished history requires an explicit destructive-action decision, a recoverable backup, target verification, rerun of every publication gate, and confirmation that no public remote contains the old objects.
- `PPS-REQ-008`: Scanner output MUST identify category and location without echoing the matched value. If a repository path is itself sensitive, the scanner MUST replace it with a stable local path digest.

## Manual review boundary

Automation cannot reliably identify a civil name in prose, an indirect personal fact, an intentionally public identity, or every metadata field in an approved binary. The release-authority review therefore checks:

- Git author and committer identities against the intended public pseudonym;
- filenames, commit messages, current content, and removed historical content;
- civil names, personal email or phone data, addresses, private project names, and chat material;
- usernames, drive layout, home directories, hostnames, shares, private IP addresses, device identifiers, and screenshots;
- EXIF, archive manifests, document properties, and other binary metadata;
- whether each retained attribution is deliberately public.

The automated `PASS` supports only the configured pattern and binary-hash claims. It does not replace this review.

## Migration and rollback

The current-surface scan is additive and runs through the repository validator. The full-history scan runs locally with `--history` because shallow CI checkouts cannot prove complete history coverage.

Rollback by superseding this addendum and decision 0003, removing the executable gate in a new commit, and retaining the prior records. Existing privacy findings remain security information and must not be copied into public rollback notes.
