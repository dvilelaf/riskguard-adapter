from __future__ import annotations

from typing import Any

from eth_account import Account
from eth_account.messages import encode_defunct

from riskguard_adapter.policy import hash_json

JsonObject = dict[str, Any]

SIGNATURE_FIELDS = {"signature", "signed_payload_hash", "signer"}


def sign_receipt(receipt: JsonObject, private_key: str) -> JsonObject:
    if SIGNATURE_FIELDS & receipt.keys():
        raise ValueError("receipt is already signed")

    payload_hash = receipt_payload_hash(receipt)
    message = encode_defunct(text=_signing_message(payload_hash))
    signed = Account.sign_message(message, private_key=private_key)

    return {
        **receipt,
        "signed_payload_hash": payload_hash,
        "signer": Account.from_key(private_key).address,
        "signature": "0x" + signed.signature.hex().removeprefix("0x"),
    }


def verify_receipt_bundle(
    receipt: JsonObject,
    evidence: JsonObject,
    simulation: JsonObject,
) -> JsonObject:
    checks = {
        "evidence_hash": _match_hash(str(receipt.get("evidence_hash")), evidence),
        "simulation_hash": _match_hash(str(receipt.get("simulation_hash")), simulation),
        "signature": _verify_signature(receipt),
    }
    return {
        "checks": checks,
        "signer": receipt.get("signer"),
        "valid": all(value == "ok" for value in checks.values()),
    }


def receipt_payload_hash(receipt: JsonObject) -> str:
    unsigned = {
        key: value for key, value in receipt.items() if key not in SIGNATURE_FIELDS
    }
    return "0x" + hash_json(unsigned).removeprefix("sha256:")


def _match_hash(expected_hash: str, preimage: JsonObject) -> str:
    return "ok" if expected_hash == hash_json(preimage) else "mismatch"


def _verify_signature(receipt: JsonObject) -> str:
    signature = receipt.get("signature")
    signer = receipt.get("signer")
    payload_hash = receipt.get("signed_payload_hash")
    if not isinstance(signature, str) or not isinstance(signer, str):
        return "missing"
    if (
        not isinstance(payload_hash, str)
        or payload_hash != receipt_payload_hash(receipt)
    ):
        return "mismatch"

    try:
        recovered = Account.recover_message(
            encode_defunct(text=_signing_message(payload_hash)),
            signature=signature,
        )
    except Exception:
        return "mismatch"

    return "ok" if recovered.lower() == signer.lower() else "mismatch"


def _signing_message(payload_hash: str) -> str:
    return (
        "RiskGuard Policy Verdict Receipt\n"
        f"payload_hash={payload_hash}\n"
        "This signature proves who produced this demo receipt."
    )
