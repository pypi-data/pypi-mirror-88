# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_pointers',
 'pytest_pointers.tests',
 'pytest_pointers.tests.mock_structure']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.3.15,<0.4.0', 'rich>=9.3.0,<10.0.0']

entry_points = \
{'pytest11': ['plugin = pytest_pointers.plugin']}

setup_kwargs = {
    'name': 'pytest-pointers',
    'version': '0.2.3',
    'description': 'Pytest plugin to define functions you test with special marks for better navigation and reports',
    'long_description': '## Pytest Plugin to show real test coverage\n\n### TLTR\n\nWith this plugin you will be able to see all methods in project with the number of their tests\n\n![](https://jaklimoff-misc.s3.eu-central-1.amazonaws.com/pytest-pointers/example_output.jpg)\n',
    'author': 'Jack Klimov',
    'author_email': 'jaklimoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaklimoff/pytest-pointers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
