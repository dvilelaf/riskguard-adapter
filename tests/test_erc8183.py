from __future__ import annotations

from pathlib import Path

from bnbagent.erc8183 import DeliverableManifest

from riskguard_adapter.agents import run_demo
from riskguard_adapter.erc8183 import (
    build_deliverable_manifest,
    manifest_hash_hex,
    manifest_payload,
)
from riskguard_adapter.policy import hash_json

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "examples" / "policies" / "default-policy.json"
SAFE_PLAN_PATH = ROOT / "examples" / "plans" / "safe-action.json"
UNSAFE_PLAN_PATH = ROOT / "examples" / "plans" / "unsafe-action.json"
REGISTRY_ADDRESS = "0x10932358609f911B5cA1a131298C91a327ACAdC1"


def test_build_deliverable_manifest_attaches_riskguard_receipt_metadata() -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)
    receipt = result["runs"][0]["receipt"]

    manifest = build_deliverable_manifest(
        receipt,
        job_id=42,
        chain_id=97,
        registry_address=REGISTRY_ADDRESS,
    )

    assert isinstance(manifest, DeliverableManifest)
    assert manifest.job_id == 42
    assert manifest.chain_id == 97
    assert manifest.contracts["policy_receipt_registry"] == REGISTRY_ADDRESS
    assert manifest.response["content_type"] == "application/vnd.riskguard.receipt+json"
    assert manifest.metadata["riskguard_integration_mode"] == "manifest-only"
    assert manifest.metadata["riskguard_receipt_hash"] == hash_json(receipt)
    assert manifest.metadata["riskguard_decision"] == "allow"
    assert manifest.metadata["riskguard_policy_hash"] == receipt["policy_hash"]
    assert manifest.verify(manifest.manifest_hash())


def test_manifest_payload_includes_hex_manifest_hash() -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)
    receipt = result["runs"][1]["receipt"]

    payload = manifest_payload(
        receipt,
        job_id=43,
        chain_id=97,
        registry_address=REGISTRY_ADDRESS,
    )

    assert payload["manifest_hash"].startswith("0x")
    assert len(payload["manifest_hash"]) == 66
    assert payload["manifest"]["metadata"]["riskguard_decision"] == "block"
    assert payload["manifest"]["metadata"]["riskguard_receipt_hash"] == hash_json(
        receipt
    )


def test_manifest_hash_hex_returns_bytes32_hex() -> None:
    result = run_demo(POLICY_PATH, SAFE_PLAN_PATH, UNSAFE_PLAN_PATH)
    receipt = result["runs"][0]["receipt"]
    manifest = build_deliverable_manifest(
        receipt,
        job_id=42,
        chain_id=97,
        registry_address=REGISTRY_ADDRESS,
    )

    value = manifest_hash_hex(manifest)

    assert value.startswith("0x")
    assert len(value) == 66
