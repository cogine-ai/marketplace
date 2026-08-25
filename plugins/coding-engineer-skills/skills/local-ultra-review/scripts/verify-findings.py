#!/usr/bin/env python3
import argparse
import collections
import json
from pathlib import Path


TERMINAL_STATUSES = {"confirmed", "false_positive", "pre_existing", "needs_manual_review"}
CANDIDATE_REQUIRED = [
    "id",
    "title",
    "severity",
    "category",
    "file",
    "line",
    "failure_scenario",
    "evidence",
    "verification_plan",
    "confidence",
    "reviewer",
]


def load_jsonl(path):
    rows = []
    with Path(path).open(encoding="utf-8") as fh:
        for idx, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                rows.append({"id": f"invalid-json-{idx}", "_invalid": True, "_error": str(exc), "_source": str(path)})
                continue
            if not isinstance(row, dict):
                rows.append(
                    {
                        "id": f"invalid-json-type-{idx}",
                        "_invalid": True,
                        "_error": "JSONL row is not an object",
                        "_source": str(path),
                    }
                )
                continue
            rows.append(row)
    return rows


def collect_candidates(inputs):
    rows = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.glob("*.jsonl")):
                rows.extend(
                    row
                    for row in load_jsonl(child)
                    if row.get("type") != "reviewer_complete"
                )
        else:
            rows.extend(
                row for row in load_jsonl(path) if row.get("type") != "reviewer_complete"
            )
    return rows


def line_exists(repo, file_path, line):
    path = repo / file_path
    if not path.exists() or not path.is_file():
        return False, "file does not exist"
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        return False, f"file could not be read: {exc}"
    if line < 1 or line > len(lines):
        return False, f"line {line} is outside file length {len(lines)}"
    return True, lines[line - 1]


def input_paths(inputs):
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(path.glob("*.jsonl"))
        else:
            yield path


def candidate_key(candidate):
    candidate_id = candidate.get("id") or candidate.get("candidate_id") or "unknown"
    return candidate.get("reviewer") or "", candidate_id


def collect_verdicts(inputs):
    verdicts = {}
    verdict_rows = []
    completions = []
    errors = []
    for path in input_paths(inputs):
        rows = []
        with path.open(encoding="utf-8") as fh:
            for line_number, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
                    continue
                if not isinstance(row, dict):
                    errors.append(f"{path}:{line_number}: verdict output is not a JSON object")
                    continue
                rows.append((line_number, row))

        for index, (line_number, row) in enumerate(rows):
            if row.get("type") == "verifier_complete":
                if index != len(rows) - 1:
                    errors.append(f"{path}:{line_number}: verifier completion must be the final line")
                completions.append(row)
                continue
            candidate_id = row.get("candidate_id")
            reviewer = row.get("reviewer")
            if not candidate_id or not reviewer:
                errors.append(
                    f"{path}:{line_number}: verifier verdict requires candidate_id and reviewer"
                )
                continue
            verdict_rows.append(row)
            verdicts.setdefault((reviewer, candidate_id), []).append(row)
    return verdicts, verdict_rows, completions, errors


def independent_verdict(candidate, verdicts, duplicate_candidate_keys):
    key = candidate_key(candidate)
    if key in duplicate_candidate_keys:
        return None, "candidate id is duplicated within its originating reviewer"
    rows = verdicts.get(key, [])
    if len(rows) != 1:
        if not rows:
            return None, "no independent verifier verdict was supplied"
        return None, "multiple verifier verdicts were supplied"

    verdict = rows[0]
    status = verdict.get("status")
    verifier_id = verdict.get("verifier_id")
    reviewer_id = candidate.get("reviewer")
    if status not in TERMINAL_STATUSES:
        return None, "verifier verdict has an invalid status"
    if verdict.get("independent") is not True:
        return None, "verifier verdict did not assert an independent context"
    if not verifier_id:
        return None, "verifier verdict is missing verifier_id"
    if not reviewer_id:
        return None, "candidate is missing its originating reviewer id"
    if verifier_id == reviewer_id:
        return None, "verifier_id matches the originating reviewer"
    if not verdict.get("summary"):
        return None, "verifier verdict is missing a summary"
    return verdict, ""


def verifier_payload(verdict, notes):
    payload = {
        "summary": verdict["summary"],
        "method": "independent_verifier",
        "verifier_id": verdict["verifier_id"],
        "independent": True,
        "notes": notes,
    }
    if isinstance(verdict.get("notes"), list) and verdict["notes"]:
        payload["notes"] = verdict["notes"] + notes
    return payload


