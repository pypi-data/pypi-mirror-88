# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cruft_helloworld']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cruft-helloworld',
    'version': '0.1.1',
    'description': 'Cruft Python Hello-World',
    'long_description': '# cruft_helloworld\n\n![PyPI](https://img.shields.io/pypi/v/cruft_helloworld?style=flat-square)\n![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/yoyonel/cruft_helloworld/Test%20&%20Lint/master?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/yoyonel/cruft_helloworld/master?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cruft_helloworld?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/cruft_helloworld?style=flat-square)\n\nCruft Python Hello-World\n\n## Requirements\n\n* Python 3.6.1 or newer\n* [poetry](https://poetry.eustance.io/) 1.1 or newer\n\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual enviroment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n\n### Cookiecutter template\n\nThis project was created using [cruft](https://github.com/cruft/cruft) and the\n[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.\nIn order to update this repository to the latest template version run\n\n```sh\ncruft update\n```\n\nin the root of this repository.\n\n',
    'author': 'lionel atty',
    'author_email': 'yoyonel@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yoyonel/cruft_helloworld',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
