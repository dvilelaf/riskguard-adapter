# BNB Hack form answers

Use this as the answer sheet when BNB confirms the current main-track
submission route.

Main-track form listed by the official page:

https://forms.gle/6jDbA1xrbtxHu2W87

Direct Google Forms URL observed by redirect:

https://docs.google.com/forms/d/e/1FAIpQLSemYQ0DbtqP3fe1sPs4wpUmKcoJos913TKgcgoQ5RQwt66LQg/viewform?usp=send_form

Note: the form requires Google login before fields are visible from this
environment, so exact field labels must be matched manually in the browser.

Status as of 2026-06-02: the form is closed to new responses in the browser.
See `docs/bnb-main-form-status.md`.

## Identity

Project name:

```text
RiskGuard Adapter
```

Team:

```text
Solo builder.
```

Contact email:

```text
<use David's preferred email>
```

Telegram/Discord/contact:

```text
<use David's preferred public contact>
```

## Track

Recommended track/category:

```text
Main track / AI / agent infrastructure
```

Project category:

```text
AI, DeFAI, BNB Chain agent infrastructure
```

## Short description

```text
RiskGuard Adapter checks autonomous DeFi action proposals against declared risk
policies before execution and emits deterministic allow/block Policy Verdict
Receipts. The prototype includes a local agent demo, a manifest-only
BNBAgent/ERC-8183 evidence payload, a BSC testnet receipt registry, and two
successful BSC testnet receipt transactions.
```

## Long description

```text
AI agents can propose on-chain financial actions faster than users can review
them. RiskGuard Adapter adds a small, composable policy-verdict layer for BNB
Chain agent workflows.

A strategy agent proposes a DeFi action. RiskGuard evaluates the action against
a declared policy: chain id, value, action, target contract, token and slippage.
It then emits a deterministic Policy Verdict Receipt with an allow or block
decision, a concrete reason, and stable hashes for the proposal, policy,
non-executing demo simulation record and evidence.

The current prototype is intentionally narrow. It does not custody funds,
execute trades, claim production safety or replace BNBAgent/ERC-8004/ERC-8183.
It demonstrates how a RiskGuard receipt can be generated locally, carried in
ERC-8183 DeliverableManifest.metadata, and anchored through a minimal BSC
testnet receipt registry.
```

## Links

Repository:

```text
https://github.com/dvilelaf/riskguard-adapter
```

Release:

```text
https://github.com/dvilelaf/riskguard-adapter/releases/tag/v0.1.0
```

Submission page:

```text
https://dvilelaf.github.io/riskguard-adapter/
```

Deck PDF:

```text
https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/deck.pdf
```

Demo video:

```text
https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-demo.mp4
```

Submission bundle:

```text
https://github.com/dvilelaf/riskguard-adapter/releases/download/v0.1.0/riskguard-submission-bundle.zip
```

Tweet URL:

```text
<paste tweet URL after posting>
```

## BSC testnet demo anchoring

Chain:

```text
BSC testnet
```

Chain id:

```text
97
```

Contract:

```text
0x10932358609f911B5cA1a131298C91a327ACAdC1
```

Deploy tx:

```text
0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
```

Allow receipt tx:

```text
0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
```

Block receipt tx:

```text
0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd
```

Explorer links:

```text
https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1
https://testnet.bscscan.com/tx/0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
https://testnet.bscscan.com/tx/0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
https://testnet.bscscan.com/tx/0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd
```

Receipt count:

```text
2
```

BscScan source verification:

```text
verified
```

## Implemented features

```text
- riskguard validate validates a single proposed action against a policy.
- riskguard demo runs policy-compliant and policy-violating demo flows.
- riskguard foundry-env exports contract-ready receipt hashes.
- riskguard manifest builds a manifest-only ERC-8183 evidence payload.
- PolicyReceiptRegistry records receipt hashes on BSC testnet.
- Evidence bundle includes allow/block receipts plus evidence and simulation preimages.
- CI verifies Python, Solidity and local EVM e2e.
```

## Non-claims

```text
RiskGuard Adapter does not claim production security, audited status, mainnet
readiness, custody, real trading, real ERC-8183 job submission/settlement or
opBNB deployment.
```

## If asked for future roadmap

```text
Next steps are a narrated demo video, real ERC-8183 job submission, opBNB
deployment, a public receipt hash checker, and DeFAI/treasury policy templates.
```
