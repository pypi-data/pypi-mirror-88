# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tocot']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['tocot = tocot.main:main']}

setup_kwargs = {
    'name': 'tocot',
    'version': '0.1.4',
    'description': 'Table Of Contents wO Tsukuru',
    'long_description': '# tocot\nTable Of Contents wO Tsukuru\n\nThis script build a TOC for markdown\n',
    'author': 'dondakeshimo',
    'author_email': 'went.went.takkun135@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
