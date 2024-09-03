import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def md5sum(filename, blocksize=65536):
    """
    Calculate the MD5 checksum of a file.

    :param filename: Path to the file.
    :param blocksize: Block size to read the file in chunks.
    :return: MD5 checksum as a hexadecimal string or None if an error occurs.
    """
    hash = hashlib.md5()
    try:
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
    except (IOError, OSError) as e:
        print(f"Error processing file {filename}: {e}", file=sys.stderr)
        return None
    return hash.hexdigest()

def process_files(files, max_workers=10):
    """
    Process a list of files to calculate their MD5 checksums concurrently.

    :param files: List of file paths.
    :param max_workers: Maximum number of threads to use.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(md5sum, file): file for file in files}
        for future in as_completed(futures):
            file = futures[future]
            try:
                md5 = future.result()
                if md5:
                    print(f"{md5}  {file}")
                else:
                    print(f"Failed to process file: {file}", file=sys.stderr)
            except Exception as e:
                print(f"Error processing file {file}: {e}", file=sys.stderr)

def main():
    """
    Main entry point for the script.
    """
    if len(sys.argv) > 1:
        process_files(sys.argv[1:])
    else:
        print("Usage: python fmd5sum.py <file1> <file2> ...", file=sys.stderr)

if __name__ == "__main__":
    main()
