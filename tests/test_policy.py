from __future__ import annotations

import json
from pathlib import Path

from riskguard_adapter.policy import evaluate_plan, load_json

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "examples" / "policies" / "default-policy.json"
SAFE_PLAN_PATH = ROOT / "examples" / "plans" / "safe-action.json"
UNSAFE_PLAN_PATH = ROOT / "examples" / "plans" / "unsafe-action.json"


def test_safe_plan_produces_allow_receipt() -> None:
    policy = load_json(POLICY_PATH)
    plan = load_json(SAFE_PLAN_PATH)

    receipt = evaluate_plan(policy, plan)

    assert receipt["decision"] == "allow"
    assert receipt["reason"] == "plan satisfies policy"
    assert receipt["agent_id"] == "strategy-agent-demo"
    assert receipt["proposal_hash"].startswith("sha256:")
    assert receipt["policy_hash"].startswith("sha256:")
    assert receipt["simulation_hash"].startswith("sha256:")
    assert receipt["evidence_hash"].startswith("sha256:")


def test_unsafe_plan_blocks_slippage() -> None:
    policy = load_json(POLICY_PATH)
    plan = load_json(UNSAFE_PLAN_PATH)

    receipt = evaluate_plan(policy, plan)

    assert receipt["decision"] == "block"
    assert receipt["reason"] == "slippage 500 bps exceeds max 100 bps"


def test_plan_blocks_wrong_chain() -> None:
    policy = load_json(POLICY_PATH)
    plan = load_json(SAFE_PLAN_PATH)
    plan["chain_id"] = 56

    receipt = evaluate_plan(policy, plan)

    assert receipt["decision"] == "block"
    assert receipt["reason"] == "chain id 56 is not allowed"


def test_receipt_hashes_are_deterministic() -> None:
    policy = load_json(POLICY_PATH)
    plan = load_json(SAFE_PLAN_PATH)

    first = evaluate_plan(policy, plan)
    second = evaluate_plan(json.loads(json.dumps(policy)), json.loads(json.dumps(plan)))

    assert first == second
