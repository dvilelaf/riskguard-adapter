#!/usr/bin/env bash
set -euo pipefail

RPC_URL="${BNB_TESTNET_RPC_URL:-https://data-seed-prebsc-1-s1.bnbchain.org:8545}"
RESULTS_PATH="${RESULTS_PATH:-docs/testnet-results.md}"

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "missing required env var: ${name}" >&2
    exit 1
  fi
}

extract_transaction_hash() {
  local output="$1"
  local hash
  hash="$(
    printf '%s\n' "$output" \
      | grep -Eo '"transactionHash":"0x[0-9a-fA-F]{64}"' \
      | head -n1 \
      | cut -d'"' -f4
  )"
  if [[ -n "$hash" ]]; then
    printf '%s\n' "$hash"
    return
  fi

  printf '%s\n' "$output" | awk '/^transactionHash/ {print $2; exit}'
}

require_env DEPLOYER_ADDRESS
require_env DEPLOYER_PRIVATE_KEY

chain_id="$(cast chain-id --rpc-url "$RPC_URL")"
if [[ "$chain_id" != "97" ]]; then
  echo "expected BSC testnet chain id 97, got ${chain_id}" >&2
  exit 1
fi

balance="$(cast balance "$DEPLOYER_ADDRESS" --ether --rpc-url "$RPC_URL")"
if [[ "$balance" == "0.000000000000000000" ]]; then
  echo "deployer has zero tBNB: ${DEPLOYER_ADDRESS}" >&2
  echo "fund it first: https://www.bnbchain.org/en/testnet-faucet" >&2
  exit 1
fi

deploy_output="$(
  forge create contracts/PolicyReceiptRegistry.sol:PolicyReceiptRegistry \
    --rpc-url "$RPC_URL" \
    --private-key "$DEPLOYER_PRIVATE_KEY" \
    --broadcast \
    --legacy \
    --out /tmp/riskguard-forge-out \
    --cache-path /tmp/riskguard-forge-cache
)"

registry_address="$(printf '%s\n' "$deploy_output" | awk '/Deployed to:/ {print $3}')"
deploy_tx="$(printf '%s\n' "$deploy_output" | awk '/Deployer:/ {next} /Transaction hash:/ {print $3; exit}')"

if [[ -z "$registry_address" ]]; then
  echo "$deploy_output"
  echo "failed to parse deployed registry address" >&2
  exit 1
fi

eval "$(uv run riskguard foundry-env)"

allow_output="$(
  cast send "$registry_address" \
    "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
    "$AGENT_ID" "$SAFE_PROPOSAL_HASH" "$POLICY_HASH" \
    "$SAFE_SIMULATION_HASH" "$SAFE_EVIDENCE_HASH" "$SAFE_DECISION" \
    --rpc-url "$RPC_URL" \
    --private-key "$DEPLOYER_PRIVATE_KEY" \
    --legacy
)"
allow_tx="$(extract_transaction_hash "$allow_output")"

block_output="$(
  cast send "$registry_address" \
    "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
    "$AGENT_ID" "$BLOCK_PROPOSAL_HASH" "$POLICY_HASH" \
    "$BLOCK_SIMULATION_HASH" "$BLOCK_EVIDENCE_HASH" "$BLOCK_DECISION" \
    --rpc-url "$RPC_URL" \
    --private-key "$DEPLOYER_PRIVATE_KEY" \
    --legacy
)"
block_tx="$(extract_transaction_hash "$block_output")"

receipt_count="$(
  cast call "$registry_address" "receiptCount()(uint256)" --rpc-url "$RPC_URL"
)"

if [[ "$receipt_count" != "2" && "$receipt_count" != "0x0000000000000000000000000000000000000000000000000000000000000002" ]]; then
  echo "unexpected receipt count: ${receipt_count}" >&2
  exit 1
fi

cat > "$RESULTS_PATH" <<EOF
# BNB testnet results

Date: $(date -Iseconds)

## Network

- Chain: BSC testnet
- Chain id: ${chain_id}
- RPC: ${RPC_URL}

## Deployer

- Address: ${DEPLOYER_ADDRESS}
- Starting balance: ${balance} tBNB

## Contract

- PolicyReceiptRegistry: ${registry_address}
- Deploy tx: ${deploy_tx:-unknown}

## Receipt transactions

- Allow receipt tx: ${allow_tx:-unknown}
- Block receipt tx: ${block_tx:-unknown}
- Receipt count: ${receipt_count}
EOF

printf 'registry_address=%s\n' "$registry_address"
printf 'deploy_tx=%s\n' "${deploy_tx:-unknown}"
printf 'allow_tx=%s\n' "${allow_tx:-unknown}"
printf 'block_tx=%s\n' "${block_tx:-unknown}"
printf 'receipt_count=%s\n' "$receipt_count"
printf 'results_path=%s\n' "$RESULTS_PATH"
