# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gordo.client',
    'version': '0.1.5',
    'description': 'Gordo client',
    'long_description': '# Gordo client\nSeparete client for [Gordo](https://github.com/equinor/gordo) project.\n\n# Install\n`pip install gordo-client`\n\n# Uninstall\n`pip uninstall gordo-client`\n',
    'author': 'Equinor ASA',
    'author_email': 'fg_gpl@equinor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/equinor/gordo-client',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
