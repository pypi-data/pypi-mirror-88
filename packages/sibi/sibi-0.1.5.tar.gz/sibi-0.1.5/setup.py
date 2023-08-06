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
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['sibi = sibi.main:app']}

setup_kwargs = {
    'name': 'sibi',
    'version': '0.1.5',
    'description': 'Synchronous Interactiver Brokers Interface',
    'long_description': '**Solid** is an XMLRPC interface to Interactive Brokers API.\n\nThe main purpose of this library is to transform the `async` world of tws api into `sync` procedures, in order to develop custom applications easily.\n\nIt needs TWS **9.76.1** or greater python api to work.\n\n---\n\n## Example\n* Create a file `testxmlrpc.py` with:\n\n```Python\nimport xmlrpc.client\n\ns = xmlrpc.client.ServerProxy(\'http://localhost:7080\')\n\nbars = s.reqHistoricalData("EUR", "CASH", "GBP", "IDEALPRO")\n\nprint(bars)\n```\n\nAnd that\'s it.',
    'author': 'Manuel Fedele',
    'author_email': 'manuelfedele@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
