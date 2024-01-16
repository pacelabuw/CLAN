import os
import pytest
from pathlib import Path
from unittest.mock import Mock

from src.utils.constants import INPUT_DIR, OUTPUT_DIR
from src.utils.setup import setup_filesystem, get_cha_files


def test_setup_filesystem_no_dirs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    expected_input_dir = tmp_path / INPUT_DIR
    expected_output_dir = tmp_path / OUTPUT_DIR
    monkeypatch.setattr(Path, "cwd", Mock(return_value=tmp_path))

    assert not expected_input_dir.exists()
    assert not expected_output_dir.exists()

    with pytest.raises(Exception):
        setup_filesystem()

    assert expected_input_dir.exists()
    assert expected_output_dir.exists()


def test_setup_filesystem_with_dirs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    expected_input_dir = tmp_path / INPUT_DIR
    expected_output_dir = tmp_path / OUTPUT_DIR
    monkeypatch.setattr(Path, "cwd", Mock(return_value=tmp_path))

    os.mkdir(expected_input_dir)
    os.mkdir(expected_output_dir)

    assert expected_input_dir.exists()
    assert expected_output_dir.exists()

    setup_filesystem()


def test_get_cha_files_no_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    os.mkdir("input")
    
    result = get_cha_files()
    assert len(result) == 0


def test_get_cha_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    files = ["f1.cha", "f2.CHA", "f3.txt", "f4.cha.csv"]
    monkeypatch.chdir(tmp_path)
    os.mkdir("input")

    for file in files:
        with open(f"input/{file}", "w") as f:
            f.write("test")

    result = get_cha_files()
    assert len(result) == 2

    for file in result:
        assert file.split(".")[-1].lower() == "cha"
