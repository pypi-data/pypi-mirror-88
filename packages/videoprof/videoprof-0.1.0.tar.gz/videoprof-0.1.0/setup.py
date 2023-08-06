# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['videoprof']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colored>=1.4.2,<2.0.0',
 'pymediainfo>=5.0.3,<6.0.0']

entry_points = \
{'console_scripts': ['videoprof = videoprof.videoprof:main']}

setup_kwargs = {
    'name': 'videoprof',
    'version': '0.1.0',
    'description': 'Profile various attributes of local videos like resolution, codec, container, audio channels, and more!',
    'long_description': None,
    'author': 'Christian Lent',
    'author_email': 'christian@lent.us',
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
