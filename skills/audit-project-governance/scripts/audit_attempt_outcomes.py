#!/usr/bin/env python3
"""Audit GFD attempt declarations and append-only outcome events."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PRODUCT_VERDICTS = {
    "passed",
    "failed",
    "not_executed",
    "not_applicable",
    "inconclusive",
}
FAILURE_CLASSES = {
    "product_failure",
    "operator_error",
    "orchestration_error",
    "environment_failure",
    "unclassified",
}
RELATION_TYPES = {
    "retries",
    "supersedes",
    "caused_by",
    "corrects",
    "validates_correction_for",
    "invalidated_by",
}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    confidence: str
    path: str
    message: str
    correction: str


@dataclass
class AuditReport:
    verdict: str
    attempts: int
    outcome_events: int
    findings: list[Finding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": "Attempt Outcome Integrity",
            "verdict": self.verdict,
            "attempts": self.attempts,
            "outcome_events": self.outcome_events,
            "findings": [asdict(finding) for finding in self.findings],
        }


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _resolve_local_ref(schema_root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"only local schema references are supported: {ref}")
    node: Any = schema_root
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    if not isinstance(node, dict):
        raise ValueError(f"schema reference does not resolve to an object: {ref}")
    return node


def validate_schema_instance(
    value: Any,
    schema: dict[str, Any],
    schema_root: dict[str, Any] | None = None,
    location: str = "$",
) -> list[str]:
    """Validate the JSON Schema subset used by the two GFD contracts."""

    root = schema if schema_root is None else schema_root
    errors: list[str] = []

    if "$ref" in schema:
        return validate_schema_instance(
            value,
            _resolve_local_ref(root, schema["$ref"]),
            root,
            location,
        )

    if "oneOf" in schema:
        matches = [
            validate_schema_instance(value, option, root, location)
            for option in schema["oneOf"]
        ]
        if sum(not result for result in matches) != 1:
            errors.append(f"{location}: expected exactly one matching schema")
        return errors

    expected_type = schema.get("type")
    if expected_type is not None:
        expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_type_matches(value, item) for item in expected_types):
            return [f"{location}: expected type {expected_types}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: {value!r} is not an allowed value")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: string is shorter than minLength")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{location}: string does not match {schema['pattern']}")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{location}: invalid date-time")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{location}: integer is below minimum")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: array has too few items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{location}: array items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    validate_schema_instance(item, item_schema, root, f"{location}[{index}]")
                )

    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{location}: missing required property {required}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{location}: unexpected property {key}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(
                    validate_schema_instance(value[key], child_schema, root, f"{location}.{key}")
                )

    return errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def finding(
    code: str,
    severity: str,
    path: Path | str,
    message: str,
    correction: str,
    confidence: str = "high",
) -> Finding:
    return Finding(code, severity, confidence, str(path), message, correction)


def validate_attempt(
    path: Path,
    record: dict[str, Any],
    schema: dict[str, Any],
) -> list[Finding]:
    findings: list[Finding] = []
    for error in validate_schema_instance(record, schema):
        findings.append(
            finding("AOI-SCHEMA", "high", path, error, "Conform the attempt to the published schema.")
        )
    if findings:
        return findings

    gates = record["planned_gates"]
    gate_ids = [gate["gate_id"] for gate in gates]
    sequences = [gate["sequence"] for gate in gates]
    if len(gate_ids) != len(set(gate_ids)):
        findings.append(
            finding("AOI-GATE-ID", "high", path, "planned gate identifiers are not unique", "Assign one stable identifier per gate.")
        )
    if len(sequences) != len(set(sequences)) or sequences != sorted(sequences):
        findings.append(
            finding("AOI-GATE-SEQUENCE", "high", path, "planned gate sequence is duplicated or unordered", "Use unique ascending gate sequence values.")
        )

    target = record["target_product_gate"]
    if target is not None:
        matching = [gate for gate in gates if gate["gate_id"] == target]
        if not matching or matching[0]["kind"] != "product":
            findings.append(
                finding("AOI-TARGET-GATE", "high", path, "target_product_gate does not identify a planned product gate", "Reference one planned gate with kind product.")
            )

    occurrence = record["source_occurrence_id"]
    promotion = record["promotion_basis"]
    if occurrence is not None and promotion is None:
        findings.append(
            finding("AOI-OCCURRENCE-PROMOTION", "medium", path, "session occurrence was promoted without a promotion basis", "Record declared attempt, material impact, recurrence, or causal significance.")
        )
    if occurrence is None and promotion not in (None, "declared_attempt"):
        findings.append(
            finding("AOI-OCCURRENCE-SOURCE", "medium", path, "promotion basis requires a source occurrence", "Add source_occurrence_id or use declared_attempt.")
        )
    return findings


def _relation_types(record: dict[str, Any]) -> set[str]:
    return {
        relation.get("type", "")
        for relation in record.get("relations", [])
        if isinstance(relation, dict)
    }


def _semantic_terminal_findings(
    path: Path,
    event: dict[str, Any],
    attempt: dict[str, Any],
) -> list[Finding]:
    findings: list[Finding] = []
    required = {
        "execution_status",
        "gate_results",
        "last_successful_gate",
        "terminal_gate",
        "product_gate_executed",
        "product_verdict",
        "primary_failure_classification",
        "contributing_factors",
    }
    missing = sorted(required - event.keys())
    if missing:
        return [
            finding("AOI-TERMINAL-FIELDS", "high", path, f"terminal outcome is missing {', '.join(missing)}", "Record execution, gate progression, verdict, and classification fields.")
        ]

    planned = {gate["gate_id"]: gate for gate in attempt["planned_gates"]}
    results = event["gate_results"]
    result_by_id: dict[str, dict[str, Any]] = {}
    for result in results:
        gate_id = result.get("gate_id")
        if gate_id in result_by_id:
            findings.append(
                finding("AOI-GATE-DUPLICATE", "high", path, f"gate result {gate_id} is duplicated", "Keep one result per gate in an outcome.")
            )
            continue
        result_by_id[gate_id] = result
        planned_gate = planned.get(gate_id)
        if planned_gate is None:
            findings.append(
                finding("AOI-GATE-UNPLANNED", "high", path, f"gate result {gate_id} was not declared", "Add the gate to the immutable attempt before execution.")
            )
            continue
        if result.get("sequence") != planned_gate["sequence"] or result.get("kind") != planned_gate["kind"]:
            findings.append(
                finding("AOI-GATE-IDENTITY", "high", path, f"gate result {gate_id} changes sequence or kind", "Preserve the planned gate identity.")
            )

        executed = result.get("executed")
        gate_result = result.get("result")
        proof_status = result.get("proof_status")
        if executed is False and gate_result not in {"not_executed", "not_applicable"}:
            findings.append(
                finding("AOI-GATE-NOT-RUN", "high", path, f"unexecuted gate {gate_id} has result {gate_result}", "Use not_executed or not_applicable.")
            )
        if executed is True and gate_result == "not_executed":
            findings.append(
                finding("AOI-GATE-RAN", "high", path, f"executed gate {gate_id} is marked not_executed", "Record the observed result or inconclusive.")
            )
        expected_proof = {
            "passed": "PASS",
            "failed": "FAIL",
            "not_executed": "UNAVAILABLE",
            "not_applicable": "SKIP",
            "inconclusive": "UNAVAILABLE",
        }.get(gate_result)
        if expected_proof and proof_status != expected_proof:
            findings.append(
                finding("AOI-PROOF-STATUS", "medium", path, f"gate {gate_id} result {gate_result} conflicts with proof status {proof_status}", f"Use proof status {expected_proof}.")
            )

    executed_results = [result for result in results if result.get("executed")]
    terminal_candidates = [
        result
        for result in results
        if result.get("executed") or result.get("result") == "not_applicable"
    ]
    expected_terminal = (
        max(terminal_candidates, key=lambda item: item.get("sequence", -1))["gate_id"]
        if terminal_candidates
        else None
    )
    if event["terminal_gate"] != expected_terminal:
        findings.append(
            finding("AOI-TERMINAL-GATE", "high", path, "terminal_gate is not the last executed gate", "Reference the executed gate with the highest declared sequence.")
        )

    passed_results = [
        result for result in executed_results if result.get("result") == "passed"
    ]
    expected_last_success = (
        max(passed_results, key=lambda item: item.get("sequence", -1))["gate_id"]
        if passed_results
        else None
    )
    if event["last_successful_gate"] != expected_last_success:
        findings.append(
            finding("AOI-LAST-SUCCESS", "high", path, "last_successful_gate does not match gate evidence", "Reference the highest-sequence executed passing gate.")
        )

    target_gate = attempt.get("target_product_gate")
    target_result = result_by_id.get(target_gate) if target_gate else None
    target_executed = bool(target_result and target_result.get("executed"))
    if event["product_gate_executed"] != target_executed:
        findings.append(
            finding("AOI-PRODUCT-EXECUTION", "high", path, "product_gate_executed conflicts with the target gate result", "Derive this field from the declared target gate evidence.")
        )

    verdict = event["product_verdict"]
    classification = event["primary_failure_classification"]
    if verdict == "failed":
        if not target_executed or not target_result or target_result.get("result") != "failed":
            findings.append(
                finding("AOI-PRODUCT-BLAME", "critical", path, "product failure was assigned without an executed failed product gate", "Use not_executed or inconclusive and route the correction to the observed failure layer.")
            )
        if classification != "product_failure":
            findings.append(
                finding("AOI-PRODUCT-CLASS", "high", path, "failed product verdict lacks product_failure classification", "Classify the observed product defect as product_failure.")
            )
    if verdict == "passed" and (
        not target_executed or not target_result or target_result.get("result") != "passed"
    ):
        findings.append(
            finding("AOI-PRODUCT-PASS", "critical", path, "product passed without an executed passing product gate", "Use not_executed or inconclusive until the product gate passes.")
        )
    if verdict in {"not_executed", "not_applicable", "inconclusive"} and classification == "product_failure":
        findings.append(
            finding("AOI-WRONG-LAYER", "critical", path, f"{verdict} cannot be classified as product_failure", "Use operator_error, orchestration_error, environment_failure, or unclassified from evidence.")
        )
    if verdict == "passed" and classification is not None:
        findings.append(
            finding("AOI-PASS-CLASS", "medium", path, "passing product outcome has a primary failure classification", "Use null when no failure occurred.")
        )
    return findings


def _semantic_addendum_findings(
    path: Path,
    event: dict[str, Any],
    events: dict[str, dict[str, Any]],
    event_paths: dict[str, Path],
) -> list[Finding]:
    findings: list[Finding] = []
    classification = event.get("classification")
    if not isinstance(classification, dict):
        return [
            finding("AOI-ADDENDUM-FIELDS", "high", path, "classification addendum lacks classification data", "Add target identity, hash, verdict, class, and rationale.")
        ]
    target_id = classification.get("target_event_id")
    supersedes = event.get("supersedes_event_id")
    if supersedes != target_id:
        findings.append(
            finding("AOI-ADDENDUM-LINK", "high", path, "classification addendum does not supersede its target event", "Set supersedes_event_id to target_event_id.")
        )
    target = events.get(target_id)
    if target is None:
        findings.append(
            finding("AOI-ADDENDUM-TARGET", "high", path, f"classification target {target_id!r} is unavailable", "Retain and reference the original event.")
        )
    else:
        expected_hash = sha256_file(event_paths[target_id])
        if classification.get("target_record_sha256", "").upper() != expected_hash:
            findings.append(
                finding("AOI-ADDENDUM-HASH", "high", path, "classification target hash does not match the preserved event", "Record the SHA-256 of the exact historical event bytes.")
            )
    if target is not None and classification.get("primary_failure_classification") == "product_failure":
        if not target.get("product_gate_executed") or target.get("product_verdict") != "failed":
            findings.append(
                finding("AOI-ADDENDUM-BLAME", "critical", path, "retrospective product_failure lacks an executed failed product gate", "Keep the classification unclassified or route it to the observed layer.")
            )
    if classification.get("product_verdict") in {"not_executed", "not_applicable", "inconclusive"} and classification.get("primary_failure_classification") == "product_failure":
        findings.append(
            finding("AOI-ADDENDUM-LAYER", "critical", path, "retrospective classification blames an unexecuted product", "Use a non-product class supported by evidence.")
        )
    return findings


def _semantic_materiality_findings(path: Path, event: dict[str, Any]) -> list[Finding]:
    materiality = event.get("materiality")
    if not isinstance(materiality, dict):
        return [
            finding("AOI-MATERIALITY-FIELDS", "high", path, "materiality event lacks assessment data", "Record change class, affected evidence, decision, and rerun choice.")
        ]
    findings: list[Finding] = []
    change_class = materiality.get("change_class")
    affects = materiality.get("affects_evidence")
    rerun = materiality.get("requires_new_attempt")
    decision = materiality.get("decision_ref")
    relations = _relation_types(event)
    if change_class in {"editorial", "observational"} and rerun and not decision:
        findings.append(
            finding("AOI-NONMATERIAL-RERUN", "medium", path, f"{change_class} change forces a new attempt without an exception decision", "Keep prior evidence or cite a decision explaining the material effect.")
        )
    if change_class == "normative" and affects:
        if not rerun:
            findings.append(
                finding("AOI-NORMATIVE-RERUN", "high", path, "material normative change does not require a new attempt", "Require a new attempt for affected gates.")
            )
        if not decision:
            findings.append(
                finding("AOI-NORMATIVE-DECISION", "high", path, "normative change lacks a decision reference", "Cite the authority changing the acceptance contract.")
            )
        if "invalidated_by" not in relations:
            findings.append(
                finding("AOI-NORMATIVE-LINEAGE", "high", path, "material normative change does not invalidate or supersede prior evidence", "Add an invalidated_by relation.")
            )
    if change_class == "implementation_or_material_environment" and affects:
        if not decision or not materiality.get("affected_gate_ids"):
            findings.append(
                finding("AOI-MATERIAL-DECISION", "high", path, "material implementation or environment change lacks gate-scoped decision", "Cite the decision and affected gates.")
            )
    return findings


def _semantic_correction_findings(path: Path, event: dict[str, Any]) -> list[Finding]:
    correction = event.get("correction")
    if not isinstance(correction, dict):
        return [
            finding("AOI-CORRECTION-FIELDS", "high", path, "correction event lacks correction data", "Record correction identifier, state, description, and evidence.")
        ]
    relations = _relation_types(event)
    state = correction.get("state")
    findings: list[Finding] = []
    if state == "applied_not_validated" and "validates_correction_for" in relations:
        findings.append(
            finding("AOI-CORRECTION-PREMATURE", "high", path, "unvalidated correction claims a validation relation", "Remove the validation claim until a later attempt supplies evidence.")
        )
    if state == "validated" and "validates_correction_for" not in relations:
        findings.append(
            finding("AOI-CORRECTION-VALIDATION", "high", path, "validated correction lacks a validating attempt relation", "Link the later attempt that validates the correction.")
        )
    return findings


def validate_outcome(
    path: Path,
    event: dict[str, Any],
    schema: dict[str, Any],
    attempts: dict[str, dict[str, Any]],
    events: dict[str, dict[str, Any]],
    event_paths: dict[str, Path],
) -> list[Finding]:
    findings: list[Finding] = []
    for error in validate_schema_instance(event, schema):
        findings.append(
            finding("AOI-SCHEMA", "high", path, error, "Conform the outcome event to the published schema.")
        )
    if findings:
        return findings

    attempt = attempts.get(event["attempt_id"])
    if attempt is None:
        return [
            finding("AOI-ATTEMPT-REF", "high", path, f"attempt {event['attempt_id']!r} is unavailable", "Retain and reference the immutable attempt declaration.")
        ]

    kind = event["record_kind"]
    if kind == "terminal_outcome":
        findings.extend(_semantic_terminal_findings(path, event, attempt))
    elif kind == "classification_addendum":
        findings.extend(_semantic_addendum_findings(path, event, events, event_paths))
    elif kind == "materiality_assessment":
        findings.extend(_semantic_materiality_findings(path, event))
    elif kind == "correction_update":
        findings.extend(_semantic_correction_findings(path, event))

    for relation in event.get("relations", []):
        if relation.get("type") not in RELATION_TYPES:
            findings.append(
                finding("AOI-RELATION", "medium", path, f"unknown causal relation {relation.get('type')!r}", "Use a relation defined by the outcome schema.")
            )
    return findings


def audit_policy_text(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lowered = " ".join(text.lower().split())
    if re.search(r"every\s+(?:failed\s+)?(?:read|command|path|lookup).*\battempt\b", lowered):
        findings.append(
            finding("AOI-BUREAUCRACY", "medium", path, "policy promotes every trivial session occurrence into a governed attempt", "Require declared purpose, material impact, recurrence, or causal significance.")
        )
    if re.search(r"(?:every|all)\s+(?:error|failure)s?.{0,40}\bproduct_failure\b", lowered):
        findings.append(
            finding("AOI-CLASSIFY-ALL", "critical", path, "policy classifies failures as product_failure without execution evidence", "Route by product, operator, orchestration, environment, or unclassified evidence.")
        )
    return findings


def check_append_only(
    repository: Path,
    baseline_ref: str,
    record_paths: list[str],
) -> list[Finding]:
    command = ["git", "diff", "--name-status", baseline_ref, "--", *record_paths]
    completed = subprocess.run(
        command,
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        return [
            finding("AOI-GIT-UNAVAILABLE", "medium", repository, completed.stderr.strip() or "git append-only check failed", "Provide a reachable baseline ref and tracked record paths.", "medium")
        ]
    findings: list[Finding] = []
    for line in completed.stdout.splitlines():
        status, _, name = line.partition("\t")
        if status.startswith("A"):
            continue
        findings.append(
            finding("AOI-APPEND-ONLY", "high", name or repository, f"historical record changed with Git status {status}", "Append a superseding event instead of modifying or deleting the original record.")
        )
    return findings


def discover_record_files(record_roots: Iterable[Path]) -> list[Path]:
    paths: set[Path] = set()
    for root in record_roots:
        if root.is_file() and root.suffix.lower() == ".json":
            paths.add(root.resolve())
        elif root.is_dir():
            paths.update(path.resolve() for path in root.rglob("*.json"))
    return sorted(paths)


def run_audit(
    schema_dir: Path,
    record_roots: list[Path],
    policy_paths: list[Path] | None = None,
    repository: Path | None = None,
    baseline_ref: str | None = None,
    append_only_paths: list[str] | None = None,
) -> AuditReport:
    attempt_schema_path = schema_dir / "attempt-record.schema.json"
    outcome_schema_path = schema_dir / "attempt-outcome.schema.json"
    if not attempt_schema_path.is_file() or not outcome_schema_path.is_file():
        missing = attempt_schema_path if not attempt_schema_path.is_file() else outcome_schema_path
        item = finding("AOI-SCHEMA-UNAVAILABLE", "high", missing, "required schema is unavailable", "Provide both GFD attempt governance schemas.")
        return AuditReport("not_evaluable", 0, 0, [item])

    try:
        attempt_schema = load_json(attempt_schema_path)
        outcome_schema = load_json(outcome_schema_path)
    except (OSError, json.JSONDecodeError) as error:
        item = finding("AOI-SCHEMA-PARSE", "high", schema_dir, str(error), "Repair the schema JSON before evaluating records.")
        return AuditReport("not_evaluable", 0, 0, [item])

    findings: list[Finding] = []
    attempts: dict[str, dict[str, Any]] = {}
    attempt_paths: dict[str, Path] = {}
    events: dict[str, dict[str, Any]] = {}
    event_paths: dict[str, Path] = {}

    for path in discover_record_files(record_roots):
        try:
            record = load_json(path)
        except (OSError, json.JSONDecodeError) as error:
            findings.append(
                finding("AOI-JSON-PARSE", "high", path, str(error), "Repair or remove the invalid JSON record.")
            )
            continue
        if not isinstance(record, dict):
            findings.append(
                finding("AOI-RECORD-TYPE", "high", path, "JSON record is not an object", "Use an attempt or outcome object.")
            )
            continue
        record_type = record.get("record_type")
        if record_type == "attempt":
            identifier = record.get("attempt_id")
            if isinstance(identifier, str) and identifier in attempts:
                findings.append(
                    finding("AOI-ATTEMPT-DUPLICATE", "high", path, f"attempt_id {identifier} duplicates {attempt_paths[identifier]}", "Assign a globally stable attempt identifier.")
                )
            elif isinstance(identifier, str):
                attempts[identifier] = record
                attempt_paths[identifier] = path
            findings.extend(validate_attempt(path, record, attempt_schema))
        elif record_type == "attempt_outcome_event":
            identifier = record.get("event_id")
            if isinstance(identifier, str) and identifier in events:
                findings.append(
                    finding("AOI-EVENT-DUPLICATE", "high", path, f"event_id {identifier} duplicates {event_paths[identifier]}", "Assign a globally stable outcome event identifier.")
                )
            elif isinstance(identifier, str):
                events[identifier] = record
                event_paths[identifier] = path
        elif "$schema" not in record:
            findings.append(
                finding("AOI-UNKNOWN-RECORD", "medium", path, "JSON file is neither a schema nor a GFD attempt record", "Limit audit roots to attempt governance records.", "medium")
            )

    for identifier, event in events.items():
        findings.extend(
            validate_outcome(
                event_paths[identifier],
                event,
                outcome_schema,
                attempts,
                events,
                event_paths,
            )
        )

    for path in policy_paths or []:
        try:
            findings.extend(audit_policy_text(path, path.read_text(encoding="utf-8")))
        except OSError as error:
            findings.append(
                finding("AOI-POLICY-UNAVAILABLE", "medium", path, str(error), "Provide a readable policy file.", "medium")
            )

    if repository and baseline_ref and append_only_paths:
        findings.extend(
            check_append_only(repository, baseline_ref, append_only_paths)
        )

    if not attempts and not events and not findings:
        verdict = "not_applicable"
    elif any(item.severity in {"critical", "high"} for item in findings):
        verdict = "non_conformant"
    elif findings:
        verdict = "partially_conformant"
    else:
        verdict = "conformant"
    return AuditReport(verdict, len(attempts), len(events), findings)


def print_text(report: AuditReport) -> None:
    print("Attempt Outcome Integrity")
    print(f"VERDICT {report.verdict}")
    print(f"ATTEMPTS {report.attempts}")
    print(f"OUTCOME_EVENTS {report.outcome_events}")
    if not report.findings:
        print("PASS no attempt outcome integrity finding")
        return
    for item in report.findings:
        print(
            f"{item.severity.upper():13} {item.code} {item.path}: "
            f"{item.message} Correction: {item.correction}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--schema-dir", type=Path)
    parser.add_argument("--records", type=Path, action="append")
    parser.add_argument("--policy", type=Path, action="append", default=[])
    parser.add_argument("--baseline-ref")
    parser.add_argument("--append-only-path", action="append", default=[])
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    schema_dir = (args.schema_dir or root / "schemas").resolve()
    record_roots = [path.resolve() for path in (args.records or [root / "examples" / "attempt-lineage"])]
    report = run_audit(
        schema_dir=schema_dir,
        record_roots=record_roots,
        policy_paths=[path.resolve() for path in args.policy],
        repository=root if args.baseline_ref else None,
        baseline_ref=args.baseline_ref,
        append_only_paths=args.append_only_path,
    )
    if args.json_output:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print_text(report)
    return 1 if report.verdict in {"non_conformant", "not_evaluable"} else 0


if __name__ == "__main__":
    sys.exit(main())
