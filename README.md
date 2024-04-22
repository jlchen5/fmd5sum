# fmd5sum

This script will use Python’s hashlib library, which provides the MD5 functionality, and try to optimize the file reading and hashing process using buffers and possibly concurrency.

## How It Works
- Hash Function: Uses hashlib.md5() to create a new MD5 hash object.
- File Reading: Reads the file in chunks (specified by blocksize) to handle large files efficiently.
- Concurrency: Utilizes ThreadPoolExecutor from Python's concurrent.futures module to hash multiple files in parallel, which can significantly speed up the process when dealing with multiple files on multi-core processors.
- Error Handling: Gracefully handles errors such as missing files or read permissions.

## Install
This package can download by `pip` conmmand.

```bash
$ pip install fmd5sum
```

## Usage
You would run this script from the command line, providing the files you wish to hash as arguments. For example:

```bash
$ python fmd5sum.py file1.txt file2.txt
```

This command will print the MD5 hashes of `file1.txt` and `file2.txt`.

## Notes
- Performance: While this script adds concurrency, its performance benefit will primarily be seen when processing multiple files due to the overhead of starting Python and loading libraries. The read operation's optimization (by using a large block size) also helps with very large files.    Installation: Make sure you have Python installed on your system to use this script. Most Linux systems have Python installed by default.
- Limitations: For single, especially smaller, files, the original md5sum might still outperform this script due to the overhead of Python.
