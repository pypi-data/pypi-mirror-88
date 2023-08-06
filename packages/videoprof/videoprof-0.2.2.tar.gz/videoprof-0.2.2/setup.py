# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['videoprof']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colored>=1.4.2,<2.0.0',
 'pymediainfo>=5.0.3,<6.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['videoprof = videoprof.videoprof:main']}

setup_kwargs = {
    'name': 'videoprof',
    'version': '0.2.2',
    'description': 'Video Profiler - profile various attributes of local videos like resolution, codec, container, audio channels, and more!',
    'long_description': '# videoprof - A CLI Video Profiler for Python\n\nProfile various attributes of local videos like resolution, codec, container, audio channels, and more!\n\n## Installation\n\nTo install, you can add the "videoprof" package from pip:\n\n```bash\npip3 install --user --upgrade videoprof\n```\n\n## Requirements\n\n### libmediainfo\n\nThis application can not work without libmediainfo. To install libmediainfo on Debian or Ubuntu:\n\n```bash\napt-get install libmediainfo0v5\n```\n\nIf you see a message like the following, it must not be installed:\n\n```\nCould not analyze videos: make sure libmediainfo is installed!\n```\n\n### A Compatible Python version:\n\n- 3.6\n- 3.7\n- 3.8\n- 3.9\n\n## Usage\n\n```\nUsage: videoprof [OPTIONS] [SOURCES]...\n\nOptions:\n  -c, --config TEXT              JSON configuration file\n  -s, --sqlite-cache TEXT        SQLite cache file\n  -f, --files                    Show individual file badges and exit\n  -d, --directories              Show directory badges and exit\n  -p, --directory-depth INTEGER  Directory depth for summaries\n  -o, --only-flagged             Only show individual files or directories on\n                                 flagged entries\n\n  -m, --media-info               Show media info for the first found file and\n                                 exit\n\n  --help                         Show this message and exit.\n```\n\n## Screenshots\n\nSummary view:\n\n![videoprof summary view](images/summary.png)\n\nDirectory view:\n\n![videoprof directory view](images/directories.png)\n\nFlaged directory view:\n\n![videoprof flagged directory view](images/flagged.png)\n\n## Configuration\n\nVideoprof is very configurable - any attribute that is returned by mediainfo can be profiled. When videoprof is first run, it will generate a default configuration in `~/.config/videoprof/config.json` (on POSIX/Linux systems).\n\nThe [default configuration](videoprof/default_config.json) mostly codifies Blu-Ray specs as "success", DVD specs as "warning", and everything else as an error. While simple, it does contain most features useable within the configuration and can be used as a reference.\n',
    'author': 'Christian Lent',
    'author_email': 'christian@lent.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
