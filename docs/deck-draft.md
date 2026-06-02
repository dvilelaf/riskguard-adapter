# Deck draft

Target: BNB Hack main track.

Length: 7 slides maximum.

## Slide 1: RiskGuard Adapter

Pre-execution policy verdicts for BNB Chain agents.

Evidence:

- open source;
- BSC testnet deployed;
- two successful receipt transactions;
- manifest-only ERC-8183 evidence payload;
- local tests and e2e checks.

Speaker note:

> RiskGuard is a small adapter for agentic DeFi workflows. It checks a proposed
> action against a declared policy before execution and emits a deterministic
> allow/block receipt.

## Slide 2: Problem

Autonomous agents can propose on-chain financial actions faster than users can
review them.

Risk today:

- blind trust in agent output;
- manual review that does not scale;
- unclear evidence about why an action was allowed or blocked;
- missing DeFi-specific policy verdict before execution.

Speaker note:

> The issue is not that agents cannot create transactions. The issue is that
> users need programmable, inspectable policy checks before those actions move
> closer to signing or settlement.

## Slide 3: Solution

RiskGuard Adapter turns policy constraints into deterministic verdict receipts.

It checks:

- chain id;
- max value;
- allowed action;
- target contract allowlist;
- token allowlist;
- max slippage.

Outputs:

- `allow` receipt for policy-compliant actions;
- `block` receipt for policy violations;
- receipt hashes for proposal, policy, simulation and evidence.

Speaker note:

> This is intentionally narrow. RiskGuard is not a wallet or a security
> protocol. It is the policy-verdict layer that can be called by an agent,
> wallet workflow or job system.

## Slide 4: Demo evidence

Implemented today:

- `riskguard validate`;
- `riskguard demo`;
- `riskguard foundry-env`;
- `riskguard manifest`;
- Solidity `PolicyReceiptRegistry`;
- BSC testnet deployment;
- allow and block receipt transactions;
- `just full-ci`.

BSC testnet:

- Contract: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Receipt count: `2`

Speaker note:

> The demo shows both sides: one proposed action that satisfies policy, and one
> proposed action blocked by slippage. Both are represented as receipts and
> anchored through the testnet registry.

## Slide 5: Architecture

```text
Agent intent / job
  -> RiskGuard policy check
  -> Policy Verdict Receipt
  -> ERC-8183 manifest metadata
  -> BSC testnet receipt anchoring
```

Important boundary:

- manifest-only ERC-8183 payload is implemented;
- real ERC-8183 job submission is a follow-up;
- opBNB is a follow-up;
- no mainnet funds or trading are used.

Speaker note:

> The manifest path lets a RiskGuard receipt hash travel with job evidence.
> The current submission does not claim real ERC-8183 settlement.

## Slide 6: Why BNB

BNB Chain is pushing AI agents, DeFAI and useful on-chain infrastructure.

RiskGuard fits because it gives builders:

- a reusable guardrail before autonomous DeFi actions;
- deterministic evidence for allow/block decisions;
- BSC testnet anchoring;
- a small integration surface for agents and wallets;
- an open-source base for future BNBAgent/ERC-8183 work.

Speaker note:

> The value is not a large app. It is a small component that can sit in the
> agent stack wherever a proposed financial action needs a policy verdict.

## Slide 7: Roadmap

Next:

- public demo video;
- BscScan source verified;
- real ERC-8183 job submission;
- public receipt verifier;
- opBNB deployment;
- policy templates for DeFAI and treasury workflows.

Submission target:

- primary fit: AI-agent infrastructure / DeFAI safety;
- judging angle: small, verifiable guardrail with live BSC testnet evidence.

Speaker note:

> The submission is deliberately scoped: deployed demo anchoring, deterministic
> receipts and a clear path to deeper agent integration.
