# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adso', 'adso.data', 'adso.topicmodel', 'adso.transform']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'nltk>=3.5,<4.0',
 'numba>=0.51,<0.52',
 'pathlib>=1.0.1,<2.0.0',
 'requests>=2.25.0,<3.0.0',
 'scipy>=1.5.4,<2.0.0',
 'sparse>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'adso',
    'version': '0.0.1.post2',
    'description': 'A topic-modelling library',
    'long_description': 'adso\n====\n\n**A topic modelling library built on top of scipy/numpy and nltk.**\n\ninstall\n^^^^^^^\n\nTo install::\n\n    pip install adso\n\nconfig\n^^^^^^\n\nadso need to write some files to disk.\nAs default adso uses the ``~/.adso`` folder, but it can be change setting the enviromental variable ``ADSODIR``.\n\ndocumentation\n^^^^^^^^^^^^^\n\nDocumentation with examples is hosted on `GitHub Pages <https://tnto.github.io/adso/index.html>`_\n\nSome examples on how to use adso are also available in ``tests`` and ``examples`` folders.\n\n\n',
    'author': "Michele 'TnTo' Ciruzzi",
    'author_email': 'tnto@hotmail.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TnTo/adso',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
