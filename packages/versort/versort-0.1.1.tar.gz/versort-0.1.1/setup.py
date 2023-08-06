# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versort', 'versort.sorters']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.7,<21.0', 'plumbum>=1.6.9,<2.0.0', 'semver>=2.13.0,<3.0.0']

extras_require = \
{'docs': ['mkdocstrings>=0.13.6,<0.14.0', 'mkdocs-material>=6.1.7,<7.0.0']}

entry_points = \
{'console_scripts': ['versort = versort.cli:VerSortApp.run']}

setup_kwargs = {
    'name': 'versort',
    'version': '0.1.1',
    'description': 'Sort versions according to different versioning schemas',
    'long_description': '# VerSort\n\n![License](https://img.shields.io/github/license/Tecnativa/versort)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/versort)\n![PyPI](https://img.shields.io/pypi/v/versort)\n![CI](https://github.com/Tecnativa/versort/workflows/CI/badge.svg)\n[![codecov](https://codecov.io/gh/Tecnativa/versort/branch/master/graph/badge.svg?token=1gDyBgOuPr)](https://codecov.io/gh/Tecnativa/versort)\n\nSort versions according to different versioning schemas.\n\n## Install\n\nTo use as a CLI app:\n\n```sh\npipx install versort\n```\n\nTo use as a library:\n\n```sh\npip install versort\n```\n\n## Usage\n\n### Supported version algorithms\n\n-   [PEP440](https://www.python.org/dev/peps/pep-0440/)\n-   [SemVer](https://semver.org/)\n\n### As a library\n\n```python\nfrom versort import get_sorter\n\nsorter = get_sorter("pep440")()\nprint(sorter.sort("v1", "2a1", "2"))\n```\n\n### CLI\n\nYou can call `versort` directly, or as a Python module with `python -m versort`.\n\n```sh\n➤ echo 2 2a1 v1 | versort --stdin pep440\nv1\n2a1\n2\n\n➤ versort --reverse pep440 2 2a1 v1\n2\n2a1\nv1\n\n➤ versort --first pep440 2 2a1 v1\nv1\n\n➤ python -m versort --reverse --first pep440 2 2a1 v1\n2\n```\n',
    'author': 'Jairo Llopis',
    'author_email': 'jairo.llopis@tecnativa.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://versort.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
