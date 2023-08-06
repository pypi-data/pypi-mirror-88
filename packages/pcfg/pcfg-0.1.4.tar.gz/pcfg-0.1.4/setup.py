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
    'version': '0.1.4',
    'description': 'Generate sentences from a probabilistic context-free grammar.',
    'long_description': 'pcfg\n====\n[![Documentation Status](https://readthedocs.org/projects/pcfg/badge/?version=latest)](https://pcfg.readthedocs.io/en/latest/?badge=latest)\n\n\nDescription\n-----------\n\nImplement the ``generate()`` method for NLTK\'s [probabilistic context-free grammar](https://www.nltk.org/api/nltk.html#nltk.grammar.PCFG) to probabilistically generate valid sentences. (NLTK stands for Natural Language Toolkit.)\n\nInstallation\n------------\n\n```zsh\npip install pcfg\n```\n\nDocumentation\n-------------\n\nRead the latest documentation for **pcfg** [here](https://pcfg.readthedocs.io/).\n\n\nExample usage\n-------------\n\nA ``PCFG`` can be initialized in the same way that an NLTK [probabilistic context-free grammar](https://www.nltk.org/api/nltk.html#nltk.grammar.PCFG) is initialized:\n\n```python3\n>>> from pcfg import PCFG\n>>> grammar = PCFG.fromstring("""\n... S -> Subject Action [1.0]\n... Subject -> "a cow" [0.7] | "some guy" [0.1] | "the woman" [0.2]\n... Action -> "eats lunch" [0.5] | "was here" [0.5]\n... """)\n```\n\nTo generate sentences, simply use the ``generate()`` method:\n\n```python3\n>> > for sentence in grammar.generate(3):\n    ...\nprint(sentence)\n```\n\nThe output could be the following:\n\n```text\nthe woman eats lunch\nthe woman was here\na cow was here\n```\n\nOf course, your output may be different because the sentences are generated probabilistically.\n\nLicense\n-------\n[MIT](https://github.com/thomasbreydo/pcfg/blob/master/LICENSE)\n',
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomasbreydo/pcfg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
