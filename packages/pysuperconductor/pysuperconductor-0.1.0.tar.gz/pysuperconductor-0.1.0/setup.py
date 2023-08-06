# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysuperconductor']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.19.3', 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'pysuperconductor',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Deepak',
    'author_email': 'dmallubhotla+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
