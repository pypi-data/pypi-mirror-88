# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dude']
install_requires = \
['humanize>=3.1.0,<4.0.0', 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['dude = dude:main']}

setup_kwargs = {
    'name': 'dude',
    'version': '0.1.2',
    'description': 'tool similar to du but a little fancier i guess',
    'long_description': None,
    'author': 'Andrew Herbig',
    'author_email': 'notandrewherbig@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrew12/dude',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
