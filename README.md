# fmd5sum

`fmd5sum` is a small, cross-platform command-line tool and Python library for
calculating standard MD5 checksums. It processes multiple files concurrently,
keeps output in input order, and returns a non-zero exit status if any file
cannot be read.

> [!WARNING]
> MD5 is not collision resistant. Use this tool for compatibility and
> non-adversarial file integrity checks, not for passwords, signatures, or
> security-sensitive verification.

## Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux
- No runtime dependencies outside the Python standard library

## Installation

### Install the command with pipx

This is the recommended option for end users because it keeps the command in
an isolated environment:

```bash
pipx install fmd5sum
fmd5sum --help
```

### Install with pip

```bash
python -m pip install fmd5sum
```

### Install from source

Clone the repository, create a virtual environment, and install the project.

Windows PowerShell:

```powershell
git clone https://github.com/jlchen5/fmd5sum.git
cd fmd5sum
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
```

macOS or Linux:

```bash
git clone https://github.com/jlchen5/fmd5sum.git
cd fmd5sum
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

### Install with Conda

```bash
conda env create -f environment.yml
conda activate fmd5sum-env
```

## Usage

Calculate one or more checksums:

```bash
fmd5sum file1.txt file2.img
```

Wildcard patterns are expanded by `fmd5sum`, including on Windows shells that
do not expand them. Quote the pattern to get consistent behavior:

```bash
fmd5sum "images/*.jpg" "images/*.png"
```

Choose the worker count and read block size:

```bash
fmd5sum --workers 4 --blocksize 1048576 file1.iso file2.iso
```

The package can also be run without installing its console script:

```bash
python -m fmd5sum file1.txt file2.img
```

Run `fmd5sum --help` for all options. A successful run returns exit code `0`.
If one or more files cannot be processed, valid checksums are still printed and
the command returns exit code `1`. Invalid arguments return exit code `2`.

## Python API

```python
from fmd5sum import md5sum, process_files

checksum = md5sum("path/to/file.ext")
status = process_files(["file1.txt", "file2.img"], max_workers=4)
```

`md5sum()` returns `None` and reports an error to stderr when the file cannot
be read. It raises `ValueError` when `blocksize` is not positive.
`process_files()` returns a command-style status code: `0` for success and `1`
when at least one file failed.

## Performance

Concurrency is applied across independent files. A single file is read by one
worker because standard MD5 has a sequential chaining dependency. The default
worker count is capped at eight and never exceeds the number of input files or
available CPUs. Use `--workers` to tune throughput for the storage device.

Thread-based workers avoid multiprocessing startup and serialization overhead,
especially on Windows and macOS. Actual throughput depends mainly on storage,
file sizes, cache state, and the number of independent devices. Benchmark with
representative data before increasing concurrency.

## Development and packaging

Install development dependencies and run the tests:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Build a platform-independent wheel and source archive:

```bash
python -m build
```

The artifacts are written to `dist/`. The generated `py3-none-any` wheel can be
installed on Windows, macOS, and Linux with a supported Python version.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
