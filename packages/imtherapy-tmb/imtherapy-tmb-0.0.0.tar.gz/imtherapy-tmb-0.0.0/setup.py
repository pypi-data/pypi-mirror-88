# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imtherapy_tmb']

package_data = \
{'': ['*']}

install_requires = \
['imtherapy', 'pipen']

entry_points = \
{'imtherapy_feature_transform': ['tmb = imtherapy_tmb:FeatureTransformTmb']}

setup_kwargs = {
    'name': 'imtherapy-tmb',
    'version': '0.0.0',
    'description': 'Tumor mutation burden feature transformation module for imtherapy',
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
