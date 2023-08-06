# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpraa']

package_data = \
{'': ['*'],
 'cpraa': ['.git/*',
           '.git/hooks/*',
           '.git/info/*',
           '.git/logs/*',
           '.git/logs/refs/heads/*',
           '.git/logs/refs/remotes/origin/*',
           '.git/objects/pack/*',
           '.git/refs/heads/*',
           '.git/refs/remotes/origin/*',
           '.idea/*',
           '.idea/inspectionProfiles/*',
           'AFs/*']}

install_requires = \
['z3-solver>=4.8.8,<5.0.0']

setup_kwargs = {
    'name': 'cpraa',
    'version': '0.2.0',
    'description': 'A checker for probabilistic abstract argumentation',
    'long_description': None,
    'author': 'Nikolai Käfer',
    'author_email': 'nikolai.kaefer@tu-dresden.de',
    'maintainer': 'Nikolai Käfer',
    'maintainer_email': 'nikolai.kaefer@tu-dresden.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