def verify_candidate(candidate, repo, changed_paths, verdicts, duplicate_candidate_keys):
    cid = candidate.get("id") or candidate.get("candidate_id") or "unknown"
    base = {
        "candidate_id": cid,
        "reviewer": candidate.get("reviewer", ""),
        "title": candidate.get("title", ""),
        "severity": candidate.get("severity", "NeedsManualReview"),
        "category": candidate.get("category", "other"),
        "file": candidate.get("file", ""),
        "line": candidate.get("line", 0),
        "introduced_by_diff": bool(candidate.get("introduced_by_diff")),
        "failure_scenario": candidate.get("failure_scenario", ""),
        "evidence": candidate.get("evidence", []),
        "suggested_fix_direction": candidate.get("suggested_fix_direction", ""),
    }

    notes = []
    if candidate.get("_invalid"):
        base["status"] = "false_positive"
        base["verification"] = {"summary": candidate.get("_error", "invalid JSON"), "method": "static", "notes": ["candidate was not parseable JSON"]}
        return base

    missing = [key for key in CANDIDATE_REQUIRED if candidate.get(key) in ("", None, [])]
    if missing:
        notes.append("missing required fields: " + ", ".join(missing))

    path = candidate.get("file", "")
    line = candidate.get("line", 0)
    exists, line_info = line_exists(repo, path, int(line) if isinstance(line, int) else 0)
    if not exists:
        base["status"] = "false_positive"
        base["verification"] = {"summary": line_info, "method": "static", "notes": notes}
        return base
    notes.append(f"line exists: {path}:{line}")

    if path not in changed_paths:
        notes.append("referenced file is not in changed_files")

    verdict, verdict_error = independent_verdict(
        candidate,
        verdicts,
        duplicate_candidate_keys,
    )
    if verdict is not None and verdict["status"] != "confirmed":
        base["status"] = verdict["status"]
        if verdict["status"] == "pre_existing":
            base["severity"] = "Pre-existing"
        base["verification"] = verifier_payload(verdict, notes)
        return base
    if verdict_error:
        notes.append(verdict_error)

    if candidate.get("introduced_by_diff") is False or candidate.get("severity") == "Pre-existing":
        base["status"] = "pre_existing"
        base["severity"] = "Pre-existing"
        base["verification"] = {"summary": "Candidate is marked as not introduced by the diff.", "method": "base_comparison", "notes": notes}
        return base

    if candidate.get("confidence") != "high":
        base["status"] = "needs_manual_review"
        base["verification"] = {"summary": "Candidate did not meet high-confidence gate.", "method": "static", "notes": notes}
        return base

    if missing:
        base["status"] = "needs_manual_review"
        base["verification"] = {"summary": "Candidate is missing required proof fields.", "method": "static", "notes": notes}
        return base

    if verdict is not None:
        base["status"] = "confirmed"
        base["verification"] = verifier_payload(verdict, notes)
        return base

    base["status"] = "needs_manual_review"
    base["verification"] = {"summary": "Programmatic gates passed, but no independent verifier confirmation was attached.", "method": "static", "notes": notes}
    return base


def reviewer_execution_state(manifest, candidate_count):
    errors = []
    reviewers = manifest.get("reviewers") or []
    required_count = manifest.get("required_reviewer_count", len(reviewers))
    if manifest.get("execution_complete") is not True:
        errors.append("reviewer manifest is not complete")
    if not reviewers or len(reviewers) != required_count:
        errors.append("reviewer manifest does not contain every required reviewer")
    identities = [row.get("reviewer") for row in reviewers]
    if any(not identity for identity in identities) or len(set(identities)) != len(identities):
        errors.append("reviewer manifest identities are missing or duplicated")
    if any(row.get("status") != "completed" for row in reviewers):
        errors.append("one or more reviewers did not complete")
    for row in reviewers:
        receipt = row.get("completion_receipt")
        row_candidate_count = row.get("candidates", 0)
        receipt_valid = (
            isinstance(receipt, dict)
            and receipt.get("type") == "reviewer_complete"
            and receipt.get("reviewer") == row.get("reviewer")
            and not isinstance(receipt.get("candidate_count"), bool)
            and receipt.get("candidate_count") == row_candidate_count
        )
        if not receipt_valid:
            errors.append("reviewer completion receipt is missing or invalid")
    reported_candidates = sum(
        row.get("candidates", 0)
        for row in reviewers
        if isinstance(row.get("candidates", 0), int)
        and not isinstance(row.get("candidates", 0), bool)
    )
    if reported_candidates != candidate_count:
        errors.append(
            f"reviewer candidate count {reported_candidates} does not match "
            f"{candidate_count} collected candidates"
        )
    return not errors, errors


