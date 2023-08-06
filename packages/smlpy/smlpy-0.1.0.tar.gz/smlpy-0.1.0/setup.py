# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smlpy']

package_data = \
{'': ['*']}

install_requires = \
['jsons>=1.3.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pyserial-asyncio>=0.5,<0.6',
 'pyserial>=3.5,<4.0',
 'pyyaml>=5.3.1,<6.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'smlpy',
    'version': '0.1.0',
    'description': 'smlpy enables reading of smart meter language (sml) data from a smart power meter. ',
    'long_description': None,
    'author': 'christian.sauer',
    'author_email': 'christian.sauer@email.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ChristianSauer/smlpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
