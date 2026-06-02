# RiskGuard Adapter

[![CI](https://github.com/dvilelaf/riskguard-adapter/actions/workflows/ci.yml/badge.svg)](https://github.com/dvilelaf/riskguard-adapter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

DeFi policy verdict receipts for BNB Chain agents and ERC-8183-style jobs.

RiskGuard Adapter checks proposed autonomous DeFi actions against declared risk
policies before execution and emits deterministic allow/block Policy Verdict
Receipts. The prototype includes a local agent demo, manifest-compatible
ERC-8183 evidence metadata, EVM-signed demo receipts, a verified BSC testnet
receipt registry, and two anchored testnet receipt transactions.

The prototype anchors two demo receipts on BSC testnet: one `allow` verdict and
one `block` verdict.

Public release: https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0

Submission page: https://dvilelaf.github.io/riskguard-adapter/

Receipt hash checker: https://dvilelaf.github.io/riskguard-adapter/verifier.html

License: MIT

Demo video:
https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4

## 30-second pitch

BNBAgent and ERC-8004/8183 give agents identity, job rails, escrow and evidence
flows. RiskGuard answers a narrower DeFi-specific question before execution or
settlement:

> Did this proposed autonomous financial action comply with the declared risk
> policy?

RiskGuard does not replace wallets, agents, registries or escrow. It adds a
small policy-verdict adapter that can be composed with agent jobs, wallet
workflows or BSC testnet anchoring contracts today.

```text
Agent intent / job
  -> RiskGuard policy check
  -> Policy Verdict Receipt
  -> ERC-8183 manifest metadata
  -> BSC testnet receipt registry demo anchoring today
```

## BSC testnet demo anchoring

Network: BSC testnet, chain id `97`.

- Contract: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Deploy tx:
  `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
- Allow receipt tx:
  `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block receipt tx:
  `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
- On-chain receipt count: `2`
- BscScan source verification: verified.
  Source: `contracts/PolicyReceiptRegistry.sol`.

This registry is intentionally minimal: it records receipt hashes on BSC
testnet for hackathon demo evidence. It does not authenticate callers, validate
receipt preimages, or prove that a receipt came from a production RiskGuard
deployment.

Explorer links:

- Contract:
  https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1
- Deploy tx:
  https://testnet.bscscan.com/tx/0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
- Allow tx:
  https://testnet.bscscan.com/tx/0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
- Block tx:
  https://testnet.bscscan.com/tx/0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd

Full run details: `docs/testnet-results.md`.

## What works today

- Policy JSON and action-plan JSON inputs.
- Deterministic allow/block evaluation.
- Deterministic receipt fields:
  - `agent_id`;
  - `policy_id`;
  - `decision`;
  - `reason`.
- Stable receipt hashes:
  - `proposal_hash`;
  - `policy_hash`;
  - `simulation_hash`;
  - `evidence_hash`.
- Persisted evidence and simulation preimages for the demo receipts.
- EVM-signed demo receipts and local signature verification.
- Local `StrategyAgent` and `RiskGuardAgent` demo.
- Manifest-only BNBAgent/ERC-8183 `DeliverableManifest.metadata` payload.
- Foundry/cast environment output for receipt transactions.
- Solidity `PolicyReceiptRegistry` contract.
- Local Anvil end-to-end deployment and two receipt transactions.
- Real BSC testnet deployment and two receipt transactions.
- Python tests, Ruff checks, Python package build and Solidity tests.

## What is intentionally not claimed

RiskGuard is an early prototype. It does not claim to:

- prevent hacks;
- guarantee transaction safety;
- be audited;
- be production-ready for mainnet funds;
- execute trades;
- custody funds;
- replace BNBAgent, ERC-8004, ERC-8183, Safe or wallets;
- implement a new escrow, registry, reputation system or trust standard.

## Try it in 5 minutes

This repo uses `uv` for Python package management and `just` for repeatable
commands.

```bash
just install
just demo
just sign-demo
just verify-demo
just foundry-env
uv run riskguard manifest --receipt examples/evidence/safe-receipt.json --job-id 42 --chain-id 97 --registry-address 0x10932358609f911B5cA1a131298C91a327ACAdC1
just test
just check
```

Run a single safe plan:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/safe-action.json
```

Run a single unsafe plan:

```bash
uv run riskguard validate \
  --policy examples/policies/default-policy.json \
  --plan examples/plans/unsafe-action.json
```

Generate a clean evidence bundle:

```bash
uv run riskguard demo --evidence-dir /tmp/riskguard-evidence
ls /tmp/riskguard-evidence
```

Expected files:

```text
safe-receipt.json
safe-evidence.json
safe-simulation.json
unsafe-receipt.json
unsafe-evidence.json
unsafe-simulation.json
```

Run the broad local verification suite:

```bash
just full-ci
```

`just full-ci` runs Ruff, Python tests, package build, Solidity tests and a
local Anvil deployment with two receipt transactions.

Build a manifest-only ERC-8183-compatible evidence payload:

```bash
uv run riskguard manifest \
  --receipt examples/evidence/safe-receipt.json \
  --job-id 42 \
  --chain-id 97 \
  --registry-address 0x10932358609f911B5cA1a131298C91a327ACAdC1
```

This does not submit or settle a real ERC-8183 job. It shows how a RiskGuard
receipt hash can be carried in `DeliverableManifest.metadata`.

Verify a signed receipt bundle:

```bash
just sign-demo
just verify-demo
```

`just sign-demo` expects `RISKGUARD_SIGNER_PRIVATE_KEY` in the environment.
The committed signed receipts are deterministic demo fixtures. `just
verify-demo` recomputes the evidence and simulation hashes, recovers the EVM
signature, and checks it against the published demo signer address. This is not
the funded BSC deployer key and is not a production identity claim.

## Receipt format

Example shape:

```json
{
  "agent_id": "strategy-agent-demo",
  "decision": "allow",
  "evidence_hash": "sha256:85bb8312f359bd2ff666bbfc367ae51e1ed0508b758efaca79553ecf86c05d68",
  "policy_hash": "sha256:1e15d7d1874bc88d87c5a6c8896e9947e63a01e267798a83ce69f9c15faa3695",
  "policy_id": "default-bnb-testnet-demo",
  "proposal_hash": "sha256:347dd403e5ddc6abe42e1439493eb20bcec08ee61591fbcee8b71f7a2377ae5a",
  "reason": "plan satisfies policy",
  "simulation_hash": "sha256:0c35068a9211e991fd9c18f4e6391df0883467095b0ee70353700ac219fcd47a"
}
```

The receipt is deterministic: the same policy and proposed action produce the
same hashes. In this prototype, `simulation_hash` commits to a non-executing
demo simulation record; no external DeFi simulator or transaction execution is
claimed.

## Repository layout

```text
riskguard-adapter/
  contracts/                 Minimal Solidity receipt registry
  src/riskguard_adapter/      Python package and CLI
  examples/                   Sample policies and action plans
  docs/                       Submission, validation and runbook notes
  scripts/                    Local and BSC testnet scripts
  tests/                      Python tests
```

## Useful commands

- `just install`: create/update the `.venv` with dev dependencies.
- `just demo`: run safe and unsafe local demo flows.
- `just sign-demo`: sign the demo receipts with `RISKGUARD_SIGNER_PRIVATE_KEY`.
- `just verify-demo`: verify signed receipts against evidence and simulation
  preimages.
- `just foundry-env`: print contract-ready receipt hash exports.
- `just test`: run the Python test suite.
- `just check`: run Ruff lint checks.
- `just build`: build the Python package.
- `just forge-test`: run receipt registry Solidity tests.
- `just local-e2e`: run local Anvil deploy plus two receipt transactions.
- `just full-ci`: run all local Python, Solidity and EVM checks.
- `just testnet-chain`: verify the configured BSC testnet RPC.
- `just submit-testnet`: deploy and record both receipts on BSC testnet after
  faucet funding.
- `just receipt-count`: verify on-chain receipt count for a deployed registry.

For the submitted BSC testnet registry:

```bash
POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
```

## Public Artifacts

- Submission page: https://dvilelaf.github.io/riskguard-adapter/
- Receipt hash checker: https://dvilelaf.github.io/riskguard-adapter/verifier.html
- Deck: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf
- Demo video: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4
- BSC testnet results: `docs/testnet-results.md`

## Roadmap

- Static receipt hash checker.
- Real ERC-8183 job submission.
- opBNB deployment.
- Policy templates for agentic treasury and DeFAI workflows.
