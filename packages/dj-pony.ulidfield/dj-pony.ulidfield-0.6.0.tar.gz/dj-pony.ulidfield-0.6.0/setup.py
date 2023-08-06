# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_pony', 'dj_pony.ulidfield']

package_data = \
{'': ['*'],
 'dj_pony.ulidfield': ['static/css/*',
                       'static/img/*',
                       'static/js/*',
                       'templates/dj_pony_ulidfield/*']}

install_requires = \
['django>=2.2', 'ulid-py>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'dj-pony.ulidfield',
    'version': '0.6.0',
    'description': 'A ULID Field for Django that does all the work for you.',
    'long_description': None,
    'author': 'Samuel Bishop',
    'author_email': 'sam@techdragon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
