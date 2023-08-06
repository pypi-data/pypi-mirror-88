# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inspyre_toolbox', 'inspyre_toolbox.live_timer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'inspyre-toolbox',
    'version': '1.0a2',
    'description': 'A toolbox containing some useful tools for Inspyre Softworks packages. Generally useful to some programmers too.',
    'long_description': None,
    'author': 'tayjaybabee',
    'author_email': 'tayjaybabee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
