# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pycoloram']
setup_kwargs = {
    'name': 'pycoloram',
    'version': '1.0.3',
    'description': 'Модуль для работы с цветным текстом',
    'long_description': None,
    'author': 'amfili',
    'author_email': 'amfili.com@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
