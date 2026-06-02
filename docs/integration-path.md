# Integration path

Date: 2026-06-02

## Decision

Preferred path: BNBAgent / ERC-8183 evidence adapter.

Fallback path: minimal BNB testnet `PolicyReceiptRegistry`.

RiskGuard should not build a custom ERC-8183 policy, hook, escrow or wallet
guard for the MVP.

## Implemented lightweight path

RiskGuard produces a deterministic Policy Verdict Receipt locally, then
attaches its hash to a local BNBAgent / ERC-8183 `DeliverableManifest`.

Flow:

1. `StrategyAgent` proposes a DeFAI action.
2. `RiskGuardAgent` validates the plan against a declared policy.
3. RiskGuard emits a receipt with:
   - `agent_id`;
   - `proposal_hash`;
   - `policy_hash`;
   - `evidence_hash`;
   - `decision`;
   - `reason`.
4. The canonical receipt JSON is hashed.
5. A BNBAgent ERC-8183 deliverable manifest includes the receipt hash in
   `DeliverableManifest.metadata`.
6. `manifest_hash()` returns the bytes32 value that a real ERC-8183 submit flow
   would pass as the deliverable hash.

One-sentence story:

> RiskGuard produces verifiable DeFi policy verdicts off-chain and carries
> them as BNBAgent/ERC-8183-compatible manifest metadata.

## Target preferred path

The next deeper integration would submit the manifest hash through
`ERC8183Client.submit(job_id, deliverable, opt_params)` and anchor the
deliverable in the native job flow. That is intentionally not part of the
current MVP unless it stays lightweight.

## Why not a hook/policy contract now

ERC-8183 hooks and custom policies are the deeper integration point, but they
are not the right spike target. They increase audit surface, require more
contract work and make the project sound like a security protocol.

The MVP should prove the verdict content and evidence path first.

## Available BNBAgent APIs

Observed in `bnbagent 0.3.4`:

- `ERC8183Client`
  - `create_job(...)`
  - `register_job(...)`
  - `set_budget(...)`
  - `fund(...)`
  - `submit(job_id, deliverable, opt_params)`
  - `settle(job_id, evidence=b"")`
  - `get_job(...)`
  - `get_job_status(...)`
  - `get_verdict(...)`
- `DeliverableManifest`
  - `manifest_hash()`
  - `verify(on_chain_hash)`
  - extensible `metadata`
- `ERC8004Agent`
- `EVMWalletProvider`
- `SigningPolicy`
- `AgentEndpoint`

## Fallback path

Use `contracts/PolicyReceiptRegistry.sol` to record two receipt hashes on BSC
testnet:

- safe action: `Decision.Allow`;
- unsafe action: `Decision.Block`.

This fallback is only for BNB Hack's on-chain transaction requirement. It must
be described as a minimal receipt registry fallback, not as the product.

## Current status

Validated locally:

- `bnbagent==0.3.4` and `uagents==0.25.2` are project dependencies.
- `riskguard validate` produces deterministic allow/block receipts.
- `riskguard demo` produces one safe and one unsafe receipt.
- `riskguard manifest` builds a local ERC-8183 `DeliverableManifest` payload
  with `riskguard_receipt_hash` in `metadata`.
- `PolicyReceiptRegistry` compiles and passes local Foundry tests.
- Local Anvil end-to-end deploy and two receipt transactions pass.

Validated on BSC testnet:

- `PolicyReceiptRegistry`: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Deploy tx:
  `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
- Allow tx:
  `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block tx:
  `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
- `receiptCount()` returns `2`.

Not yet done:

- Real BNBAgent ERC-8183 job submission.
- opBNB deployment.
