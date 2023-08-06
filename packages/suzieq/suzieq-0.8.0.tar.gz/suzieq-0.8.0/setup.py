# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suzieq',
 'suzieq..ropeproject',
 'suzieq.cli',
 'suzieq.cli.sqcmds',
 'suzieq.engines',
 'suzieq.engines.pandas',
 'suzieq.gui',
 'suzieq.gui.pages',
 'suzieq.poller',
 'suzieq.poller.nodes',
 'suzieq.poller.services',
 'suzieq.restServer',
 'suzieq.sqobjects',
 'suzieq.utilities']

package_data = \
{'': ['*'], 'suzieq.gui': ['notebooks/*']}

install_requires = \
['PyYAML',
 'aiofiles',
 'aiohttp==3.6.2',
 'async-timeout',
 'asyncssh',
 'dateparser>=1.0.0,<2.0.0',
 'faker>=4.1.1,<5.0.0',
 'fastapi>=0.61.1,<0.62.0',
 'graphviz>=0.15,<0.16',
 'jsonpath-ng>=1.5.1,<2.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'netconan>=0.11.2,<0.12.0',
 'networkx>=2.4,<3.0',
 'pandas==1.1.4',
 'prompt-toolkit>2',
 'pyarrow',
 'python-nubia==0.2b5',
 'streamlit>=0.72.0,<0.73.0',
 'tabulate>=0.8.7,<0.9.0',
 'textfsm',
 'uvicorn>=0.11.8,<0.12.0',
 'uvloop']

setup_kwargs = {
    'name': 'suzieq',
    'version': '0.8.0',
    'description': '',
    'long_description': None,
    'author': 'Dinesh G Dutt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
