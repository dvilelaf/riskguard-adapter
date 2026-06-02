# Demo transcript

Use this as the narrated script or caption source for the demo video.

## Intro

RiskGuard Adapter is a small policy/evidence adapter for BNB Chain agent
workflows.

The question it answers is narrow:

> Did this autonomous DeFi action comply with the declared policy before
> execution?

It does not custody funds, execute trades, claim production safety or submit a
real ERC-8183 job. The current evidence is local policy evaluation, signed demo
receipt fixtures, manifest-only ERC-8183 metadata and BSC testnet receipt
transactions.

## Show policy

Open:

```bash
sed -n '1,220p' examples/policies/default-policy.json
```

Narration:

> The policy is a JSON document. It limits the chain, value, action, target
> contract, token and slippage.

## Policy-compliant action

Run:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/safe-action.json
```

Expected key output:

```json
{
  "agent_id": "strategy-agent-demo",
  "decision": "allow",
  "policy_id": "default-bnb-testnet-demo",
  "reason": "plan satisfies policy"
}
```

Narration:

> This proposed action is policy-compliant. RiskGuard returns an allow verdict
> and stable hashes for the proposal, policy, simulation and evidence.

## Policy-violating action

Run:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/unsafe-action.json
```

Expected key output:

```json
{
  "agent_id": "strategy-agent-demo",
  "decision": "block",
  "policy_id": "default-bnb-testnet-demo",
  "reason": "slippage 500 bps exceeds max 100 bps"
}
```

Narration:

> This proposed action violates the policy because slippage is too high.
> RiskGuard returns a block verdict with a concrete reason.

## Evidence files

Run:

```bash
ls examples/evidence
sed -n '1,220p' examples/evidence/safe-receipt.json
sed -n '1,220p' examples/evidence/unsafe-receipt.json
```

Narration:

> The evidence bundle contains the checked-in allow and block receipts used in
> the submission package.

## Signed receipt verification

Open:

```bash
sed -n '1,220p' examples/evidence/safe-signed-receipt.json
```

Run:

```bash
just verify-demo
```

Expected key output:

```json
{
  "checks": {
    "evidence_hash": "ok",
    "expected_signer": "ok",
    "signature": "ok",
    "simulation_hash": "ok"
  },
  "valid": true
}
```

Narration:

> The browser checker recomputes the hash preimages. The CLI verifier also
> recovers the EVM signature and checks it against the expected demo signer.

## ERC-8183 manifest-only metadata

Run:

```bash
uv run riskguard manifest \
  --receipt examples/evidence/safe-receipt.json \
  --job-id 42 \
  --chain-id 97 \
  --registry-address 0x10932358609f911B5cA1a131298C91a327ACAdC1
```

Expected key output:

```json
{
  "manifest_hash": "0x...",
  "manifest": {
    "metadata": {
      "riskguard_integration_mode": "manifest-only",
      "riskguard_decision": "allow",
      "riskguard_receipt_hash": "sha256:..."
    }
  }
}
```

Narration:

> This is manifest-only. It does not submit or settle a real ERC-8183 job. It
> shows how the RiskGuard receipt hash can travel in
> `DeliverableManifest.metadata`.

## BSC testnet anchoring

Open:

```bash
sed -n '1,220p' docs/testnet-results.md
```

Run:

```bash
POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

Expected output:

```text
2
```

Narration:

> The BSC testnet registry has two receipt transactions: one allow and one
> block. The chain stores receipt component hashes; the local bundle carries
> the preimages and signed demo receipt fixture. The current on-chain receipt
> count is two.

## Close

Narration:

> RiskGuard Adapter is open source, tested, deployed on BSC testnet and scoped
> as a small policy-verdict adapter for BNB Chain agent workflows. The next
> steps are a real ERC-8183 job submission, opBNB deployment and policy
> templates for DeFAI and treasury workflows.
