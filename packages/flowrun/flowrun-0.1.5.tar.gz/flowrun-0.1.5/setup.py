# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowrun']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0', 'sseclient>=0.0.27,<0.0.28']

setup_kwargs = {
    'name': 'flowrun',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'pskishere',
    'author_email': 'pskishere@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
