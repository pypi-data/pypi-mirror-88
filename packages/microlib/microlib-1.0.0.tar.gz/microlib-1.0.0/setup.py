# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microlib']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6.0" and python_version < "3.8.0"': ['importlib-metadata>=3.1,<4.0']}

setup_kwargs = {
    'name': 'microlib',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Nicolas Hainaux',
    'author_email': 'nh.techn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
