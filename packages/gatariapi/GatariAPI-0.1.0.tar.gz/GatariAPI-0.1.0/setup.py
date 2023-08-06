# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gatariapi']
setup_kwargs = {
    'name': 'gatariapi',
    'version': '0.1.0',
    'description': 'API of Osu!Gatari for Python',
    'long_description': None,
    'author': 'ChezZz',
    'author_email': 'egorchernobai@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
