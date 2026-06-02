# BNB Hack submission roadmap

Date: 2026-06-02

## Team decision

Decision: **go for submission, with frozen scope**.

Approval is unanimous only under this interpretation:

- submit RiskGuard Adapter as a small BNB Chain safety/evidence adapter;
- target BNB Hack main track first;
- aim for the 3,000 USDT prize as the realistic base case;
- keep 7,000 USDT as a stretch outcome, not as the planning assumption;
- do not turn the project into a broad product before submission.

This is not an unconditional product green light. The team rejected broad
scope expansion because it would reduce the prize/hour ratio for a solo
builder using AI.

## Prize target

Primary target: **BNB Hack main track 3rd prize, 3,000 USDT**.

Stretch target: **2nd prize, 7,000 USDT**, only if the submission package makes
the project feel like BNB-native agent infrastructure rather than a CLI demo.

Do not plan around 1st prize. The current project is useful and credible, but
it is not yet a complete agent product with adoption, UI, deep sponsor
integration or community traction.

## Why this is a go

RiskGuard already has the hard proof that many hackathon projects lack:

- deterministic allow/block Policy Verdict Receipts;
- a local agent demo;
- a minimal BSC testnet receipt registry;
- real BSC testnet deployment;
- two successful BSC testnet receipt transactions;
- tests and repeatable `just` targets.

BNB Hack rewards open-source work, integration, usability, innovation,
documentation, roadmap and proof on BSC/opBNB. The official rules require
GitHub, deck, demo video, deployment or connection to BSC/opBNB, at least two
successful contract transactions, and a tweet. RiskGuard already covers the
deployment/transaction requirement.

## Product framing

One-liner:

> RiskGuard Adapter is a DeFi-specific policy verdict adapter for autonomous
> BNB Chain agents and ERC-8183-style jobs.

Judge story:

> AI agents can propose DeFi actions faster than users can review them.
> RiskGuard checks a proposed action against user-defined policy before
> execution and emits a verifiable verdict receipt designed to be attached to
> an agent job, wallet workflow or BSC testnet proof.

Architecture story:

```text
Agent intent / job
  -> RiskGuard policy check
  -> Policy Verdict Receipt
  -> BNBAgent/ERC-8183-compatible manifest metadata
  -> BSC testnet receipt registry proof today
```

Say:

- programmable guardrails;
- pre-signing policy verdict;
- open-source adapter;
- BSC testnet deployed;
- composable with agent and wallet flows;
- early prototype with clear integration roadmap.

Do not say:

- prevents hacks;
- guarantees safe transactions;
- audited;
- production-ready for mainnet funds;
- trust layer;
- escrow;
- wallet security protocol;
- first or only, unless later proven.

## Scope freeze

Allowed before submission:

- README judge pass;
- demo evidence bundle;
- demo video;
- short deck;
- tweet/submission copy;
- BNBAgent/ERC-8183 manifest-only adapter;
- optional contract verification if it is quick.

Not allowed before submission:

- dashboard;
- hosted backend;
- indexer;
- multi-chain support;
- mainnet funds;
- real trading;
- custom wallet;
- custom escrow;
- new reputation system;
- broad policy engine rewrite;
- real ERC-8183 job lifecycle unless it works inside the timebox.

## Roadmap

Total target: **6-10 focused hours**.

Hard stop: **12 hours** unless a nearly finished submission only needs small
polish.

### Milestone 1: Submission narrative

Timebox: 1 hour.

Tasks:

- Rewrite the README top section for judges.
- State exactly what is implemented versus roadmap.
- Put the BSC testnet contract and tx links near the top.
- Add the 30-second pitch.
- Add the architecture diagram.

Done when:

- a judge can understand the project in the first 60 seconds of reading;
- the README does not overclaim production security;
- the repo clearly points to `docs/testnet-results.md`.

### Milestone 2: Evidence package

Timebox: 1-2 hours.

Tasks:

- Generate a clean evidence directory with one allow receipt and one block
  receipt.
- Capture terminal output for:
  - `just test`;
  - `just check`;
  - `just local-e2e`;
  - `POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count`.
- Keep final BSC testnet address and tx hashes in documentation.
- Try contract verification only if a BscScan API key and Foundry command path
  are immediately available.

Done when:

