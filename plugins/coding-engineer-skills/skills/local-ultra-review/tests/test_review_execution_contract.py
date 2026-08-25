import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUN_REVIEWERS = SKILL_ROOT / "scripts" / "run-reviewers.py"
VERIFY_FINDINGS = SKILL_ROOT / "scripts" / "verify-findings.py"
RENDER_REPORT = SKILL_ROOT / "scripts" / "render-report.py"
RENDER_GITHUB_SUMMARY = SKILL_ROOT / "scripts" / "render-github-summary.py"


class ReviewerExecutionContractTests(unittest.TestCase):
    def make_bundle(self, root: Path):
        repo = root / "repo with spaces"
        repo.mkdir()
        (repo / "sample.py").write_text("print('ok')\n", encoding="utf-8")
        bundle = root / "review bundle.json"
        bundle.write_text(
            json.dumps({"repo_root": str(repo), "changed_files": [{"path": "sample.py"}]}),
            encoding="utf-8",
        )
        return repo, bundle

    def test_packets_backend_generates_five_packets_but_never_claims_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, bundle = self.make_bundle(root)
            out = root / "review packets"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUN_REVIEWERS),
                    "--bundle",
                    str(bundle),
                    "--mode",
                    "deep",
                    "--backend",
                    "packets",
                    "--out",
                    str(out),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["execution_complete"])
            self.assertEqual(5, len(manifest["reviewers"]))
            self.assertEqual({"packet_generated"}, {row["status"] for row in manifest["reviewers"]})
            self.assertEqual(5, len(list(out.glob("*.prompt.md"))))

    def test_light_packets_include_a_dedicated_security_reviewer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, bundle = self.make_bundle(root)
            out = root / "light review packets"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUN_REVIEWERS),
                    "--bundle",
                    str(bundle),
                    "--mode",
                    "light",
                    "--backend",
                    "packets",
                    "--out",
                    str(out),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(4, manifest["required_reviewer_count"])
            self.assertEqual(
                {"correctness", "security", "integration", "tests"},
                {row["reviewer"] for row in manifest["reviewers"]},
            )
            self.assertTrue((out / "security.prompt.md").is_file())

    def test_cli_backend_rejects_a_noop_command_that_emits_no_completion_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, bundle = self.make_bundle(root)
            out = root / "cli output"
            command = [sys.executable, "-c", "import sys; sys.stdin.read()"]
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUN_REVIEWERS),
                    "--bundle",
                    str(bundle),
                    "--mode",
                    "deep",
                    "--backend",
                    "cli",
                    "--parallelism",
                    "1",
                    "--cwd",
                    str(repo),
                    "--out",
                    str(out),
                    "--command",
                    *command,
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(0, proc.returncode)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(command, manifest["command"])
            self.assertFalse(manifest["execution_complete"])
            self.assertEqual({"failed"}, {row["status"] for row in manifest["reviewers"]})

    def test_cli_backend_accepts_explicit_zero_finding_completion_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, bundle = self.make_bundle(root)
            out = root / "cli output"
            command = [
                sys.executable,
                "-c",
                (
                    "import json,re,sys; "
                    "prompt=sys.stdin.read(); "
                    "role=re.search(r'You are the `([^`]+)` reviewer', prompt).group(1); "
                    "print(json.dumps({'type':'reviewer_complete','reviewer':role,'candidate_count':0}))"
                ),
            ]
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUN_REVIEWERS),
                    "--bundle",
                    str(bundle),
                    "--mode",
                    "deep",
                    "--backend",
                    "cli",
                    "--parallelism",
                    "1",
                    "--cwd",
                    str(repo),
                    "--out",
                    str(out),
                    "--command",
                    *command,
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["execution_complete"])
            self.assertEqual({"completed"}, {row["status"] for row in manifest["reviewers"]})
            self.assertEqual(0, sum(row["candidates"] for row in manifest["reviewers"]))

    def test_report_marks_packet_only_runs_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, bundle = self.make_bundle(root)
            reviewers = root / "reviewers.json"
            reviewers.write_text(
                json.dumps(
                    {
                        "mode": "deep",
                        "backend": "packets",
                        "execution_complete": False,
                        "reviewers": [
                            {"reviewer": role, "status": "packet_generated", "candidates": 0}
                            for role in ["correctness", "security", "integration", "state-concurrency", "tests"]
                        ],
                    }
                ),
                encoding="utf-8",
            )
            findings = root / "findings.json"
            findings.write_text(json.dumps({"counts": {}}), encoding="utf-8")
            execution = root / "verification.json"
            execution.write_text(
                json.dumps(
                    {
                        "execution": {
                            "execution_complete": False,
                            "reviewers_complete": False,
                            "verifier_complete": False,
                            "mode": "deep",
                            "reviewers": json.loads(
                                reviewers.read_text(encoding="utf-8")
                            )["reviewers"],
                            "errors": ["reviewer packets were not executed"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            report = root / "report.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_REPORT),
                    "--bundle",
                    str(bundle),
                    "--findings",
                    str(findings),
                    "--execution",
                    str(execution),
                    "--out",
                    str(report),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            text = report.read_text(encoding="utf-8")
            self.assertIn("Execution status: `INCOMPLETE`", text)
            self.assertIn("reviewer packets were not executed", text)

    def test_github_summary_refuses_incomplete_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pr_context = root / "pr-context.json"
            pr_context.write_text(
                json.dumps(
                    {
                        "number": 12,
                        "title": "Example",
                        "head_sha": "a" * 40,
                    }
                ),
                encoding="utf-8",
            )
            findings = root / "findings.json"
            findings.write_text(json.dumps({"important": [], "nits": []}), encoding="utf-8")
            execution = root / "verification.json"
            execution.write_text(
                json.dumps({"execution": {"execution_complete": False}}),
                encoding="utf-8",
            )
            out = root / "github-summary.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RENDER_GITHUB_SUMMARY),
                    "--pr-context",
                    str(pr_context),
                    "--findings",
                    str(findings),
                    "--execution",
                    str(execution),
                    "--out",
                    str(out),
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(0, proc.returncode)
            self.assertIn("review execution is incomplete", proc.stderr)
            self.assertFalse(out.exists())


class ArtifactPathContractTests(unittest.TestCase):
    def test_worktree_pipeline_uses_one_absolute_session_directory(self):
        for path in [SKILL_ROOT / "SKILL.md", SKILL_ROOT / "README.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("<session-dir>", text, str(path))
            self.assertNotRegex(
                text,
                re.compile(r'--(?:out|bundle|candidates|verdicts|reviewers|verification|findings|execution|report|pr-context|body-file|session-dir) "\.local-ultra-review/'),
                str(path),
            )
            self.assertRegex(
                text,
                re.compile(
                    r'finalize-session\.sh"\s*\\\s*'
                    r'--session-dir "<session-dir>"'
                ),
                str(path),
            )

    def test_absolute_session_directory_survives_worktree_collection_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo with spaces"
            repo.mkdir()
            for args in [
                ["git", "init", "-b", "main"],
                ["git", "config", "user.name", "Local Ultra Test"],
                ["git", "config", "user.email", "local-ultra@example.invalid"],
            ]:
                subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True)
            (repo / "sample.py").write_text("print('ok')\n", encoding="utf-8")
            subprocess.run(["git", "add", "sample.py"], cwd=repo, check=True)
            subprocess.run(
                ["git", "commit", "-m", "initial"],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            )

            output_root = repo / ".local-ultra-review"
            prepare = subprocess.run(
                [
                    "bash",
                    str(SKILL_ROOT / "scripts" / "prepare-worktree.sh"),
                    "--base",
                    "HEAD",
                    "--session-id",
                    "path-contract",
                    "--output-dir",
                    str(output_root),
                ],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            )
            metadata = json.loads(prepare.stdout)
            session_dir = Path(metadata["session_dir"])
            worktree = Path(metadata["worktree"])
            self.assertEqual(output_root / "path-contract", session_dir)

            subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "collect-context.py"),
                    "--base",
                    "HEAD",
                    "--out",
                    str(session_dir / "review-bundle.json"),
                ],
                cwd=worktree,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((session_dir / "review-bundle.json").is_file())
            self.assertFalse((worktree / ".local-ultra-review").exists())

            finalize = subprocess.run(
                [
                    "bash",
                    str(SKILL_ROOT / "scripts" / "finalize-session.sh"),
                    "--session-dir",
                    str(session_dir),
                    "--status",
                    "success",
                ],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, finalize.returncode, finalize.stderr or finalize.stdout)
            self.assertFalse(worktree.exists(), finalize.stdout)
            self.assertTrue((session_dir / "review-bundle.json").is_file())


class IndependentVerifierContractTests(unittest.TestCase):
    def run_verifier(
        self,
        root: Path,
        candidates: dict | list[dict],
        verdicts: dict | list[dict] | None = None,
        include_completion: bool = True,
        include_reviewer_receipts: bool = True,
        include_candidate_receipt_in_jsonl: bool = False,
    ):
        _, bundle = ReviewerExecutionContractTests().make_bundle(root)
        candidate_rows = candidates if isinstance(candidates, list) else [candidates]
        candidate_path = root / "candidates.jsonl"
        candidate_output_rows = list(candidate_rows)
        if include_candidate_receipt_in_jsonl:
            candidate_output_rows.append(
                {
                    "type": "reviewer_complete",
                    "reviewer": "correctness",
                    "candidate_count": sum(
                        1 for row in candidate_rows if row.get("reviewer") == "correctness"
                    ),
                }
            )
        candidate_path.write_text(
            "".join(json.dumps(row) + "\n" for row in candidate_output_rows),
            encoding="utf-8",
        )
        reviewer_manifest = root / "reviewers.json"
        reviewer_manifest.write_text(
            json.dumps(
                {
                    "mode": "deep",
                    "backend": "host",
                    "execution_complete": True,
                    "required_reviewer_count": 5,
                    "reviewers": [
                        {
                            **{
                                "reviewer": reviewer,
                                "status": "completed",
                                "candidates": sum(
                                    1
                                    for row in candidate_rows
                                    if row.get("reviewer") == reviewer
                                ),
                            },
                            **(
                                {
                                    "completion_receipt": {
                                        "type": "reviewer_complete",
                                        "reviewer": reviewer,
                                        "candidate_count": sum(
                                            1
                                            for row in candidate_rows
                                            if row.get("reviewer") == reviewer
                                        ),
                                    }
                                }
                                if include_reviewer_receipts
                                else {}
                            ),
                        }
                        for reviewer in [
                            "correctness",
                            "security",
                            "integration",
                            "state-concurrency",
                            "tests",
                        ]
                    ],
                }
            ),
            encoding="utf-8",
        )
        args = [
            sys.executable,
            str(VERIFY_FINDINGS),
            "--bundle",
            str(bundle),
            "--candidates",
            str(candidate_path),
            "--reviewers",
            str(reviewer_manifest),
            "--out-jsonl",
            str(root / "verification.jsonl"),
            "--out-json",
            str(root / "verification.json"),
        ]
        verdict_rows = [] if verdicts is None else (verdicts if isinstance(verdicts, list) else [verdicts])
        if verdict_rows or include_completion:
            verdict_path = root / "verifier-verdicts.jsonl"
            output_rows = list(verdict_rows)
            if include_completion:
                verifier_ids = {row.get("verifier_id") for row in verdict_rows if row.get("verifier_id")}
                output_rows.append(
                    {
                        "type": "verifier_complete",
                        "verifier_id": next(iter(verifier_ids), "independent-verifier"),
                        "candidate_count": len(candidate_rows),
                        "verdict_count": len(verdict_rows),
                    }
                )
            verdict_path.write_text(
                "".join(json.dumps(row) + "\n" for row in output_rows),
                encoding="utf-8",
            )
            args.extend(["--verdicts", str(verdict_path)])
        proc = subprocess.run(args, text=True, capture_output=True)
        self.assertEqual(0, proc.returncode, proc.stderr)
        payload = json.loads((root / "verification.json").read_text(encoding="utf-8"))
        return payload

    @staticmethod
    def candidate():
        return {
            "id": "C1",
            "reviewer": "correctness",
            "title": "Concrete bug",
            "severity": "Important",
            "category": "correctness",
            "file": "sample.py",
            "line": 1,
            "introduced_by_diff": True,
            "failure_scenario": "The changed path returns the wrong value.",
            "evidence": ["sample.py:1"],
            "verification_plan": "Execute the failing branch.",
            "confidence": "high",
            "status": "confirmed",
        }

    def test_candidate_cannot_self_confirm(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(Path(tmp), self.candidate(), include_completion=False)
            finding = payload["findings"][0]
            self.assertEqual("needs_manual_review", finding["status"])
            self.assertFalse(payload["execution"]["execution_complete"])

    def test_independent_verifier_can_confirm(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(
                Path(tmp),
                self.candidate(),
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "Reproduced from the changed line.",
                },
            )
            finding = payload["findings"][0]
            self.assertEqual("confirmed", finding["status"])
            self.assertTrue(
                payload["execution"]["execution_complete"],
                payload["execution"]["errors"],
            )

    def test_same_reviewer_verdict_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(
                Path(tmp),
                self.candidate(),
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "correctness",
                    "independent": True,
                    "summary": "Self-verification is not independent.",
                },
            )
            finding = payload["findings"][0]
            self.assertEqual("needs_manual_review", finding["status"])
            self.assertFalse(payload["execution"]["execution_complete"])

    def test_verifier_cannot_confirm_a_candidate_missing_proof_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate = self.candidate()
            del candidate["verification_plan"]
            payload = self.run_verifier(
                Path(tmp),
                candidate,
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "The verdict cannot repair a malformed candidate.",
                },
            )
            finding = payload["findings"][0]
            self.assertEqual("needs_manual_review", finding["status"])
            self.assertFalse(payload["execution"]["execution_complete"])

    def test_verifier_cannot_claim_independence_without_origin_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate = self.candidate()
            del candidate["reviewer"]
            payload = self.run_verifier(
                Path(tmp),
                candidate,
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "No originating reviewer id exists to compare.",
                },
            )
            finding = payload["findings"][0]
            self.assertEqual("needs_manual_review", finding["status"])
            self.assertFalse(payload["execution"]["execution_complete"])

    def test_same_candidate_id_from_different_reviewers_maps_to_distinct_verdicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            correctness = self.candidate()
            security = self.candidate()
            security.update(
                {
                    "reviewer": "security",
                    "title": "Different security bug",
                    "category": "security",
                    "failure_scenario": "The changed path exposes private data.",
                }
            )
            payload = self.run_verifier(
                Path(tmp),
                [correctness, security],
                [
                    {
                        "candidate_id": "C1",
                        "reviewer": "correctness",
                        "status": "confirmed",
                        "verifier_id": "independent-verifier",
                        "independent": True,
                        "summary": "Confirmed the correctness failure only.",
                    },
                    {
                        "candidate_id": "C1",
                        "reviewer": "security",
                        "status": "false_positive",
                        "verifier_id": "independent-verifier",
                        "independent": True,
                        "summary": "Rejected the unrelated security claim.",
                    },
                ],
            )
            self.assertTrue(payload["execution"]["execution_complete"])
            statuses = {row["reviewer"]: row["status"] for row in payload["findings"]}
            self.assertEqual(
                {"correctness": "confirmed", "security": "false_positive"},
                statuses,
            )

    def test_duplicate_candidate_id_within_one_reviewer_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = self.candidate()
            second = self.candidate()
            second["title"] = "Another correctness bug"
            payload = self.run_verifier(
                Path(tmp),
                [first, second],
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "Only one of the duplicate candidates was checked.",
                },
            )
            self.assertFalse(payload["execution"]["execution_complete"])
            self.assertEqual(
                {"needs_manual_review"},
                {row["status"] for row in payload["findings"]},
            )

    def test_verifier_completion_receipt_is_required_even_with_a_valid_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(
                Path(tmp),
                self.candidate(),
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "Reproduced from the changed line.",
                },
                include_completion=False,
            )
            self.assertFalse(payload["execution"]["execution_complete"])

    def test_zero_candidate_verifier_completion_can_finish_the_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(Path(tmp), [], [])
            self.assertEqual([], payload["findings"])
            self.assertTrue(payload["execution"]["execution_complete"])

    def test_completed_reviewer_manifest_without_receipts_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(
                Path(tmp),
                self.candidate(),
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "Reproduced from the changed line.",
                },
                include_reviewer_receipts=False,
            )
            self.assertFalse(payload["execution"]["execution_complete"])
            self.assertIn(
                "reviewer completion receipt is missing or invalid",
                payload["execution"]["errors"],
            )

    def test_candidate_input_ignores_the_terminal_reviewer_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_verifier(
                Path(tmp),
                self.candidate(),
                {
                    "candidate_id": "C1",
                    "reviewer": "correctness",
                    "status": "confirmed",
                    "verifier_id": "independent-verifier",
                    "independent": True,
                    "summary": "Reproduced from the changed line.",
                },
                include_candidate_receipt_in_jsonl=True,
            )
            self.assertTrue(
                payload["execution"]["execution_complete"],
                payload["execution"]["errors"],
            )
            self.assertEqual(1, len(payload["findings"]))

    def test_static_confirm_escape_hatch_is_removed(self):
        proc = subprocess.run(
            [sys.executable, str(VERIFY_FINDINGS), "--help"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertNotIn("--static-confirm", proc.stdout)


if __name__ == "__main__":
    unittest.main()
