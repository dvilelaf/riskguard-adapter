set shell := ["bash", "-uc"]
set dotenv-load := true

bnb_rpc := env_var_or_default("BNB_TESTNET_RPC_URL", "https://data-seed-prebsc-1-s1.bnbchain.org:8545")
registry := env_var_or_default("POLICY_RECEIPT_REGISTRY_ADDRESS", "0x10932358609f911B5cA1a131298C91a327ACAdC1")

# Install dependencies
install:
    uv sync --all-groups

# Run the demo CLI
run:
    uv run riskguard

# Run safe and unsafe local demo flows
demo:
    uv run riskguard demo --evidence-dir /tmp/riskguard-evidence

# Print contract-ready Foundry/cast env vars for demo receipts
foundry-env:
    @uv run riskguard foundry-env

# Sign demo receipts with an EVM key loaded from RISKGUARD_SIGNER_PRIVATE_KEY
sign-demo:
    : "${RISKGUARD_SIGNER_PRIVATE_KEY:?Set RISKGUARD_SIGNER_PRIVATE_KEY}"
    uv run riskguard sign --receipt examples/evidence/safe-receipt.json --out examples/evidence/safe-signed-receipt.json
    uv run riskguard sign --receipt examples/evidence/unsafe-receipt.json --out examples/evidence/unsafe-signed-receipt.json

# Verify demo signed receipts against their preimages
verify-demo:
    uv run riskguard verify --receipt examples/evidence/safe-signed-receipt.json --evidence examples/evidence/safe-evidence.json --simulation examples/evidence/safe-simulation.json --expected-signer 0xDC4814F2BC829880073D2B64355c518Fc7648Cda
    uv run riskguard verify --receipt examples/evidence/unsafe-signed-receipt.json --evidence examples/evidence/unsafe-evidence.json --simulation examples/evidence/unsafe-simulation.json --expected-signer 0xDC4814F2BC829880073D2B64355c518Fc7648Cda

# Compile the receipt registry without writing Foundry output into the repo
forge-build:
    forge build --contracts contracts --out /tmp/riskguard-forge-out --cache-path /tmp/riskguard-forge-cache

# Run receipt registry Solidity tests
forge-test:
    forge test --contracts contracts --out /tmp/riskguard-forge-out --cache-path /tmp/riskguard-forge-cache

# Run local Anvil deploy + two receipt transactions
local-e2e:
    bash scripts/local-e2e.sh

# Deploy and record both receipts on BSC testnet after faucet funding
submit-testnet:
    bash scripts/submit-testnet.sh

# Wait for faucet funding, then deploy and record both receipts
wait-submit-testnet:
    bash scripts/wait-submit-testnet.sh

# Check BSC testnet chain id
testnet-chain:
    cast chain-id --rpc-url "{{bnb_rpc}}"

# Check disposable deployer balance
testnet-balance:
    : "${DEPLOYER_ADDRESS:?Set DEPLOYER_ADDRESS}"
    cast balance "$DEPLOYER_ADDRESS" --ether --rpc-url "{{bnb_rpc}}"

# Deploy with a disposable BSC testnet key only. Never use funded/mainnet keys.
deploy-registry:
    : "${DEPLOYER_PRIVATE_KEY:?Set DEPLOYER_PRIVATE_KEY}"
    forge create contracts/PolicyReceiptRegistry.sol:PolicyReceiptRegistry \
      --rpc-url "{{bnb_rpc}}" \
      --private-key "$DEPLOYER_PRIVATE_KEY" \
      --legacy \
      --out /tmp/riskguard-forge-out \
      --cache-path /tmp/riskguard-forge-cache

# Record the safe allow receipt with a disposable BSC testnet key only
record-allow:
    : "${DEPLOYER_PRIVATE_KEY:?Set DEPLOYER_PRIVATE_KEY}"
    : "${POLICY_RECEIPT_REGISTRY_ADDRESS:?Set POLICY_RECEIPT_REGISTRY_ADDRESS}"
    eval "$(uv run riskguard foundry-env)"
    cast send "$POLICY_RECEIPT_REGISTRY_ADDRESS" \
      "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
      "$AGENT_ID" "$SAFE_PROPOSAL_HASH" "$POLICY_HASH" \
      "$SAFE_SIMULATION_HASH" "$SAFE_EVIDENCE_HASH" "$SAFE_DECISION" \
      --rpc-url "{{bnb_rpc}}" \
      --private-key "$DEPLOYER_PRIVATE_KEY" \
      --legacy

# Record the unsafe block receipt with a disposable BSC testnet key only
record-block:
    : "${DEPLOYER_PRIVATE_KEY:?Set DEPLOYER_PRIVATE_KEY}"
    : "${POLICY_RECEIPT_REGISTRY_ADDRESS:?Set POLICY_RECEIPT_REGISTRY_ADDRESS}"
    eval "$(uv run riskguard foundry-env)"
    cast send "$POLICY_RECEIPT_REGISTRY_ADDRESS" \
      "recordReceipt(bytes32,bytes32,bytes32,bytes32,bytes32,uint8)" \
      "$AGENT_ID" "$BLOCK_PROPOSAL_HASH" "$POLICY_HASH" \
      "$BLOCK_SIMULATION_HASH" "$BLOCK_EVIDENCE_HASH" "$BLOCK_DECISION" \
      --rpc-url "{{bnb_rpc}}" \
      --private-key "$DEPLOYER_PRIVATE_KEY" \
      --legacy

# Verify receipt count on BSC testnet
receipt-count:
    : "${POLICY_RECEIPT_REGISTRY_ADDRESS:?Set POLICY_RECEIPT_REGISTRY_ADDRESS}"
    cast call "$POLICY_RECEIPT_REGISTRY_ADDRESS" "receiptCount()(uint256)" --rpc-url "{{bnb_rpc}}"

# Verify the deployed registry source on BscScan testnet
verify-bscscan:
    : "${ETHERSCAN_API_KEY:?Set ETHERSCAN_API_KEY}"
    forge verify-contract \
      "{{registry}}" \
      contracts/PolicyReceiptRegistry.sol:PolicyReceiptRegistry \
      --chain 97 \
      --compiler-version 0.8.34 \
      --evm-version prague \
      --verifier etherscan \
      --watch

# Format code
format:
    uv run ruff format src/ tests/
    uv run ruff check --fix src/ tests/

# Check code
check:
    uv run ruff check src/ tests/

# Run tests
test:
    uv run python -m pytest -q

# Build package
build:
    uv build

# Refresh lockfile
lock:
    uv lock

# Remove generated Python caches
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    rm -rf .pytest_cache .ruff_cache dist build *.egg-info

# Run local quality checks
ci: check test build

# Run all Python, Solidity and local EVM checks
full-ci: ci forge-test local-e2e
