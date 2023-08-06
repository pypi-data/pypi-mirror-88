# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sitri',
 'sitri.providers',
 'sitri.providers.base',
 'sitri.providers.contrib',
 'sitri.providers.contrib.vault',
 'sitri.settings',
 'sitri.settings.contrib',
 'sitri.settings.contrib.vault',
 'sitri.strategy']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0', 'pydantic>=1.7.3,<2.0.0', 'pytest_cases>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'sitri',
    'version': '0.10.22',
    'description': 'Library for one endpoint config managment',
    'long_description': '\n<p align="center">\n  <a href="https://github.com/elastoo-team/sitri">\n    <img src="docs/_static/logo.gif">\n  </a>\n  <h1 align="center">\n    Sitri Configuration Library\n  </h1>\n</p>\n\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FElastoo-Team%2Fsitri%2Fbadge&style=popout)](https://actions-badge.atrox.dev/Elastoo-Team/sitri/goto)\n[![codecov](https://codecov.io/gh/Elastoo-Team/sitri/branch/master/graph/badge.svg)](https://codecov.io/gh/elastoo-team/sitri)\n![PyPI](https://img.shields.io/pypi/v/sitri)\n![Read the Docs](https://img.shields.io/readthedocs/sitri)\n[![CodeFactor](https://www.codefactor.io/repository/github/elastoo-team/sitri/badge)](https://www.codefactor.io/repository/github/elastoo-team/sitri)\n\nSitri - library for managing authorization and configuration data from a single object with possibly different or identical providers\n\n#  Installation\n\n```bash\npoetry add sitri\n```\n\nor\n```bash\npip3 install sitri\n```\n\n# Basics with SystemProvider\n\n```python\nfrom sitri.providers.contrib import SystemConfigProvider\nfrom sitri import Sitri\n\nconf = Sitri(\n    config_provider=SystemConfigProvider(prefix="basics"),\n)\n```\nSystem provider use system environment for get config data. For unique - sitri lookup to "namespace" by prefix.\n\nExample:\n\n*In console:*\n```bash\nexport BASICS_NAME=Huey\n```\n\n*In code:*\n```python\nname = conf.get_config("name")\n\nprint(name)  # output: Huey\n```\n\n#  Docs\nRead base API references and other part documentation on https://sitri.readthedocs.io/\n',
    'author': 'Alexander Lavrov',
    'author_email': 'egnod@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Egnod/sitri',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
