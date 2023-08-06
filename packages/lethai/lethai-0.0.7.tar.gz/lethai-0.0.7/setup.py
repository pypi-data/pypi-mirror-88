# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lethai', 'lethai.utils']

package_data = \
{'': ['*'], 'lethai': ['public/*']}

install_requires = \
['numpy>=1.19.4,<2.0.0',
 'requests>=2.25.0,<3.0.0',
 'transformers>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'lethai',
    'version': '0.0.7',
    'description': 'Lethical AI python library',
    'long_description': None,
    'author': 'Amanl04',
    'author_email': 'amanlodha423@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
