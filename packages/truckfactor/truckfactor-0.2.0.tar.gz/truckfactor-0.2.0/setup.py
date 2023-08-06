# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truckfactor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'pandas>=1.1.5,<2.0.0']

entry_points = \
{'console_scripts': ['truckfactor = truckfactor.compute:run']}

setup_kwargs = {
    'name': 'truckfactor',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'HelgeCPH',
    'author_email': 'ropf@itu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
