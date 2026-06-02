from __future__ import annotations

import argparse
import json
from pathlib import Path

from riskguard_adapter.agents import run_demo, write_demo_evidence
from riskguard_adapter.erc8183 import manifest_payload
from riskguard_adapter.foundry import demo_to_foundry_env
from riskguard_adapter.policy import evaluate_plan, load_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = PROJECT_ROOT / "examples" / "policies" / "default-policy.json"
DEFAULT_SAFE_PLAN = PROJECT_ROOT / "examples" / "plans" / "safe-action.json"
DEFAULT_UNSAFE_PLAN = PROJECT_ROOT / "examples" / "plans" / "unsafe-action.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="riskguard",
        description="RiskGuard Adapter demo CLI.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit.",
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a proposed DeFAI action plan against a policy.",
    )
    validate_parser.add_argument(
        "--policy",
        required=True,
        type=Path,
        help="Path to a JSON policy file.",
    )
    validate_parser.add_argument(
        "--plan",
        required=True,
        type=Path,
        help="Path to a JSON action plan file.",
    )

    demo_parser = subparsers.add_parser(
        "demo",
        help="Run the safe and unsafe demo flows.",
    )
    demo_parser.add_argument(
        "--policy",
        default=DEFAULT_POLICY,
        type=Path,
        help="Path to a JSON policy file.",
    )
    demo_parser.add_argument(
        "--safe-plan",
        default=DEFAULT_SAFE_PLAN,
        type=Path,
        help="Path to a safe JSON action plan file.",
    )
    demo_parser.add_argument(
        "--unsafe-plan",
        default=DEFAULT_UNSAFE_PLAN,
        type=Path,
        help="Path to an unsafe JSON action plan file.",
    )
    demo_parser.add_argument(
        "--evidence-dir",
        type=Path,
        help="Optional directory where receipt JSON files will be written.",
    )

    foundry_parser = subparsers.add_parser(
        "foundry-env",
        help="Print Foundry/cast environment variables for demo receipts.",
    )
    foundry_parser.add_argument(
        "--policy",
        default=DEFAULT_POLICY,
        type=Path,
        help="Path to a JSON policy file.",
    )
    foundry_parser.add_argument(
        "--safe-plan",
        default=DEFAULT_SAFE_PLAN,
        type=Path,
        help="Path to a safe JSON action plan file.",
    )
    foundry_parser.add_argument(
        "--unsafe-plan",
        default=DEFAULT_UNSAFE_PLAN,
        type=Path,
        help="Path to an unsafe JSON action plan file.",
    )
    manifest_parser = subparsers.add_parser(
        "manifest",
        help="Build a BNBAgent/ERC-8183 manifest-only payload for a receipt.",
    )
    manifest_parser.add_argument(
        "--receipt",
        required=True,
        type=Path,
        help="Path to a RiskGuard receipt JSON file.",
    )
    manifest_parser.add_argument(
        "--job-id",
        required=True,
        type=int,
        help="Demo ERC-8183 job id to include in the manifest.",
    )
    manifest_parser.add_argument(
        "--chain-id",
        required=True,
        type=int,
        help="EVM chain id to include in the manifest.",
    )
    manifest_parser.add_argument(
        "--registry-address",
        required=True,
        help="PolicyReceiptRegistry address used as BSC testnet proof.",
    )
    args = parser.parse_args()

    if args.version:
        from riskguard_adapter import __version__

        print(__version__)
        return

    if args.command == "validate":
        receipt = evaluate_plan(load_json(args.policy), load_json(args.plan))
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return

    if args.command == "demo":
        result = run_demo(args.policy, args.safe_plan, args.unsafe_plan)
        if args.evidence_dir:
            write_demo_evidence(result, args.evidence_dir)
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    if args.command == "foundry-env":
        result = run_demo(args.policy, args.safe_plan, args.unsafe_plan)
        print(demo_to_foundry_env(result, render=True), end="")
        return

    if args.command == "manifest":
        payload = manifest_payload(
            load_json(args.receipt),
            job_id=args.job_id,
            chain_id=args.chain_id,
            registry_address=args.registry_address,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
