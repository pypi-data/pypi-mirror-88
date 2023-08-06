# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trycast']
setup_kwargs = {
    'name': 'trycast',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'David Foster',
    'author_email': 'david@dafoster.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
