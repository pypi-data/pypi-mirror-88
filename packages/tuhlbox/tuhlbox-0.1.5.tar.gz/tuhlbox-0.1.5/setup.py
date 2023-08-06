# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuhlbox']

package_data = \
{'': ['*']}

install_requires = \
['dstoolbox>=0.10.1,<0.11.0',
 'gensim>=3.8.3,<4.0.0',
 'simpletransformers>=0.51.1,<0.52.0',
 'sklearn>=0.0,<0.1',
 'stanza>=1.1.1,<2.0.0',
 'tensorflow-gpu>=2.3.1,<3.0.0',
 'torch>=1.7.0,<2.0.0',
 'treegrams>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'tuhlbox',
    'version': '0.1.5',
    'description': 'Personal toolbox of language processing models.',
    'long_description': None,
    'author': 'Benjamin Murauer',
    'author_email': 'b.murauer@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.uibk.ac.at/csak8736/tuhlbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
