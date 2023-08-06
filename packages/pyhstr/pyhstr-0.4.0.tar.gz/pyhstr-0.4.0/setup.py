# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhstr', 'tests']

package_data = \
{'': ['*'], 'tests': ['favorites/*', 'history/*']}

setup_kwargs = {
    'name': 'pyhstr',
    'version': '0.4.0',
    'description': 'History suggest box for the standard Python shell, IPython, and bpython',
    'long_description': '# pyhstr\n\n![build status](https://github.com/adder46/pyhstr/workflows/pyhstr/badge.svg) [![codecov](https://codecov.io/gh/adder46/pyhstr/branch/master/graph/badge.svg?token=ZMY0VUX8WS)](https://codecov.io/gh/adder46/pyhstr)\n\nInspired by hstr, **pyhstr** is a history suggest box that lets you quickly search, navigate, and manage your Python shell history. At this point, it supports the standard Python shell, IPython, and bpython. The plan is to support ptpython as well, but some help is needed for that to happen (see [issue #7](https://github.com/adder46/pyhstr/issues/7)).\n\n## Installation\n\n\n```\npip install pyhstr\n```\n\n## Usage\n\nThe **standard** shell and **bpython**:\n\n  ```python\n  >>> from pyhstr import hh\n  >>> hh\n  ```\n\n**IPython**:\n\n  ```ipython\n  In [1]: import pyhstr\n  In [2]: %hh\n  ```\n\nMaking an alias should be more convenient though, for example:\n\n```bash\nalias py=\'python3 -ic "from pyhstr import hh"\'\n```\n\n## Screencast\n\n![screenshot](pyhstr.gif)\n\n## Development\n\nYou will need [poetry](https://github.com/python-poetry/poetry), preferably with these options in config:\n\n```toml\nvirtualenvs.create = true\nvirtualenvs.in-project = true\n```\n\nThen clone the repo, cd into it, make a venv, activate it, and install the project:\n\n```sh\ngit clone https://github.com/adder46/pyhstr\ncd pyhstr\npoetry env use python3\n. .venv/bin/activate\npoetry install\n```\n\nTo run tests, mypy checks, and style checks, you need to have Pythons:\n\n- 3.7\n- 3.8\n- 3.9\n\nFor installing all the Python versions, I recommend [pyenv](https://github.com/pyenv/pyenv).\n\nOnce you have them, run:\n\n```\ntox\n```\n\n## Licensing\n\nLicensed under the [MIT License](https://opensource.org/licenses/MIT). For details, see [LICENSE](https://github.com/adder46/pyhstr/blob/master/LICENSE).',
    'author': 'adder46',
    'author_email': 'dedmauz69@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
