# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_cz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-demo-cz',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'cz',
    'author_email': 'cz9874304@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
