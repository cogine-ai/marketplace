import json
from pathlib import Path


def load_execution(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    execution = payload.get("execution")
    if not isinstance(execution, dict):
        raise RuntimeError("execution artifact does not contain an execution object")
    return execution


def require_complete_execution(path):
    execution = load_execution(path)
    if execution.get("execution_complete") is not True:
        reasons = execution.get("errors") or []
        detail = f": {'; '.join(str(reason) for reason in reasons)}" if reasons else ""
        raise RuntimeError(f"review execution is incomplete{detail}")
    return execution
