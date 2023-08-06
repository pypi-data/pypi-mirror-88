# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sczr_tcp']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'orjson>=3.4.6,<4.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pygame>=2.0.0,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['sczr-tcp = sczr_tcp.cli:main']}

setup_kwargs = {
    'name': 'sczr-tcp',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Michał Rokita',
    'author_email': 'mrokita@mrokita.pl',
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
