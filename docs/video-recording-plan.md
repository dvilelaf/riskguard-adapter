# Video recording plan

Target length: 90-150 seconds.

Tone: direct terminal walkthrough. No cinematic intro, no broad security claims.

## Recording setup

Terminal tabs:

1. repo root;
2. BscScan contract page;
3. BscScan allow tx;
4. BscScan block tx.

Files to open during recording:

- `examples/policies/default-policy.json`;
- `examples/plans/safe-action.json`;
- `examples/plans/unsafe-action.json`;
- `examples/evidence/safe-receipt.json`;
- `examples/evidence/unsafe-receipt.json`;
- `docs/testnet-results.md`.

Commands to run:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/safe-action.json

uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/unsafe-action.json

uv run riskguard manifest \
  --receipt examples/evidence/safe-receipt.json \
  --job-id 42 \
  --chain-id 97 \
  --registry-address 0x10932358609f911B5cA1a131298C91a327ACAdC1

POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

Avoid running `just full-ci` live unless the recording needs a longer proof
segment. It is better to show the command and mention it passes than to spend
video time on logs.

## Script

### 0:00-0:15: Problem

> AI agents can propose DeFi actions quickly, but users need a programmable
> check before those actions move toward signing or settlement.

Show the architecture block from `README.md`.

### 0:15-0:30: Product

> RiskGuard Adapter checks a proposed action against a declared policy and
> emits a deterministic Policy Verdict Receipt.

Show `examples/policies/default-policy.json`.

### 0:30-0:55: Policy-compliant action

Run the policy-compliant validation command.

Say:

> This action stays within policy. RiskGuard returns `allow` and stable hashes
> for the proposal, policy, simulation and evidence.

Show `examples/evidence/safe-receipt.json`.

### 0:55-1:20: Policy-violating action

Run the policy-violating validation command.

Say:

> This action exceeds the slippage policy. RiskGuard returns `block` with a
> concrete reason.

Show `examples/evidence/unsafe-receipt.json`.

### 1:20-1:45: On-chain proof

Show `docs/testnet-results.md` and BscScan links.

Run:

```bash
POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

Say:

> The BSC testnet registry has two receipt transactions: one allow and one
> block.

### 1:45-2:10: ERC-8183 manifest path

Run the manifest command.

Say:

> This is manifest-only. It does not submit a real ERC-8183 job. It shows how a
> RiskGuard receipt hash can be carried in `DeliverableManifest.metadata`.

### 2:10-2:25: Close

> RiskGuard is open source, tested, deployed on BSC testnet and scoped as a
> small policy-verdict adapter for BNB Chain agent workflows.

## Claims to avoid

- prevents hacks;
- guarantees safety;
- audited;
- production-ready;
- mainnet;
- real trading;
- real ERC-8183 settlement;
- opBNB deployed.
