# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['structlog_to_seq']

package_data = \
{'': ['*']}

extras_require = \
{'console': ['structlog>=20.1,<20.2',
             'colorama>=0.4.3,<0.5.0',
             'colorful>=0.5.4,<0.6.0']}

setup_kwargs = {
    'name': 'structlog-to-seq',
    'version': '0.3.0',
    'description': 'A collection of structlog processors for using structlog with Seq log server',
    'long_description': None,
    'author': 'Gergő Jedlicska',
    'author_email': 'gergo@jedlicska.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
