# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['storage']
setup_kwargs = {
    'name': 'hcs-storage',
    'version': '1.3',
    'description': 'a storage class wrapping a dict.',
    'long_description': 'About\n=====\n\na storage class wrapping a dict.\n\n\nFeedback and getting involved\n-----------------------------\n\nSend feedback and bug reports by email to hcs at furuvik dot net.\n\n- Code Repository: https://gitlab.com/hcs/hcs-storage\n',
    'author': 'Christer Sjöholm',
    'author_email': 'hcs@furuvik.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/hcs-storage/',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
