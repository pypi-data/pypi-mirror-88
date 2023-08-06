# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pedroai']

package_data = \
{'': ['*']}

install_requires = \
['plotnine>=0.7,<0.8',
 'pydantic>=1.7.3,<2.0.0',
 'pysimdjson[dev]>=2.4.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'rich>=9.3.0,<10.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['pedroai = pedroai.main:cli']}

setup_kwargs = {
    'name': 'pedroai',
    'version': '0.1.11',
    'description': '',
    'long_description': None,
    'author': 'Pedro Rodriguez',
    'author_email': 'me@pedro.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
