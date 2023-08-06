# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webship']

package_data = \
{'': ['*']}

install_requires = \
['fabric2>=2.5.0,<3.0.0']

entry_points = \
{'console_scripts': ['webship = webship:program.run']}

setup_kwargs = {
    'name': 'webship',
    'version': '0.1.1.dev0',
    'description': 'Tools to deploy python web application',
    'long_description': None,
    'author': 'kamal',
    'author_email': 'kamal@xoxzo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
