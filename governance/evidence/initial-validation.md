# Evidence record: initial repository validation

Claim: the local `0.1-draft` repository satisfies its stated pre-publication document checks at the uncommitted pre-release snapshot created on 2026-08-01.

Evidence type: automated validation plus manual source and writing review

Status: `PASS` for local pre-publication readiness. Public GitHub state remains `UNAVAILABLE` until owner approval.

Date: 2026-08-01

## Environment

- Windows PowerShell
- Python 3.11.0
- Git 2.47.1.windows.2
- GitHub CLI 2.86.0
- Branch `main`, with no commit at the start of validation
- 32 repository files, 25 Markdown files, and 135,474 bytes before this evidence record and the audit report were added

Machine-specific paths and credentials are intentionally omitted.

## Commands and results

| Check | Method | Result |
|---|---|---|
| Repository validator | `python -X utf8 scripts/validate_repository.py` | `PASS` for required files, internal links, bilingual status, citation fields, skill manifest, private-material scan, and publication language; external links `SKIP` in the no-network mode |
| External link pass | `python -X utf8 scripts/validate_repository.py --external` | 19 URLs responded below 400; automated checks reported `UNAVAILABLE` for an ISO page returning 403 to `HEAD` and the planned security-advisory URL before repository creation |
| CFF schema | Parse YAML and validate against the official CFF 1.2.0 `schema.json` | `PASS` after quoting `date-released` as a string |
| Skill format | Official Codex `quick_validate.py` against the vendored skill directory | `PASS`: `Skill is valid!` |
| Skill identity | Size and SHA-256 comparison for the four source files | `PASS`: all copied files match the provenance manifest |
| GitHub account and name | Authenticated account query, repository lookup, and public repository/code search | `PASS` for authenticated account `leuzeus`; exact repository absent on that account; `PASS` for detecting earlier exact-phrase uses; public repository creation remains `UNAVAILABLE` pending approval |
| Prior-art sources | Direct web and immutable GitHub commit pages | `PASS` for the claims retained in `references/prior-art.md`; the review is explicitly non-exhaustive |
| English/French alignment | Section and concept comparison plus automated shared-term checks | `PASS` for shared definition, maturity, profiles, navigation, adoption, and contribution meaning |
| Writing-quality audit | `avoid-ai-writing` vocabulary, structure, formatting, and second-pass scan | `PASS` for authored prose; required quoted status lines and source terminology were preserved |

## Useful blocks observed

The CFF schema check found that an unquoted YAML date became a date object while the schema requires a string. The field was changed to `"2026-08-01"` and revalidated.

The publication-language scanner also flagged a cautionary sentence containing the phrase it was designed to prohibit. This was a false-block example, not a maturity claim. The sentence was made more specific; the scanner's future false-positive rate remains unknown.

## Limits

The validator checks target existence for internal links but does not prove every statement true. It checks selected bilingual concepts, not formal semantic equivalence. Automated external checks use `HEAD`; servers may reject that method while remaining available to a browser.

No GitHub repository, description, security advisory form, tag, release, or remote exists yet. No runtime software, production system, migration, hardware claim, complete lifecycle, or maintenance period was validated.

## Reproduction

Run the two validator commands from the repository root on the same commit. Re-run CFF schema validation with the official version 1.2.0 schema and run the official skill validator. Network results may change.

## Validity

This evidence is invalidated by any change to publication documents, validation code, citation metadata, vendored source files, license, authority map, or release state. The pre-publication review must report the final committed SHA after the commits are created.
