# Final team review

Date: 2026-06-02

Scope: BNB Hack submission readiness for RiskGuard Adapter.

## Reviewers

- Hackathon submission expert: prize fit, form readiness, judge framing.
- Solidity/on-chain verification expert: deployed contract, BscScan source
  visibility, verification path.
- Product/security skeptic: secret handling, proof strength, misleading claims,
  evidence quality.

## Decision

Decision: **GO for BNB Hack submission only with explicit caveats**.

Allowed submission framing:

- solo builder using AI assistance;
- open-source prototype;
- deterministic policy verdict receipts;
- manifest-only ERC-8183 evidence payload;
- BSC testnet demo anchoring with two successful receipt transactions;
- BscScan source verified, source available in GitHub.

Rejected submission framing:

- expert-audited;
- production security system;
- guaranteed safe DeFi execution;
- real ERC-8183 job lifecycle or settlement;
- cryptographic proof that the on-chain receipt came from a production
  RiskGuard deployment.

## Findings

### High: final form cannot be submitted by the agent

The BNB Hack Google Form requires the user's authenticated browser/account. The
tweet URL and personal contact details must be added by the user before final
submission.

Status: accepted. Tracked as external actions in `docs/submission-tracker.md`.

### High: BscScan source was not verified

The live BscScan testnet page originally said the contract was unverified. The
repo had enough source metadata to verify it: single Solidity file, no
constructor args, Solc `0.8.34`, optimizer disabled, EVM `prague`.

Status: fixed. BscScan returned `Pass - Verified`.

Verification command:

```bash
just verify-bscscan
```

### High: on-chain registry is only demo anchoring

`PolicyReceiptRegistry` records hashes and decisions, but it does not
authenticate callers, validate receipt preimages, enforce uniqueness, or prove a
production RiskGuard run.

Status: accepted. README and submission docs now use "demo anchoring" instead
of broad "proof" language.

### Medium: evidence preimages were not persisted

The original demo wrote receipt JSON only. Reviewers could see the hashes but
not the evidence and simulation preimages.

Status: fixed. `riskguard demo` now writes:

- `safe-receipt.json`
- `safe-evidence.json`
- `safe-simulation.json`
- `unsafe-receipt.json`
- `unsafe-evidence.json`
- `unsafe-simulation.json`

### Medium: simulation hash could be misread as external simulation

The demo uses a policy-only simulation placeholder with `status: not-run`.

Status: accepted. README and submission docs now state that no external DeFi
simulator is claimed.

### Medium: secret handling needs discipline

The local disposable deployer key is intentionally kept in
`.env.bsc-testnet-wallet`, which is ignored and untracked. It must not be shown
in recordings, release bundles, screenshots or form text.

Status: accepted. Public-file scans must remain clean before submission.

## Verification Snapshot

Fresh verification before this document:

- `uv run python -m pytest tests/test_policy.py tests/test_agents.py -q`:
  `9 passed`.
- `just full-ci`: Ruff passed, 21 Python tests passed, package build passed, 2
  Solidity tests passed, local Anvil e2e returned `local_e2e_receipt_count=2`.
- BSC testnet `receiptCount()`: `2`.
- BscScan source verification: `Pass - Verified`.
- Public GitHub Actions CI: latest listed run succeeded.
- GitHub Pages responded HTTP 200.
- Private-key scan across public project files returned no matches.

## Final Recommendation

Submit after:

1. The user posts the required tweet.
2. The user fills the Google Form from an authenticated browser.
3. The form text keeps the caveats above.

BscScan verification is complete.
