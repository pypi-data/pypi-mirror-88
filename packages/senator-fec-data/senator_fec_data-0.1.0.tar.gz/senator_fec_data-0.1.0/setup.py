# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['senator_fec_data']

package_data = \
{'': ['*'], 'senator_fec_data': ['data/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'matplotlib>=3.3.3,<4.0.0',
 'pandas>=1.1.5,<2.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'senator-fec-data',
    'version': '0.1.0',
    'description': 'Python package to obtain the FEC data of current US senators.',
    'long_description': None,
    'author': 'Bryn',
    'author_email': 'bam2231@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
