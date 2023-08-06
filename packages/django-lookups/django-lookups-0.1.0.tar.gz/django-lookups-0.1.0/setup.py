# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_lookups']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.11,<4']

setup_kwargs = {
    'name': 'django-lookups',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mistahchris',
    'author_email': 'chris@thesogu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
