#!/usr/bin/env bash
set -euo pipefail

RPC_URL="${BNB_TESTNET_RPC_URL:-https://data-seed-prebsc-1-s1.bnbchain.org:8545}"
TIMEOUT_SECONDS="${WAIT_SUBMIT_TIMEOUT_SECONDS:-1800}"
INTERVAL_SECONDS="${WAIT_SUBMIT_INTERVAL_SECONDS:-20}"

if [[ -z "${DEPLOYER_ADDRESS:-}" ]]; then
  echo "missing required env var: DEPLOYER_ADDRESS" >&2
  exit 1
fi

deadline=$((SECONDS + TIMEOUT_SECONDS))

while (( SECONDS <= deadline )); do
  balance="$(cast balance "$DEPLOYER_ADDRESS" --ether --rpc-url "$RPC_URL")"
  timestamp="$(date -Iseconds)"
  echo "${timestamp} balance=${balance} tBNB"

  if [[ "$balance" != "0.000000000000000000" ]]; then
    exec bash scripts/submit-testnet.sh
  fi

  sleep "$INTERVAL_SECONDS"
done

echo "timed out waiting for tBNB funding: ${DEPLOYER_ADDRESS}" >&2
exit 1
