# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mopidy_ytmusic']

package_data = \
{'': ['*']}

install_requires = \
['Mopidy>=3.0.2,<4.0.0',
 'youtube_dl>=2020.12.9,<2021.0.0',
 'ytmusicapi>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'mopidy-ytmusic',
    'version': '0.1.2',
    'description': 'Mopidy extension for playling music/managing playlists in Youtube Music',
    'long_description': None,
    'author': 'Ozymandias (Tomas Ravinskas)',
    'author_email': 'tomas.rav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
