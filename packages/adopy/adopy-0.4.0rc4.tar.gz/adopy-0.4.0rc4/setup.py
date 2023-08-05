# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adopy', 'adopy.base', 'adopy.functions', 'adopy.tasks']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'pandas', 'scipy>=1.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata'],
 'docs': ['sphinx',
          'sphinx_rtd_theme',
          'sphinx-autobuild',
          'recommonmark',
          'sphinx-issues>=1.2.0,<2.0.0',
          'ipykernel>=5.3.4,<6.0.0',
          'nbsphinx>=0.8.0,<0.9.0',
          'matplotlib>=3.3.3,<4.0.0',
          'jupyterlab>=2.2.9,<3.0.0'],
 'test': ['pytest>=6.0', 'pytest-cov', 'codecov']}

setup_kwargs = {
    'name': 'adopy',
    'version': '0.4.0rc4',
    'description': 'Adaptive Design Optimization on Experimental Tasks',
    'long_description': '# ADOpy <img src="https://adopy.github.io/logo/adopy-logo.svg" align="right" width="300px">\n\n[![PyPI](https://img.shields.io/pypi/v/adopy.svg?color=green)](https://pypi.org/project/adopy/)\n[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n[![Travis CI](https://travis-ci.org/adopy/adopy.svg?branch=develop)](https://travis-ci.org/adopy/adopy)\n[![CodeCov](https://codecov.io/gh/adopy/adopy/branch/develop/graph/badge.svg?token=jFnJgnVV1k)](https://codecov.io/gh/adopy/adopy)\n\n**ADOpy** is a Python implementation of Adaptive Design Optimization (ADO; Myung, Cavagnaro, & Pitt, 2013), which computes optimal designs dynamically in an experiment. Its modular structure permit easy integration into existing experimentation code.\n\nADOpy supports Python 3.6 or above and relies on NumPy, SciPy, and Pandas.\n\n### Features\n\n- **Grid-based computation of optimal designs using only three classes**: `adopy.Task`, `adopy.Model`, and `adopy.Engine`.\n- **Easily customizable for your own tasks and models**\n- **Pre-implemented Task and Model classes including**:\n  - Psychometric function estimation for 2AFC tasks (`adopy.tasks.psi`)\n  - Delay discounting task (`adopy.tasks.ddt`)\n  - Choice under risk and ambiguity task (`adopy.tasks.cra`)\n- **Example code for experiments using PsychoPy** ([link][example-code])\n\n[example-code]: https://github.com/adopy/adopy/tree/master/examples\n\n### Installation\n\n```bash\n# Install from PyPI\npip install adopy\n\n# Install from Github (developmental version)\npip install git+https://github.com/adopy/adopy.git@develop\n```\n\n### Resources\n\n- [**Getting started**](https://adopy.org/getting-started.html)\n- [**Documentation**](https://adopy.org)\n- [**Bug reports**](https://github.com/adopy/adopy/issues)\n\n## Citation\n\nIf you use ADOpy, please cite this package along with the specific version.\nIt greatly encourages contributors to continue supporting ADOpy.\n\n> Yang, J., Pitt, M. A., Ahn, W., & Myung, J. I. (2020).\n> ADOpy: A Python Package for Adaptive Design Optimization.\n> _Behavior Research Methods_, 1-24.\n> https://doi.org/10.3758/s13428-020-01386-4\n\n## Acknowledgement\n\nThe research was supported by National Institute of Health Grant R01-MH093838 to Mark A. Pitt and Jay I. Myung, the Basic Science Research Program through the National Research Foundation (NRF) of Korea funded by the Ministry of Science, ICT, & Future Planning (NRF-2018R1C1B3007313 and NRF-2018R1A4A1025891), the Institute for Information & Communications Technology Planning & Evaluation (IITP) grant funded by the Korea government (MSIT) (No. 2019-0-01367, BabyMind), and the Creative-Pioneering Researchers Program through Seoul National University to Woo-Young Ahn.\n\n## References\n\n- Myung, J. I., Cavagnaro, D. R., and Pitt, M. A. (2013).\n  A tutorial on adaptive design optimization.\n  _Journal of Mathematical Psychology, 57_, 53–67.\n',
    'author': 'Jaeyeong Yang',
    'author_email': 'jaeyeong.yang1125@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://adopy.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
