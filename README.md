# fmd5sum

This script will use Python’s hashlib library, which provides the MD5 functionality, and try to optimize the file reading and hashing process using buffers and possibly concurrency.

## How It Works
- Hash Function: Uses hashlib.md5() to create a new MD5 hash object.
- File Reading: Reads the file in chunks (specified by blocksize) to handle large files efficiently.
- Concurrency: Utilizes ThreadPoolExecutor from Python's concurrent.futures module to hash multiple files in parallel, which can significantly speed up the process when dealing with multiple files on multi-core processors.
- Error Handling: Gracefully handles errors such as missing files or read permissions.

## Install fmd5sum
- Using pip

```bash
$ pip install fmd5sum
```

## Usage
After installation, you can use fmd5sum directly from the command line to calculate MD5 hashes of files.

### Using fmd5sum from the Command Line
```bash
$ python fmd5sum.py file1.txt file2.img

$ python fmd5sum.py -j 8 -b 1048576 largefile.iso

$ python fmd5sum.py *
```



### Using fmd5sum as a Python Module
If you prefer to use fmd5sum within a Python script, here’s how you can do it:
```python
from fmd5sum.fmd5sum import md5sum

# Example usage of the md5sum function
file_path = 'example.txt'
hash_result = md5sum(file_path)
print(f"The MD5 sum of {file_path} is {hash_result}")
```

This script imports the md5sum function from the fmd5sum module and uses it to calculate the MD5 hash of example.txt.

### Advanced Usage - Handling Multiple Files
If you want to handle multiple files within a script and utilize the concurrent processing, you could extend the module's functionality like this:
```python
from fmd5sum.fmd5sum import md5sum, main
import sys

# Function to process multiple files
def process_files(files):
    for file in files:
        print(f"{md5sum(file)}  {file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_files(sys.argv[1:])
    else:
        print("Usage: python -m fmd5sum <file1> <file2> ...", file=sys.stderr)

```
This script allows the fmd5sum module to be used as a standalone script or imported module that processes multiple files given as command line arguments.

### Summary of Functions
- `md5sum(filename, blocksize=65536)`: Computes the MD5 hash for a given filename with an optional blocksize parameter.
- `main()`: Entry point for the command line utility (if you have implemented it to handle command line arguments).

### Error handling
Implement error handling in your scripts and functions to manage situations like file not found errors, permission errors, and others that may occur during file operations.

```python
try:
    hash_result = md5sum(file_path)
    print(f"The MD5 sum of {file_path} is {hash_result}")
except IOError as e:
    print(f"Error processing file {file_path}: {str(e)}")
```

Using these instructions, you can effectively use `fmd5sum` to calculate MD5 checksums, either through the command line interface or within other Python scripts, leveraging its concurrency features for better performance with multiple files.

## Notes
- Performance: While this script adds concurrency, its performance benefit will primarily be seen when processing multiple files due to the overhead of starting Python and loading libraries. The read operation's optimization (by using a large block size) also helps with very large files.    Installation: Make sure you have Python installed on your system to use this script. Most Linux systems have Python installed by default.
- Limitations: For single, especially smaller, files, the original md5sum might still outperform this script due to the overhead of Python.


## License

This project is licensed under the [MIT License](https://github.com/jlchen5/fmd5sum/blob/main/LICENSE).
