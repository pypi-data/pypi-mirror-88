# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chachacha', 'chachacha.drivers']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'jinja2>=2.11.1,<3.0.0',
 'keepachangelog>=0.3.1,<0.4.0',
 'poetry-version>=0.1.5,<0.2.0',
 'semver>=2.9.1,<3.0.0']

entry_points = \
{'console_scripts': ['chachacha = chachacha.main:main']}

setup_kwargs = {
    'name': 'chachacha',
    'version': '0.2.1',
    'description': 'Chachacha changes changelogs',
    'long_description': '# CHACHACHA\n\n[![Build Status](https://travis-ci.org/aogier/chachacha.svg?branch=master)](https://travis-ci.org/aogier/chachacha)\n[![codecov](https://codecov.io/gh/aogier/chachacha/branch/master/graph/badge.svg)](https://codecov.io/gh/aogier/chachacha)\n[![Package version](https://badge.fury.io/py/chachacha.svg)](https://pypi.org/project/chachacha)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/chachacha?logo=python&logoColor=%235F9)](https://pypi.org/project/chachacha)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/aogier/chachacha.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/aogier/chachacha/context:python)\n\nChachacha changes changelogs. This is a tool you can use to keep your changelog tidy,\nfollowing the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)\nspecification which is the most implemented plugin at the moment.\n\n## Installation\n\nGrab latest copy from [releases page](https://github.com/aogier/chachacha/releases)\nand place it where you can invoke it.\n\nAlternatively you can choose to install Python package and cope with `$PATH` configuration.\n\n```console\n$ pip install chachacha\n\n...\n```\n\n## Quickstart\n\nInit a new changelog and then add some changes:\n\n```shell\nchachacha init\nchachacha added Glad to meet you\ncat CHANGELOG.md\n```\n\nSubcommands are modeled from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)\nspecification:\n\n```shell\nchachacha --help\nUsage: chachacha [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --filename TEXT  changelog filename\n  --driver TEXT    changelog format driver\n  --help           Show this message and exit.\n\nCommands:\n  init        initialize a new file\n  config      configure changelog options\n  release     release a version\n  added       add an "added" entry\n  changed     add a "changed" entry\n  deprecated  add a "deprecated" entry\n  fixed       add a "fixed" entry\n  removed     add a "removed" entry\n  security    add a "security" entry\n```\n\nSo you can *add*, *change*, *deprecate*, *fix*, *remove* and *security\nannounce* your changes.\n\nKAC format plugin driver heavily depends on Colin Bounouar\'s\n[keepachangelog library](https://github.com/Colin-b/keepachangelog).\n\nReleasing a version is simple as:\n\n```shell\nchachacha release --help\n\nUsage: main.py release [OPTIONS] [SPEC]\n\n  Update the changelog to release version SPEC.\n\n  SPEC should either be the version number to release or the strings\n  "major", "minor" or "patch".\n\nOptions:\n  --help  Show this message and exit.\n```\n\nSpecification follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)\nthanks to python [semver library](https://python-semver.readthedocs.io/en/latest/).\n\n## Configuration\n\nStarting from 0.1.3, Chachacha supports a small configuration system directly\nembedded in the file via a hack on Markdown link syntax. This allow for\na number of features like generating compare history:\n\n```shell\nchachacha init\n\nchachacha config git_provider GH\nchachacha config repo_name aogier/chachacha\nchachacha config tag_template \'v{t}\'\n\nchachacha added one feature\nchachacha added another feature\nchachacha release\nchachacha security hole\nchachacha added capability\ncat CHANGELOG.md\n\n\n[...]\n- another feature\n\n[Unreleased]: https://github.com/aogier/chachacha/compare/v0.0.1...HEAD\n[0.0.1]: https://github.com/aogier/chachacha/releases/tag/v0.0.1\n\n[//]: # (C3-1-DKAC-GGH-Raogier/chachacha-Tv{t})\n```\nConfiguration system keys are:\n\n* `git_provider`: a git repo provider driver (supported: `GH` for github.com)\n* `repo_name`: repo name + namespace your repo is\n* `tag_template`: a tag template which maps release versions with tag names.\n  Variable `t` will be expanded with the version number.\n\n## Examples\n\n### Start a changelog, add entries and then release\n\n```shell\nchachacha init\n# quoting is supported\nchachacha added "this is a new feature I\'m excited about"\nchachacha added this is also good\nchachacha deprecated this is no longer valid\n```\n\nFile is now:\n\n```shell\ncat CHANGELOG.md\n\n# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\nand this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n## [Unreleased]\n\n### Added\n\n- this is a new feature I\'m excited about\n- this is also good\n\n### Deprecated\n\n- this is no longer valid\n\n[//]: # (C3-1-DKAC)\n```\n\nNow release it:\n\n```shell\nchachacha release\nchachacha added new version added item\n```\n\nFile is now:\n\n```\ncat CHANGELOG.md\n\n# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\nand this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n## [Unreleased]\n\n### Added\n\n- new version added item\n\n## [0.0.1] - 2020-02-26\n\n### Added\n\n- this is a new feature I\'m excited about\n- this is also good\n\n### Deprecated\n\n- this is no longer valid\n\n[//]: # (C3-1-DKAC)\n```',
    'author': 'Alessandro Ogier',
    'author_email': 'alessandro.ogier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aogier/chachacha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
