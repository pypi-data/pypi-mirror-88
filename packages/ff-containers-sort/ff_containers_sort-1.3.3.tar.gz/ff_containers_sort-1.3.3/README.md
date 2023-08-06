# ff_containers_sort

[![PyPi Package](https://img.shields.io/pypi/v/ff_containers_sort.svg)](https://pypi.org/project/ff_containers_sort/)

## Requirements

* Python 3.6+

## Installation

Install with [pip](https://packaging.python.org/tutorials/installing-packages/):
```bash
pip install ff_containers_sort
```

## Overview

**ff_containers_sort** sorts and re-numbers Firefox Container config objects in the Firefox containers.json config file.

### Features

* alphabetical sorting of containers
* manual sorting mode
* safely updates containers.json after manual changes
* preserves Firefox private container objects
* creates backups of Firefox Container config prior to making changes
    * deletes backups older than 7 days
* tested on Linux, Windows & Mac

## Usage

```bash
python ff_containers_sort.py [--no-sort] [--manual]
```

## Changelog

See [CHANGELOG.md](https://github.com/naamancampbell/ff_containers_sort/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/naamancampbell/ff_containers_sort/blob/master/LICENSE)