- the demo proof can be shown without live debugging;
- `receiptCount()` returns `2`;
- missing contract verification, if any, is documented as non-blocking.

### Milestone 3: BNBAgent/ERC-8183 evidence adapter

Timebox: 1-2 hours.

Build only the lightweight version:

- construct a local `DeliverableManifest`;
- attach `riskguard_receipt_hash` in `metadata`;
- print the manifest hash;
- add a test or documented command proving the manifest roundtrip.

Current status: implemented as `riskguard manifest`.

Do not attempt full ERC-8183 job submission unless the manifest-only path is
finished early and the remaining work looks trivial.

Done when:

- the submission can honestly claim ERC-8183-compatible manifest evidence;
- it does not claim a real settled ERC-8183 job unless one exists.

Kill criteria:

- stop if SDK debugging, funding, storage, settlement or job lifecycle work
  consumes more than 2 hours.

### Milestone 4: Demo video

Timebox: 2-3 hours.

Target length: 90-150 seconds.

Script:

1. Problem: autonomous DeFi agents need policy checks before execution.
2. Product: RiskGuard emits allow/block Policy Verdict Receipts.
3. Demo: show policy, safe action, unsafe action, receipts and tests.
4. On-chain proof: show BSC testnet contract, txs and `receiptCount=2`.
5. Integration: show BNBAgent/ERC-8183 manifest metadata path.
6. Close: open source, deployed, tested and ready for integrations.

Done when:

- the video can be uploaded with the submission;
- no live step is required for judges to believe the demo.

### Milestone 5: Deck and submission copy

Timebox: 2 hours.

Deck: 7 slides maximum.

Slides:

1. RiskGuard Adapter: pre-execution policy verdicts for BNB Chain agents.
2. Problem: agentic wallets can act faster than users can review.
3. Solution: policy verdict adapter before signing/execution.
4. Demo proof: CLI, tests, BSC testnet contract and two txs.
5. Architecture: agent/job -> RiskGuard -> manifest/proof -> BSC testnet.
6. Why BNB: DeFAI and agent infrastructure need composable guardrails.
7. Roadmap/business model: hosted policy API, team policies, templates and
   integrations.

Submission copy:

- GitHub repo URL;
- demo video URL;
- deck URL;
- BSC testnet contract address;
- deploy, allow and block tx URLs;
- tweet URL with `@BNBChain`, `#BNBHack` and the chosen track/challenge.

Done when:

- all artifacts are ready before adding any further features.

### Milestone 6: Final verification and submit

Timebox: 1 hour.

Tasks:

- Run `just full-ci`.
- Run `git diff --check`.
- Run `git status --ignored --short .env.bsc-testnet-wallet` and confirm it
  prints `!! .env.bsc-testnet-wallet`.
- Run `git ls-files --error-unmatch .env.bsc-testnet-wallet && exit 1 || true`
  and confirm the file is not tracked.
- Source `.env.bsc-testnet-wallet` locally and run
  `rg -n --fixed-strings "$DEPLOYER_PRIVATE_KEY" README.md docs examples src scripts contracts .env.example`;
  confirm no private key appears.
- Submit to BNB Hack main track.
- Post the required tweet.

Done when:

- the project is submitted;
- the final links are added to a submission log document.

## Stretch backlog

Only start these after submission assets are complete:

- tiny static receipt verifier page;
- BscScan testnet contract verification;
- real ERC-8183 job submission;
- opBNB deployment;
- one community feedback post in BNB Discord/forum;
- one short tutorial article.

Each stretch must have a 1-day maximum. If it does not materially improve the
submission within that cap, stop.

## Final go/no-go rules

Go if:

- README, video, deck and tx proof are clear;
- the story is agent safety/evidence, not a generic CLI;
- the repo stays easy to run;
- no private key or funded mainnet wallet is involved.

Submit immediately if:

- the submission package is complete and only stretch features remain.

Stop or pivot if:

- the project cannot be explained in 30 seconds;
- BNBAgent integration consumes more than the timebox;
- the work starts requiring backend infra, custody, real trading or a dashboard;
- the expected prize/hour falls below the 3,000 USDT target logic.

## Sources

- BNB Hack official page: https://www.bnbchain.org/en/hackathons/bnb-ai-hack
- BNB Hack submission requirements and scoring criteria on the same page.
