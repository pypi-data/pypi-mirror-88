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
    'version': '0.1.6',
    'description': 'Table Of Contents wO Tsukuru',
    'long_description': '# tocot\nTable Of Contents wO Tsukuru\n\nThis script build a TOC for markdown\n\n# Required\nPython >= 3.6\n\n# Install\n```\npip install tocot\n```\n\n# Usage\n```\n$ tocot --help\nUsage: tocot [OPTIONS] IN_FILE OUT_FILE\n\nOptions:\n  -l, --level INTEGER    [default: 2]\n  -e, --to_embed TEXT    [default: [TOC]]\n  --exclude_symbol TEXT  [default: exclude-toc]\n  --help                 Show this message and exit.\n```\n\n### example\nYou have to write "[TOC]" in your markdown file, then run below command, "[TOC]" is replaced to Table of Contents.\n```\n$ tocot README.md new_README.md\n```\n\nIf you want to change "[TOC]" to "table of contents template".\n```\n$ tocot -e "table of contents template" README.md new_README.md\n```\n\nYou can select how deep include Table of contents.\nIncluding title level is defined the number of "#".\n```\n$ tocot -l 4 README.md new_README.md\n```\n\nIf you want to exclude title, you write comment "exclude-toc" next to the title.\n```\n$ tocot README.md new_README.md\n```\n\nYou can change "exclude-toc" to "i hate this title".\n```\n$ tocot --exclude_symbol "i hate this title" README.md new_README.md\n```\n\nif you want to debug, you can write to stdout.\n```\n$ tocot README.md -\n```\n',
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
