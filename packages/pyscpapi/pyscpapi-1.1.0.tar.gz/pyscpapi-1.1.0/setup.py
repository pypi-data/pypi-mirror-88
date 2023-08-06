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
    'version': '1.1.0',
    'description': 'SCP API for python (https://api.scpslgame.com/)',
    'long_description': '## pyscpapi\n\n# Installing\n\nYou can get the library directly from PyPI:\n```\npython3 -m pip install pyscpapi\n```\n\nIf you are using Windows, then the following should be used instead:\n```\npy -3 -m pip install pyscpapi\n```\n\n# HOW TO USE\nRead official API:\nhttps://api.scpslgame.com/\n\nSimple Code:\n\n```py\nimport asyncio\nfrom Pyscp_Api.api import API\n\nasync def start():\n    ip = await API.ip()\n    serverinfo = await API.serverinfo(id_ = YOUR_ID, key = YOUR_KEY, list_ = "true", players = "true")\n    lobbylist = await API.lobbylist(key = YOUR_KEY, minimal = "Test")\n    return (ip, serverinfo, lobbylist)\n  \nip, serverinfo, lobbylist = asyncio.run(start())\nprint(f"IP:          {ip}")\nprint(f"Server Info: {serverinfo}")\nprint(f"Lobby List:  {lobbylist}")\n```\n\n\n# Donate\nhttps://money.yandex.ru/to/410015858804944/0\n\n\n\n',
    'author': 'LEv145',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LEv145/SCP-Secret-Laboratory-API-python-pyscpapi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
