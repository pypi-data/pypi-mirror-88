# ff-containers-sort

[![PyPi Package](https://img.shields.io/pypi/v/ff-containers-sort.svg)](https://pypi.org/project/ff-containers-sort/)

## Requirements

* Python 3.6+

## Overview

**ff-containers-sort** sorts and re-numbers Firefox Containers config objects in the Firefox containers.json config file

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
ff-containers-sort [--no-sort] [--manual]
```

## Changelog

See [CHANGELOG.md](https://github.com/naamancampbell/ff-containers-sort/blob/main/CHANGELOG.md)

## License

See [LICENSE](https://github.com/naamancampbell/ff-containers-sort/blob/main/LICENSE)