# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sibi', 'sibi.ibapi']

package_data = \
{'': ['*']}

install_requires = \
['Twisted>=20.3.0,<21.0.0',
 'loguru>=0.5.3,<0.6.0',
 'redis>=3.5.3,<4.0.0',
 'treq>=20.9.0,<21.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'sibi',
    'version': '0.1.1',
    'description': 'Synchronous Interactiver Brokers Interface',
    'long_description': None,
    'author': 'Manuel Fedele',
    'author_email': 'manuelfedele@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
