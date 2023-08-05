# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imtherapy',
 'imtherapy.feature_selection',
 'imtherapy.feature_transform',
 'imtherapy.machine_learning']

package_data = \
{'': ['*'], 'imtherapy': ['reports/*', 'scripts/*']}

install_requires = \
['pipen',
 'pipen-args',
 'pipen-report',
 'pipen-verbose',
 'pyparam',
 'rich>=9.0.0,<10.0.0',
 'simplug']

entry_points = \
{'console_scripts': ['imtherapy = imtherapy:main']}

setup_kwargs = {
    'name': 'imtherapy',
    'version': '0.0.0',
    'description': 'A framework to explore, select and discover predictive markers for cancer immunotherapy',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
