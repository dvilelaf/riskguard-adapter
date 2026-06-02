# BNB testnet runbook

Date: 2026-06-02

## Decision

Primary chain: BSC testnet.

- Chain id: `97`
- RPC: `https://data-seed-prebsc-1-s1.bnbchain.org:8545`
- Faucet: https://www.bnbchain.org/en/testnet-faucet

Fallback chain: opBNB testnet only if BSC testnet faucet or RPC blocks.

## Verified locally

```bash
cast chain-id --rpc-url https://data-seed-prebsc-1-s1.bnbchain.org:8545
```

Expected:

```text
97
```

```bash
forge build --contracts contracts --out /tmp/riskguard-forge-out --cache-path /tmp/riskguard-forge-cache
```

Expected:

```text
Compiler run successful!
```

Equivalent repo target:

```bash
just forge-build
```

Run local Solidity tests before deploying:

```bash
just forge-test
```

Run the full local deploy + two-transaction flow on Anvil before using faucet
funds:

```bash
just local-e2e
```

Current local e2e result:

```text
local_e2e_receipt_count=2
```

## Environment

```bash
export BNB_TESTNET_RPC_URL="https://data-seed-prebsc-1-s1.bnbchain.org:8545"
export BNB_TESTNET_CHAIN_ID=97
export DEPLOYER_ADDRESS="0x..."
export DEPLOYER_PRIVATE_KEY="0x..."
export POLICY_RECEIPT_REGISTRY_ADDRESS="0x..."
```

Never use a wallet with real funds.

## Wallet

Create a disposable testnet wallet:

```bash
cast wallet new
```

Current local disposable wallet:

```text
0xd1ef957f7f5091D9c0341eCAB24Db5E1dA006B92
```

Its private key is stored only in the ignored local file:

```text
.env.bsc-testnet-wallet
```

Load it for local commands:

```bash
set -a
source .env.bsc-testnet-wallet
set +a
```

Fund it from the official faucet:

```text
https://www.bnbchain.org/en/testnet-faucet
```

Fallback faucet:

```text
https://faucet.chainstack.com/bnb-testnet-faucet
```

Chainstack advertises up to 0.5 BNB every 24 hours, but it requires a
Chainstack API key and checks that the requesting address has Ethereum mainnet
history and a minimum ETH balance. Treat it as a fallback, not the primary
route.

Check balance:

```bash
cast balance "$DEPLOYER_ADDRESS" --ether --rpc-url "$BNB_TESTNET_RPC_URL"
```

Equivalent repo target:

```bash
just testnet-balance
```

Current balance check:

```text
0.299922008400000000
```

The wallet has been funded and used for the first BSC testnet submission.

## Deploy

The first BSC testnet deployment is complete. Re-run only if a fresh contract
address is needed.

Single-command path after funding:

```bash
set -a
source .env.bsc-testnet-wallet
set +a
just submit-testnet
```

This deploys the registry, submits allow/block receipts, verifies count and
writes `docs/testnet-results.md`.

Current result:

```text
PolicyReceiptRegistry: 0x10932358609f911B5cA1a131298C91a327ACAdC1
Receipt count: 2
```

If the faucet may arrive while this session is running, use:

```bash
set -a
source .env.bsc-testnet-wallet
set +a
just wait-submit-testnet
```

Optional timeout controls:

```bash
export WAIT_SUBMIT_TIMEOUT_SECONDS=1800
export WAIT_SUBMIT_INTERVAL_SECONDS=20
```

```bash
forge create contracts/PolicyReceiptRegistry.sol:PolicyReceiptRegistry \
  --rpc-url "$BNB_TESTNET_RPC_URL" \
  --private-key "$DEPLOYER_PRIVATE_KEY" \
  --legacy \
  --out /tmp/riskguard-forge-out \
  --cache-path /tmp/riskguard-forge-cache
```

Equivalent repo target:

```bash
just deploy-registry
```

Save the deployed address:

```bash
export POLICY_RECEIPT_REGISTRY_ADDRESS="0x..."
```

## Receipt hashes

Use receipt-derived bytes32 values from the local demo:

```bash
eval "$(uv run riskguard foundry-env)"
```

Equivalent repo target:

```bash
eval "$(just foundry-env)"
```

## Record allow receipt

Only run this after `POLICY_RECEIPT_REGISTRY_ADDRESS` is set.

`Decision.Allow = 0`.

```bash
cast send "$POLICY_RECEIPT_REGISTRY_ADDRESS" \
  "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
  "$AGENT_ID" "$SAFE_PROPOSAL_HASH" "$POLICY_HASH" \
  "$SAFE_SIMULATION_HASH" "$SAFE_EVIDENCE_HASH" "$SAFE_DECISION" \
  --rpc-url "$BNB_TESTNET_RPC_URL" \
  --private-key "$DEPLOYER_PRIVATE_KEY" \
  --legacy
```

Equivalent repo target:

```bash
just record-allow
```

## Record block receipt

Only run this after `POLICY_RECEIPT_REGISTRY_ADDRESS` is set.

`Decision.Block = 1`.

```bash
cast send "$POLICY_RECEIPT_REGISTRY_ADDRESS" \
  "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
  "$AGENT_ID" "$BLOCK_PROPOSAL_HASH" "$POLICY_HASH" \
  "$BLOCK_SIMULATION_HASH" "$BLOCK_EVIDENCE_HASH" "$BLOCK_DECISION" \
  --rpc-url "$BNB_TESTNET_RPC_URL" \
  --private-key "$DEPLOYER_PRIVATE_KEY" \
  --legacy
```

Equivalent repo target:

```bash
just record-block
```

## Verify

If `just submit-testnet` succeeds, this section is already complete.

```bash
cast call "$POLICY_RECEIPT_REGISTRY_ADDRESS" "receiptCount()(uint256)" \
  --rpc-url "$BNB_TESTNET_RPC_URL"
```

Equivalent repo target:

```bash
just receipt-count
```

Current proof lives in:

```text
docs/testnet-results.md
```

```bash
cast call "$POLICY_RECEIPT_REGISTRY_ADDRESS" \
  "getReceipt(uint256)((bytes32,bytes32,bytes32,bytes32,bytes32,uint8,uint256))" \
  0 \
  --rpc-url "$BNB_TESTNET_RPC_URL"
```

## Kill criteria

- Stop if faucet, RPC and deploy take more than 60 minutes after wallet setup.
- Do not submit without a contract address and two successful transaction
  hashes.
- If BSC testnet blocks, try opBNB testnet once before pivoting.
