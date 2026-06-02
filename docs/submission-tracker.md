# Submission tracker

Date: 2026-06-02

Repo: https://github.com/dvilelaf/riskguard-adapter

## Status summary

Status: **submission package locally complete; external publishing steps remain**.

Completed locally:

- repo initialized and pushed public;
- README judge-ready;
- BSC testnet proof documented;
- safe/policy-compliant and policy-violating evidence receipts generated;
- manifest-only ERC-8183 payload implemented;
- deck draft written;
- HTML deck written;
- video recording plan written;
- submission copy written;
- CI and e2e checks passed;
- team review completed.

External remaining:

- record/upload demo video;
- upload/export final deck if the hackathon form requires a PDF or hosted deck
  rather than a GitHub file;
- post tweet;
- submit BNB Hack form;
- optionally verify contract source on BscScan after obtaining API key.

## Milestone tracker

| Milestone | Deliverables | Status | Acceptance evidence |
|---|---|---|---|
| 1. Submission narrative | `README.md` | Complete | README starts with pitch, proof links and non-claims. |
| 2. Evidence package | `examples/evidence/safe-receipt.json`, `examples/evidence/unsafe-receipt.json`, `docs/testnet-results.md` | Complete | Evidence drift check is clean; BSC `receiptCount()` returns `2`. |
| 3. ERC-8183 manifest adapter | `src/riskguard_adapter/erc8183.py`, `riskguard manifest`, `tests/test_erc8183.py` | Complete | Manifest tests pass; CLI emits `manifest_hash` and metadata. |
| 4. Demo video plan | `docs/video-recording-plan.md` | Ready to record | Commands and script are written. Video URL external. |
| 5. Deck and copy | `docs/deck-draft.md`, `docs/deck.html`, `docs/submission-copy.md` | Locally complete | Deck can be opened from repo; submission text ready. |
| 6. Final submit | GitHub URL, video URL, deck URL, tweet URL, BNB Hack form | Partially complete | GitHub URL exists. Video, tweet and form are external. |

## Submission links

- GitHub:
  https://github.com/dvilelaf/riskguard-adapter
- Deck Markdown:
  https://github.com/dvilelaf/riskguard-adapter/blob/main/docs/deck-draft.md
- Deck HTML:
  https://github.com/dvilelaf/riskguard-adapter/blob/main/docs/deck.html
- Video:
  external pending after recording
- Tweet:
  external pending after posting
- BNB Hack submission:
  external pending after form submit

## Verification commands

Run before final submit:

```bash
just full-ci
git diff --check
rm -rf /tmp/riskguard-review-evidence
uv run riskguard demo --evidence-dir /tmp/riskguard-review-evidence
diff -u examples/evidence/safe-receipt.json /tmp/riskguard-review-evidence/safe-receipt.json
diff -u examples/evidence/unsafe-receipt.json /tmp/riskguard-review-evidence/unsafe-receipt.json
POLICY_RECEIPT_REGISTRY_ADDRESS=0x10932358609f911B5cA1a131298C91a327ACAdC1 just receipt-count
git status --ignored --short .env.bsc-testnet-wallet
git ls-files --error-unmatch .env.bsc-testnet-wallet && exit 1 || true
set -a; source .env.bsc-testnet-wallet; set +a
rg -n --fixed-strings "$DEPLOYER_PRIVATE_KEY" README.md docs examples src scripts contracts .env.example
```

Expected:

- `just full-ci` passes;
- both evidence diffs are empty;
- `receiptCount()` returns `2`;
- `.env.bsc-testnet-wallet` is ignored and not tracked;
- private-key scan returns no matches.

## External blockers

### Demo video

Reason: requires local screen/audio recording and upload destination.

Input needed:

- upload destination: YouTube, Loom, Google Drive or BNB Hack-supported host.

Source material:

- `docs/video-recording-plan.md`

### Tweet

Reason: requires posting from user's X/Twitter account.

Source material:

- `docs/submission-copy.md`

### BNB Hack form

Reason: requires manual form submission and final artifact URLs.

Source material:

- `docs/submission-copy.md`
- `docs/submission-package.md`

### BscScan source verification

Reason: current shell has no `BSCSCAN_API_KEY` or `ETHERSCAN_API_KEY`.

Status:

- attempted Sourcify verification;
- Foundry could not generate standard JSON input without additional config;
- not blocking because source is public in GitHub and tx proof exists.
