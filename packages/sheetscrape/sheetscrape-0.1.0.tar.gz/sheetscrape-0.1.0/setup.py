# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sheetscrape', 'sheetscrape.parsers', 'sheetscrape.tests']

package_data = \
{'': ['*']}

install_requires = \
['gspread>=3.6.0,<4.0.0', 'oauth2client>=4.1.3,<5.0.0', 'pandas>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'sheetscrape',
    'version': '0.1.0',
    'description': 'Tools for parsing google sheets',
    'long_description': None,
    'author': 'Davis Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
