// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract PolicyReceiptRegistry {
    enum Decision {
        Allow,
        Block
    }

    struct Receipt {
        bytes32 agentId;
        bytes32 proposalHash;
        bytes32 policyHash;
        bytes32 simulationHash;
        bytes32 evidenceHash;
        Decision decision;
        uint256 timestamp;
    }

    Receipt[] private receipts;

    event PolicyReceiptRecorded(
        uint256 indexed receiptId,
        bytes32 indexed agentId,
        bytes32 proposalHash,
        bytes32 policyHash,
        bytes32 simulationHash,
        bytes32 evidenceHash,
        Decision decision
    );

    function recordReceipt(
        bytes32 agentId,
        bytes32 proposalHash,
        bytes32 policyHash,
        bytes32 simulationHash,
        bytes32 evidenceHash,
        Decision decision
    ) external returns (uint256 receiptId) {
        receiptId = receipts.length;
        receipts.push(
            Receipt({
                agentId: agentId,
                proposalHash: proposalHash,
                policyHash: policyHash,
                simulationHash: simulationHash,
                evidenceHash: evidenceHash,
                decision: decision,
                timestamp: block.timestamp
            })
        );

        emit PolicyReceiptRecorded(
            receiptId,
            agentId,
            proposalHash,
            policyHash,
            simulationHash,
            evidenceHash,
            decision
        );
    }

    function getReceipt(uint256 receiptId) external view returns (Receipt memory) {
        return receipts[receiptId];
    }

    function receiptCount() external view returns (uint256) {
        return receipts.length;
    }
}

