# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunktalib',
 'splunktalib.common',
 'splunktalib.concurrent',
 'splunktalib.conf_manager',
 'splunktalib.schedule',
 'splunktalib.tests',
 'splunktalib.tests.splunktaucclib.functional']

package_data = \
{'': ['*'],
 'splunktalib.tests': ['data/*', 'data/package/*', 'data/package/default/*']}

install_requires = \
['httplib2>=0.18,<0.19', 'sortedcontainers>=2.2,<3.0']

setup_kwargs = {
    'name': 'splunktalib',
    'version': '1.1.6',
    'description': 'Supporting library for Splunk Add-ons',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/splunk/addonfactory-ta-library-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
