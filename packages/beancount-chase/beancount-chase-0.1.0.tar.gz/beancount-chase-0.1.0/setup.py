# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_chase']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.3,<3.0.0']

setup_kwargs = {
    'name': 'beancount-chase',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Beancount Caisse d'Epargne Importer\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ArthurFDLR/beancount-chase/beancount-chase)](https://github.com/ArthurFDLR/beancount-chase/actions)\n[![PyPI](https://img.shields.io/pypi/v/beancount-chase)](https://pypi.org/project/beancount-chase/)\n[![PyPI - Version](https://img.shields.io/pypi/pyversions/beancount-chase.svg)](https://pypi.org/project/beancount-chase/)\n[![GitHub](https://img.shields.io/github/license/ArthurFDLR/beancount-chase)](https://github.com/ArthurFDLR/beancount-chase/blob/master/LICENSE.txt)\n[![Linting](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`beancount-chase` is a [Beancount](http://furius.ca/beancount/) importer for [Chase Bank](https://www.chase.com/) CSV statements.\n\n## Installation\n\n```console\n    $ pip install beancount-chase\n```\n\n## Usage\n\n```python\n    CONFIG = [\n        ChaseImporter(\n            account='Assets:US:CB:Checking',\n            expenseCat='Expenses:FIXME',    #Optional\n            creditCat='Income:FIXME',       #Optional\n        ),\n    ]\n```\n\n## Contribution\n\nFeel free to contribute!\n\nPlease make sure you have Python 3.6+ and [`Poetry`](https://poetry.eustace.io/) installed.\n\n1. Git clone the repository - `git clone https://github.com/ArthurFDLR/beancount-chase`\n\n2. Install the packages required for development - `poetry install`\n\n3. That's basically it. You should now be able to run lint checks and the test suite - `make lint test`.\n",
    'author': 'Arthur Findelair',
    'author_email': 'arthfind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArthurFDLR/beancount-chase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
