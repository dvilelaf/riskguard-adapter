from __future__ import annotations

from pathlib import Path

from riskguard_adapter.agents import (
    RiskGuardAgent,
    StrategyAgent,
    run_demo,
    write_demo_evidence,
)
from riskguard_adapter.policy import load_json

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "examples" / "policies" / "default-policy.json"
SAFE_PLAN_PATH = ROOT / "examples" / "plans" / "safe-action.json"
UNSAFE_PLAN_PATH = ROOT / "examples" / "plans" / "unsafe-action.json"


def test_strategy_agent_proposes_configured_plan() -> None:
    plan = load_json(SAFE_PLAN_PATH)

    proposed = StrategyAgent(plan).propose()

    assert proposed == plan
    assert proposed is not plan


def test_risk_guard_agent_returns_policy_verdict() -> None:
    policy = load_json(POLICY_PATH)
    plan = load_json(UNSAFE_PLAN_PATH)

    receipt = RiskGuardAgent(policy).evaluate(plan)

    assert receipt["decision"] == "block"
    assert receipt["reason"] == "slippage 500 bps exceeds max 100 bps"


def test_run_demo_returns_safe_and_unsafe_receipts() -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)

    assert [run["label"] for run in result["runs"]] == ["safe", "unsafe"]
    assert result["runs"][0]["receipt"]["decision"] == "allow"
    assert result["runs"][1]["receipt"]["decision"] == "block"


def test_write_demo_evidence_creates_receipt_files(tmp_path) -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)

    write_demo_evidence(result, tmp_path)

    assert (tmp_path / "safe-receipt.json").exists()
    assert (tmp_path / "unsafe-receipt.json").exists()
    assert load_json(tmp_path / "safe-receipt.json")["decision"] == "allow"
    assert load_json(tmp_path / "unsafe-receipt.json")["decision"] == "block"
