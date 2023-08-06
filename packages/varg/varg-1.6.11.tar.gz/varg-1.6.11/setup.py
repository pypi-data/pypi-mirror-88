# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['varg', 'varg.cli', 'varg.resources', 'varg.utils']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'click==7.1.2',
 'coloredlogs>=14.0,<15.0',
 'cyvcf2>=0.10.0,<0.11.0',
 'importlib-metadata>=3.1.1,<4.0.0']

entry_points = \
{'console_scripts': ['varg = varg.__main__:main']}

setup_kwargs = {
    'name': 'varg',
    'version': '1.6.11',
    'description': 'Benchmark vcf-files against a truth-set of positive controls',
    'long_description': None,
    'author': 'henrikstranneheim',
    'author_email': 'henrik.stranneheim@scilifelab.se',
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
