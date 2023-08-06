# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcp_pilot']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1,<2']

extras_require = \
{'bigquery': ['google-cloud-bigquery>=1,<2'],
 'build': ['google-cloud-build>=3,<4'],
 'pubsub': ['google-cloud-pubsub>=2,<3'],
 'sheets': ['gspread>=3,<4'],
 'speech': ['google-cloud-speech>=1,<2'],
 'storage': ['google-cloud-storage>=1,<2'],
 'tasks': ['google-cloud-tasks>=2,<3', 'google-cloud-scheduler>=2,<3']}

setup_kwargs = {
    'name': 'gcp-pilot',
    'version': '0.3.3',
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
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
