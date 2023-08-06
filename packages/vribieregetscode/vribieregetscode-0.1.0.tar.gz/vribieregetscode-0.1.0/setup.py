# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vribieregetscode']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['getscode = '
                     'vribieregetscode.script:get_url_and_print_status_code']}

setup_kwargs = {
    'name': 'vribieregetscode',
    'version': '0.1.0',
    'description': 'Print the HTTP status code for an HTTP GET',
    'long_description': None,
    'author': 'Vincent Ribiere',
    'author_email': 'vribiere@fortinet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/fortinet_vincent/vribieregetscode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
