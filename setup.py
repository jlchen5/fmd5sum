from setuptools import setup, find_packages

setup(
    name='fmd5sum',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A fast MD5 checksum calculator using concurrency.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jlchen5/fmd5sum',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fmd5sum=fmd5sum.fmd5sum:main',
        ],
    },
    install_requires=[
        'concurrent-futures; python_version < "3.2"'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
