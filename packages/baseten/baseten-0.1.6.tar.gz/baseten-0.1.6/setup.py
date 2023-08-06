# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baseten', 'baseten.common', 'baseten.examples', 'baseten.workflow']

package_data = \
{'': ['*'], 'baseten': ['templates/*']}

install_requires = \
['click>=7.0',
 'colorama>=0.4.3',
 'coolname>=1.1.0',
 'h5py>=2.10.0',
 'jinja2>=2.10.3',
 'joblib>=0.12.5',
 'keyring>=19.2',
 'pandas>=0.25.1',
 'pyyaml>=5.1',
 'requests>=2.22']

entry_points = \
{'console_scripts': ['baseten = baseten.cli:cli_group']}

setup_kwargs = {
    'name': 'baseten',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Amir Haghighat',
    'author_email': 'amir@baseten.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
