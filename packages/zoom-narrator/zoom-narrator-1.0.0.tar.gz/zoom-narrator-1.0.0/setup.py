# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zoom_narrator', 'zoom_narrator.test']

package_data = \
{'': ['*'], 'zoom_narrator.test': ['fixtures/*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0',
 'asyncclick>=7.1.2,<8.0.0',
 'pysubs2>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['zoom-narrator = zoom_narrator.main:main']}

setup_kwargs = {
    'name': 'zoom-narrator',
    'version': '1.0.0',
    'description': 'Play audio while streaming its closed captions to Zoom',
    'long_description': None,
    'author': 'Daniel Maxwell-Ross',
    'author_email': 'daniel@maxwell-ross.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
