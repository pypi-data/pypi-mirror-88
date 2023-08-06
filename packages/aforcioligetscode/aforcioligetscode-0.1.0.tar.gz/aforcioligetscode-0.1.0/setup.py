# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aforcioligetscode']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['getscode = '
                     'aforcioligetscode.script:get_url_and_print_status_code']}

setup_kwargs = {
    'name': 'aforcioligetscode',
    'version': '0.1.0',
    'description': 'Print the HTTP status code for an HTTP GET',
    'long_description': None,
    'author': 'Alain Forcioli',
    'author_email': 'aforcioli@fortinet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/al1foobar/aforcioligetscode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
