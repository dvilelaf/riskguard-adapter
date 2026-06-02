#!/usr/bin/env bash
set -euo pipefail

PORT="${ANVIL_PORT:-18545}"
RPC_URL="http://127.0.0.1:${PORT}"
PRIVATE_KEY="${ANVIL_PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}"

anvil --host 127.0.0.1 --port "$PORT" --chain-id 31337 --silent &
ANVIL_PID="$!"

cleanup() {
  kill "$ANVIL_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

for _ in {1..30}; do
  if cast chain-id --rpc-url "$RPC_URL" >/dev/null 2>&1; then
    break
  fi
  sleep 0.2
done

if ! cast chain-id --rpc-url "$RPC_URL" >/dev/null 2>&1; then
  echo "anvil rpc did not start at ${RPC_URL}" >&2
  exit 1
fi

deploy_output="$(
  forge create contracts/PolicyReceiptRegistry.sol:PolicyReceiptRegistry \
    --rpc-url "$RPC_URL" \
    --private-key "$PRIVATE_KEY" \
    --broadcast \
    --out /tmp/riskguard-forge-out \
    --cache-path /tmp/riskguard-forge-cache
)"

registry_address="$(printf '%s\n' "$deploy_output" | awk '/Deployed to:/ {print $3}')"

if [[ -z "$registry_address" ]]; then
  echo "$deploy_output"
  echo "failed to parse deployed registry address" >&2
  exit 1
fi

eval "$(uv run riskguard foundry-env)"

cast send "$registry_address" \
  "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
  "$AGENT_ID" "$SAFE_PROPOSAL_HASH" "$POLICY_HASH" \
  "$SAFE_SIMULATION_HASH" "$SAFE_EVIDENCE_HASH" "$SAFE_DECISION" \
  --rpc-url "$RPC_URL" \
  --private-key "$PRIVATE_KEY" \
  >/dev/null

cast send "$registry_address" \
  "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
  "$AGENT_ID" "$BLOCK_PROPOSAL_HASH" "$POLICY_HASH" \
  "$BLOCK_SIMULATION_HASH" "$BLOCK_EVIDENCE_HASH" "$BLOCK_DECISION" \
  --rpc-url "$RPC_URL" \
  --private-key "$PRIVATE_KEY" \
  >/dev/null

receipt_count="$(
  cast call "$registry_address" "receiptCount()(uint256)" --rpc-url "$RPC_URL"
)"

if [[ "$receipt_count" != "2" && "$receipt_count" != "0x0000000000000000000000000000000000000000000000000000000000000002" ]]; then
  echo "unexpected receipt count: ${receipt_count}" >&2
  exit 1
fi

printf 'local_e2e_registry=%s\n' "$registry_address"
printf 'local_e2e_receipt_count=%s\n' "$receipt_count"
