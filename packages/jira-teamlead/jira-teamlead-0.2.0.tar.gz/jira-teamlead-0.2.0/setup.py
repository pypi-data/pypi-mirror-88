# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jira_teamlead', 'jira_teamlead.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'dataclasses>=0.8,<0.9',
 'jira>=2.0.0,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['jtl = jira_teamlead.__main__:jtl']}

setup_kwargs = {
    'name': 'jira-teamlead',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Aleksey Negramotnov',
    'author_email': 'aleksey.negramotnov@nedra.digital',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.7',
}


setup(**setup_kwargs)
