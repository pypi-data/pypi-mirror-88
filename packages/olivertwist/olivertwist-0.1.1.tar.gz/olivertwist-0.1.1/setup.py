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
    'version': '0.1.1',
    'description': 'DBT DAG Auditor',
    'long_description': '\n\n![Alt text](./images/oliver_twist_logo.png)\n# oliver-twist\n\nDAG Auditor\n\n![Build status badge](https://github.com/autotraderuk/oliver-twist/workflows/CI/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\noliver-twist is a dag auditing tool that audits the [DBT](https://www.getdbt.com/) DAG and generates a summary report. The rules implemented can be found [here](RULES.md)\n\n![please sir, can I automate my DAG auditing](./images/oliver_dag_meme.jpg)\n\n# Getting Started\n\nTo get started, install the package\n\n```shell\n$ pip install olivertwist\n```\n\nand then run it by passing it your dbt manifest JSON\n\n```shell\nolivertwist manifest.json\n```\n\nThis will report any failures to the console, and also in HTML format in a directory called `target`. You can optionally auto-open the report in a browser with:\n\n```shell\nolivertwist manifest.json --browser\n```\n\nFull options are available with:\n\n\n```shell\nolivertwist manifest.json --help\n```\n\n## Developer\n\n### To dev locally\n\nClone this repo and install all the projects packages:\n\n`poetry install`\n\nTo get the latest versions of the dependencies and to update the poetry.lock file run:\n\n`poetry update`\n\nTo run oliver-twist and generate the summary report run:\n\n`poetry run olivertwist example_manifest.json`\n\n\n### Creating a distribution\n\n```poetry build --format wheel```\n',
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
