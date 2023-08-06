# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mighty', 'mighty.game']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'mighty',
    'version': '1.0.0',
    'description': 'Mighty card game engine',
    'long_description': None,
    'author': 'DongJin Shin',
    'author_email': 'dongjin.shin.00@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
