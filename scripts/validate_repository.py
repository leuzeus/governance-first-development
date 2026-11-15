#!/usr/bin/env python3
"""Validate the publication boundaries of the GFD documentation repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "README.fr.md",
    "MANIFESTO.md",
    "METHOD.md",
    "GLOSSARY.md",
    "STATUS.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE",
    "CITATION.cff",
    "AGENTS.md",
    "CHANGELOG.md",
    "references/prior-art.md",
    "templates/authority-map.md",
    "templates/decision-record.md",
    "templates/evidence-record.md",
    "templates/governance-profile.md",
    "templates/attempt-record.json",
    "templates/attempt-outcome.json",
    "examples/personal-agent-driven-project.md",
    "examples/attempt-lineage/README.md",
    "governance/authority-map.md",
    "governance/decisions/0001-initial-method-and-license.md",
    "governance/decisions/0002-attempt-outcome-integrity.md",
    "governance/decisions/0003-publication-privacy-scrub.md",
    "governance/decisions/0004-public-repository-security-baseline.md",
    "governance/addenda/0001-attempt-outcome-integrity.md",
    "governance/addenda/0002-publication-privacy-scrub.md",
    "governance/publication-privacy-policy.json",
    "governance/evidence/initial-validation.md",
    "governance/audits/initial-audit.md",
    "governance/audits/attempt-outcome-baseline.md",
    "schemas/attempt-record.schema.json",
    "schemas/attempt-outcome.schema.json",
    "scripts/validate_attempt_governance.py",
    "scripts/audit_publication_privacy.py",
    "skills/audit-project-governance/SKILL.md",
    "skills/audit-project-governance/VERSION",
    "skills/audit-project-governance/PACKAGE_MANIFEST.json",
    "skills/audit-project-governance/agents/openai.yaml",
    "skills/audit-project-governance/assets/icon.svg",
    "skills/audit-project-governance/scripts/audit_attempt_outcomes.py",
    "skills/audit-project-governance/references/audit-reference.md",
    "skills/audit-project-governance/references/attempt-outcome-integrity.md",
    "skills/audit-project-governance/PROVENANCE.md",
    "tools/package_skill.py",
    "tools/sync_skill.py",
    "tests/test_attempt_governance.py",
    "tests/test_skill_distribution.py",
    "tests/test_publication_privacy.py",
    "skills/audit-session-progress/LICENSE",
    "skills/audit-session-progress/SKILL.md",
    "skills/audit-session-progress/VERSION",
    "skills/audit-session-progress/PACKAGE_MANIFEST.json",
    "skills/audit-session-progress/PROVENANCE.md",
    "skills/audit-session-progress/README.md",
    "skills/audit-session-progress/agents/openai.yaml",
    "skills/audit-session-progress/references/diagnostic.md",
    "skills/audit-session-progress/references/evaluation.md",
)

SKILL_DIRS = (
    ROOT / "skills" / "audit-project-governance",
    ROOT / "skills" / "audit-session-progress",
)

EN_STATUS = (
    "Experimental proposal — tested only on ongoing projects; "
    "no completed full-lifecycle reference implementation yet."
)
FR_STATUS = (
    "Proposition expérimentale — expérimentée uniquement sur des projets en cours; "
    "aucune application de référence n’a encore couvert un cycle de vie complet."
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
AUTOLINK_RE = re.compile(r"<(https?://[^>]+)>")


@dataclass
class Result:
    name: str
    status: str
    detail: str


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files() -> Result:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        return Result("required-files", "FAIL", ", ".join(missing))
    return Result("required-files", "PASS", f"{len(REQUIRED_FILES)} files present")


def check_internal_links() -> Result:
    broken: list[str] = []
    for source in markdown_files():
        text = read_text(source)
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (source.parent / path_part).resolve()
            if not resolved.exists():
                broken.append(f"{source.relative_to(ROOT)} -> {target}")
    if broken:
        return Result("internal-links", "FAIL", "; ".join(broken))
    return Result("internal-links", "PASS", "all relative targets exist")


def check_status_language() -> Result:
    readme = read_text(ROOT / "README.md")
    readme_fr = read_text(ROOT / "README.fr.md")
    status = read_text(ROOT / "STATUS.md")
    errors: list[str] = []
    if EN_STATUS not in readme:
        errors.append("English status missing from README.md")
    if FR_STATUS not in readme_fr:
        errors.append("French status missing from README.fr.md")
    if EN_STATUS not in status:
        errors.append("English status missing from STATUS.md")
    for shared in (
        "0.1-draft",
        "METHOD.md",
        "STATUS.md",
        "ROADMAP.md",
        "audit-project-governance",
        "EXPLORE",
        "FAST",
        "STANDARD",
        "ASSURED",
        "EMERGENCY",
    ):
        if shared not in readme or shared not in readme_fr:
            errors.append(f"shared concept missing in a README: {shared}")
    if errors:
        return Result("bilingual-status", "FAIL", "; ".join(errors))
    return Result("bilingual-status", "PASS", "required status and shared concepts present")


def check_citation() -> Result:
    text = read_text(ROOT / "CITATION.cff")
    required = {
        "cff-version": "1.2.0",
        "title": "Governance-First Development",
        "version": "0.1-draft",
        "license": "MIT",
        "name": "LeuZeuS",
        "repository-code": "https://github.com/leuzeus/governance-first-development",
    }
    missing = [f"{key}: {value}" for key, value in required.items() if value not in text]
    if missing:
        return Result("citation-metadata", "FAIL", "missing " + ", ".join(missing))
    if "authors:" not in text or 'date-released: "2026-08-06"' not in text:
        return Result("citation-metadata", "FAIL", "authors or release date missing")
    return Result("citation-metadata", "PASS", "required CFF fields present")


def check_skill_manifest_for(skill_dir: Path) -> Result:
    manifest_path = skill_dir / "PACKAGE_MANIFEST.json"
    errors: list[str] = []
    try:
        manifest = json.loads(read_text(manifest_path))
    except (OSError, json.JSONDecodeError) as error:
        return Result("skill-manifest", "FAIL", str(error))
    files = manifest.get("files")
    version = manifest.get("version")
    if manifest.get("format_version") != 1:
        errors.append("format_version must be 1")
    if manifest.get("name") != skill_dir.name:
        errors.append("unexpected skill name")
    if manifest.get("archive_root") != skill_dir.name:
        errors.append("unexpected archive root")
    if not isinstance(files, list) or not files or files != sorted(set(files)):
        errors.append("files must be a non-empty sorted unique list")
        files = []
    for relative in files:
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            errors.append(f"unsafe path {relative}")
        elif not (skill_dir / relative_path).is_file():
            errors.append(f"missing package file {relative}")
    required_package_files = {
        "PACKAGE_MANIFEST.json",
        "PROVENANCE.md",
        "SKILL.md",
        "VERSION",
        "README.md",
        "agents/openai.yaml",
    }
    if skill_dir.name == "audit-project-governance":
        required_package_files.update({
            "references/attempt-outcome-integrity.md",
            "scripts/audit_attempt_outcomes.py",
        })
    elif skill_dir.name == "audit-session-progress":
        required_package_files.update({
            "LICENSE",
            "references/diagnostic.md",
            "references/evaluation.md",
        })
    if not required_package_files.issubset(set(files)):
        errors.append("required runtime or provenance file absent from package")
    try:
        version_text = read_text(skill_dir / "VERSION").strip()
        skill_text = read_text(skill_dir / "SKILL.md")
        provenance_text = read_text(skill_dir / "PROVENANCE.md")
    except OSError as error:
        errors.append(str(error))
    else:
        if version != version_text:
            errors.append("manifest and VERSION disagree")
        if f"Version du skill : `{version}`" not in skill_text:
            errors.append("SKILL.md version marker disagrees")
        if f"`{version}`" not in provenance_text:
            errors.append("PROVENANCE.md lacks current version")
    if errors:
        return Result("skill-manifest", "FAIL", "; ".join(errors))
    return Result("skill-manifest", "PASS", f"{len(files)} declared files for version {version}")


def check_skill_manifest() -> Result:
    results = [(directory.name, check_skill_manifest_for(directory)) for directory in SKILL_DIRS]
    failures = [f"{name}: {result.detail}" for name, result in results if result.status != "PASS"]
    if failures:
        return Result("skill-manifest", "FAIL", "; ".join(failures))
    return Result("skill-manifest", "PASS", "; ".join(f"{name}: {result.detail}" for name, result in results))


def check_json_contracts() -> Result:
    roots = [
        ROOT / "schemas",
        ROOT / "templates",
        ROOT / "examples" / "attempt-lineage",
        ROOT / "tests" / "fixtures" / "attempt-governance",
    ]
    paths = [directory / "PACKAGE_MANIFEST.json" for directory in SKILL_DIRS]
    paths.append(ROOT / "governance" / "publication-privacy-policy.json")
    for root in roots:
        if root.is_dir():
            paths.extend(sorted(root.rglob("*.json")))
    errors: list[str] = []
    for path in paths:
        try:
            json.loads(read_text(path))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")
    if errors:
        return Result("json-contracts", "FAIL", "; ".join(errors))
    return Result("json-contracts", "PASS", f"{len(paths)} JSON files parse")


def check_attempt_examples() -> Result:
    command = [
        sys.executable,
        "-X",
        "utf8",
        str(ROOT / "scripts" / "validate_attempt_governance.py"),
        "--records",
        str(ROOT / "examples" / "attempt-lineage"),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = " ".join(completed.stdout.split())
    if completed.returncode != 0 or "VERDICT conformant" not in completed.stdout:
        detail = output or " ".join(completed.stderr.split()) or f"exit {completed.returncode}"
        return Result("attempt-examples", "FAIL", detail)
    return Result("attempt-examples", "PASS", "A-H corpus is conformant")


def check_publication_privacy() -> Result:
    command = [
        sys.executable,
        "-X",
        "utf8",
        str(ROOT / "scripts" / "audit_publication_privacy.py"),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = " ".join(completed.stdout.split())
    if completed.returncode == 0:
        return Result(
            "publication-privacy-current",
            "PASS",
            "tracked and untracked publication candidates passed the redacting scan",
        )
    if completed.returncode == 2:
        return Result("publication-privacy-current", "UNAVAILABLE", output or "scanner unavailable")
    return Result("publication-privacy-current", "FAIL", output or "privacy finding")


def check_publication_language() -> Result:
    forbidden = {
        "recognized standard": re.compile(r"\b(?:a |the )?(?:recognized|established) standard\b", re.I),
        "proven methodology": re.compile(r"\bproven (?:method|methodology|framework)\b", re.I),
        "unqualified validation": re.compile(r"\bscientifically validated\b", re.I),
        "unfilled date": re.compile(r"\b20\d{2}-XX-XX\b"),
        "unfilled placeholder": re.compile(r"\[(?:Your|Insert|Add|Enter|Describe|Specify|Choose)[^\]]+\]", re.I),
        "chat citation leak": re.compile(r"(?:citeturn\d+|contentReference\[oaicite|oai_citation|grok_card)", re.I),
        "AI URL tracking": re.compile(r"(?:utm_source=(?:chatgpt\.com|copilot\.com|openai|claude\.ai|perplexity\.ai)|referrer=grok\.com)", re.I),
    }
    findings: list[str] = []
    for path in markdown_files():
        if "skills" in path.parts:
            continue
        text = read_text(path)
        for label, pattern in forbidden.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)}: {label}")
    if findings:
        return Result("publication-language", "FAIL", "; ".join(findings))
    return Result("publication-language", "PASS", "no configured maturity, placeholder, or citation leak found")


def external_urls() -> list[str]:
    urls: set[str] = set()
    for path in markdown_files():
        text = read_text(path)
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://")):
                urls.add(target)
        urls.update(AUTOLINK_RE.findall(text))
    return sorted(urls)


def check_external_links() -> Result:
    unavailable: list[str] = []
    failed: list[str] = []
    checked = 0
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "gfd-link-check/0.1")]
    for url in external_urls():
        request = urllib.request.Request(url, method="HEAD")
        try:
            with opener.open(request, timeout=15) as response:
                code = response.getcode()
            checked += 1
            if code >= 400:
                failed.append(f"{code} {url}")
        except urllib.error.HTTPError as error:
            if error.code in (403, 405, 429):
                unavailable.append(f"{error.code} {url}")
            elif error.code == 404 and "security/advisories/new" in url:
                unavailable.append(f"planned repository {url}")
            else:
                failed.append(f"{error.code} {url}")
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            unavailable.append(f"{url} ({error.__class__.__name__})")
    if failed:
        return Result("external-links", "FAIL", "; ".join(failed))
    if unavailable:
        return Result(
            "external-links",
            "UNAVAILABLE",
            f"{checked} checked; unavailable: " + "; ".join(unavailable),
        )
    return Result("external-links", "PASS", f"{checked} links responded below 400")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--external",
        action="store_true",
        help="also make network requests for external links",
    )
    args = parser.parse_args()

    checks = [
        check_required_files,
        check_internal_links,
        check_status_language,
        check_citation,
        check_skill_manifest,
        check_json_contracts,
        check_attempt_examples,
        check_publication_privacy,
        check_publication_language,
    ]
    results = [check() for check in checks]
    if args.external:
        results.append(check_external_links())
    else:
        results.append(Result("external-links", "SKIP", "run with --external"))

    for result in results:
        print(f"{result.status:11} {result.name}: {result.detail}")

    return 1 if any(result.status == "FAIL" for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
