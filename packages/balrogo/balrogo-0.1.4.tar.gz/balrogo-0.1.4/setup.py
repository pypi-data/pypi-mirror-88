# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balrogo']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0,<5.0',
 'emcee>=3.0.2,<4.0.0',
 'matplotlib>=3.1.2,<4.0.0',
 'numdifftools>=0.9.39,<0.10.0',
 'numpy>=1.18.5,<2.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'scipy>=1.4.1,<2.0.0',
 'shapely>=1.6.4,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=3.3.0,<4.0.0']}

setup_kwargs = {
    'name': 'balrogo',
    'version': '0.1.4',
    'description': 'Bayesian Astrometric Likelihood Recover of Galactic Objects',
    'long_description': '# BALRoGO\n\n[![pipeline status](https://gitlab.com/eduardo-vitral/balrogo/badges/master/pipeline.svg)](https://gitlab.com/eduardo-vitral/balrogo/-/commits/master)\n[![coverage report](https://gitlab.com/eduardo-vitral/balrogo/badges/master/coverage.svg)](https://gitlab.com/eduardo-vitral/balrogo/-/commits/master)\n[![pypi](https://img.shields.io/pypi/v/balrogo.svg)](https://pypi.python.org/pypi/balrogo/)\n[![python](https://img.shields.io/pypi/pyversions/balrogo.svg)](https://pypi.python.org/pypi/balrogo)\n[![license](http://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)\n\n<!-- markdownlint-disable-next-line no-inline-html -->\n<img alt="logo" align="right" src="logo.png" width="20%" />\n\nBALRoGO: Bayesian Astrometric Likelihood Recover of Galactic Objects.\n\n- Specially developed to handle data from the Gaia space mission.\n- Extracts galactic objects such as globular clusters and dwarf galaxies.\n- Uses a combination of Bayesian and non-Bayesian approaches.\n- Provides:\n  - Fits of proper motion space.\n  - Fits of surface density.\n  - Fits of object center.\n  - Confidence regions for the color-magnitude diagram and parallaxes.\n\nIf something does not work, please [file an issue](https://gitlab.com/eduardo-vitral/balrogo/-/issues).\n\n## Attribution\n\nPlease cite [us](https://arxiv.org/abs/2010.05532) if you find this code useful in your research and add your paper to the testimonials list. The BibTeX entry for the paper is:\n\n```bibtex\n@ARTICLE{Vitral&Mamon20b,\n       author = {{Vitral}, Eduardo and {Mamon}, Gary A.},\n        title = "{Does NGC 6397 contain an intermediate-mass black hole or a more diffuse inner sub-cluster?}",\n      journal = {arXiv e-prints},\n     keywords = {Astrophysics - Astrophysics of Galaxies},\n         year = 2020,\n        month = oct,\n          eid = {arXiv:2010.05532},\n        pages = {arXiv:2010.05532},\narchivePrefix = {arXiv},\n       eprint = {2010.05532},\n primaryClass = {astro-ph.GA},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2020arXiv201005532V},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n```\n\n## Quick overview\n\nTo be written.\n\n### Using BALRoGO on [*Gaia*](https://www.cosmos.esa.int/web/gaia/data-access) data\n\nTo be written.\n\n## License\n\nCopyright (c) 2020 Eduardo Vitral & Alexandre Macedo.\n\nBALRoGO is free software made available under the [MIT License](LICENSE).\n',
    'author': 'Eduardo Vitral',
    'author_email': 'vitral@iap.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/eduardo-vitral/balrogo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
