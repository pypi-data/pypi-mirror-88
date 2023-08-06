# os-scrapy-spage

[![Build Status](https://www.travis-ci.org/cfhamlet/os-scrapy-spage.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-scrapy-spage)
[![codecov](https://codecov.io/gh/cfhamlet/os-scrapy-spage/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-scrapy-spage)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-scrapy-spage.svg)](https://pypi.python.org/pypi/os-scrapy-spage)
[![PyPI](https://img.shields.io/pypi/v/os-scrapy-spage.svg)](https://pypi.python.org/pypi/os-scrapy-spage)


This project provide [spage](https://github.com/cfhamlet/os-spage) utilities for Scrapy.


## Install

```
pip install os-scrapy-spage
```

## Usage

```
from os_scrapy_spage.utils import spage

spage_bytes = spage(response_or_failure)
```

## Unit Tests

```
sh scripts/test.sh
```

## License

MIT licensed.
