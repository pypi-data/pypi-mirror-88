# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialogy',
 'dialogy.constants',
 'dialogy.errors',
 'dialogy.parsers',
 'dialogy.postprocessing',
 'dialogy.preprocessing',
 'dialogy.types',
 'dialogy.utils',
 'dialogy.workflow']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0,<16.0']

setup_kwargs = {
    'name': 'dialogy',
    'version': '0.1.0',
    'description': 'Language understanding for human dialog.',
    'long_description': None,
    'author': 'Amresh Venugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
