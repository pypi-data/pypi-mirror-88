# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['figipy', 'figipy.resources']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'figipy',
    'version': '0.1.3',
    'description': 'Unofficial Python API for OpenFIGI (https://www.openfigi.com/)',
    'long_description': None,
    'author': 'Thomas Kluiters',
    'author_email': 'thomas.kluiters@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThomasKluiters/figipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
