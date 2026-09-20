from pathlib import Path

from duplicate_hunter.core import find_duplicates, human_bytes, sha256_file


def test_finds_only_identical_files(tmp_path: Path):
    (tmp_path / "a.txt").write_bytes(b"same-content")
    (tmp_path / "b.txt").write_bytes(b"same-content")
    (tmp_path / "same-size-not-same.txt").write_bytes(b"other-content")
    groups = find_duplicates([tmp_path])
    assert len(groups) == 1
    assert len(groups[0].files) == 2
    assert groups[0].wasted_bytes == len(b"same-content")


def test_min_size_and_hidden(tmp_path: Path):
    (tmp_path / "a").write_bytes(b"x")
    (tmp_path / "b").write_bytes(b"x")
    hidden = tmp_path / ".hidden"
    hidden.mkdir()
    (hidden / "c").write_bytes(b"large")
    (hidden / "d").write_bytes(b"large")
    assert find_duplicates([tmp_path], min_size=2) == []
    assert len(find_duplicates([tmp_path], min_size=2, include_hidden=True)) == 1


def test_non_recursive(tmp_path: Path):
    child = tmp_path / "child"
    child.mkdir()
    (child / "a").write_bytes(b"same")
    (child / "b").write_bytes(b"same")
    assert find_duplicates([tmp_path], recursive=False) == []
    assert len(find_duplicates([tmp_path])) == 1


def test_hash_and_human_size(tmp_path: Path):
    file = tmp_path / "x"
    file.write_bytes(b"abc")
    assert sha256_file(file) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert human_bytes(1024) == "1.0 KiB"
