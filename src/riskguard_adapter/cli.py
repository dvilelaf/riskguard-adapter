from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from riskguard_adapter.agents import run_demo, write_demo_evidence
from riskguard_adapter.erc8183 import manifest_payload
from riskguard_adapter.foundry import demo_to_foundry_env
from riskguard_adapter.policy import evaluate_plan, load_json
from riskguard_adapter.signatures import sign_receipt, verify_receipt_bundle

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
    sign_parser = subparsers.add_parser(
        "sign",
        help="Sign a Policy Verdict Receipt with an EVM key from the environment.",
    )
    sign_parser.add_argument(
        "--receipt",
        required=True,
        type=Path,
        help="Path to a RiskGuard receipt JSON file.",
    )
    sign_parser.add_argument(
        "--private-key-env",
        default="RISKGUARD_SIGNER_PRIVATE_KEY",
        help="Environment variable containing the EVM private key.",
    )
    sign_parser.add_argument(
        "--out",
        type=Path,
        help="Optional path where the signed receipt JSON will be written.",
    )
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify receipt preimages and EVM receipt signature.",
    )
    verify_parser.add_argument(
        "--receipt",
        required=True,
        type=Path,
        help="Path to a signed RiskGuard receipt JSON file.",
    )
    verify_parser.add_argument(
        "--evidence",
        required=True,
        type=Path,
        help="Path to the evidence preimage JSON file.",
    )
    verify_parser.add_argument(
        "--simulation",
        required=True,
        type=Path,
        help="Path to the simulation preimage JSON file.",
    )
    verify_parser.add_argument(
        "--expected-signer",
        help="Optional EVM address expected to have signed the receipt.",
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

    if args.command == "sign":
        private_key = os.environ.get(args.private_key_env)
        if not private_key:
            raise SystemExit(f"missing env var: {args.private_key_env}")
        signed = sign_receipt(load_json(args.receipt), private_key)
        rendered = json.dumps(signed, indent=2, sort_keys=True) + "\n"
        if args.out:
            args.out.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return

    if args.command == "verify":
        result = verify_receipt_bundle(
            load_json(args.receipt),
            load_json(args.evidence),
            load_json(args.simulation),
            expected_signer=args.expected_signer,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        if not result["valid"]:
            raise SystemExit(1)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
