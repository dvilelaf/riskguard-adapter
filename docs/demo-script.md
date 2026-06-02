# Demo script

Target length: 90 seconds to 3 minutes.

## Story

Autonomous agents can act on-chain, but financial actions need policy verdicts.
RiskGuard Adapter shows a strategy agent proposing a DeFAI action, a guard agent
checking declared constraints, and a BNB testnet receipt proving the verdict.

## Beats

1. Show the policy: budget, allowed contract/action and risk limits.
2. Run the safe action with
   `uv run riskguard demo --evidence-dir /tmp/riskguard-evidence`.
3. Show `approve` decision and evidence bundle.
4. Show BNB testnet policy receipt transaction.
5. Run the unsafe action in the same demo output.
6. Show `block` decision and evidence bundle.
7. Show second BNB testnet policy receipt transaction.
8. Close with: BNBAgent gives agents identity and job rails; RiskGuard adds a
   small policy-verdict adapter for financial actions.

## On-chain Recording

After the disposable BSC testnet wallet is funded, run:

```bash
set -a
source .env.bsc-testnet-wallet
set +a
just submit-testnet
```

Use `docs/testnet-results.md` for the contract address and transaction hashes
shown in beats 4 and 7.

Current BSC testnet proof:

- Contract: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Allow tx: `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block tx: `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`

## Current Pitch

BNBAgent already handles identity, jobs, escrow, settlement and evidence.
RiskGuard Adapter adds one narrow piece before execution or settlement: a
DeFi-specific policy verdict receipt. The demo shows a strategy agent proposing
one allowed action and one blocked action, with proposal, policy and evidence
hashes that can be anchored through BNBAgent/ERC-8183 or a minimal BNB testnet
receipt registry.
