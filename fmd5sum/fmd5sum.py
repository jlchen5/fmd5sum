import argparse
import glob
import hashlib
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import partial


DEFAULT_BLOCKSIZE = 512 * 1024
DEFAULT_MAX_WORKERS = 8


def _positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def _expand_file_arguments(files):
    """Expand wildcard arguments on shells that do not do it themselves."""
    expanded = []
    for filename in files:
        filename = os.fspath(filename)
        if glob.has_magic(filename):
            matches = glob.glob(filename, recursive=True)
            if matches:
                expanded.extend(matches)
                continue
        expanded.append(filename)
    return expanded


def md5sum(filename, blocksize=65536):
    """Return the MD5 checksum for a file, or None when it cannot be read."""
    if blocksize <= 0:
        raise ValueError("blocksize must be greater than zero")

    digest = hashlib.md5(usedforsecurity=False)
    try:
        with open(filename, "rb") as file_handle:
            while block := file_handle.read(blocksize):
                digest.update(block)
    except OSError as exc:
        print(f"Error processing {filename}: {exc}", file=sys.stderr)
        return None
    return digest.hexdigest()


def process_files(files, max_workers=None, blocksize=DEFAULT_BLOCKSIZE):
    """Print checksums for files and return a command-style exit status."""
    if blocksize <= 0:
        raise ValueError("blocksize must be greater than zero")
    if max_workers is not None and max_workers <= 0:
        raise ValueError("max_workers must be greater than zero")

    files = list(files)
    if not files:
        return 0

    if max_workers is None:
        cpu_count = os.cpu_count() or 1
        max_workers = min(len(files), cpu_count, DEFAULT_MAX_WORKERS)

    worker = partial(md5sum, blocksize=blocksize)
    failed = False
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filename, checksum in zip(files, executor.map(worker, files)):
            if checksum is None:
                failed = True
            else:
                print(f"{checksum}  {filename}")

    return 1 if failed else 0


def main(argv=None):
    """Run the command-line interface and return its exit status."""
    parser = argparse.ArgumentParser(
        prog="fmd5sum",
        description="Parallel MD5 checksum calculator for multiple files"
    )
    parser.add_argument("files", nargs="+", help="Files or wildcard patterns to process")
    parser.add_argument(
        "-j",
        "--workers",
        type=_positive_int,
        default=None,
        help=f"Number of worker threads (default: up to {DEFAULT_MAX_WORKERS})",
    )
    parser.add_argument(
        "-b",
        "--blocksize",
        type=_positive_int,
        default=DEFAULT_BLOCKSIZE,
        help="I/O block size in bytes (default: 512 KiB)",
    )
    args = parser.parse_args(argv)

    files = _expand_file_arguments(args.files)
    return process_files(files, max_workers=args.workers, blocksize=args.blocksize)


if __name__ == "__main__":
    raise SystemExit(main())
