from __future__ import annotations

from typing import Any

from bnbagent.erc8183 import DeliverableManifest

from riskguard_adapter.policy import hash_json, stable_json

JsonObject = dict[str, Any]


def build_deliverable_manifest(
    receipt: JsonObject,
    *,
    job_id: int,
    chain_id: int,
    registry_address: str,
) -> DeliverableManifest:
    receipt_hash = hash_json(receipt)
    decision = str(receipt["decision"])

    return DeliverableManifest(
        version=1,
        job_id=job_id,
        chain_id=chain_id,
        contracts={
            "policy_receipt_registry": registry_address,
        },
        response={
            "content": stable_json(receipt),
            "content_type": "application/vnd.riskguard.receipt+json",
        },
        metadata={
            "riskguard_integration_mode": "manifest-only",
            "riskguard_receipt_hash": receipt_hash,
            "riskguard_decision": decision,
            "riskguard_policy_hash": str(receipt["policy_hash"]),
            "riskguard_proposal_hash": str(receipt["proposal_hash"]),
            "riskguard_simulation_hash": str(receipt["simulation_hash"]),
            "riskguard_evidence_hash": str(receipt["evidence_hash"]),
        },
    )


def manifest_hash_hex(manifest: DeliverableManifest) -> str:
    return "0x" + manifest.manifest_hash().hex()


def manifest_payload(
    receipt: JsonObject,
    *,
    job_id: int,
    chain_id: int,
    registry_address: str,
) -> JsonObject:
    manifest = build_deliverable_manifest(
        receipt,
        job_id=job_id,
        chain_id=chain_id,
        registry_address=registry_address,
    )
    return {
        "manifest_hash": manifest_hash_hex(manifest),
        "manifest": manifest.to_dict(),
    }
