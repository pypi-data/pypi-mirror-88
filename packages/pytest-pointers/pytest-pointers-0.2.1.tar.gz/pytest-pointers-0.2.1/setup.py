# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_pointers',
 'pytest_pointers.tests',
 'pytest_pointers.tests.mock_structure']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.3.0,<10.0.0']

entry_points = \
{'pytest11': ['plugin = pytest_pointers.plugin']}

setup_kwargs = {
    'name': 'pytest-pointers',
    'version': '0.2.1',
    'description': 'Pytest plugin to define functions you test with special marks for better navigation and reports',
    'long_description': None,
    'author': 'Jack Klimov',
    'author_email': 'jaklimoff@gmail.com',
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
