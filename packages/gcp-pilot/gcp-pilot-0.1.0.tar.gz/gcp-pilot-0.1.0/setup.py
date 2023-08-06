# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcp_pilot']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1,<2']

extras_require = \
{'build': ['google-cloud-build>=3,<4'],
 'storage': ['google-cloud-storage>=1,<2'],
 'tasks': ['google-cloud-tasks>=2,<3', 'google-cloud-scheduler>=2,<3']}

setup_kwargs = {
    'name': 'gcp-pilot',
    'version': '0.1.0',
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
