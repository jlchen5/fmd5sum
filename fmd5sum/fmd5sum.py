import hashlib
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

def md5sum(filename, blocksize=65536):
    """Optimized MD5 checksum calculator with low-level file I/O."""
    hash_md5 = hashlib.md5()
    try:
        fd = os.open(filename, os.O_RDONLY | os.O_BINARY)
        with open(fd, "rb", closefd=True) as f:
            while True:
                block = f.read(blocksize)
                if not block:
                    break
                hash_md5.update(block)
    except (OSError, IOError) as e:
        print(f"Error processing {filename}: {e}", file=sys.stderr)
        return None
    return hash_md5.hexdigest()

def process_files(files, max_workers=None, blocksize=65536 * 8):
    """Process files using parallel execution with adaptive settings."""

    if max_workers is None:
        max_workers = os.cpu_count() or 4
    

    worker = partial(md5sum, blocksize=blocksize)
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(worker, file): file for file in files}
        
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                md5 = future.result()
                if md5:
                    print(f"{md5}  {file}")
                else:
                    print(f"Failed to process: {file}", file=sys.stderr)
            except Exception as e:
                print(f"Error processing {file}: {e}", file=sys.stderr)

def main():
    """Enhanced main function with command-line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description='Parallel MD5 checksum calculator')
    parser.add_argument('files', nargs='+', help='Files to process')
    parser.add_argument('-j', '--workers', type=int, default=None,
                        help='Number of parallel workers (default: CPU count)')
    parser.add_argument('-b', '--blocksize', type=int, default=524288,
                        help='I/O block size in bytes (default: 512KB)')
    args = parser.parse_args()

    process_files(args.files, max_workers=args.workers, blocksize=args.blocksize)

if __name__ == "__main__":
    main()
