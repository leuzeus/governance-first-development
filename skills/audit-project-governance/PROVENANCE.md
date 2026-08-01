# Provenance and divergence record

Status: informative

## Authorship and source

The project owner, publicly identified here as `LeuZeuS`, declared authorship of this skill on 2026-08-01. The skill was created before the public GFD method as a response to governance problems observed during AI-assisted project work. It was later revised and supplied by the author as a local archive, then installed as the active personal copy.

This repository copied the active snapshot on 2026-08-01. No private machine path, archive, backup, or conversation history is included. The earlier complete version history is not available in this repository, so provenance before the current snapshot depends on the author's declaration.

## License

The author confirmed ownership and selected the repository's [MIT License](../../LICENSE) for this copy. No third-party code or separate license notice was present in the four source files. If an earlier contributor or incorporated source is later identified, publication and attribution must be reviewed before the affected content is redistributed.

## Snapshot manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `SKILL.md` | 8,376 | `8A13806DB8E6C4875670098C54A87660554670DC3347D22EA1C1AF88E7F4CBF7` |
| `agents/openai.yaml` | 457 | `98F2E007E539263BC1A3B7B3D9F3206583F52235FDC08D8B7E2C6D98BF8BABA6` |
| `assets/icon.svg` | 420 | `E9301497FA98EF56AACA7EDE0857B9A18DC06C34040F0679C609A6BF49B1D38B` |
| `references/audit-reference.md` | 14,563 | `03BC7F1B4338513DD318F912B24B683796512267C30B15E6920EE30AF80C5DF2` |

Files added by this repository, including this record and `README.md`, are outside that byte-preserved manifest.

## Relationship with GFD

The skill contributed the audit profiles, change paths, evidence states, authority-led discovery, context-debt analysis, and friction framing used in GFD. It remains an implementation, not the method's authority.

Known differences are intentional and visible:

- The skill audits in read-only mode and stops before reform. GFD also defines how an authorized project may implement governed changes.
- `TARGETED`, `STANDARD`, and `DEEP` are audit-depth profiles in the skill. `STANDARD` is also a change path in GFD; the surrounding noun must disambiguate it.
- The skill uses Codex-oriented metadata and tool language. GFD is intended to be provider-neutral.
- The skill's personal-project hats include `technical_owner`, `evidence_operator`, `release_authority`, and others. This repository uses `method_editor` and `evidence_maintainer` where those names fit a method repository.
- The skill requires exactly one unexecuted first step after a formal audit. GFD does not impose that report format on all project planning.

These are current limitations and portability notes, not silent defects. A future proposal may align terminology, but it must preserve this snapshot and use a separate decision.

## Reporting divergence

Open an issue or pull request classified as `informative` for an undocumented difference. Classify a proposed behavior change to the skill as `experimental` or `normative` according to [CONTRIBUTING.md](../../CONTRIBUTING.md).
