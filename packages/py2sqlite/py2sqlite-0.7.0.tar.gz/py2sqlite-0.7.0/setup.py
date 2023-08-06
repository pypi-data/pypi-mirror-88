# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py2sqlite', 'py2sqlite.db_types']

package_data = \
{'': ['*']}

install_requires = \
['jsonpickle>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'py2sqlite',
    'version': '0.7.0',
    'description': 'Python ORM for SQLite database',
    'long_description': None,
    'author': 'Mykyta, Sergei',
    'author_email': 'isara.isara8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
