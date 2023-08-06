# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_diagrams']

package_data = \
{'': ['*']}

install_requires = \
['diagrams>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'sphinx-diagrams',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Jean-Martin Archer',
    'author_email': 'jm@jmartin.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
