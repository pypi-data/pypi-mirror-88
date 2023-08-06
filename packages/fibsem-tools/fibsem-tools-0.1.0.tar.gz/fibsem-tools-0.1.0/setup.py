# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fibsem_tools',
 'fibsem_tools.attrs',
 'fibsem_tools.io',
 'fibsem_tools.scripts']

package_data = \
{'': ['*']}

install_requires = \
['distributed>=2.30.1,<3.0.0',
 'h5py>=3.1.0,<4.0.0',
 'pymongo>=3.11.2,<4.0.0',
 'sheetscrape>=0.1.0,<0.2.0',
 'tensorstore>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'fibsem-tools',
    'version': '0.1.0',
    'description': 'Tools for processing FIBSEM datasets',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
