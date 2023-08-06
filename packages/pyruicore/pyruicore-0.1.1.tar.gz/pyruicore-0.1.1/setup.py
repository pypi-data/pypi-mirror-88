# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyruicore', 'pyruicore.data_type', 'pyruicore.model']

package_data = \
{'': ['*']}

install_requires = \
['typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pyruicore',
    'version': '0.1.1',
    'description': 'load python dict data to python class',
    'long_description': None,
    'author': 'ruicore',
    'author_email': 'hrui835@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RuiCoreSci/pyruicore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
