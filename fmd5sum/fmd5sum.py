import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    try:
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
    except IOError:
        return None
    return hash.hexdigest()

def main(files):
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(md5sum, file): file for file in files}
        for future in as_completed(futures):
            file = futures[future]
            md5 = future.result()
            if md5 is not None:
                print(f"{md5}  {file}")
            else:
                print(f"Failed to process file: {file}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("Usage: python fmd5sum.py <file1> <file2> ...", file=sys.stderr)
