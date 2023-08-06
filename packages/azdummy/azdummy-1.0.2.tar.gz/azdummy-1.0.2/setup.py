# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azdummy', 'azdummy.commands', 'azdummy.core']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9,<0.10',
 'mimesis>=4.1.2,<5.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'rich>=9.3.0,<10.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['azdummy = azdummy.main:app']}

setup_kwargs = {
    'name': 'azdummy',
    'version': '1.0.2',
    'description': 'A Python Typer-based CLI tool to generate fake data for Azure AD.',
    'long_description': '<div align="center">\n    <img src="https://github.com/daddycocoaman/AzDummy/raw/main/docs/images/AzDummy.png" width="400px" height="400px"/>\n</div>\n\n<div align="center">\n    <img src="https://img.shields.io/pypi/v/azdummy"/>\n    <img src="https://img.shields.io/pypi/pyversions/azdummy"/>\n    <img src="https://img.shields.io/pypi/l/azdummy"/>\n    <a href="https://twitter.com/mcohmi"><img src="https://img.shields.io/twitter/follow/mcohmi.svg?style=plastic"/></a>\n</div>\n\n# AzDummy\nA Python [Typer-based](https://github.com/tiangolo/typer) CLI tool to generate fake data for Azure AD. AzDummy also uses [Rich](https://github.com/willmcgugan/rich) for some dope console output.\n\n## Installation\n\nThe recommended method of installation is with [pipx](https://github.com/pipxproject/pipx). \n\n```\npipx install azdummy\n```\n\nHowever, you can install the normal way from PyPi with `python3 -m pip install azdummy`.\n\n## Usage\n\nOn first run, user will be prompted to create a config file. Location of this config file depends on OS. **Note: There are some environment variables included that are currently not used.**\n\n- Windows: \n  - `C:\\Users\\<user>\\AppData\\Roaming\\azdummy\\settings.env`\n- Linux/Mac OS: \n  - `~/.azdummy/settings.env`\n\nCurrently used variables:\n\n- **AZD_LOCALE**: (str) Two-letter shortcode for supported locales\n- **AZD_TENANT_FQDN**: (str) One of the domains in the tenant (Usually `<domain>.onmicrosoft.com` format)\n- **AZD_NUM_USERS**: (int) Number of users to generate  \n- **AZD_BLOCK_LOGIN**: (bool) Block generated users from logging in\n- **AZD_GROUP_NAMES**: (list) List of groups to add users to\n\n**NOTE: Due to restrictions on the userPrincipalName field, all names are generated in English. However, AzDummy supports other locale-specific data generation (such as addresses).**\n\n**Supported Locales:**\n- CZECH = "cs"\n- DANISH = "da"\n- GERMAN = "de"\n- AUSTRIAN_GERMAN = "de-at"\n- SWISS_GERMAN = "de-ch"\n- GREEK = "el"\n- ENGLISH = "en"\n- AUSTRALIAN_ENGLISH = "en-au"\n- CANADIAN_ENGLISH = "en-ca"\n- BRITISH_ENGLISH = "en-gb"\n- SPANISH = "es"\n- MEXICAN_SPANISH = "es-mx"\n- ESTONIAN = "et"\n- FARSI = "fa"\n- FINNISH = "fi"\n- FRENCH = "fr"\n- HUNGARIAN = "hu"\n- ICELANDIC = "is"\n- ITALIAN = "it"\n- JAPANESE = "ja"\n- KAZAKH = "kk"\n- KOREAN = "ko"\n- DUTCH = "nl"\n- BELGIUM_DUTCH = "nl-be"\n- NORWEGIAN = "no"\n- POLISH = "pl"\n- PORTUGUESE = "pt"\n- BRAZILIAN_PORTUGUESE = "pt-br"\n- RUSSIAN = "ru"\n- SLOVAK = "sk"\n- SWEDISH = "sv"\n- TURKISH = "tr"\n- UKRAINIAN = "uk"\n- CHINESE = "zh"\n## Commands\n\nCommands are available [here](docs/commands.md). You can generally use `--help/-h` for any command or subcommand for more information. With default settings, the following command will generate 500 users for `azdummy.onmicrosoft.com` (non-existant tenant).\n\n`azdummy gen users` \n\n## What do I do with the output?\n\nThe default output provides two files: `output_create.csv` and `output_create.csv`. These files can be used with the Bulk Create and Bulk Delete options in Azure Portal in the Azure AD Users menu. \n',
    'author': 'Leron Gray',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daddycocoaman/AzDummy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
