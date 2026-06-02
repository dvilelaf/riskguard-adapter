# Competitive due diligence

Date: 2026-06-02

## Decision

No-go for the original standalone AgentTrust Circuit.

Unanimous pivot-go for:

> RiskGuard Adapter for BNBAgent/uAgents: a small policy-verdict adapter that
> helps BNB/ASI agents prove whether a proposed DeFAI action complied with
> declared constraints before execution.

This is not a new wallet, registry, escrow protocol, reputation passport or
agent evidence standard. It is a demo-sized integration layer on top of the
existing BNB/ASI agent stack.

## Why the original is too duplicative

Existing or adjacent solutions already cover much of the original idea:

- BNBAgent SDK: BNB-native Python toolkit for ERC-8004 identity and ERC-8183
  agent commerce, including jobs, escrow, deliverables and evidence hashes.
- ERC-8004: identity, reputation and validation registries, including evidence
  fields such as response URI/hash.
- BNB AI Agent ecosystem: BNBAgent SDK, Virtuals ACP, Agent0 SDK and 8004scan.
- Sigil: agent-wallet guardrails with deterministic rules, simulation, AI risk
  scoring, session keys and spend/target/function limits.
- Namera: programmable wallet infrastructure for agents with session keys,
  policies, call restrictions, gas policies and rate limits.
- AAWP: agent-oriented wallet infrastructure with on-chain identity and
  guardian-style control.
- Safe: transaction guards, modules and spending limits.
- AIGP / AgentHook: structured runtime evidence and audit trail specs for AI
  agents.
- ACP / ARC-402-style protocols: agent-to-agent jobs, escrow, evidence and
  settlement.

The original "custom registry + guard + evidence hash" story would likely look
like a shallow clone.

## Defensible wedge

Build a policy evaluator that complements sponsor-native infrastructure:

> A Fetch/uAgents `RiskGuardAgent` that evaluates BNBAgent/ERC-8183 DeFAI job
> requests before execution, emits a machine-readable policy verdict receipt,
> and anchors the decision through ERC-8004/BNBAgent-compatible evidence.

The differentiator is DeFi-specific validation and settlement gating for
autonomous financial-agent jobs, not generic identity, escrow or wallet
security.

## Policy Verdict Receipt

Minimum receipt fields:

- `agent_id`
- `proposal_hash`
- `policy_hash`
- `simulation_hash`
- `decision`: `allow` or `block`
- `reason`
- `evidence_hash` or `evidence_uri`
- optional `tx_hash`

## Minimum build

- Two agents:
  - `StrategyAgent`: proposes one bounded DeFAI action.
  - `RiskGuardAgent`: evaluates the proposed action.
- One JSON policy:
  - max spend;
  - allowed token;
  - allowed contract;
  - allowed function;
  - max slippage;
  - simulation success required.
- Use BNBAgent SDK / ERC-8004 / ERC-8183 where feasible.
- One BNB testnet receipt registry only if needed for hackathon transaction
  requirements.
- Two demo paths:
  - approved action;
  - blocked unsafe action.
- At least two successful BNB testnet transactions.
- Demo video under 90 seconds.

## Hard limits

- No custom reputation system.
- No custom escrow.
- No custom agent registry.
- No session-key wallet security claims.
- No mainnet.
- No real trading.
- No "protects funds" or production security language.
- No marketplace.
- No complex dashboard.
- Max 12-16 build hours.
- If BNBAgent/uAgents integration is not working by hour 6, simplify to a
  compatible receipt demo and document the integration boundary honestly.

## Filters added after due diligence

- Standards-overlap filter: does ERC-8004, ERC-8183, ACP or AIGP already cover
  this?
- Sponsor-native filter: are we extending official BNB/ASI tools or competing
  with them?
- Commodity-hack filter: will many teams build the same AI wallet guard demo?
- Security-claim filter: would the claim require audits to be credible?
- Evidence-overlap filter: are we adding meaningful validation, or just storing
  another hash?
- Wallet-overlap filter: would a judge hear "Sigil/Namera/Safe" if we describe
  this as generic agent wallet guardrails?
- Prize/hour filter: is the likely $3k-$10k cash prize worth the effort?
- Maintenance filter: does this imply running validators, wallets, APIs,
  custody, support or a live service?
- Demo-distinctiveness filter: can the differentiator be understood in 30
  seconds?

## Unanimous team decision

Marco + Elena: pivot-go. Original is too duplicative; build a policy evaluation
agent that plugs into BNB agent-commerce flow.

Aisha + Vega: pivot-go. The defensible technical wedge is a BNBAgent-compatible
DeFAI Risk Validator, not independent trust infrastructure.

Lua + Tomas + Diablo: pivot-go. The adapter version is small, judge-legible and
survivable. If it cannot be built as an integration demo in 2-3 days, kill it.
