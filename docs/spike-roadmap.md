# Spike roadmap

Date: 2026-06-02

## Purpose

Turn the current conditional go into one of three decisions:

- go: build the BNB Hack MVP;
- pivot: keep the project, but simplify the integration story;
- kill: stop before spending real time.

This spike is for one solo builder using AI. It must take 2-3 focused hours,
with a hard 4-hour maximum. If the spike needs more time to answer the core
questions, that is evidence against the prize/hour ratio.

## Non-negotiables

- No mainnet funds.
- No custody.
- No real trading.
- No custom wallet, escrow, registry or reputation system.
- No production security claims.
- No dashboard unless the CLI and evidence path already work.
- No ASI-specific build unless a current ASI sponsor route is confirmed.

## Success criteria

The spike succeeds only if all of these are true:

- BNB Hack main-track submission path is confirmed as the primary prize route.
- ASI is either confirmed current or explicitly downgraded to secondary.
- `bnbagent` and `uagents` are real project dependencies or intentionally
  excluded with a written reason.
- A safe action and unsafe action produce deterministic Policy Verdict
  Receipts from real JSON inputs.
- The receipt includes `proposal_hash`, `policy_hash`, decision, reason and
  evidence hash.
- A plausible BNBAgent/ERC-8183/ERC-8004 anchoring path is identified.
- BNB testnet deploy plus two receipt transactions is either completed or
  estimated as low-friction with exact next commands.
- The 30-second pitch is clear without saying "wallet guardrails",
  "trust layer", "registry", "escrow" or "reputation".

## Task checklist and time estimate

Total target: 240 minutes maximum.

| Task | Estimate | Output |
|---|---:|---|
| Run baseline checks | 15 min | `just ci`, CLI version and git status verified. |
| Confirm BNB Hack route | 15 min | Current BNB main-track rules/prizes recorded. |
| Decide ASI status | 10 min | ASI marked current, secondary or dropped. |
| Add dependencies decision | 10 min | `bnbagent` and `uagents` added or explicitly deferred. |
| Implement `riskguard validate` | 35 min | Safe/unsafe JSON plans are loaded and evaluated. |
| Generate deterministic receipts | 20 min | Stable receipt JSON and hash for allow/block runs. |
| Add evaluator tests | 20 min | Unit tests for allow and multiple block reasons. |
| Add local agent demo | 35 min | `StrategyAgent` and `RiskGuardAgent` run one demo flow. |
| Inspect BNBAgent/ERC-8183 path | 35 min | Preferred anchoring path and fallback are documented. |
| Check BNB testnet deploy path | 25 min | RPC/faucet/wallet/deploy route known or blocker recorded. |
| Attempt receipt transactions | 20 min | Two tx hashes if wallet/faucet is ready; otherwise `just foundry-env` and exact `cast send` commands. |
| Update docs and decide | 20 min | `validation-gate`, demo script and GO/PIVOT/KILL updated. |

Current execution note: all spike tasks are complete. BSC testnet deploy and
both receipt transactions passed, and `docs/testnet-results.md` contains the
contract address and transaction hashes.

Hard stop: if the first eight tasks do not produce local allow/block receipts
inside 155 minutes, stop the spike and classify the project as kill or major
pivot.

## Phase 0: Setup and Baseline

Timebox: 0-15 minutes.

Goal: prove the local repo still builds before adding uncertainty.

Actions:

- Run `just ci`.
- Run `uv run riskguard --version`.
- Check `git status --short --branch`.
- Create a scratch notes file only if needed; final findings belong in docs.

Pass condition:

- `just ci` passes.
- CLI version prints `0.1.0`.
- No unexplained dirty files beyond current repo scaffolding.

Kill/simplify condition:

- If baseline tooling fails for reasons unrelated to the spike, fix only the
  baseline before continuing.

## Phase 1: Prize Route Check

Timebox: 15-40 minutes.

Goal: avoid building for the wrong prize.

Actions:

- Re-open BNB Hack main page and confirm dates, prize structure and rules.
- Confirm the required submission artifacts:
  - GitHub repo;
  - deck;
  - demo video;
  - BSC/opBNB mainnet or testnet integration;
  - at least two successful transactions;
  - tweet with the required tags.
- Search for a current ASI sponsor form or current ASI challenge page.
- If only old Fetch/ASI pages appear, mark ASI as secondary.

Pass condition:

- BNB main track remains valid.
- ASI status is classified as current, secondary or dropped.

Kill/simplify condition:

- If no current ASI route is found within 30 minutes, stop spending spike time
  on ASI and target BNB Hack main track.

Expected artifact:

- Update `docs/validation-gate.md` with the current primary target and ASI
  status.

## Phase 2: Local Policy Evaluator

Timebox: 40-95 minutes.

Goal: prove the core product exists without blockchain friction.

Actions:

- Add a `riskguard validate` CLI command.
- Load:
  - `examples/policies/default-policy.json`;
  - `examples/plans/safe-action.json`;
  - `examples/plans/unsafe-action.json`.
- Validate at least:
  - chain id;
  - max spend;
  - target contract allowlist;
  - action/function allowlist;
  - token allowlist;
  - max slippage.
