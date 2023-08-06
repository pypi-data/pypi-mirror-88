# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow',
 'flow.cli',
 'flow.cli.commands',
 'flow.cli.helpers',
 'flow.cli.helpers.login',
 'flow.cli.models',
 'flow.cli.tests',
 'flow.cli.tests.commands',
 'flow.cli.tests.helpers',
 'flow.cli.tests.helpers.iam_policies',
 'flow.cli.tests.helpers.login']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'analytics-python>=1.2.9,<2.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'immutables>=0.14,<0.15',
 'pkce>=1.0,<2.0',
 'policy-sentry==0.9.0',
 'policyuniverse>=1.3.2,<2.0.0',
 'portalocker>=2.0.0,<3.0.0',
 'sentry-sdk>=0.19.3,<0.20.0',
 'sym-cli>=0.0.60,<0.0.61',
 'validators>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['symflow = sym.flow.cli.symflow:symflow']}

setup_kwargs = {
    'name': 'sym-flow-cli',
    'version': '0.0.57',
    'description': 'The Flow CLI for Sym',
    'long_description': "# sym-flow-cli\n\nSym Flow CLI\n\n## Usage\n\n### Login\n\n`symflow login` is used to authenticate a user and write credentials to the local filesystem. \n\nFirst, the CLI asks a user for their email address. From the address, Sym should be able to resolve the user's \norganization and then the user can log in with one of two authorization flows:\n\n#### (Preferred) Auth Code Flow with PKCE\n\n`symflow login`\n\nThe CLI will perform authorization with the Sym auth provider, by opening the browser and asking the user\nto login with their Identity Provider. If successful, this returns a code to the CLI that can be used to \nsecurely acquire an access token. \n\n#### (If necessary) Password Owner Resource Flow\n\n`symflow login --no-browser` can be used to perform a username-password flow. It will prompt the user, and then \nsend these credentials to the Sym auth provider in exchange for an access token. \n\nThis requires special setup in the Sym auth provider to verify the password against a database connection. \n",
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/symopsio/sym-flow-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
