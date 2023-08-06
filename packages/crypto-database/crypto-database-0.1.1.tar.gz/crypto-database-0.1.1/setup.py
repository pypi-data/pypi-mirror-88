# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['crypto_database']
install_requires = \
['flask>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['crypto_db = crypto_database:main']}

setup_kwargs = {
    'name': 'crypto-database',
    'version': '0.1.1',
    'description': 'An educational API (with database included) about cryptocurrencies',
    'long_description': None,
    'author': 'Santiago Basulto',
    'author_email': 'santiago.basulto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
