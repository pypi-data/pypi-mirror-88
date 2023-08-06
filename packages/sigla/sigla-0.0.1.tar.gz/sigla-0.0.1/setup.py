# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigla', 'sigla.sigla', 'sigla.tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'sigla',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
