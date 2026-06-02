// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./PolicyReceiptRegistry.sol";

contract PolicyReceiptRegistryTest {
    PolicyReceiptRegistry private registry;

    bytes32 private constant AGENT_ID = keccak256("riskguard:demo-agent");
    bytes32 private constant POLICY_HASH = keccak256("riskguard:policy");
    bytes32 private constant SAFE_PROPOSAL_HASH = keccak256("riskguard:safe");
    bytes32 private constant SAFE_SIMULATION_HASH = keccak256("riskguard:safe-sim");
    bytes32 private constant SAFE_EVIDENCE_HASH = keccak256("riskguard:safe-evidence");
    bytes32 private constant BLOCK_PROPOSAL_HASH = keccak256("riskguard:block");
    bytes32 private constant BLOCK_SIMULATION_HASH = keccak256("riskguard:block-sim");
    bytes32 private constant BLOCK_EVIDENCE_HASH = keccak256("riskguard:block-evidence");

    function setUp() public {
        registry = new PolicyReceiptRegistry();
    }

    function testRecordAllowReceipt() public {
        uint256 receiptId = registry.recordReceipt(
            AGENT_ID,
            SAFE_PROPOSAL_HASH,
            POLICY_HASH,
            SAFE_SIMULATION_HASH,
            SAFE_EVIDENCE_HASH,
            PolicyReceiptRegistry.Decision.Allow
        );

        require(receiptId == 0, "first receipt id");
        require(registry.receiptCount() == 1, "receipt count");

        PolicyReceiptRegistry.Receipt memory receipt = registry.getReceipt(0);
        require(receipt.agentId == AGENT_ID, "agent id");
        require(receipt.proposalHash == SAFE_PROPOSAL_HASH, "proposal hash");
        require(receipt.policyHash == POLICY_HASH, "policy hash");
        require(receipt.simulationHash == SAFE_SIMULATION_HASH, "simulation hash");
        require(receipt.evidenceHash == SAFE_EVIDENCE_HASH, "evidence hash");
        require(
            receipt.decision == PolicyReceiptRegistry.Decision.Allow,
            "decision"
        );
    }

    function testRecordAllowAndBlockReceipts() public {
        registry.recordReceipt(
            AGENT_ID,
            SAFE_PROPOSAL_HASH,
            POLICY_HASH,
            SAFE_SIMULATION_HASH,
            SAFE_EVIDENCE_HASH,
            PolicyReceiptRegistry.Decision.Allow
        );

        uint256 receiptId = registry.recordReceipt(
            AGENT_ID,
            BLOCK_PROPOSAL_HASH,
            POLICY_HASH,
            BLOCK_SIMULATION_HASH,
            BLOCK_EVIDENCE_HASH,
            PolicyReceiptRegistry.Decision.Block
        );

        require(receiptId == 1, "second receipt id");
        require(registry.receiptCount() == 2, "receipt count");

        PolicyReceiptRegistry.Receipt memory receipt = registry.getReceipt(1);
        require(receipt.proposalHash == BLOCK_PROPOSAL_HASH, "proposal hash");
        require(
            receipt.decision == PolicyReceiptRegistry.Decision.Block,
            "decision"
        );
    }
}
