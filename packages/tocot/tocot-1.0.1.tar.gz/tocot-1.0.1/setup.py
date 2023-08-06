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
    'version': '1.0.1',
    'description': 'Table Of Contents wO Tsukuru',
    'long_description': '[![Python][python-test-image]][python-test-url]\n\n[python-test-image]: https://github.com/dondakeshimo/tocot/workflows/Python%20poetry%20lint%20test%20build/badge.svg\n[python-test-url]: https://github.com/dondakeshimo/tocot/actions?query=workflow%3A%22Python+poetry+lint+test+build%22\n\n# tocot\nTable Of Contents wO Tsukuru\n\nThis script build a TOC for markdown\n\n# Required\nPython >= 3.7\n\n# Install\n```\npip install tocot\n```\n\n# Usage\n```\n$ tocot --help\nUsage: tocot [OPTIONS] IN_FILE OUT_FILE\n\nOptions:\n  -l, --level INTEGER    [default: 2]\n  -e, --to_embed TEXT    [default: [TOC]]\n  --exclude_symbol TEXT  [default: exclude-toc]\n  --help                 Show this message and exit.\n```\n\n### example\nYou have to write "[TOC]" in your markdown file, then run below command, "[TOC]" is replaced to Table of Contents.\n```\n$ tocot README.md new_README.md\n```\n\n##### README.md\n```\n# test\nこれはテスト\n\n# 目次\n[TOC]\n\n# level1\n## level2\n### level3\n#### level4\n##### level5\n###### level6\n\n## 日本語のテスト\n\n#### level3を飛ばす\n\n# exclude <!-- exclude-toc -->\n除外されるはず\n\n\\```\n# exclude\ncode blockの中なので無視される\n\\```\n```\n\n##### new_README.md\n```\n<a id="sec1-0"></a>\n# test\nこれはテスト\n\n<a id="sec2-0"></a>\n# 目次\n* [test](#sec1-0)\n* [目次](#sec2-0)\n* [level1](#sec3-0)\n  * [level2](#sec3-1)\n  * [日本語のテスト](#sec3-2)\n\n\n<a id="sec3-0"></a>\n# level1\n<a id="sec3-1"></a>\n## level2\n### level3\n#### level4\n##### level5\n###### level6\n\n<a id="sec3-2"></a>\n## 日本語のテスト\n\n#### level3を飛ばす\n\n# exclude <!-- exclude-toc -->\n除外される\n\n\\```\n# exclude\ncode blockの中なので無視される\n\\```\n```\n\nIf you want to change "[TOC]" to "table of contents template".\n```\n$ tocot -e "table of contents template" README.md new_README.md\n```\n\nYou can select how deep include Table of contents.\nIncluding title level is defined the number of "#".\n```\n$ tocot -l 4 README.md new_README.md\n```\n\nIf you want to exclude title, you write comment "exclude-toc" next to the title.\n```\n$ tocot README.md new_README.md\n```\n\nYou can change "exclude-toc" to "i hate this title".\n```\n$ tocot --exclude_symbol "i hate this title" README.md new_README.md\n```\n\nif you want to debug, you can write to stdout.\n```\n$ tocot README.md -\n```\n',
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
