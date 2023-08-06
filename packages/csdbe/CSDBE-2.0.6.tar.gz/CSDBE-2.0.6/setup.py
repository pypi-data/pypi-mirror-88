# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['csdbe']
setup_kwargs = {
    'name': 'csdbe',
    'version': '2.0.6',
    'description': 'This is a CSDBE(Coctail script discord bot editor) writen by Winter_coctail',
    'long_description': None,
    'author': 'Winter_coctail',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
