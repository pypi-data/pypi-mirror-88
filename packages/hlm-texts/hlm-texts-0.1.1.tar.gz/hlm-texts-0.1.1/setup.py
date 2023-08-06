# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlm_texts']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1.7,<3.0.0', 'logzero>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'hlm-texts',
    'version': '0.1.1',
    'description': '',
    'long_description': "# hlm-texts [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/hlm-texts.svg)](https://badge.fury.io/py/hlm-texts)\nHlm at your fingertips\n\nThis repo currently just has `340-脂砚斋重批红楼梦.txt` and `david-hawks-the-story-of-the-stone.txt`. It may expand to other versions. If you wish to have one particular version included, make a `pull request` (fork, upload files and click the pull request button) or provide a text file to me.\n\n## Installation\n`pip install hlm-texts`\n\n## Usage\n\n```\nfrom hml_texts import hlm_en\nfrom hml_texts import hlm_zh\n```\n\n`hlm_zh` is a copy of `340-脂砚斋重批红楼梦.txt`\n\n`hml_en` is a copy of `david-hawks-the-story-of-the-stone.txt`\nboth with blank lines removed and paragraphs retaind.\n\n## Notes\nThe repo is for study purpose only. If you believe that your interests have been violated in any way, please let me know. I'll promptly follow it up with appropriate actions.",
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/hlm-texts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
