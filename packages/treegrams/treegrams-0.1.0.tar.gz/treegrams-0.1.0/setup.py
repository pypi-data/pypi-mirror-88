# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treegrams']

package_data = \
{'': ['*']}

install_requires = \
['nltk>=3.5,<4.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'treegrams',
    'version': '0.1.0',
    'description': 'Extracts sub-tree patterns from NLTK tree structures.',
    'long_description': None,
    'author': 'Benjamin Murauer',
    'author_email': 'b.murauer@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
