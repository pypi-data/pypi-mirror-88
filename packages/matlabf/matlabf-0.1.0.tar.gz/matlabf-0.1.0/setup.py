# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matlabf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'matlabf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tiago Vilela',
    'author_email': 'tiagovla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
