# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sudoisbot',
 'sudoisbot.apis',
 'sudoisbot.network',
 'sudoisbot.network.guide_modified',
 'sudoisbot.screen',
 'sudoisbot.sink',
 'sudoisbot.temps',
 'sudoisbot.util']

package_data = \
{'': ['*'], 'sudoisbot': ['sensors/*'], 'sudoisbot.screen': ['basis33/*']}

install_requires = \
['loguru>=0.5.0,<0.6.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'peewee>=3.13.3,<4.0.0',
 'python-telegram-bot>=13.0,<14.0',
 'pyyaml>=5.3.1,<6.0.0',
 'pyzmq>=19.0.2,<20.0.0',
 'requests>=2.23.0,<3.0.0',
 'sudoistemper>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['sudoisbot = sudoisbot:main']}

setup_kwargs = {
    'name': 'sudoisbot',
    'version': '0.3.3',
    'description': 'a home automation and monitoring system written to learn zmq',
    'long_description': None,
    'author': 'Benedikt Kristinsson',
    'author_email': 'benedikt@lokun.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benediktkr/sudoisbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
