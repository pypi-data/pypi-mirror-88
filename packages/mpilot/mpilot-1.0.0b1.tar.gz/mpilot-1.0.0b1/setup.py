# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpilot',
 'mpilot.cli',
 'mpilot.libraries',
 'mpilot.libraries.eems',
 'mpilot.libraries.eems.csv',
 'mpilot.libraries.eems.netcdf',
 'mpilot.parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'netCDF4>=1.5.4,<2.0.0',
 'ply>=3.11,<4.0',
 'six>=1.15.0,<2.0.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['numpy>=1.16.6,<2.0.0'],
 ':python_version >= "3.6"': ['numpy>=1.19.4,<2.0.0']}

entry_points = \
{'console_scripts': ['mpilot = mpilot.cli.mpilot:main']}

setup_kwargs = {
    'name': 'mpilot',
    'version': '1.0.0b1',
    'description': 'MPilot is a plugin-based, environmental modeling framework',
    'long_description': '# mpilot\nMPilot is a plugin-based, environmental modeling framework\n',
    'author': 'Conservation Biology Institute',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/consbio/mpilot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
