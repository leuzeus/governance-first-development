#!/usr/bin/env python3
"""Run the canonical audit skill's attempt outcome validator for this repository."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = ROOT / "skills" / "audit-project-governance" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from audit_attempt_outcomes import main  # noqa: E402


if __name__ == "__main__":
    sys.exit(main())
