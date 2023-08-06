# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['msgpack-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'msgpack-types',
    'version': '0.1.0',
    'description': 'Type stubs for msgpack',
    'long_description': '# msgpack-types [![PyPI](https://img.shields.io/pypi/v/msgpack-types.svg)](https://pypi.org/project/msgpack-types/)\n\n> Type stubs for [msgpack](https://github.com/msgpack/msgpack-python)\n\nAllows for autocomplete and static typing.\n\n## install\n\n```\npip install msgpack-types\n```\n',
    'author': 'Steve Dignam',
    'author_email': 'steve@dignam.xyz',
    'url': 'https://github.com/sbdchd/msgpack-types',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
