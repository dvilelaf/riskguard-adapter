from __future__ import annotations

import copy
from pathlib import Path

import pytest

from riskguard_adapter.policy import load_json
from riskguard_adapter.signatures import (
    sign_receipt,
    verify_receipt_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
SAFE_RECEIPT_PATH = ROOT / "examples" / "evidence" / "safe-receipt.json"
SAFE_EVIDENCE_PATH = ROOT / "examples" / "evidence" / "safe-evidence.json"
SAFE_SIMULATION_PATH = ROOT / "examples" / "evidence" / "safe-simulation.json"

SIGNER_PRIVATE_KEY = (
    "0x59c6995e998f97a5a0044966f094538eac1d6085a257075d4c8c5fcadf1bd0eb"
)
OTHER_PRIVATE_KEY = (
    "0x5de4111a56c78f382c7f5471bdaa5efb9d14f0b8d3c4f1f13f7116b8a368a365"
)
SIGNER_ADDRESS = "0xDC4814F2BC829880073D2B64355c518Fc7648Cda"


def test_sign_receipt_adds_recoverable_evm_signature() -> None:
    receipt = load_json(SAFE_RECEIPT_PATH)

    signed = sign_receipt(receipt, SIGNER_PRIVATE_KEY)

    assert signed["signer"] == SIGNER_ADDRESS
    assert signed["signature"].startswith("0x")
    assert len(signed["signature"]) == 132
    assert signed["signed_payload_hash"].startswith("0x")


def test_verify_receipt_bundle_accepts_matching_preimages_and_signature() -> None:
    receipt = sign_receipt(load_json(SAFE_RECEIPT_PATH), SIGNER_PRIVATE_KEY)
    evidence = load_json(SAFE_EVIDENCE_PATH)
    simulation = load_json(SAFE_SIMULATION_PATH)

    result = verify_receipt_bundle(receipt, evidence, simulation)

    assert result["valid"] is True
    assert result["signer"] == SIGNER_ADDRESS
    assert result["checks"]["evidence_hash"] == "ok"
    assert result["checks"]["simulation_hash"] == "ok"
    assert result["checks"]["signature"] == "ok"


def test_verify_receipt_bundle_rejects_unexpected_signer() -> None:
    receipt = sign_receipt(load_json(SAFE_RECEIPT_PATH), OTHER_PRIVATE_KEY)
    evidence = load_json(SAFE_EVIDENCE_PATH)
    simulation = load_json(SAFE_SIMULATION_PATH)

    result = verify_receipt_bundle(
        receipt,
        evidence,
        simulation,
        expected_signer=SIGNER_ADDRESS,
    )

    assert result["valid"] is False
    assert result["checks"]["expected_signer"] == "mismatch"


def test_verify_receipt_bundle_rejects_tampered_evidence() -> None:
    receipt = sign_receipt(load_json(SAFE_RECEIPT_PATH), SIGNER_PRIVATE_KEY)
    evidence = load_json(SAFE_EVIDENCE_PATH)
    simulation = load_json(SAFE_SIMULATION_PATH)
    tampered = copy.deepcopy(evidence)
    tampered["decision"] = "block"

    result = verify_receipt_bundle(receipt, tampered, simulation)

    assert result["valid"] is False
    assert result["checks"]["evidence_hash"] == "mismatch"


def test_verify_receipt_bundle_rejects_tampered_signed_receipt() -> None:
    receipt = sign_receipt(load_json(SAFE_RECEIPT_PATH), SIGNER_PRIVATE_KEY)
    evidence = load_json(SAFE_EVIDENCE_PATH)
    simulation = load_json(SAFE_SIMULATION_PATH)
    receipt["decision"] = "block"

    result = verify_receipt_bundle(receipt, evidence, simulation)

    assert result["valid"] is False
    assert result["checks"]["signature"] == "mismatch"


def test_sign_receipt_rejects_already_signed_receipt() -> None:
    receipt = sign_receipt(load_json(SAFE_RECEIPT_PATH), SIGNER_PRIVATE_KEY)

    with pytest.raises(ValueError, match="already signed"):
        sign_receipt(receipt, SIGNER_PRIVATE_KEY)
