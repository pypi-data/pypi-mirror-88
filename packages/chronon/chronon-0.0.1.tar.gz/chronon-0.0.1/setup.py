# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chronon', 'chronon.core', 'chronon.managers']

package_data = \
{'': ['*'], 'chronon': ['helpers/*']}

install_requires = \
['pandas>=1.1.3,<2.0.0', 'simpy>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'chronon',
    'version': '0.0.1',
    'description': 'Discrete event simulator',
    'long_description': None,
    'author': 'Ricardo Amigo',
    'author_email': 'ricardo.amigo@mclaren.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
