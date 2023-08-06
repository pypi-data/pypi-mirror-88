# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emb_vectors', 'pretrained_model']

package_data = \
{'': ['*']}

modules = \
['entry']
install_requires = \
['joblib==0.15.1', 'numpy==1.14.3', 'pandas==0.23.0', 'scikit-learn==0.20.2']

entry_points = \
{'console_scripts': ['yang-ion-pred = entry:run']}

setup_kwargs = {
    'name': 'yang-ion-pred',
    'version': '0.1.19',
    'description': '',
    'long_description': None,
    'author': 'anhttmle',
    'author_email': 'anhttmle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
