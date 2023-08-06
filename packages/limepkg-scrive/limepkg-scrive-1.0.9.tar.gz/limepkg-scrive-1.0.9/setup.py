# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['limepkg_scrive', 'limepkg_scrive.config', 'limepkg_scrive.web_components']

package_data = \
{'': ['*'],
 'limepkg_scrive': ['frontend/*',
                    'frontend/src/*',
                    'frontend/src/components/lwc-limepkg-scrive-loader/*',
                    'frontend/src/components/lwc-limepkg-scrive-test/*']}

install_requires = \
['lime-crm>=2.76.0,<3.0.0']

entry_points = \
{'lime_plugins': ['limepkg-scrive = limepkg_scrive']}

setup_kwargs = {
    'name': 'limepkg-scrive',
    'version': '1.0.9',
    'description': 'Scrive eSigning',
    'long_description': None,
    'author': 'Scrive AB',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
