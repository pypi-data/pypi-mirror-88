# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devinstaller_core']

package_data = \
{'': ['*']}

install_requires = \
['anymarkup>=0.8.1,<0.9.0',
 'cerberus>=1.3.2,<2.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'questionary>=1.5.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=9.2.0,<10.0.0',
 'typeguard>=2.9.1,<3.0.0']

setup_kwargs = {
    'name': 'devinstaller-core',
    'version': '0.5.7',
    'description': 'The core library for creating a Devinstaller application.',
    'long_description': '[![img](https://img.shields.io/badge/Made_in-Doom_Emacs-blue?style=for-the-badge)](https://github.com/hlissner/doom-emacs)\n[![img](https://img.shields.io/badge/follow_me-@alka1e-E4405F?style=for-the-badge&logo=instagram&labelColor=8f3c4c&logoColor=white)](https://www.instagram.com/alka1e)\n[![img](https://img.shields.io/badge/follow_me-@alka1e-1DA1F2?style=for-the-badge&logo=twitter&labelColor=27597a&logoColor=white)](https://twitter.com/alka1e)\n\n# Devinstaller Core\n\n[![img](https://img.shields.io/badge/work_in-progress-eb3434?style=for-the-badge&labelColor=7d1616)]()\n[![img](https://img.shields.io/badge/license-mit-blueviolet?style=for-the-badge)]()\n[![Documentation Status](https://readthedocs.org/projects/devinstaller-core/badge/?version=latest&style=for-the-badge)](https://devinstaller-core.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gl/devinstaller/devinstaller-core-py/branch/master/graph/badge.svg)](https://codecov.io/gl/devinstaller/devinstaller-core-py)\n[![pipeline status](https://gitlab.com/devinstaller/devinstaller-core-py/badges/master/pipeline.svg)](https://gitlab.com/devinstaller/devinstaller-core-py/-/commits/master)\n\n## Table of Contents\n\n[[_TOC_]]\n\n# What is Devinstaller Core?\n\nDevinstaller Core is the Python implementation for the Devinstaller Specification and the core library for other Devinstaller applications.\n\nThis package is not meant to be used as is. You are supposed to create applications using this library.\n\nThis Core package provided everything you need to read, parse and execute any `spec-file` and `prog-file`.\n\n[For more info ReadTheDocs](#full-documentation)\n\n# Full Documentation\n\nMain page: [Read the docs](https://devinstaller-core.readthedocs.io/en/latest/)\n\n| Topic              | Documentation link                                                       |\n| ------------------ | ------------------------------------------------------------------------ |\n| The Design process | <https://devinstaller-core.readthedocs.io/en/latest/design_process.html> |\n| Terminology        | TODO                                                                     |\n| Implementation     | <https://devinstaller-core.readthedocs.io/en/latest/implementation.html> |\n| API                | <https://devinstaller-core.readthedocs.io/en/latest/api.html>            |\n| Contributing       | <https://devinstaller-core.readthedocs.io/en/latest/contributing.html>   |\n\n_Remaining docs are WIP_\n\n# License\n\nLicensed under the terms of [MIT License](LICENSE.md)\n\n---\n\n[![forthebadge](https://forthebadge.com/images/badges/uses-git.svg)](https://forthebadge.com)\n[![forthebadge](https://forthebadge.com/images/badges/approved-by-george-costanza.svg)](https://forthebadge.com)\n[![forthebadge](https://forthebadge.com/images/badges/certified-snoop-lion.svg)](https://forthebadge.com)\n',
    'author': 'Justine Kizhakkinedath',
    'author_email': 'justine@kizhak.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://justine.kizhak.com/projects/devinstaller-core-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
