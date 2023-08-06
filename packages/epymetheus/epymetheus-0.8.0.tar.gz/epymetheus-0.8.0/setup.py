# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epymetheus',
 'epymetheus.benchmarks',
 'epymetheus.datasets',
 'epymetheus.metrics',
 'epymetheus.stochastic',
 'epymetheus.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.0,<2.0.0',
 'pandas-datareader>=0.9.0,<0.10.0',
 'pandas>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'epymetheus',
    'version': '0.8.0',
    'description': 'Python framework for multi-asset backtesting.',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
