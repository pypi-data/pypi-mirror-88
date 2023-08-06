# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['Pyscp_Api']

package_data = \
{'': ['*']}

install_requires = \
['ujson>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'pyscpapi',
    'version': '1.0.3',
    'description': 'SCP API for python (https://api.scpslgame.com/)',
    'long_description': None,
    'author': 'LEv145',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
