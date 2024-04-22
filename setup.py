from setuptools import setup, find_packages

setup(
    name="fmd5sum",
    version="0.1.0",
    description="A faster MD5 sum calculator that uses concurrency.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fmd5sum = fmd5sum.fmd5sum:main',
        ],
    },
    install_requires=[
        'concurrent-futures; python_version < "3.2"',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
