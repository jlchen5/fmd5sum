import hashlib

import pytest

from fmd5sum import md5sum, process_files
from fmd5sum.fmd5sum import main


def expected_md5(content):
    return hashlib.md5(content, usedforsecurity=False).hexdigest()


@pytest.mark.parametrize("blocksize", [1, 64 * 1024, 512 * 1024])
def test_md5sum_correctness_for_different_block_sizes(tmp_path, blocksize):
    content = b"Test content for MD5 calculation"
    test_file = tmp_path / "input.bin"
    test_file.write_bytes(content)

    assert md5sum(test_file, blocksize=blocksize) == expected_md5(content)


def test_md5sum_large_binary_file(tmp_path):
    data = bytes(range(256)) * 20_480
    test_file = tmp_path / "large.bin"
    test_file.write_bytes(data)

    assert md5sum(test_file) == expected_md5(data)


def test_md5sum_empty_file(tmp_path):
    test_file = tmp_path / "empty.bin"
    test_file.touch()

    assert md5sum(test_file) == expected_md5(b"")


@pytest.mark.parametrize("blocksize", [0, -1])
def test_md5sum_rejects_non_positive_blocksize(tmp_path, blocksize):
    test_file = tmp_path / "input.bin"
    test_file.write_bytes(b"not empty")

    with pytest.raises(ValueError, match="greater than zero"):
        md5sum(test_file, blocksize=blocksize)


def test_md5sum_nonexistent_file_returns_none(tmp_path, capsys):
    missing_file = tmp_path / "missing.bin"

    assert md5sum(missing_file) is None
    assert "Error processing" in capsys.readouterr().err


def test_process_files_preserves_input_order(tmp_path, capsys):
    files = []
    for index in range(3):
        test_file = tmp_path / f"{index}.txt"
        test_file.write_text(f"file {index}", encoding="utf-8")
        files.append(test_file)

    assert process_files(files, max_workers=2) == 0

    output_files = [line.split("  ", 1)[1] for line in capsys.readouterr().out.splitlines()]
    assert output_files == [str(path) for path in files]


def test_process_files_returns_failure_if_any_file_fails(tmp_path, capsys):
    valid_file = tmp_path / "valid.txt"
    valid_file.write_text("content", encoding="utf-8")
    missing_file = tmp_path / "missing.txt"

    assert process_files([valid_file, missing_file], max_workers=2) == 1

    captured = capsys.readouterr()
    assert str(valid_file) in captured.out
    assert captured.err.count("Error processing") == 1


def test_process_files_validates_arguments():
    assert process_files([]) == 0

    with pytest.raises(ValueError, match="blocksize"):
        process_files([], blocksize=0)
    with pytest.raises(ValueError, match="max_workers"):
        process_files([], max_workers=0)


def test_main_expands_wildcards(tmp_path, capsys):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"
    first_file.write_text("first", encoding="utf-8")
    second_file.write_text("second", encoding="utf-8")

    assert main(["--workers", "1", "--blocksize", "1", str(tmp_path / "*.txt")]) == 0

    output = capsys.readouterr().out
    assert str(first_file) in output
    assert str(second_file) in output


@pytest.mark.parametrize(
    ("option", "value"),
    [("--blocksize", "0"), ("--workers", "0"), ("--workers", "invalid")],
)
def test_main_rejects_invalid_options(tmp_path, option, value):
    test_file = tmp_path / "input.bin"
    test_file.write_bytes(b"not empty")

    with pytest.raises(SystemExit) as exc_info:
        main([option, value, str(test_file)])

    assert exc_info.value.code == 2


def test_main_returns_failure_for_missing_file(tmp_path):
    assert main([str(tmp_path / "missing.bin")]) == 1


def test_package_module_exposes_main():
    from fmd5sum import __main__ as package_main

    assert package_main.main is main
