from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from riskguard_adapter.policy import build_receipt_artifacts, evaluate_plan, load_json

JsonObject = dict[str, Any]


class StrategyAgent:
    def __init__(self, plan: JsonObject) -> None:
        self._plan = copy.deepcopy(plan)

    def propose(self) -> JsonObject:
        return copy.deepcopy(self._plan)


class RiskGuardAgent:
    def __init__(self, policy: JsonObject) -> None:
        self._policy = copy.deepcopy(policy)

    def evaluate(self, plan: JsonObject) -> JsonObject:
        return evaluate_plan(self._policy, plan)


def run_demo(
    policy_path: Path | str,
    safe_plan_path: Path | str,
    unsafe_plan_path: Path | str,
) -> JsonObject:
    policy = load_json(policy_path)
    guard_agent = RiskGuardAgent(policy)

    safe_plan = StrategyAgent(load_json(safe_plan_path)).propose()
    unsafe_plan = StrategyAgent(load_json(unsafe_plan_path)).propose()

    return {
        "runs": [
            {
                "label": "safe",
                "plan": safe_plan,
                "artifacts": build_receipt_artifacts(policy, safe_plan),
                "receipt": guard_agent.evaluate(safe_plan),
            },
            {
                "label": "unsafe",
                "plan": unsafe_plan,
                "artifacts": build_receipt_artifacts(policy, unsafe_plan),
                "receipt": guard_agent.evaluate(unsafe_plan),
            },
        ]
    }


def write_demo_evidence(result: JsonObject, directory: Path | str) -> None:
    evidence_dir = Path(directory)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    for run in result["runs"]:
        artifacts = run["artifacts"]
        files = {
            "evidence": artifacts["evidence"],
            "receipt": run["receipt"],
            "simulation": artifacts["simulation"],
        }
        for suffix, payload in files.items():
            path = evidence_dir / f"{run['label']}-{suffix}.json"
            path.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
