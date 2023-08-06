# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s3fetch']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.15.18,<2.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['s3fetch = s3fetch:cmd']}

setup_kwargs = {
    'name': 's3fetch',
    'version': '1.0.0',
    'description': 'Simple S3 download tool.',
    'long_description': None,
    'author': 'Shane Anderson',
    'author_email': 'shane@reactivate.cx',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
