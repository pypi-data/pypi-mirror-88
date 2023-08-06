# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sigla', 'sigla.lib', 'sigla.lib.template_renderers', 'sigla.ui']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'click>=7.1.2,<8.0.0', 'pydash>=4.9.1,<5.0.0']

entry_points = \
{'console_scripts': ['greet = sigla.ui.location:cli', 'sigla = sigla.main:cli']}

setup_kwargs = {
    'name': 'sigla',
    'version': '0.0.4',
    'description': '',
    'long_description': None,
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
