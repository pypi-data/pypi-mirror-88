# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fusegrader', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf', 'fire', 'loguru', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'fuse-grader',
    'version': '0.1.1',
    'description': 'Student side assignment grader engine.',
    'long_description': '==========\nfusegrader\n==========\n\n\n\nStudent side assignment grader engine.\n\n\n\nFeatures\n--------\n\n* TODO\n\n',
    'author': 'Anish Shrestha',
    'author_email': 'anishshrestha@fusemachines.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Anyesh/fusegrader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
