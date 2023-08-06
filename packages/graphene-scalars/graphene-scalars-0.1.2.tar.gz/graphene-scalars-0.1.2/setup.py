# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_scalars']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1.8,<3.0.0',
 'phonenumbers>=8.12.14,<9.0.0',
 'pydantic[typing_extensions,email]>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'graphene-scalars',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Alfredo Poveda',
    'author_email': 'alfpovsistemas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
