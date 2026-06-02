# RiskGuard Adapter v0.1.0

First hackathon submission package for RiskGuard Adapter.

## Included

- Policy JSON and action-plan JSON inputs.
- Deterministic `allow` and `block` Policy Verdict Receipts.
- Local `StrategyAgent` and `RiskGuardAgent` demo.
- Manifest-only BNBAgent/ERC-8183 evidence payload via `riskguard manifest`.
- Solidity `PolicyReceiptRegistry`.
- BSC testnet deployment.
- Two successful BSC testnet receipt transactions.
- Evidence bundle.
- EVM-signed demo receipt fixtures.
- CLI receipt bundle verification with expected-signer checking.
- Public browser receipt hash checker.
- Submission README, deck, video plan, transcript and copy.

## BSC testnet proof

- Contract:
  `0x10932358609f911B5cA1a131298C91a327ACAdC1`
- Deploy tx:
  `0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd`
- Allow receipt tx:
  `0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5`
- Block receipt tx:
  `0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd`
- `receiptCount()`: `2`

## Verification

Last local verification before release:

- `just full-ci`: passed.
- Python tests: 31 passed.
- Solidity tests: 2 passed.
- Local Anvil e2e: `local_e2e_receipt_count=2`.
- Evidence drift check: clean.
- Signed receipt verification: safe and blocked fixtures valid.
- BSC testnet `receiptCount()`: `2`.
- Private key scan: no public-file leak found.

## Known non-claims

This release does not claim:

- production security;
- audited status;
- mainnet readiness;
- real trading;
- custody;
- real ERC-8183 job submission or settlement;
- opBNB deployment.

Those are explicitly future work or out of scope for the current submission
package.
