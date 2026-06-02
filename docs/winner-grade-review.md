# Winner-grade review

Date: 2026-06-02

Implementation reviewed through: `ef6fec1`

Later commits may update this document or release packaging without changing
the reviewed implementation surface.

## Decision

Decision: **GO for BNB Hack submission if a live submission route is confirmed**.

Current blocker: the official BNB main-track Google Form linked from the public
BNB Hack page is closed to new responses. The project package is ready to send
once BNB support provides a current route.

## Hito Status

| Hito | Status | Evidence |
|---|---|---|
| 0. Submission route | Externally blocked | `docs/bnb-main-form-status.md` documents the closed official form and support message. |
| 1. Receipt fixture verification | Complete | `riskguard sign`, `riskguard verify`, signed receipt fixtures, expected-signer checks and tamper tests. |
| 2. Public hash checker | Complete | `docs/verifier.html` is live and checks receipt preimages plus signed payload hash. |
| 3. Human-facing cleanup | Complete | README, landing page, deck and submission copy use product-first wording and remove backstage framing. |
| 4. Demo media | Ready for narrated recording | `docs/video-recording-plan.md` and `docs/demo-transcript.md` include signed verification, hash checker and BSC anchoring. |
| 5. Final review and release | Complete | Team re-review returned zero accepted technical/copy findings; release assets were refreshed. |

## Public Deliverables

- Landing page: https://dvilelaf.github.io/riskguard-adapter/
- Receipt hash checker: https://dvilelaf.github.io/riskguard-adapter/verifier.html
- Repository: https://github.com/dvilelaf/riskguard-adapter
- Release: https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0
- Deck PDF: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf
- Demo video asset: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4
- Submission bundle: https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-submission-bundle.zip
- Verified BSC testnet source:
  https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1#code

## Technical Evidence

- Contract: `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Deploy tx:
  `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
- Allow receipt tx:
  `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block receipt tx:
  `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
- `receiptCount()` returns `2`
- Demo signer checked by CLI:
  `0xDC4814F2BC829880073D2B64355c518Fc7648Cda`

## Verification Snapshot

Fresh local verification after final fixes:

```bash
just ci
just verify-demo
git diff --check
```

Result:

- Ruff passed.
- Python tests: `31 passed`.
- Package build passed.
- Safe signed receipt verification returned `valid: true`.
- Unsafe signed receipt verification returned `valid: true`.
- `git diff --check` passed.

Public checks:

- GitHub CI succeeded for `ef6fec1`.
- GitHub Pages deploy succeeded for `ef6fec1`.
- Published landing page contains the primary CTA row and BSC Testnet
  Anchoring section.
- Published hash checker contains the CLI EVM recovery caveat.
- Published release bundle contains `docs/verifier.html`,
  `docs/evidence/*-signed-receipt.json` and updated release notes.
- Published PDF deck has no browser date/path/page footer artifacts.

## Team Review Closure

Accepted findings fixed:

- Browser verifier overclaimed signer verification. It is now framed as a hash
  checker; CLI verification is the signer-verification path.
- CLI verification accepted any self-declared signer. It now supports
  `--expected-signer`, and `just verify-demo` pins the demo signer.
- CLI verification returned exit code `0` on invalid bundles. It now exits `1`.
- Demo signer private key was embedded in `Justfile`. `sign-demo` now requires
  `RISKGUARD_SIGNER_PRIVATE_KEY`.
- Public docs linked internal strategy language. Public artifact links now
  focus on product deliverables.
- README evidence instructions listed files not produced by `riskguard demo`.
  The generated file list now matches the command.
- `eth-account` was only a transitive dependency. It is now direct.
- Deck PDF had browser print chrome. It was regenerated without headers and
  footers.
- Landing lacked a primary judge action. It now has `Watch demo`, `Check
  receipt hashes`, and `View source`.
- Submission copy was stale relative to the signed receipt/hash checker work.
  It now includes signed fixtures, checker and BscScan source verification.

Re-review results:

- Backend/crypto reviewer: zero accepted findings.
- Product/copy reviewer: zero accepted findings.
- Hackathon/human reviewer: stale bundle and signing-message overclaim were
  fixed before this document.

## Honest Limits

Do not claim:

- production security;
- audited status;
- mainnet readiness;
- custody;
- real trading;
- real ERC-8183 job settlement;
- opBNB deployment;
- that BSC testnet storage proves production RiskGuard execution.

Allowed claim:

RiskGuard is an open-source BNB Chain agent-infrastructure prototype that
checks autonomous DeFi action proposals against declared policies, emits
deterministic verdict receipts, exposes signed demo receipt fixtures, anchors
receipt component hashes on BSC testnet and carries receipt metadata through a
manifest-only ERC-8183-compatible payload.

## Remaining Actions

1. Ask BNB Hack support for the current submission route.
2. Record or replace the narrated demo video using
   `docs/video-recording-plan.md`.
3. Post the tweet from the user account if required by the final form.
4. Submit through the confirmed route.
