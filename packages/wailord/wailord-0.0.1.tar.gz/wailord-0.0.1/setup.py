# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wailord', 'wailord.exp', 'wailord.io']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'Pint-Pandas>=0.1,<0.2',
 'Pint>=0.16.1,<0.17.0',
 'Sphinx>=3.3.1,<4.0.0',
 'ase>=3.20.1,<4.0.0',
 'black>=20.8b1,<21.0',
 'click>=7.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'flake8>=3.8.4,<4.0.0',
 'konfik>=2.0.0,<3.0.0',
 'pandas>=1.1.3,<2.0.0',
 'parsimonious>=0.8.1,<0.9.0',
 'pytest-datadir>=1.3.1,<2.0.0',
 'releases>=1.6.3,<2.0.0',
 'robpol86-sphinxcontrib-googleanalytics>=0.1,<0.2',
 'siuba>=0.0.24,<0.0.25',
 'sphinx-autobuild>=2020.9.1,<2021.0.0',
 'sphinx-comments>=0.0.3,<0.0.4',
 'sphinx-copybutton>=0.3.1,<0.4.0',
 'sphinx-fasvg>=0.1.3,<0.2.0',
 'sphinx-issues>=1.2.0,<2.0.0',
 'sphinx-library>=1.1.2,<2.0.0',
 'sphinx-minipres>=0.2.1,<0.3.0',
 'sphinx-proof>=0.0.3,<0.0.4',
 'sphinx-sitemap>=2.2.0,<3.0.0',
 'sphinx-togglebutton>=0.2.3,<0.3.0',
 'sphinx-versions>=1.1.3,<2.0.0',
 'sphinxcontrib-apidoc>=0.3.0,<0.4.0',
 'sphinxcontrib-doxylink>=1.6.1,<2.0.0',
 'sphinxcontrib-github_ribbon>=0.9.0,<0.10.0',
 'sphinxcontrib.contributors>=1.0,<2.0',
 'vg>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['run = wailord.cli:main']}

setup_kwargs = {
    'name': 'wailord',
    'version': '0.0.1',
    'description': 'Wailord is a python library to interact with ORCA',
    'long_description': '=======\nWailord\n=======\n\n.. image:: https://w.wallhaven.cc/full/4x/wallhaven-4xgw53.jpg\n        :alt: Logo of sorts\n\n.. image:: https://img.shields.io/pypi/v/wailord.svg\n        :target: https://pypi.python.org/pypi/wailord\n\n.. image:: https://img.shields.io/travis/HaoZeke/wailord.svg\n        :target: https://travis-ci.com/HaoZeke/wailord\n\n.. image:: https://readthedocs.org/projects/wailord/badge/?version=latest\n        :target: https://wailord.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/HaoZeke/wailord/shield.svg\n     :target: https://pyup.io/repos/github/HaoZeke/wailord/\n     :alt: Updates\n\n\n\nWailord is a python library to interact with ORCA\n\n\n* Free software: GNU General Public License v3\n* Documentation: https://wailord.readthedocs.io. **TBD**\n\n\nFeatures\n--------\n\n* Integrates with SLURM in a manner of speaking\n\nLimitations\n-----------\n\n* By choice, the split-job syntax has not been included in the current formulation\n  - The `pre` keyword is a notable exception, as it performs a geometry optimization of the `xyz` file before passing through to the rest of the calculations\n\nCredits\n-------\n\n* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n* The image is from wallhaven.cc\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Rohit Goswami',
    'author_email': 'rog32@hi.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HaoZeke/wailord',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
