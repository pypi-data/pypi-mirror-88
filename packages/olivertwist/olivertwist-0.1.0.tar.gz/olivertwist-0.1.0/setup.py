# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olivertwist',
 'olivertwist.metricengine',
 'olivertwist.reporter',
 'olivertwist.ruleengine',
 'olivertwist.rules']

package_data = \
{'': ['*'],
 'olivertwist.reporter': ['html/css/*',
                          'html/images/*',
                          'html/webfonts/*',
                          'templates/*']}

install_requires = \
['Jinja2==2.11.2',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'networkx>=2.5,<3.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['olivertwist = olivertwist.main:main',
                     'ot = olivertwist.main:main']}

setup_kwargs = {
    'name': 'olivertwist',
    'version': '0.1.0',
    'description': 'DBT DAG Auditor',
    'long_description': None,
    'author': 'Angelos Georgiadis',
    'author_email': 'angelos.georgiadis@autotrader.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/autotraderuk/oliver-twist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
