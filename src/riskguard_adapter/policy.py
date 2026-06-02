from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


def load_json(path: Path | str) -> JsonObject:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def evaluate_plan(policy: JsonObject, plan: JsonObject) -> JsonObject:
    decision, reason = _decision(policy, plan)
    evidence = {
        "checks": {
            "action": plan.get("action"),
            "chain_id": plan.get("chain_id"),
            "slippage_bps": plan.get("slippage_bps"),
            "target_contract": plan.get("target_contract"),
            "token": plan.get("token"),
            "value_wei": str(plan.get("value_wei", "0")),
        },
        "decision": decision,
        "reason": reason,
    }
    simulation = {
        "mode": "policy-only",
        "status": "not-run",
        "summary": "No external DeFi simulation was run in this spike.",
    }

    receipt = {
        "agent_id": str(plan.get("agent_id", "unknown-agent")),
        "decision": decision,
        "evidence_hash": hash_json(evidence),
        "policy_hash": hash_json(policy),
        "policy_id": str(policy.get("policy_id", "unknown-policy")),
        "proposal_hash": hash_json(plan),
        "reason": reason,
        "simulation_hash": hash_json(simulation),
    }
    return receipt


def hash_json(value: JsonObject) -> str:
    encoded = stable_json(value).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def stable_json(value: JsonObject) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _decision(policy: JsonObject, plan: JsonObject) -> tuple[str, str]:
    chain_id = _required_int(plan, "chain_id")
    allowed_chain_ids = {int(item) for item in policy.get("allowed_chain_ids", [])}
    if allowed_chain_ids and chain_id not in allowed_chain_ids:
        return "block", f"chain id {chain_id} is not allowed"

    value_wei = _required_int(plan, "value_wei")
    max_value_wei = _required_int(policy, "max_value_wei")
    if value_wei > max_value_wei:
        return "block", f"value {value_wei} wei exceeds max {max_value_wei} wei"

    action = str(plan.get("action", ""))
    allowed_actions = {str(item) for item in policy.get("allowed_actions", [])}
    if allowed_actions and action not in allowed_actions:
        return "block", f"action {action!r} is not allowed"

    target_contract = plan.get("target_contract")
    allowed_contracts = {
        str(item).lower() for item in policy.get("allowed_contracts", [])
    }
    if allowed_contracts and str(target_contract).lower() not in allowed_contracts:
        return "block", f"target contract {target_contract!r} is not allowed"

    token = plan.get("token")
    allowed_tokens = {str(item).lower() for item in policy.get("allowed_tokens", [])}
    if allowed_tokens and str(token).lower() not in allowed_tokens:
        return "block", f"token {token!r} is not allowed"

    slippage_bps = _required_int(plan, "slippage_bps")
    max_slippage_bps = _required_int(policy, "max_slippage_bps")
    if slippage_bps > max_slippage_bps:
        return (
            "block",
            f"slippage {slippage_bps} bps exceeds max {max_slippage_bps} bps",
        )

    return "allow", "plan satisfies policy"


def _required_int(value: JsonObject, key: str) -> int:
    if key not in value:
        raise ValueError(f"missing required field: {key}")
    return int(value[key])
