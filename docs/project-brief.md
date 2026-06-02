# Project brief

Date: 2026-06-02

## Working title

RiskGuard Adapter: policy verdict receipts for BNBAgent / uAgents DeFAI jobs.

## Target

BNB Hack first. ASI / Fetch-style agent intelligence is the preferred sponsor
angle if the active submission route still matches the challenge signal.

The original standalone AgentTrust Circuit concept is no-go after competitor
review. This project must complement BNBAgent SDK / ERC-8004 / ERC-8183 rather
than replace them.

## Demo Flow

1. `StrategyAgent` proposes a bounded action.
2. `RiskGuardAgent` checks a deterministic policy.
3. Safe action is approved and recorded.
4. Unsafe action is blocked and recorded.
5. `PolicyReceiptRegistry` stores policy verdict receipt hashes on BNB testnet
   only if needed for hackathon transaction requirements.
6. Evidence bundle can be verified locally.

## Acceptance Criteria

- One repo.
- One README.
- One policy file.
- One approved run.
- One blocked run.
- One evidence bundle per run.
- BNBAgent/ERC-8004-compatible evidence path where feasible.
- One BNB testnet receipt registry only if needed.
- At least two successful BNB testnet transactions.
- One demo video script.

## Current Spike Status

Passed:

- `riskguard validate` emits deterministic allow/block receipts.
- `riskguard demo` runs safe and unsafe local agent flows.
- `riskguard demo --evidence-dir ...` writes safe and unsafe receipt JSON
  files.
- `riskguard foundry-env` emits contract-ready bytes32 exports derived from
  the local demo receipts.
- `bnbagent` and `uagents` are installed as project dependencies.
- Preferred integration path is BNBAgent/ERC-8183 evidence adapter.
- Fallback path is `PolicyReceiptRegistry` on BSC testnet.
- BSC testnet RPC returns chain id 97.
- `PolicyReceiptRegistry` compiles with Foundry.
- `PolicyReceiptRegistry` passes local Solidity tests.
- Local Anvil e2e deploys the registry, records allow/block receipts and
  verifies count 2.
- BSC testnet `PolicyReceiptRegistry` deployed.
- BSC testnet allow/block receipt transactions recorded.
- `docs/testnet-results.md` contains address and tx hashes.

Pending:

- Demo video recording.

## Kill Criteria

- If uAgents integration burns more than half a day, keep the agent interface
  minimal and prioritize the BNB on-chain proof.
- If wallet/contract integration is not working by hour 6, simplify to an
  evidence hash registry plus mocked action.
- If the demo is not sent or sendable within 7 days, shrink or kill.
- If the work starts looking like a custom registry, wallet, escrow, reputation
  system or trust protocol, stop and return to the adapter scope.
