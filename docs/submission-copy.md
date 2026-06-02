# Submission copy

Use this as the source text for the BNB Hack form, GitHub description, tweet
and video description.

## Project title

RiskGuard Adapter

## Short tagline

DeFi policy verdict receipts for BNB Chain agents and ERC-8183-style jobs.

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

## Implemented proof

- `riskguard validate` for single plan evaluation.
- `riskguard demo` for policy-compliant and policy-violating local agent flows.
- `riskguard foundry-env` for contract-ready receipt hash exports.
- `riskguard manifest` for manifest-only ERC-8183 evidence payloads.
- Solidity `PolicyReceiptRegistry`.
- BSC testnet deployment.
- One allow receipt transaction.
- One block receipt transaction.
- `receiptCount()` returns `2`.
- `just full-ci` passes locally.

## BSC testnet links

- Contract:
  https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1
- Deploy tx:
  https://testnet.bscscan.com/tx/0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
- Allow tx:
  https://testnet.bscscan.com/tx/0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
- Block tx:
  https://testnet.bscscan.com/tx/0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd

## Demo video description

RiskGuard Adapter is a small policy-verdict adapter for BNB Chain agent
workflows. The demo shows a policy-compliant DeFi action receiving an `allow`
receipt, a policy-violating action receiving a `block` receipt, two BSC testnet receipt
transactions, and a manifest-only ERC-8183 evidence payload carrying the
RiskGuard receipt hash.

## Tweet draft

RiskGuard Adapter for #BNBHack:

DeFi policy verdict receipts for BNB Chain agents.

- allow/block policy checks
- manifest-only ERC-8183 evidence payload
- BSC testnet deployed
- 2 receipt txs
- open source + tested

GitHub: https://github.com/dvilelaf/riskguard-adapter
Release: https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0
Deck: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf
Demo: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4

@BNBChain #BNBHack

## Submission form checklist

- GitHub URL: `https://github.com/dvilelaf/riskguard-adapter`
- Release URL: `https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0`
- Demo video URL:
  `https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4`
- Deck URL:
  `https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf`
- Tweet URL: external pending after posting
- Contract address:
  `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Track: Main track / AI-agent infrastructure angle
- Source verification status: pending, source available in repo
