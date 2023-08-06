# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abq']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=1.25.0,<2.0.0',
 'httpx==0.13.3',
 'oauth2client>=4.1.3,<5.0.0',
 'pydantic[dotenv]>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'abq',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'sakuv2',
    'author_email': 'loots2438@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
