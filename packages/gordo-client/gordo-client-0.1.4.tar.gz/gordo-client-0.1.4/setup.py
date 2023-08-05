# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gordo_client']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.0,<5.0',
 'gordo-dataset>=2.2,<3.0',
 'pandas>=1.0,<2.0',
 'scikit-learn>=0.23,<1.0',
 'tensorflow-estimator>=2.1.0,<2.2.0',
 'wrapt>=1.11,<2.0']

setup_kwargs = {
    'name': 'gordo-client',
    'version': '0.1.4',
    'description': 'Gordo client',
    'long_description': '# Gordo client\nSeparete client for [Gordo](https://github.com/equinor/gordo) project.\n\n# Install\n`pip install gordo-client`\n\n# Uninstall\n`pip uninstall gordo-client`\n',
    'author': 'Equinor ASA',
    'author_email': 'fg_gpl@equinor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/equinor/gordo-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
