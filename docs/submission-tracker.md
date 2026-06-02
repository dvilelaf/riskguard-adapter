# Submission tracker

Date: 2026-06-02

Repo: https://github.com/dvilelaf/riskguard-adapter

Release: https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0

## Status summary

Status: **submission package complete; final tweet/form account actions remain**.

Completed locally:

- repo initialized and pushed public;
- public release created with PDF deck asset;
- README judge-ready;
- BSC testnet proof documented;
- safe/policy-compliant and policy-violating evidence receipts generated;
- manifest-only ERC-8183 payload implemented;
- deck draft written;
- HTML deck written;
- PDF deck generated;
- video recording plan written;
- demo transcript written;
- fallback silent demo video render script written;
- fallback silent demo video uploaded as release asset;
- submission bundle uploaded as release asset;
- GitHub Pages enabled with public submission page;
- submission copy written;
- BNB Hack form package written;
- CI and e2e checks passed;
- team review completed.

External remaining:

- post tweet;
- submit BNB Hack form;

Optional polish:

- replace fallback silent demo video with narrated upload;
- verify contract source on BscScan after obtaining API key.

## Milestone tracker

| Milestone | Deliverables | Status | Acceptance evidence |
|---|---|---|---|
| 1. Submission narrative | `README.md` | Complete | README starts with pitch, proof links and non-claims. |
| 2. Evidence package | `examples/evidence/safe-receipt.json`, `examples/evidence/unsafe-receipt.json`, `docs/testnet-results.md` | Complete | Evidence drift check is clean; BSC `receiptCount()` returns `2`. |
| 3. ERC-8183 manifest adapter | `src/riskguard_adapter/erc8183.py`, `riskguard manifest`, `tests/test_erc8183.py` | Complete | Manifest tests pass; CLI emits `manifest_hash` and metadata. |
| 4. Demo video | `docs/video-recording-plan.md`, `docs/demo-transcript.md`, `scripts/render-demo-video.sh`, release asset `riskguard-demo.mp4` | Fallback complete | Silent fallback video exists. Narrated recording remains recommended. |
| 5. Deck and copy | `docs/deck-draft.md`, `docs/deck.html`, `docs/deck.pdf`, `docs/submission-copy.md` | Locally complete | PDF deck is generated; submission text ready. |
| 6. Final submit | GitHub URL, video URL, deck URL, tweet URL, BNB Hack form | Partially complete | GitHub/release/deck/form text exist. Video, tweet and form submission are external. |

## Submission links

- GitHub:
  https://github.com/dvilelaf/riskguard-adapter
- Release:
  https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0
- GitHub Pages:
  https://dvilelaf.github.io/riskguard-adapter/
- Deck Markdown:
  https://github.com/dvilelaf/riskguard-adapter/blob/main/docs/deck-draft.md
- Deck HTML:
  https://github.com/dvilelaf/riskguard-adapter/blob/main/docs/deck.html
- Deck PDF:
  https://github.com/dvilelaf/riskguard-adapter/blob/main/docs/deck.pdf
- Deck PDF release asset:
  https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf
- Submission bundle:
  https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-submission-bundle.zip
- Video fallback:
  https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4
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

GitHub issues:

- Optional narrated demo video:
  https://github.com/dvilelaf/riskguard-adapter/issues/3
- Tweet:
  https://github.com/dvilelaf/riskguard-adapter/issues/2
- BNB Hack form:
  https://github.com/dvilelaf/riskguard-adapter/issues/4
- Optional BscScan verification:
  https://github.com/dvilelaf/riskguard-adapter/issues/1

### Optional narrated demo video

Reason: recommended for stronger judging, but no longer blocks a minimal
submission because a fallback MP4 release asset exists.

Input needed:

- upload destination: YouTube, Loom, Google Drive or BNB Hack-supported host;
- optional voice recording.

Source material:

- `docs/video-recording-plan.md`
- `docs/demo-transcript.md`

Fallback asset:

- https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4

### Tweet

Reason: requires posting from user's X/Twitter account.

Source material:

- `docs/submission-copy.md`

### BNB Hack form

Reason: requires manual form submission and final artifact URLs.

Source material:

- `docs/submission-copy.md`
- `docs/submission-package.md`
- `docs/bnb-hack-form.md`

### BscScan source verification

Reason: current shell has no `BSCSCAN_API_KEY` or `ETHERSCAN_API_KEY`.

Status:

- attempted Sourcify verification;
- Foundry could not generate standard JSON input without additional config;
- not blocking because source is public in GitHub and tx proof exists.
