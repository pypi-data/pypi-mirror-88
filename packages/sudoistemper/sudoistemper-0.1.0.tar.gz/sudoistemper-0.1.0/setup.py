# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temper']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.4,<4.0']

entry_points = \
{'console_scripts': ['temper = temper.temper:main']}

setup_kwargs = {
    'name': 'sudoistemper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'urwen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
