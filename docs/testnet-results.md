# BNB testnet results

Date: 2026-06-02T16:11:46+02:00

## Network

- Chain: BSC testnet
- Chain id: 97
- RPC: https://data-seed-prebsc-1-s1.bnbchain.org:8545

## Deployer

- Address: 0xd1ef957f7f5091D9c0341eCAB24Db5E1dA006B92
- Starting balance: 0.300000000000000000 tBNB

## Contract

- PolicyReceiptRegistry: 0x10932358609f911B5cA1a131298C91a327ACAdC1
- Deploy tx: 0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd

## Receipt transactions

- Allow receipt tx: 0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
- Block receipt tx: 0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd
- Receipt count: 2

Verification command:

```bash
cast call 0x10932358609f911B5cA1a131298C91a327ACAdC1 \
  "receiptCount()(uint256)" \
  --rpc-url https://data-seed-prebsc-1-s1.bnbchain.org:8545
```

Observed output:

```text
2
```

## Explorer

- Contract: https://testnet.bscscan.com/address/0x10932358609f911B5cA1a131298C91a327ACAdC1
- Deploy tx: https://testnet.bscscan.com/tx/0xbd47d87313653322da71522637fbe8aa296477ed603cb0d7eed8f69464c8c5cd
- Allow tx: https://testnet.bscscan.com/tx/0x4d14e3b02ff6bbb66a43340237bbf0aad1ad3413865925554bf7f16bddf5cfd5
- Block tx: https://testnet.bscscan.com/tx/0xb36948eb76e13f02210c163441eeb456133dbb96dfeb7289789a27c5be772cbd
