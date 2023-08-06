# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_authlib']

package_data = \
{'': ['*']}

install_requires = \
['authlib>=0.14.1,<0.15.0',
 'starlette>=0.14.1,<0.15.0',
 'uvicorn>=0.11.3,<0.12.0']

setup_kwargs = {
    'name': 'starlette-authlib',
    'version': '0.1.7',
    'description': "A drop-in replacement for Starlette session middleware, using authlib's jwt",
    'long_description': None,
    'author': 'Alessandro Ogier',
    'author_email': 'alessandro.ogier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
