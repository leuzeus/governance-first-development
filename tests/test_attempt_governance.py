from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "skills" / "audit-project-governance" / "scripts" / "audit_attempt_outcomes.py"
SPEC = importlib.util.spec_from_file_location("audit_attempt_outcomes", CORE_PATH)
assert SPEC and SPEC.loader
AOI = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AOI
SPEC.loader.exec_module(AOI)


class AttemptOutcomeIntegrityTests(unittest.TestCase):
    schema_dir = ROOT / "schemas"
    examples = ROOT / "examples" / "attempt-lineage"
    fixtures = ROOT / "tests" / "fixtures" / "attempt-governance"

    @classmethod
    def _load(cls, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @classmethod
    def _schemas(cls) -> tuple[dict, dict]:
        return (
            cls._load(cls.schema_dir / "attempt-record.schema.json"),
            cls._load(cls.schema_dir / "attempt-outcome.schema.json"),
        )

    def test_positive_cases_A_through_H_are_conformant(self) -> None:
        report = AOI.run_audit(self.schema_dir, [self.examples])
        self.assertEqual("conformant", report.verdict)
        self.assertEqual(9, report.attempts)
        self.assertEqual(11, report.outcome_events)
        self.assertEqual([], report.findings)

    def test_product_failure_requires_an_executed_failed_product_gate(self) -> None:
        report = AOI.run_audit(
            self.schema_dir,
            [self.fixtures / "invalid-product-blame"],
        )
        self.assertEqual("non_conformant", report.verdict)
        self.assertIn("AOI-PRODUCT-BLAME", {item.code for item in report.findings})

    def test_product_verdict_must_match_target_gate_execution_and_result(self) -> None:
        _, outcome_schema = self._schemas()
        attempt = self._load(self.examples / "D-environment-failure" / "attempt.json")
        outcome = self._load(self.examples / "D-environment-failure" / "outcome.json")
        outcome["product_verdict"] = "not_executed"
        findings = AOI.validate_outcome(
            Path("executed-but-not-executed-verdict.json"),
            outcome,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            {outcome["event_id"]: outcome},
            {outcome["event_id"]: Path("executed-but-not-executed-verdict.json")},
        )
        self.assertIn("AOI-PRODUCT-NOT-EXECUTED", {item.code for item in findings})

    def test_terminal_outcome_requires_progression_fields(self) -> None:
        attempt_schema, outcome_schema = self._schemas()
        attempt = self._load(self.examples / "B-operator-error" / "attempt.json")
        outcome = self._load(self.examples / "B-operator-error" / "outcome.json")
        del outcome["last_successful_gate"]
        findings = AOI.validate_outcome(
            Path("missing-progression.json"),
            outcome,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            {outcome["event_id"]: outcome},
            {outcome["event_id"]: Path("missing-progression.json")},
        )
        self.assertIn("AOI-TERMINAL-FIELDS", {item.code for item in findings})
        self.assertEqual([], AOI.validate_schema_instance(attempt, attempt_schema))

    def test_correction_cannot_claim_validation_before_a_later_attempt(self) -> None:
        _, outcome_schema = self._schemas()
        attempt = self._load(self.examples / "H-correction-not-validated" / "attempt.json")
        correction = self._load(self.examples / "H-correction-not-validated" / "correction.json")
        correction["relations"].append(
            {"type": "validates_correction_for", "target_id": "case-H-environment-correction"}
        )
        findings = AOI.validate_outcome(
            Path("premature-correction.json"),
            correction,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            {correction["event_id"]: correction},
            {correction["event_id"]: Path("premature-correction.json")},
        )
        self.assertIn("AOI-CORRECTION-PREMATURE", {item.code for item in findings})

    def test_editorial_change_does_not_force_expensive_work_without_decision(self) -> None:
        _, outcome_schema = self._schemas()
        attempt = self._load(self.examples / "G-normative-materiality" / "old-attempt.json")
        event = self._load(self.examples / "G-normative-materiality" / "materiality.json")
        event["materiality"].update(
            {
                "change_class": "editorial",
                "affects_evidence": False,
                "requires_new_attempt": True,
                "decision_ref": None,
            }
        )
        findings = AOI.validate_outcome(
            Path("editorial-rerun.json"),
            event,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            {event["event_id"]: event},
            {event["event_id"]: Path("editorial-rerun.json")},
        )
        self.assertIn("AOI-NONMATERIAL-RERUN", {item.code for item in findings})

    def test_material_normative_change_requires_decision_rerun_and_lineage(self) -> None:
        _, outcome_schema = self._schemas()
        attempt = self._load(self.examples / "G-normative-materiality" / "old-attempt.json")
        event = self._load(self.examples / "G-normative-materiality" / "materiality.json")
        event["materiality"]["requires_new_attempt"] = False
        event["materiality"]["decision_ref"] = None
        event["relations"] = []
        findings = AOI.validate_outcome(
            Path("normative-without-lineage.json"),
            event,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            {event["event_id"]: event},
            {event["event_id"]: Path("normative-without-lineage.json")},
        )
        codes = {item.code for item in findings}
        self.assertTrue(
            {"AOI-NORMATIVE-RERUN", "AOI-NORMATIVE-DECISION", "AOI-NORMATIVE-LINEAGE"}.issubset(codes)
        )

    def test_retrospective_addendum_preserves_the_original_hash(self) -> None:
        _, outcome_schema = self._schemas()
        base = self.examples / "F-retrospective-classification"
        attempt = self._load(base / "attempt.json")
        original = self._load(base / "original-outcome.json")
        addendum = self._load(base / "classification-addendum.json")
        events = {original["event_id"]: original, addendum["event_id"]: addendum}
        event_paths = {
            original["event_id"]: base / "original-outcome.json",
            addendum["event_id"]: base / "classification-addendum.json",
        }
        findings = AOI.validate_outcome(
            base / "classification-addendum.json",
            addendum,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            events,
            event_paths,
        )
        self.assertEqual([], findings)
        changed = copy.deepcopy(addendum)
        changed["classification"]["target_record_sha256"] = "0" * 64
        findings = AOI.validate_outcome(
            Path("wrong-hash.json"),
            changed,
            outcome_schema,
            {attempt["attempt_id"]: attempt},
            {original["event_id"]: original, changed["event_id"]: changed},
            {original["event_id"]: base / "original-outcome.json", changed["event_id"]: Path("wrong-hash.json")},
        )
        self.assertIn("AOI-ADDENDUM-HASH", {item.code for item in findings})

    def test_policy_audit_rejects_bureaucracy_and_blanket_product_blame(self) -> None:
        path = self.fixtures / "overgoverned-policy.md"
        findings = AOI.audit_policy_text(path, path.read_text(encoding="utf-8"))
        self.assertEqual(
            {"AOI-BUREAUCRACY", "AOI-CLASSIFY-ALL"},
            {item.code for item in findings},
        )

    @unittest.skipUnless(shutil.which("git"), "Git is unavailable")
    def test_append_only_check_detects_a_rewritten_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            records = repository / "records"
            records.mkdir()
            record = records / "outcome.json"
            record.write_text('{"state":"original"}\n', encoding="utf-8")
            commands = [
                ["git", "init", "--quiet"],
                ["git", "config", "user.email", "fixture@example.invalid"],
                ["git", "config", "user.name", "Fixture"],
                ["git", "add", "records/outcome.json"],
                ["git", "commit", "--quiet", "-m", "fixture baseline"],
            ]
            for command in commands:
                subprocess.run(command, cwd=repository, check=True, capture_output=True)
            record.write_text('{"state":"rewritten"}\n', encoding="utf-8")
            findings = AOI.check_append_only(repository, "HEAD", ["records"])
            self.assertIn("AOI-APPEND-ONLY", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
