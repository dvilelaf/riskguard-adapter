# BNB Hack form package

Use this document when filling the BNB Hack submission form.

## Project name

RiskGuard Adapter

## Team

Solo builder using AI assistance.

## Track

Main track / AI-agent infrastructure angle.

## Repository

https://github.com/dvilelaf/riskguard-adapter

## Release

https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0

## Deck

https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf

## Demo video

Fallback release asset:

https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4

Recommended upgrade before final submit: record a narrated version using the
same source material and replace this URL in the form.

Local source material:

- `docs/video-recording-plan.md`
- `docs/demo-transcript.md`

## Tweet

External pending after posting.

Draft:

```text
RiskGuard Adapter for #BNBHack:

DeFi policy verdict receipts for BNB Chain agents.

- allow/block policy checks
- manifest-only ERC-8183 evidence payload
- BSC testnet deployed
- 2 receipt txs
- open source + tested

GitHub: https://github.com/dvilelaf/riskguard-adapter
Demo: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4

@BNBChain #BNBHack
```

## Short description

RiskGuard Adapter checks autonomous DeFi action proposals against declared risk
policies before execution and emits deterministic allow/block Policy Verdict
Receipts. The prototype includes a local agent demo, a manifest-only
BNBAgent/ERC-8183 evidence payload, a BSC testnet receipt registry, and two
successful BSC testnet receipt transactions.

## Long description

AI agents can propose on-chain financial actions faster than users can review
them. RiskGuard Adapter adds a small, composable policy-verdict layer for BNB
Chain agent workflows.

A strategy agent proposes a DeFi action. RiskGuard evaluates the action against
a declared policy: chain id, value, action, target contract, token and slippage.
It then emits a deterministic Policy Verdict Receipt with an `allow` or `block`
decision, a concrete reason, and stable hashes for the proposal, policy,
simulation and evidence.

The current prototype is intentionally narrow. It does not custody funds,
execute trades, claim production safety or replace BNBAgent/ERC-8004/ERC-8183.
It demonstrates how a RiskGuard receipt can be generated locally, carried in
ERC-8183 `DeliverableManifest.metadata`, and anchored through a minimal BSC
testnet receipt registry.

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
- Receipt count: `2`

Explorer links:

- Contract:
  https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1
- Deploy tx:
  https://testnet.bscscan.com/tx/0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
- Allow tx:
  https://testnet.bscscan.com/tx/0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
- Block tx:
  https://testnet.bscscan.com/tx/0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd

## Implemented features

- `riskguard validate` validates a single proposed action against a policy.
- `riskguard demo` runs policy-compliant and policy-violating demo flows.
- `riskguard foundry-env` exports contract-ready receipt hashes.
- `riskguard manifest` builds a manifest-only ERC-8183 evidence payload.
- `PolicyReceiptRegistry` records receipt hashes on BSC testnet.
- Evidence bundle includes allow and block receipts.
- CI verifies Python, Solidity and local EVM e2e.

## Commands

```bash
just install
just demo
just full-ci

uv run riskguard manifest \
  --receipt examples/evidence/safe-receipt.json \
  --job-id 42 \
  --chain-id 97 \
  --registry-address 0x10932358609f911B5cA1a131298C91a327ACAdC1

POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

## What is not claimed

- No production security claim.
- No audited status.
- No mainnet readiness.
- No custody.
- No real trading.
- No real ERC-8183 job submission or settlement.
- No opBNB deployment yet.

## Post-submission follow-up

- Close issue after recording/uploading video:
  https://github.com/dvilelaf/riskguard-adapter/issues/3
- Close issue after posting tweet:
  https://github.com/dvilelaf/riskguard-adapter/issues/2
- Close issue after submitting BNB Hack form:
  https://github.com/dvilelaf/riskguard-adapter/issues/4
