from __future__ import annotations

import hashlib
from typing import Any, overload

JsonObject = dict[str, Any]


def hash_to_bytes32(value: str) -> str:
    if value.startswith("sha256:"):
        hex_value = value.removeprefix("sha256:")
    elif value.startswith("0x"):
        hex_value = value.removeprefix("0x")
    else:
        raise ValueError(f"unsupported hash format: {value}")

    if len(hex_value) != 64:
        raise ValueError(f"expected 32-byte hash, got {len(hex_value) // 2} bytes")
    int(hex_value, 16)
    return f"0x{hex_value}"


@overload
def demo_to_foundry_env(result: JsonObject, render: bool = False) -> dict[str, str]: ...


@overload
def demo_to_foundry_env(result: JsonObject, render: bool = True) -> str: ...


def demo_to_foundry_env(
    result: JsonObject,
    render: bool = False,
) -> dict[str, str] | str:
    runs = {run["label"]: run["receipt"] for run in result["runs"]}
    safe = runs["safe"]
    block = runs["unsafe"]

    env = {
        "AGENT_ID": _agent_id_hash(str(safe["agent_id"])),
        "POLICY_HASH": hash_to_bytes32(str(safe["policy_hash"])),
        "SAFE_PROPOSAL_HASH": hash_to_bytes32(str(safe["proposal_hash"])),
        "SAFE_SIMULATION_HASH": hash_to_bytes32(str(safe["simulation_hash"])),
        "SAFE_EVIDENCE_HASH": hash_to_bytes32(str(safe["evidence_hash"])),
        "SAFE_DECISION": "0",
        "BLOCK_PROPOSAL_HASH": hash_to_bytes32(str(block["proposal_hash"])),
        "BLOCK_SIMULATION_HASH": hash_to_bytes32(str(block["simulation_hash"])),
        "BLOCK_EVIDENCE_HASH": hash_to_bytes32(str(block["evidence_hash"])),
        "BLOCK_DECISION": "1",
    }

    if not render:
        return env

    return "\n".join(f'export {key}="{value}"' for key, value in env.items()) + "\n"


def _agent_id_hash(agent_id: str) -> str:
    return "0x" + hashlib.sha256(agent_id.encode("utf-8")).hexdigest()
