#!/usr/bin/env python3
"""Validate the publication boundaries of the GFD documentation repository."""

from __future__ import annotations

import argparse
import hashlib
import re
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
    "examples/personal-agent-driven-project.md",
    "governance/authority-map.md",
    "governance/decisions/0001-initial-method-and-license.md",
    "governance/evidence/initial-validation.md",
    "governance/audits/initial-audit.md",
    "skills/audit-project-governance/SKILL.md",
    "skills/audit-project-governance/agents/openai.yaml",
    "skills/audit-project-governance/assets/icon.svg",
    "skills/audit-project-governance/references/audit-reference.md",
    "skills/audit-project-governance/PROVENANCE.md",
)

SKILL_MANIFEST = {
    "skills/audit-project-governance/SKILL.md": (
        8376,
        "8A13806DB8E6C4875670098C54A87660554670DC3347D22EA1C1AF88E7F4CBF7",
    ),
    "skills/audit-project-governance/agents/openai.yaml": (
        457,
        "98F2E007E539263BC1A3B7B3D9F3206583F52235FDC08D8B7E2C6D98BF8BABA6",
    ),
    "skills/audit-project-governance/assets/icon.svg": (
        420,
        "E9301497FA98EF56AACA7EDE0857B9A18DC06C34040F0679C609A6BF49B1D38B",
    ),
    "skills/audit-project-governance/references/audit-reference.md": (
        14563,
        "03BC7F1B4338513DD318F912B24B683796512267C30B15E6920EE30AF80C5DF2",
    ),
}

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


def text_publication_files() -> list[Path]:
    allowed = {".md", ".cff", ".yml", ".yaml", ".py", ".txt", ""}
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix.lower() in allowed
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
    if "authors:" not in text or 'date-released: "2026-08-01"' not in text:
        return Result("citation-metadata", "FAIL", "authors or release date missing")
    return Result("citation-metadata", "PASS", "required CFF fields present")


def check_skill_manifest() -> Result:
    errors: list[str] = []
    for relative, (expected_size, expected_hash) in SKILL_MANIFEST.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing {relative}")
            continue
        data = path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest().upper()
        if len(data) != expected_size:
            errors.append(f"{relative} size {len(data)} != {expected_size}")
        if actual_hash != expected_hash:
            errors.append(f"{relative} SHA-256 mismatch")
    if errors:
        return Result("skill-manifest", "FAIL", "; ".join(errors))
    return Result("skill-manifest", "PASS", "four source files match the recorded snapshot")


def check_private_material() -> Result:
    patterns = {
        "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.I),
        "workspace drive path": re.compile(r"\bG:\\", re.I),
        "GitHub token": re.compile(r"\bgh[opurs]_[A-Za-z0-9_]{16,}"),
        "OpenAI token": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
        "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
        "chat attachment": re.compile(r"\\.codex\\attachments", re.I),
    }
    findings: list[str] = []
    for path in text_publication_files():
        if path.as_posix().endswith("scripts/validate_repository.py"):
            continue
        text = read_text(path)
        for label, pattern in patterns.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)}: {label}")
    if findings:
        return Result("private-material", "FAIL", "; ".join(findings))
    return Result("private-material", "PASS", "no configured secret or private-path pattern found")


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
        check_private_material,
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
