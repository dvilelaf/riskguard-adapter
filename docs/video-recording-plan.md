# Video recording plan

Target length: 90-150 seconds.

Tone: direct terminal walkthrough. No cinematic intro, no broad security claims.

## Recording setup

Terminal tabs:

1. repo root;
2. GitHub Pages landing page;
3. receipt hash checker page;
4. BscScan contract page;
5. BscScan allow tx;
6. BscScan block tx.

Files to open during recording:

- `examples/policies/default-policy.json`;
- `examples/plans/safe-action.json`;
- `examples/plans/unsafe-action.json`;
- `examples/evidence/safe-receipt.json`;
- `examples/evidence/safe-signed-receipt.json`;
- `examples/evidence/unsafe-receipt.json`;
- `examples/evidence/unsafe-signed-receipt.json`;
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

just verify-demo

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

### 1:20-1:45: Receipt bundle verification

Open the public receipt hash checker, load the allow sample and show all hash
checks green.

Run:

```bash
just verify-demo
```

Say:

> The browser checker recomputes the receipt hashes and signed payload hash.
> The CLI goes one step further: it recovers the EVM signature and checks the
> expected demo signer.

### 1:45-2:10: On-chain anchoring

Show `docs/testnet-results.md` and BscScan links.

Run:

```bash
POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

Say:

> The BSC testnet registry has two receipt transactions: one allow and one
> block. The chain stores receipt component hashes; the local bundle carries
> the preimages and signed demo receipt fixture.

### 2:10-2:30: ERC-8183 manifest path

Run the manifest command.

Say:

> This is manifest-only. It does not submit a real ERC-8183 job. It shows how a
> RiskGuard receipt hash can be carried in `DeliverableManifest.metadata`.

### 2:30-2:45: Close

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
