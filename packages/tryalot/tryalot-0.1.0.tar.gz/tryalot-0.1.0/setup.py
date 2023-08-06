# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tryalot']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'zstandard>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'tryalot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yuta Taniguchi',
    'author_email': 'yuta.taniguchi.y.t@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
