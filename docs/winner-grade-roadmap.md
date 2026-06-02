# Winner-grade polish roadmap

Date: 2026-06-02

Goal: turn RiskGuard from a credible solo-built hackathon MVP into a
judge-legible, money-oriented submission with one or two visible technical depth
upgrades.

Timebox: 2 focused days. Stop before day 4 unless BNB confirms a live submission
route or a sponsor route with high fit.

## Current Verdict

RiskGuard is real but thin. It has verified BSC testnet anchoring, CI,
receipts, manifest metadata and release assets. The risk is that judges see too
much process scaffolding and too little human product judgment or technical
depth.

## Target Routes

1. BNB main track: primary route if BNB provides a current submission path.
2. ASI sponsor: secondary route only if current intake is confirmed.
3. Unibase: skip unless sponsor explicitly confirms this policy-verdict angle.

## Milestones

| Milestone | Timebox | Deliverables | Done when |
|---|---:|---|---|
| 0. Submission route | 30 min | Message to BNB support, response tracked | We have a current submit route or a documented external blocker. |
| 1. Receipt fixture verification | 4-6 h | EVM-signed receipts, `riskguard sign`, `riskguard verify`, tests, regenerated evidence | Done: CLI verifies signed receipts and hash preimages. |
| 2. Public hash checker | 4-6 h | `docs/verifier.html`, public Pages link, README/link updates | Done: browser checks demo receipt hashes, signed payload hash and preimages without local setup. |
| 3. Human-facing cleanup | 2-3 h | Product-first README/landing, internal docs de-emphasized, placeholders removed | Done: public copy emphasizes product evidence and avoids backstage framing. |
| 4. Demo media | 2-3 h | Narrated 90-150s video plan, transcript, refreshed release asset/link | Ready: recording plan and transcript show signed verification, BscScan source, receipt count and manifest metadata. |
| 5. Final review and release | 1-2 h | `docs/winner-grade-review.md`, CI/e2e proof, release bundle refresh | Done: team re-review closed accepted findings, release assets and public links are current. |

## Hito 0: Submission Route

Action:

- Send the prepared message from `docs/bnb-main-form-status.md` to:
  https://mee6.xyz/i/f00NIOmDWP

Decision:

- If BNB gives a current main-track route, continue BNB main.
- If BNB does not respond within one working day, keep polishing but also ask
  ASI/BNB support whether the ASI sponsor route is still valid.

## Hito 1: Receipt Fixture Verification

Why:

The strongest technical criticism is that the registry records arbitrary hashes.
Signed receipts do not make it production-ready, but they let a reviewer check
that the committed fixture has stable preimages and a recoverable EVM signature.

Scope:

- sign canonical receipt JSON with an EVM account;
- include `signer`, `signature`, and `signed_payload_hash`;
- verify the signature and recompute policy/evidence/simulation hashes;
- keep this claim local unless the signature hash is also anchored on-chain;
- avoid using the deployer private key in docs or public files.

Deliverables:

- `src/riskguard_adapter/signatures.py`
- tests for sign/verify/tamper failure;
- CLI commands:
  - `riskguard sign --receipt ... --private-key-env RISKGUARD_SIGNER_PRIVATE_KEY`
  - `riskguard verify --receipt ... --evidence ... --simulation ...`
- regenerated demo evidence with signed receipts or signed receipt sidecars.

Current status:

- `riskguard sign` implemented;
- `riskguard verify` implemented;
- `just sign-demo` and `just verify-demo` implemented;
- signed demo receipts generated with a demo-only EVM key.

## Hito 2: Public Hash Checker

Why:

The project needs one visible artifact that feels inspectable by a human judge.
The verifier should make the receipt idea legible in 30 seconds.

Scope:

- static HTML/JS only;
- no backend;
- load demo receipt/evidence/simulation from repo links;
- recompute hashes in browser;
- show signature status when signed fields exist;
- link to BscScan contract and receipt transactions.

Deliverables:

- `docs/verifier.html`;
- `docs/evidence/*` public demo evidence copies;
- link from `docs/index.html`;
- README public artifact link.

Current status:

- static hash/preimage checker implemented;
- allow/block demo bundles load in the browser;
- browser recomputes evidence hash, simulation hash and signed payload hash;
- full EVM signature recovery and expected-signer checking remain available in
  `riskguard verify`.

## Hito 3: Human-facing Cleanup

Why:

The current public surface exposes too much planning machinery. Judges should
see a product and proof, not the internal AI workflow.

Changes:

- make `docs/index.html` product-first, not "submission package";
- trim README docs list to core docs only;
- keep local workspace paths out of public-facing docs;
- move internal strategy docs under an internal section or omit them from
  README;
- remove unresolved placeholders from public-facing docs;
- keep public framing as "solo builder, manually verified".

Current status:

- README and landing page now lead with the product claim and direct artifact
  links;
- submission copy uses "solo builder", "demo video", and "non-executing demo
  simulation record" instead of backstage phrasing;
- BNB form-status logistics are no longer a primary landing-card action.

## Hito 4: Demo Media

Recording is now unblocked. The plan and transcript were refreshed after Hitos
1-3 so the video shows the current proof surface.

Narrative:

1. Why policy receipts matter for autonomous DeFi actions.
2. Show safe and blocked action.
3. Verify receipt hashes and signature.
4. Show BSC testnet contract, verified source and `receiptCount=2`.
5. Show manifest metadata.
6. State limits: no production security claim, no mainnet funds.

Deliverables:

- `docs/video-recording-plan.md`;
- `docs/demo-transcript.md`;
- existing release video asset until a narrated recording replaces it.

Status:

- recording pack complete;
- narrated recording remains a user-side action because it needs voice/screen
  capture and upload destination choice.

## Hito 5: Final Review

Run a final team review with:

- hackathon judge;
- human-oriented reviewer;
- technical skeptic;
- security/on-chain reviewer.

GO criteria:

- BNB route exists or blocker is documented;
- public surface is product-led and human-readable;
- hash checker and signed receipt CLI verification are visible;
- all tests and public links pass.

NO-GO criteria:

- no submission route and no sponsor route;
- verifier/signature work fails or creates misleading claims;
- public docs still contain placeholders or internal-only paths.

Current status:

- GO if BNB confirms a current route;
- externally blocked only by the closed official Google Form;
- final review recorded in `docs/winner-grade-review.md`.
