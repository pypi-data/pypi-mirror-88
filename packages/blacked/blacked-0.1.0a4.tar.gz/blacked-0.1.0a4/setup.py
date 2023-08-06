# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blacked']

package_data = \
{'': ['*']}

install_requires = \
['black>=18.4a0']

entry_points = \
{'console_scripts': ['blacked = blacked.__main__:main']}

setup_kwargs = {
    'name': 'blacked',
    'version': '0.1.0a4',
    'description': '',
    'long_description': "# blacked\n## [black](https://github.com/psf/black), but with single quotes\n### What's wrong with other 'single-quoted' black options:\n- [brunette](https://github.com/odwyersoftware/brunette): uses monkey patching that basically doesn't work when running against multiple files [odwyersoftware/brunette#5](https://github.com/odwyersoftware/brunette/issues/5)\n- [axblack](https://gith️ub.com/axiros/axblack): forked from black a while ago, inconsistent with current black versions [axiros/axblack#7](https://github.com/axiros/axblack/issues/7)\n\n\n\n### ToDo:\n- add tests:\n  - Both `blacked -S` and `black -S` must produce same results\n  - `blacked` run against code formatted with `black` must change only quotes and vice-versa\n  - `blacked` must adopt any currently installed `black` version\n  - Tests must include running `blacked` against multiple files to assure multiprocessing works as expected\n  - Tests must include latest or all `black` versions\n- add support for config.cfg\n- add support for blackd\n",
    'author': 'MrMrRobat',
    'author_email': 'appkiller16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrMrRobat/blacked',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
