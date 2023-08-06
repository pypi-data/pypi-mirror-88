# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_parametrize_cases']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'pytest-parametrize-cases',
    'version': '0.1.1',
    'description': 'A more user-friendly way to write parametrized tests.',
    'long_description': None,
    'author': 'Cameron Pinnegar',
    'author_email': 'cameron.pinnegar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
