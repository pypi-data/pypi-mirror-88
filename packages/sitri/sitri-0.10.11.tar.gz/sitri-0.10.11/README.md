
<p align="center">
  <a href="https://github.com/lemegetonx/sitri">
    <img src="docs/_static/logo.gif">
  </a>
  <h1 align="center">
    Sitri Configuration Library
  </h1>
</p>

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FLemegetonX%2Fsitri%2Fbadge&style=popout)](https://actions-badge.atrox.dev/LemegetonX/sitri/goto)
[![codecov](https://codecov.io/gh/LemegetonX/sitri/branch/master/graph/badge.svg)](https://codecov.io/gh/LemegetonX/sitri)
![PyPI](https://img.shields.io/pypi/v/sitri)
![Read the Docs](https://img.shields.io/readthedocs/sitri)
[![CodeFactor](https://www.codefactor.io/repository/github/lemegetonx/sitri/badge)](https://www.codefactor.io/repository/github/lemegetonx/sitri) [![Join the chat at https://gitter.im/lemegetonx/sitri](https://badges.gitter.im/lemegetonx/sitri.svg)](https://gitter.im/lemegetonx/sitri?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Sitri - library for managing authorization and configuration data from a single object with possibly different or identical providers

#  Installation

```bash
poetry add sitri
```

or
```bash
pip3 install sitri
```

# Basics with SystemProvider

```python
from sitri.providers.contrib import SystemConfigProvider
from sitri import Sitri

conf = Sitri(
    config_provider=SystemConfigProvider(prefix="basics"),
)
```
System provider use system environment for get config data. For unique - sitri lookup to "namespace" by prefix.

Example:

*In console:*
```bash
export BASICS_NAME=Huey
```

*In code:*
```python
name = conf.get_config("name")

print(name)  # output: Huey
```

#  Docs
Read base API references and other part documentation on https://sitri.readthedocs.io/
