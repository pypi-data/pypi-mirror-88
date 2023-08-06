# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcp_pilot']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client',
 'google-cloud-build',
 'google-cloud-scheduler>=2,<3',
 'google-cloud-storage',
 'google-cloud-tasks']

setup_kwargs = {
    'name': 'gcp-pilot',
    'version': '0.0.1',
    'description': 'Google Cloud Platform Friendly Pilot',
    'long_description': None,
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
