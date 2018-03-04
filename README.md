# HashCheck

Simple tool to check one or more (up to 100) hashes against the [Hashes.org API](https://hashes.org/).

## Usage

usage: ``hashcheck.py [-h] [-s HASH] [-f FILE] [-c COMMASEP] -k KEY``
You must include your API key with the ``-k`` option.

### Requirements

* requests
* argparse
* json