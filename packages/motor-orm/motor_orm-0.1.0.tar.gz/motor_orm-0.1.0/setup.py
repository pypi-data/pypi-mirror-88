# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motor_orm']

package_data = \
{'': ['*']}

install_requires = \
['motor>=2.3.0,<3.0.0', 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'motor-orm',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dmirty Simonov',
    'author_email': 'demalf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
