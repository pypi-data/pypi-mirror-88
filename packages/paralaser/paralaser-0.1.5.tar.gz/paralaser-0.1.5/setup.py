# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paralaser', 'paralaser.lib']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'faiss-gpu>=1.6.5,<2.0.0',
 'fastBPE>=0.1.0,<0.2.0',
 'jieba>=0.42.1,<0.43.0',
 'numpy>=1.19.4,<2.0.0',
 'torch>=1.7.1,<2.0.0',
 'transliterate>=1.10.2,<2.0.0',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'paralaser',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