- Emit deterministic receipts for allow and block decisions.
- Hash receipts with stable JSON serialization.

Pass condition:

- `riskguard validate --policy examples/policies/default-policy.json --plan
  examples/plans/safe-action.json` emits `allow`.
- `riskguard validate --policy examples/policies/default-policy.json --plan
  examples/plans/unsafe-action.json` emits `block`.
- Unit tests cover one allow case and at least two block reasons.

Kill/simplify condition:

- If receipts cannot be generated from real JSON examples by minute 95, stop.
  The project is not ready for prize work.

Expected artifact:

- Evidence files under `examples/evidence/` or a clearly documented CLI output
  format.

## Phase 3: Agent Interface

Timebox: 95-135 minutes.

Goal: show the project is agent-facing without letting uAgents dominate.

Actions:

- Create a minimal `StrategyAgent` interface that returns a proposed action.
- Create a minimal `RiskGuardAgent` interface that returns a policy verdict.
- Try a local uAgents message exchange only if it stays lightweight.
- If uAgents takes too long, keep plain Python agents and document the
  uAgents-compatible boundary.

Pass condition:

- One command runs safe and unsafe agent flows locally.
- The RiskGuard side produces the same receipt format as Phase 2.

Kill/simplify condition:

- If uAgents local exchange is not working within 45 minutes of this phase,
  drop uAgents runtime integration for the spike and keep a compatible
  interface.

Expected artifact:

- A local demo command such as `riskguard demo`.

## Phase 4: BNBAgent / ERC-8183 Path

Timebox: 135-180 minutes.

Goal: decide whether the MVP integrates directly with BNBAgent or only claims
compatibility.

Actions:

- Inspect installed `bnbagent` APIs and examples.
- Identify whether the receipt should attach through:
  - ERC-8183 job attestation/evaluator fields;
  - ERC-8004 validation response;
  - BNBAgent job metadata/evidence;
  - minimal `PolicyReceiptRegistry` fallback.
- Write down the exact chosen path and why.

Pass condition:

- One preferred path is selected.
- One fallback path is selected.
- The selected path can be explained in one sentence.

Kill/simplify condition:

- If BNBAgent integration is still unclear after this phase, do not keep
  digging during the spike. Ship a BNBAgent-compatible receipt demo and mark
  direct integration as a follow-up.

Expected artifact:

- Update `docs/project-brief.md` or create `docs/integration-path.md`.

## Phase 5: BNB Testnet Feasibility

Timebox: 180-225 minutes.

Goal: prove that the hackathon's on-chain requirement is not a hidden blocker.

Actions:

- Confirm target chain:
  - BSC testnet, chain id 97, or opBNB testnet if rules make it easier.
- Confirm wallet and faucet path.
- Confirm RPC endpoint.
- Decide whether to use the existing `PolicyReceiptRegistry` contract.
- Attempt deployment only if wallet/faucet/RPC are ready.
- Attempt two `recordReceipt` transactions if deployment succeeds.

Pass condition:

- Best case: contract deployed and two successful receipt transactions exist.
- Acceptable spike result: exact deploy/tx commands are known, and no faucet,
  RPC or KYC blocker appears.

Kill/simplify condition:

- If faucet/RPC/deploy consumes more than 60 minutes after setup, mark the
  project yellow and do not submit until on-chain proof works.

Expected artifact:

- Contract address and tx hashes if completed.
- Otherwise: exact missing blocker and next command.

## Phase 6: Decision Gate

Timebox: 225-240 minutes.

Goal: make the decision while the evidence is fresh.

Actions:

- Re-run `just ci`.
- Update `docs/validation-gate.md`.
- Update `docs/demo-script.md` if the demo path changed.
- Write the final verdict:
  - go;
  - pivot;
  - kill.

Go if:

- Local allow/block receipts work.
- BNB main-track route is confirmed.
- On-chain receipt path is solved or very close.
- The BNBAgent/ERC-8183 story is credible.
- The demo can be recorded within one more focused session.

Pivot if:

- Local receipts work, but direct BNBAgent/uAgents integration is too slow.
- BNB testnet is plausible but not completed.
- The pitch is still clear as a BNBAgent-compatible receipt adapter.

Kill if:

- Local receipts do not work.
- BNB on-chain proof looks painful.
- The project sounds like Sigil/Namera/Safe when explained.
- The only prize route left is ASI and ASI is not currently open.

## Final deliverables after a go

- `riskguard validate` CLI.
- `riskguard demo` CLI.
- Two JSON receipts:
  - safe action: allow;
  - unsafe action: block.
- One chosen integration path doc.
- BNB testnet contract address and two transaction hashes, if available.
- Updated 90-second demo script.
- Updated README with exact demo commands.

## Prize expectation after this spike

Primary target: BNB Hack main track.

Realistic cash target: 3,000 USDT.

Stretch target: 7,000-10,000 USDT if the BNB-native integration and demo are
clean.

ASI target: only if a current ASI sponsor form is found. Otherwise, ASI remains
useful narrative context, not the target prize.
