# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oebl_irs_workflow', 'oebl_irs_workflow.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.4,<4.0.0',
 'apis-core>=0.15.0,<0.16.0',
 'djangorestframework>=3.12.2,<4.0.0']

setup_kwargs = {
    'name': 'oebl-irs-workflow',
    'version': '0.1.2',
    'description': 'Workflow module for the IRS extension of the APIS framework',
    'long_description': None,
    'author': 'Matthias Schlögl',
    'author_email': 'm.schloegl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
