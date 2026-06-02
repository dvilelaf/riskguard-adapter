from __future__ import annotations

from pathlib import Path

from riskguard_adapter.agents import run_demo
from riskguard_adapter.foundry import demo_to_foundry_env, hash_to_bytes32

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "examples" / "policies" / "default-policy.json"
SAFE_PLAN_PATH = ROOT / "examples" / "plans" / "safe-action.json"
UNSAFE_PLAN_PATH = ROOT / "examples" / "plans" / "unsafe-action.json"


def test_hash_to_bytes32_converts_sha256_prefix() -> None:
    value = "sha256:" + ("a" * 64)

    assert hash_to_bytes32(value) == "0x" + ("a" * 64)


def test_demo_to_foundry_env_uses_receipt_hashes() -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)

    env = demo_to_foundry_env(result)

    assert env["AGENT_ID"].startswith("0x")
    assert env["POLICY_HASH"] == hash_to_bytes32(
        result["runs"][0]["receipt"]["policy_hash"]
    )
    assert env["SAFE_PROPOSAL_HASH"] == hash_to_bytes32(
        result["runs"][0]["receipt"]["proposal_hash"]
    )
    assert env["SAFE_SIMULATION_HASH"] == hash_to_bytes32(
        result["runs"][0]["receipt"]["simulation_hash"]
    )
    assert env["SAFE_EVIDENCE_HASH"] == hash_to_bytes32(
        result["runs"][0]["receipt"]["evidence_hash"]
    )
    assert env["BLOCK_PROPOSAL_HASH"] == hash_to_bytes32(
        result["runs"][1]["receipt"]["proposal_hash"]
    )


def test_demo_to_foundry_env_renders_exports() -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)

    rendered = demo_to_foundry_env(result, render=True)

    assert 'export SAFE_DECISION="0"' in rendered
    assert 'export BLOCK_DECISION="1"' in rendered
