# Validation gate

Date: 2026-06-02

Question: is RiskGuard Adapter viable, useful, prize-relevant, differentiated
and apparently unblocked?

## Verdict

Status: go for BNB Hack MVP.

RiskGuard Adapter passes only as a small BNBAgent/uAgents adapter. It does not
pass as a standalone trust layer, wallet guard, registry, escrow system,
reputation system or generic evidence protocol.

Team validation status: unanimous yellow/go-conditioned. No reviewer found a
fatal blocker, but nobody approved this as a clean unconditional go.

Spike execution status at 2026-06-02 15:16 CEST:

- Local allow/block receipts: passed.
- Local agent demo: passed.
- Contract-ready Foundry env output: passed.
- `bnbagent` and `uagents` dependencies: added.
- BNBAgent/ERC-8183 path: selected as evidence adapter.
- BSC testnet RPC and contract compile: passed.
- Local Solidity receipt registry tests: passed.
- Local Anvil deploy and two receipt transactions: passed.
- Post-faucet BSC testnet submit script: prepared and balance-gated.
- Wait-for-faucet submit script: prepared.
- Disposable BSC testnet wallet: created.
- Disposable wallet funded by faucet.
- Real BNB testnet deploy and two transactions: passed.
- `docs/testnet-results.md`: written.

## Gate status

| Gate | Status | Reason |
|---|---|---|
| Viable | Green | `bnbagent` and `uagents` are project dependencies. Local policy evaluator, demo and Foundry env commands work. BSC testnet RPC returns chain id 97, the receipt registry compiles with Foundry, and real BSC testnet deploy plus two receipt transactions passed. |
| Useful | Green/yellow | BNBAgent handles identity/jobs/escrow/evidence, but its built-in `SigningPolicy` appears focused on typed-data signing safety, not DeFi-specific job/action validation such as slippage, target contract, action budget and simulation verdicts. |
| Prize-relevant | Green/yellow | BNB Hack lists AI/DeFAI-style tracks, main prizes of 10k / 7k / 3k USDT and sponsored challenges. ASI is only a secondary target until a current sponsor form is confirmed; the ASI/Fetch page found by the team appears to describe a 2025 round that is closed. |
| Similar solutions | Yellow/red | Similar infrastructure exists: BNBAgent SDK, ERC-8004, ERC-8183, Sigil, Safe, AIGP, AgentHook, Virtuals ACP, Namera, AAWP and related agent-commerce/evidence systems. Differentiation must be narrow. |
| Roadblocks | Yellow | The BNB Hack MVP path has no fatal technical blocker left. Remaining yellow items are real BNBAgent job submission, sponsor-current ASI requirements and judge novelty. |

## What is validated

- BNB Hack is active as an online event until 2026-12-31.
- BNB Hack lists AI, DeSoc, DeSci and DePIN categories.
- BNB Hack lists main cash prizes of 10k / 7k / 3k USDT plus kickstart perks.
- BNB Hack lists ASI Alliance as a sponsored challenge.
- BNB Hack requires an open-source submission, demo assets, a BSC/opBNB
  mainnet or testnet deployment/integration and at least two successful
  transactions within the hackathon timeframe.
- BNBAgent SDK exists as a Python package and public GitHub repo.
- `uv run --with bnbagent --with uagents python ...` successfully imported:
  - `bnbagent 0.3.4`
  - `uagents 0.25.2`
- Project dependencies now include:
  - `bnbagent>=0.3.4`
  - `uagents>=0.25.2`
- Local commands now work:
  - `uv run riskguard validate --policy examples/policies/default-policy.json --plan examples/plans/safe-action.json`
  - `uv run riskguard validate --policy examples/policies/default-policy.json --plan examples/plans/unsafe-action.json`
  - `uv run riskguard demo`
- `uv run riskguard foundry-env`
- Real BSC testnet proof:
  - `PolicyReceiptRegistry`: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
  - deploy tx: `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
  - allow tx: `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
  - block tx: `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
  - receipt count: `2`
- BNBAgent exposes useful classes:
  - `ERC8004Agent`
  - `ERC8183Client`
  - `EVMWalletProvider`
  - `SigningPolicy`
  - `PolicyViolation`
  - `Verdict`
- uAgents exposes core classes:
  - `Agent`
  - `Context`
  - `Model`

## What is not validated yet

- That current ASI sponsor submissions are still open through a current form.
- That real BNBAgent/ERC-8183 job submission works end-to-end.
- That judges will consider this sufficiently novel rather than an incremental
  BNBAgent demo.
- That ASI sponsor submissions are current enough to justify ASI-specific work.

## Spike decision

Current decision: go for BNB Hack MVP.

Proceed to submission prep:

- record a short demo video;
- prepare a small deck;
- publish/open-source the repo;
- submit through BNB Hack main track.

Keep ASI as secondary unless a current ASI sponsor route is confirmed manually.
Do not build ASI-specific functionality yet.

## Differentiator required

The project must be described as:

> A DeFi-specific policy validator / evaluator for BNBAgent/uAgents and
> ERC-8183 jobs that emits a Policy Verdict Receipt before execution or
> settlement.

It must not be described as:

- a new agent trust layer;
- a new wallet guardrail product;
- a new ERC-8004 alternative;
- a new escrow protocol;
- a new evidence standard;
- a production security layer.

The 30-second pitch must be:

> BNBAgent handles identity, jobs, escrow and settlement. RiskGuard adds the
> DeFi-specific policy verdict that says whether a proposed autonomous
> financial action complied with declared constraints before it executed.

## Remaining validation work

Timebox: one focused session after wallet/faucet setup.

Success criteria:

- Fund one disposable BSC testnet wallet.
- Deploy `PolicyReceiptRegistry`.
- Record one allow receipt and one block receipt.
- Capture contract address and transaction hashes.
- Optionally run a real BNBAgent/ERC-8183 job submission using the receipt hash
  as deliverable metadata.
- Confirm manually whether ASI still accepts current sponsor submissions.

Kill or simplify if:

- No current ASI sponsor form is found within 30 minutes.
- BNBAgent job submission consumes the session without producing a clear tx or
  deliverable hash.
- uAgents integration dominates the demo instead of helping it.
- The project looks like a clone of BNBAgent/Sigil/Safe/AIGP.
- The differentiator cannot be explained in 30 seconds.
- BNB testnet deployment and two receipt transactions cannot be completed
  inside the spike window after wallet/faucet setup.

## Sources

- BNB Hack: https://www.bnbchain.org/en/hackathons/bnb-ai-hack
- BNB testnet faucet: https://www.bnbchain.org/en/testnet-faucet
- Chainstack BNB testnet faucet: https://faucet.chainstack.com/bnb-testnet-faucet
- BNBAgent SDK: https://github.com/bnb-chain/bnbagent-sdk
- BNB AI Agent Solutions: https://www.bnbchain.org/en/solutions/ai-agent
- ERC-8004: https://eips.ethereum.org/EIPS/eip-8004
- Fetch/uAgents docs: https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- Fetch/ASI historical BNB challenge: https://www.fetch.ai/events/bnb-hackathon-2025
- ASI challenge historical page: https://luma.com/7uhpamhq
- Sigil: https://sigil.codes/
- Namera: https://www.namera.ai/
- AAWP: https://aawp.ai/
- AIGP: https://open-aigp.org/
