# Submission package

Date: 2026-06-02

Purpose: keep the BNB Hack submission artifacts, proof links and demo commands
in one judge-facing checklist.

## Project

Name: RiskGuard Adapter

One-liner:

> DeFi policy verdict receipts for BNB Chain agents and ERC-8183-style jobs.

Short description:

> RiskGuard checks autonomous DeFi actions against a declared policy before
> execution and emits deterministic allow/block Policy Verdict Receipts designed
> to be attached to agent job evidence. Today, the proof is anchored on BSC
> testnet; opBNB is a roadmap target.

## Primary submission target

- Event: BNB Hack Online Edition
- Target: Main track
- Realistic prize target: 3,000 USDT
- Stretch prize target: 7,000 USDT
- Planning assumption: solo builder using AI, 6-10 focused hours remaining

## Repository proof

Local commands:

```bash
just install
just demo
just foundry-env
just full-ci
```

Single safe verdict:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/safe-action.json
```

Single blocked verdict:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/unsafe-action.json
```

Evidence bundle:

```bash
uv run riskguard demo --evidence-dir examples/evidence
```

Generated files:

- `examples/evidence/safe-receipt.json`
- `examples/evidence/unsafe-receipt.json`

Evidence drift check:

```bash
rm -rf /tmp/riskguard-review-evidence
uv run riskguard demo --evidence-dir /tmp/riskguard-review-evidence
diff -u examples/evidence/safe-receipt.json /tmp/riskguard-review-evidence/safe-receipt.json
diff -u examples/evidence/unsafe-receipt.json /tmp/riskguard-review-evidence/unsafe-receipt.json
```

Manifest-only ERC-8183 evidence payload:

```bash
uv run riskguard manifest \
  --receipt examples/evidence/safe-receipt.json \
  --job-id 42 \
  --chain-id 97 \
  --registry-address 0x10932358609f911B5cA1a131298C91a327ACAdC1
```

This command does not submit or settle a real ERC-8183 job. It builds a local
`DeliverableManifest` payload with the RiskGuard receipt hash in `metadata`.

## BSC testnet proof

- Chain: BSC testnet
- Chain id: 97
- Contract:
  `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Deploy tx:
  `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
- Allow receipt tx:
  `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block receipt tx:
  `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
- On-chain `receiptCount()`: `2`

Copy-paste verification:

```bash
POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

Explorer links:

- Contract:
  https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1
- Deploy tx:
  https://testnet.bscscan.com/tx/0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
- Allow tx:
  https://testnet.bscscan.com/tx/0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
- Block tx:
  https://testnet.bscscan.com/tx/0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd

## Video script

Target length: 90-150 seconds.

1. Problem: autonomous DeFi agents need risk-policy checks before execution.
2. Product: RiskGuard emits deterministic allow/block verdict receipts.
3. Demo: show `default-policy.json`, policy-compliant action and allow receipt.
4. Demo: show policy-violating action and block receipt.
5. Proof: show BSC testnet contract, allow tx, block tx and `receiptCount=2`.
6. Integration: explain BNBAgent/ERC-8183 evidence metadata path.
7. Close: open-source, tested, deployed on BSC testnet and ready for
   lightweight integration experiments.

Avoid saying:

- prevents hacks;
- guarantees safe transactions;
- audited;
- production-ready;
- replaces wallets or BNBAgent.

## Deck outline

Maximum: 7 slides.

1. Title: RiskGuard Adapter.
2. Problem: agents can act faster than users can review.
3. Solution: policy verdict adapter before execution.
4. Demo proof: CLI, receipts, tests, BSC testnet txs.
5. Architecture: agent/job -> RiskGuard -> manifest/proof -> BSC testnet.
6. Why BNB: DeFAI and autonomous wallets need composable guardrails.
7. Roadmap: manifest adapter, verifier, opBNB, policy templates.

## Submission checklist

- GitHub repo is public.
- README has BSC testnet proof near the top.
- `docs/testnet-results.md` is current.
- `examples/evidence/` contains policy-compliant and policy-violating receipts.
- Demo video URL is ready.
- Deck URL is ready.
- Tweet URL is ready.
- Final `just full-ci` passes.
- `git diff --check` passes.
- `git status --ignored --short .env.bsc-testnet-wallet` prints
  `!! .env.bsc-testnet-wallet`.
- `git ls-files --error-unmatch .env.bsc-testnet-wallet && exit 1 || true`
  confirms the wallet env file is not tracked.
- `rg -n --fixed-strings "$DEPLOYER_PRIVATE_KEY" README.md docs examples src scripts contracts .env.example`
  finds no private key after sourcing `.env.bsc-testnet-wallet` locally.

## Open before submit

- Record or upload demo video.
- Create deck.
- Publish repo and submit.

Draft assets:

- Deck draft: `docs/deck-draft.md`
- Video recording plan: `docs/video-recording-plan.md`
- Submission copy: `docs/submission-copy.md`
