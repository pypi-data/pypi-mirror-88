# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapflow',
 'snapflow.cli',
 'snapflow.core',
 'snapflow.core.conversion',
 'snapflow.core.data_formats',
 'snapflow.core.extraction',
 'snapflow.core.metadata',
 'snapflow.core.sql',
 'snapflow.core.storage',
 'snapflow.core.typing',
 'snapflow.db',
 'snapflow.examples',
 'snapflow.logging',
 'snapflow.modules',
 'snapflow.modules.core',
 'snapflow.modules.core.pipes',
 'snapflow.project',
 'snapflow.testing',
 'snapflow.utils']

package_data = \
{'': ['*'],
 'snapflow.core.sql': ['templates/*'],
 'snapflow.modules.core': ['schemas/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'colorful>=0.5.4,<0.6.0',
 'jinja2>=2.11.1,<3.0.0',
 'loguru>=0.5.1,<0.6.0',
 'networkx>=2.4,<3.0',
 'pandas>=1.0.1,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.3.13,<2.0.0',
 'sqlparse>=0.3.1,<0.4.0',
 'strictyaml>=1.0.6,<2.0.0']

entry_points = \
{'console_scripts': ['snapflow = snapflow.cli:app']}

setup_kwargs = {
    'name': 'snapflow',
    'version': '0.1.3',
    'description': 'Functional Data Pipelines',
    'long_description': None,
    'author': 'Ken Van Haren',
    'author_email': 'kenvanharen@gmail.com',
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
