# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dacalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dacalc',
    'version': '0.0.1',
    'description': 'A simple python calculator written by DA',
    'long_description': None,
    'author': 'Damon Allison',
    'author_email': 'damon@damonallison.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
