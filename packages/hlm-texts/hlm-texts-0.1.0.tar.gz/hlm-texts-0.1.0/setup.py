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
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'freemt',
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
