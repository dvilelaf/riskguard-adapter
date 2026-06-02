# RiskGuard Adapter

DeFi policy verdict receipts for BNB Chain agents and ERC-8183-style jobs.

RiskGuard Adapter is an open-source policy/evidence adapter for autonomous
financial agents. A strategy agent proposes a DeFi action, RiskGuard checks it
against a declared policy before execution, and the result is emitted as a
machine-readable Policy Verdict Receipt.

The prototype is deployed on BSC testnet and has two successful receipt
transactions: one `allow` verdict and one `block` verdict.

## 30-second pitch

BNBAgent and ERC-8004/8183 give agents identity, job rails, escrow and evidence
flows. RiskGuard answers a narrower DeFi-specific question before execution or
settlement:

> Did this proposed autonomous financial action comply with the declared risk
> policy?

RiskGuard does not replace wallets, agents, registries or escrow. It adds a
small policy-verdict adapter that can be composed with agent jobs, wallet
workflows or BSC testnet proof contracts today.

```text
Agent intent / job
  -> RiskGuard policy check
  -> Policy Verdict Receipt
  -> planned BNBAgent/ERC-8183 evidence metadata
  -> BSC testnet receipt registry proof today
```

## BSC testnet proof

Network: BSC testnet, chain id `97`.

- Contract: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Deploy tx:
  `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
- Allow receipt tx:
  `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block receipt tx:
  `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
- On-chain receipt count: `2`
- BscScan source verification: pending, non-blocking for the current prototype.
  Source: `contracts/PolicyReceiptRegistry.sol`.

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
unsafe-receipt.json
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
same hashes.

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

## Submission docs

- Competitive due diligence: `docs/competitive-due-diligence.md`
- Validation gate: `docs/validation-gate.md`
- Spike roadmap: `docs/spike-roadmap.md`
- Submission roadmap and team approval: `docs/submission-roadmap.md`
- Submission package checklist: `docs/submission-package.md`
- Submission tracker: `docs/submission-tracker.md`
- Deck draft: `docs/deck-draft.md`
- HTML deck: `docs/deck.html`
- PDF deck: `docs/deck.pdf`
- Video recording plan: `docs/video-recording-plan.md`
- Submission copy: `docs/submission-copy.md`
- Integration path: `docs/integration-path.md`
- Demo script: `docs/demo-script.md`
- BNB testnet results: `docs/testnet-results.md`
- BNB testnet runbook: `docs/testnet-runbook.md`

## Roadmap

Before submission:

1. Polish the judge-facing README, demo evidence and demo video.
2. Prepare a 7-slide deck and submission copy.
3. Run final CI and submit to BNB Hack main track.

After submission:

- BscScan contract verification.
- Tiny static receipt verifier.
- Real ERC-8183 job submission if it stays lightweight.
- opBNB deployment.
- Policy templates for agentic treasury and DeFAI workflows.

## Compass context

Strategy and grant-planning docs live in:

`/media/david/DATA/repos/compass/docs/pilots/bnb-asi-project-ideas.md`
