# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_annotate']
install_requires = \
['diot', 'pardoc', 'pipen']

setup_kwargs = {
    'name': 'pipen-annotate',
    'version': '0.0.0',
    'description': 'Use docstring to annotate pipen processes',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
