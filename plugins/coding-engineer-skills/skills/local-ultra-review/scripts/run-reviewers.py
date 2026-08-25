#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import subprocess
import sys
import time
from pathlib import Path


REVIEWERS = {
    "correctness": "02-reviewer-correctness.md",
    "security": "03-reviewer-security.md",
    "integration": "04-reviewer-integration.md",
    "state-concurrency": "05-reviewer-state-concurrency.md",
    "tests": "06-reviewer-tests.md",
}

MODES = {
    "light": ["correctness", "security", "integration", "tests"],
    "deep": ["correctness", "security", "integration", "state-concurrency", "tests"],
    "max": ["correctness", "security", "integration", "state-concurrency", "tests"],
}


def read(path):
    return Path(path).read_text(encoding="utf-8")


def build_prompt(skill_dir, bundle, role):
    prompts = Path(skill_dir) / "prompts"
    contract = read(prompts / "00-review-contract.md")
    lens = read(prompts / REVIEWERS[role])
    bundle_json = json.dumps(bundle, indent=2, sort_keys=True)
    return f"""# Local Ultra Review Reviewer Packet

You are the `{role}` reviewer. Work independently. Do not assume another reviewer will catch your category.

## Shared Contract

{contract}

## Lens

{lens}

## Review Bundle

```json
{bundle_json}
```

Return JSONL candidate findings matching schemas/candidate-finding.schema.json.
After the final candidate, emit exactly one terminal completion record:

{{"type":"reviewer_complete","reviewer":"{role}","candidate_count":<number of candidate rows>}}

If no candidates meet the bar, return only the completion record. Do not emit prose or markdown fences.
"""


def parse_reviewer_output(text, role):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("reviewer emitted no completion record")

    rows = []
    completion = None
    for index, stripped in enumerate(lines):
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"reviewer emitted invalid JSONL on output line {index + 1}: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"reviewer output line {index + 1} is not a JSON object")
        if payload.get("type") == "reviewer_complete":
            if completion is not None:
                raise ValueError("reviewer emitted multiple completion records")
            if index != len(lines) - 1:
                raise ValueError("reviewer completion record must be the final output line")
            if payload.get("reviewer") != role:
                raise ValueError("reviewer completion record has the wrong reviewer identity")
            candidate_count = payload.get("candidate_count")
            if isinstance(candidate_count, bool) or not isinstance(candidate_count, int) or candidate_count < 0:
                raise ValueError("reviewer completion record has an invalid candidate_count")
            completion = payload
            continue

        payload["reviewer"] = role
        rows.append(payload)

    if completion is None:
        raise ValueError("reviewer emitted no completion record")
    if completion["candidate_count"] != len(rows):
        raise ValueError(
            "reviewer completion candidate_count does not match the parsed candidate rows"
        )
    return rows, completion


def run_cli(command_argv, prompt, cwd, timeout):
    if not command_argv:
        raise ValueError("CLI command cannot be empty")
    proc = subprocess.run(
        command_argv,
        input=prompt,
        cwd=cwd,
        shell=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return proc


def reviewer_job(role, prompt, args):
    start = time.time()
    result = {
        "reviewer": role,
        "backend": args.backend,
        "started_at": start,
        "prompt_path": str(Path(args.out) / f"{role}.prompt.md"),
    }
    prompt_path = Path(result["prompt_path"])
    prompt_path.write_text(prompt, encoding="utf-8")

    if args.backend == "cli":
        if not args.command:
            result.update({"status": "skipped", "reason": "--command is required for cli backend"})
            return result
        try:
            proc = run_cli(args.command, prompt, args.cwd, args.timeout)
            raw_path = Path(args.out) / f"{role}.raw.txt"
            raw_path.write_text(proc.stdout + ("\n[stderr]\n" + proc.stderr if proc.stderr else ""), encoding="utf-8", errors="replace")
            rows = []
            completion = None
            parse_error = ""
            if proc.returncode == 0:
                try:
                    rows, completion = parse_reviewer_output(proc.stdout, role)
                except ValueError as exc:
                    parse_error = str(exc)
            jsonl_path = Path(args.out) / f"{role}.jsonl"
            with jsonl_path.open("w", encoding="utf-8") as fh:
                for row in rows:
                    fh.write(json.dumps(row, sort_keys=True) + "\n")
            status = "completed" if proc.returncode == 0 and not parse_error else "failed"
            result.update(
                {
                    "status": status,
                    "exit_code": proc.returncode,
                    "raw_path": str(raw_path),
                    "jsonl_path": str(jsonl_path),
                    "candidates": len(rows),
                }
            )
            if completion is not None:
                result["completion_receipt"] = completion
            if parse_error:
                result["reason"] = parse_error
        except ValueError as exc:
            result.update({"status": "failed", "reason": str(exc), "exit_code": 2})
        except subprocess.TimeoutExpired:
            result.update({"status": "timeout", "exit_code": 124})
    elif args.backend == "packets":
        result.update(
            {
                "status": "packet_generated",
                "reason": (
                    "Prompt packet generated only. The host must dispatch it to an "
                    "independent reviewer context; this is not a completed review."
                ),
                "candidates": 0,
            }
        )
    else:
        result.update({"status": "failed", "reason": f"unsupported backend: {args.backend}"})

    result["finished_at"] = time.time()
    result["duration_seconds"] = round(result["finished_at"] - start, 3)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--mode", default="deep", choices=sorted(MODES))
    parser.add_argument("--backend", default="packets", choices=["packets", "cli"])
    parser.add_argument("--parallelism", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--out", required=True)
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--cwd", default=".")
    parser.add_argument(
        "--command",
        nargs=argparse.REMAINDER,
        default=[],
        help="Explicit CLI argv. This option must be last.",
    )
    args = parser.parse_args()

    if args.backend == "cli" and not args.command:
        parser.error("--command is required for the cli backend")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
    roles = MODES[args.mode]
    prompts = {role: build_prompt(args.skill_dir, bundle, role) for role in roles}

    results = []
    if args.backend == "cli" and args.parallelism > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.parallelism, len(roles))) as pool:
            futures = [pool.submit(reviewer_job, role, prompts[role], args) for role in roles]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
    else:
        for role in roles:
            results.append(reviewer_job(role, prompts[role], args))

    execution_complete = (
        args.backend == "cli"
        and len(results) == len(roles)
        and all(result["status"] == "completed" for result in results)
    )
    manifest = {
        "mode": args.mode,
        "backend": args.backend,
        "command": args.command,
        "execution_complete": execution_complete,
        "required_reviewer_count": len(roles),
        "reviewers": results,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if args.backend == "cli" and not execution_complete:
        sys.exit(1)


if __name__ == "__main__":
    main()
