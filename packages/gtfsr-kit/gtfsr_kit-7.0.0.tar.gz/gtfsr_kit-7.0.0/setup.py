# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtfsr_kit']

package_data = \
{'': ['*']}

install_requires = \
['gtfs-kit>=5.0.2,<6.0.0', 'gtfs-realtime-bindings>=0.0.6,<0.0.7']

setup_kwargs = {
    'name': 'gtfsr-kit',
    'version': '7.0.0',
    'description': 'A Python 3.8+ library to process General Transit Feed Specification Realtime (GTFSR) data',
    'long_description': None,
    'author': 'Alex Raichev',
    'author_email': 'araichev@mrcagney.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
