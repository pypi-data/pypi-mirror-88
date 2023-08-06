# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluf']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.3,<0.4.0', 'matplotlib>=3.3.3,<4.0.0']

setup_kwargs = {
    'name': 'fluf',
    'version': '0.1.8',
    'description': 'Simple caching & workflow',
    'long_description': None,
    'author': 'Mark Fiers',
    'author_email': 'mark.fiers.42@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
