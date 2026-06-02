from __future__ import annotations

import json
from pathlib import Path

from riskguard_adapter import __version__
from riskguard_adapter.cli import main

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "examples" / "policies" / "default-policy.json"
SAFE_PLAN_PATH = ROOT / "examples" / "plans" / "safe-action.json"
UNSAFE_PLAN_PATH = ROOT / "examples" / "plans" / "unsafe-action.json"


def test_version_exists() -> None:
    assert __version__


def test_validate_outputs_allow_receipt(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "riskguard",
            "validate",
            "--policy",
            str(POLICY_PATH),
            "--plan",
            str(SAFE_PLAN_PATH),
        ],
    )

    main()

    output = json.loads(capsys.readouterr().out)
    assert output["decision"] == "allow"
    assert output["reason"] == "plan satisfies policy"


def test_validate_outputs_block_receipt(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "riskguard",
            "validate",
            "--policy",
            str(POLICY_PATH),
            "--plan",
            str(UNSAFE_PLAN_PATH),
        ],
    )

    main()

    output = json.loads(capsys.readouterr().out)
    assert output["decision"] == "block"
    assert output["reason"] == "slippage 500 bps exceeds max 100 bps"


def test_demo_outputs_safe_and_unsafe_runs(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["riskguard", "demo"])

    main()

    output = json.loads(capsys.readouterr().out)
    assert [run["label"] for run in output["runs"]] == ["safe", "unsafe"]
    assert output["runs"][0]["receipt"]["decision"] == "allow"
    assert output["runs"][1]["receipt"]["decision"] == "block"


def test_demo_writes_evidence_dir(monkeypatch, capsys, tmp_path) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["riskguard", "demo", "--evidence-dir", str(tmp_path)],
    )

    main()

    json.loads(capsys.readouterr().out)
    assert (tmp_path / "safe-receipt.json").exists()
    assert (tmp_path / "unsafe-receipt.json").exists()
    assert (tmp_path / "safe-evidence.json").exists()
    assert (tmp_path / "unsafe-simulation.json").exists()


def test_foundry_env_outputs_export_lines(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["riskguard", "foundry-env"])

    main()

    output = capsys.readouterr().out
    assert 'export SAFE_DECISION="0"' in output
    assert 'export BLOCK_DECISION="1"' in output
    assert 'export SAFE_PROPOSAL_HASH="0x' in output


def test_manifest_outputs_erc8183_payload(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "riskguard",
            "manifest",
            "--receipt",
            str(ROOT / "examples" / "evidence" / "safe-receipt.json"),
            "--job-id",
            "42",
            "--chain-id",
            "97",
            "--registry-address",
            "0x10932358609f911B5cA1a131298C91a327ACAdC1",
        ],
    )

    main()

    output = json.loads(capsys.readouterr().out)
    assert output["manifest_hash"].startswith("0x")
    assert output["manifest"]["job_id"] == 42
    assert output["manifest"]["metadata"]["riskguard_decision"] == "allow"
    assert (
        output["manifest"]["metadata"]["riskguard_integration_mode"]
        == "manifest-only"
    )


def test_sign_outputs_signed_receipt(monkeypatch, capsys) -> None:
    monkeypatch.setenv(
        "RISKGUARD_SIGNER_PRIVATE_KEY",
        "0x59c6995e998f97a5a0044966f094538eac1d6085a257075d4c8c5fcadf1bd0eb",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "riskguard",
            "sign",
            "--receipt",
            str(ROOT / "examples" / "evidence" / "safe-receipt.json"),
        ],
    )

    main()

    output = json.loads(capsys.readouterr().out)
    assert output["signature"].startswith("0x")
    assert output["signer"] == "0xDC4814F2BC829880073D2B64355c518Fc7648Cda"


def test_verify_outputs_valid_for_signed_receipt_bundle(
    monkeypatch,
    capsys,
    tmp_path,
) -> None:
    monkeypatch.setenv(
        "RISKGUARD_SIGNER_PRIVATE_KEY",
        "0x59c6995e998f97a5a0044966f094538eac1d6085a257075d4c8c5fcadf1bd0eb",
    )
    signed_receipt = tmp_path / "signed-safe-receipt.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "riskguard",
            "sign",
            "--receipt",
            str(ROOT / "examples" / "evidence" / "safe-receipt.json"),
            "--out",
            str(signed_receipt),
        ],
    )
    main()
    capsys.readouterr()

    monkeypatch.setattr(
        "sys.argv",
        [
            "riskguard",
            "verify",
            "--receipt",
            str(signed_receipt),
            "--evidence",
            str(ROOT / "examples" / "evidence" / "safe-evidence.json"),
            "--simulation",
            str(ROOT / "examples" / "evidence" / "safe-simulation.json"),
        ],
    )

    main()

    output = json.loads(capsys.readouterr().out)
    assert output["valid"] is True
    assert output["checks"]["signature"] == "ok"
