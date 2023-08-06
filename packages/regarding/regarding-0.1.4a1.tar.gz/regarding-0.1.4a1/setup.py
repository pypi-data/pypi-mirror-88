# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regarding']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=50.3.2,<51.0.0', 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['regarding = regarding.__main__:main']}

setup_kwargs = {
    'name': 'regarding',
    'version': '0.1.4a1',
    'description': 'Create __about__.py files for Poetry and setup.py projects.',
    'long_description': '#########\nRegarding\n#########\n\nCreate "about file" source files for storing a software project\'s metadata.\n',
    'author': 'Travis Shirk',
    'author_email': 'travis@pobox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicfit/regarding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
