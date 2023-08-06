# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itly_plugin_amplitude']

package_data = \
{'': ['*']}

install_requires = \
['itly-sdk>=0.1.0,<0.2.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'itly-plugin-amplitude',
    'version': '0.1.12',
    'description': 'Iteratively Analytics SDK - Amplitude Plugin',
    'long_description': '',
    'author': 'Iteratively',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
