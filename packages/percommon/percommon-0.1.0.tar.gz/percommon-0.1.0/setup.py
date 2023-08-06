# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['percommon']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.4,<4.0.0',
 'django-cors-headers>=3.6.0,<4.0.0',
 'django-extensions>=3.1.0,<4.0.0',
 'djangorestframework>=3.12.2,<4.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'percommon',
    'version': '0.1.0',
    'description': 'Common modules for developering per apps',
    'long_description': None,
    'author': 'Robert Townley',
    'author_email': 'me@roberttownley.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