def verifier_execution_state(candidates, verdicts, verdict_rows, completions, parse_errors):
    errors = list(parse_errors)
    completion = completions[0] if len(completions) == 1 else None
    if len(completions) != 1:
        errors.append("exactly one verifier completion record is required")

    candidate_keys = [candidate_key(candidate) for candidate in candidates]
    duplicate_candidate_keys = {
        key for key, count in collections.Counter(candidate_keys).items() if count > 1
    }
    if duplicate_candidate_keys:
        errors.append("candidate ids are duplicated within an originating reviewer")

    malformed_candidates = []
    for candidate in candidates:
        if candidate.get("_invalid"):
            malformed_candidates.append(candidate_key(candidate))
            continue
        missing = [key for key in CANDIDATE_REQUIRED if candidate.get(key) in ("", None, [])]
        if missing:
            malformed_candidates.append(candidate_key(candidate))
    if malformed_candidates:
        errors.append("one or more candidates do not satisfy the candidate protocol")

    for key in set(candidate_keys):
        rows = verdicts.get(key, [])
        if len(rows) != 1:
            errors.append(f"candidate {key[0]}:{key[1]} does not have exactly one verdict")
            continue
        _, verdict_error = independent_verdict(
            {"reviewer": key[0], "id": key[1]},
            verdicts,
            duplicate_candidate_keys,
        )
        if verdict_error:
            errors.append(f"candidate {key[0]}:{key[1]}: {verdict_error}")

    extra_verdict_keys = set(verdicts) - set(candidate_keys)
    if extra_verdict_keys:
        errors.append("verifier output contains verdicts for unknown candidates")

    if completion is not None:
        candidate_count = completion.get("candidate_count")
        verdict_count = completion.get("verdict_count")
        verifier_id = completion.get("verifier_id")
        if isinstance(candidate_count, bool) or candidate_count != len(candidates):
            errors.append("verifier completion candidate_count does not match candidates")
        if isinstance(verdict_count, bool) or verdict_count != len(verdict_rows):
            errors.append("verifier completion verdict_count does not match verdict rows")
        if not verifier_id:
            errors.append("verifier completion is missing verifier_id")
        if any(row.get("verifier_id") != verifier_id for row in verdict_rows):
            errors.append("verdict verifier_id does not match the completion record")

    return not errors, completion, duplicate_candidate_keys, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--candidates", nargs="+", required=True)
    parser.add_argument("--verdicts", nargs="*", default=[])
    parser.add_argument("--reviewers", required=True)
    parser.add_argument("--out-jsonl", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
    repo = Path(bundle.get("repo_root", "."))
    changed_paths = {item["path"] for item in bundle.get("changed_files", [])}
    candidates = collect_candidates(args.candidates)
    reviewer_manifest = json.loads(Path(args.reviewers).read_text(encoding="utf-8"))
    verdicts, verdict_rows, completions, verdict_parse_errors = collect_verdicts(args.verdicts)
    verifier_complete, completion, duplicate_candidate_keys, verifier_errors = verifier_execution_state(
        candidates,
        verdicts,
        verdict_rows,
        completions,
        verdict_parse_errors,
    )
    verified = [
        verify_candidate(
            candidate,
            repo,
            changed_paths,
            verdicts,
            duplicate_candidate_keys,
        )
        for candidate in candidates
    ]
    reviewers_complete, reviewer_errors = reviewer_execution_state(
        reviewer_manifest,
        len(candidates),
    )

    out_jsonl = Path(args.out_jsonl)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_jsonl.open("w", encoding="utf-8") as fh:
        for row in verified:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    counts = {}
    for row in verified:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    execution_errors = reviewer_errors + verifier_errors
    execution = {
        "execution_complete": reviewers_complete and verifier_complete,
        "reviewers_complete": reviewers_complete,
        "verifier_complete": verifier_complete,
        "candidate_count": len(candidates),
        "verdict_count": len(verdict_rows),
        "verifier_id": (completion or {}).get("verifier_id", ""),
        "mode": reviewer_manifest.get("mode", ""),
        "reviewers": reviewer_manifest.get("reviewers", []),
        "errors": execution_errors,
    }
    payload = {"counts": counts, "findings": verified, "execution": execution}
    Path(args.out_json).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "counts": counts,
                "execution": execution,
                "out_jsonl": str(out_jsonl),
                "out_json": args.out_json,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
