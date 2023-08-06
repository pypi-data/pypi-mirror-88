# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noglobal_magic']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=5.5', 'pyflakes>=2']

setup_kwargs = {
    'name': 'noglobal-magic',
    'version': '0.1.0rc0',
    'description': 'magic command for prohibit using global variables in Jupyter Notebook',
    'long_description': "# noglobal-magic\n\nMagic command for prohibit using global variables in Jupyter Notebook.\n\n## Installation\n\nMake sure you've this `noglobal-magic` (And the Python package `pyflakes`).\n\n```shell\npip install noglobal-magic\n```\n\n## How to use\n\nIn a cell on Jupyter Notebook, load and activate this extension:\n\n```notebook\n%load_ext noglobal_magic\n%no_global\n```\n\nYou've ready to enjoy coding.\n\nLet's see how it works:\n",
    'author': 'tokusumi',
    'author_email': 'tksmtoms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tokusumi/noglobal-magic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
