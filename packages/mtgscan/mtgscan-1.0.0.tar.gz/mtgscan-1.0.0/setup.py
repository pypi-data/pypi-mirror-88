# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtgscan']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'requests>=2.25.0,<3.0.0',
 'symspellpy>=6.7.0,<7.0.0']

setup_kwargs = {
    'name': 'mtgscan',
    'version': '1.0.0',
    'description': 'Convert an image of Magic cards to decklist',
    'long_description': None,
    'author': 'fortierq',
    'author_email': 'qpfortier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
