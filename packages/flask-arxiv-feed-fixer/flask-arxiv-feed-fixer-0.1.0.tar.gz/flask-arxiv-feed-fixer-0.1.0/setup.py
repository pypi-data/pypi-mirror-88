# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_arxiv_feed_fixer']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'flask-arxiv-feed-fixer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Kail',
    'author_email': 'andrew.a.kail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
