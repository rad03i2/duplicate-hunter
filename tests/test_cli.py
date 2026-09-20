import json
from pathlib import Path

from duplicate_hunter.cli import main


def test_quarantine_is_preview_by_default(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_text("duplicate")
    (source / "b.txt").write_text("duplicate")
    quarantine = tmp_path / "quarantine"
    assert main([str(source), "--quarantine", str(quarantine)]) == 0
    assert (source / "a.txt").exists() and (source / "b.txt").exists()
    assert not quarantine.exists()


def test_apply_quarantine_keeps_one_and_writes_manifest(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_text("duplicate")
    (source / "b.txt").write_text("duplicate")
    quarantine = tmp_path / "quarantine"
    assert main([str(source), "--quarantine", str(quarantine), "--apply"]) == 0
    remaining = list(source.glob("*.txt"))
    assert len(remaining) == 1
    manifest = json.loads((quarantine / "duplicate-hunter-manifest.json").read_text())
    assert len(manifest) == 1
    assert Path(manifest[0]["destination"]).exists()


def test_json_report(tmp_path: Path):
    (tmp_path / "a").write_bytes(b"x")
    (tmp_path / "b").write_bytes(b"x")
    report = tmp_path / "report.json"
    assert main([str(tmp_path), "--json", str(report)]) == 0
    data = json.loads(report.read_text())
    assert data["recoverable_bytes"] == 1
    assert len(data["groups"]) == 1
