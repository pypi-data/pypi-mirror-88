# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['password_generator']
install_requires = \
['Flask-RESTful', 'marshmallow', 'webargs']

setup_kwargs = {
    'name': 'random-password-generator',
    'version': '2.1.1',
    'description': 'Simple and custom random password generator for python',
    'long_description': None,
    'author': 'Surya Teja',
    'author_email': '94suryateja@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
