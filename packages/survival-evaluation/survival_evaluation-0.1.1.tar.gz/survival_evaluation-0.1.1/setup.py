# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['survival_evaluation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'survival-evaluation',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Humza Haider',
    'author_email': 'humza@haiderstats.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
