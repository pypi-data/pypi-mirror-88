# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcfg']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=3.1.1,<4.0.0', 'nltk>=3.5,<4.0']

setup_kwargs = {
    'name': 'pcfg',
    'version': '0.1.2',
    'description': 'Generate sentences from a probabilistic context-free grammar.',
    'long_description': None,
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomasbreydo/pcfg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
