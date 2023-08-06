# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['penvy',
 'penvy.bash',
 'penvy.check',
 'penvy.cli',
 'penvy.cmd',
 'penvy.conda',
 'penvy.container',
 'penvy.dotenv',
 'penvy.env',
 'penvy.filesystem',
 'penvy.git',
 'penvy.logger',
 'penvy.logger.colorlog',
 'penvy.parameters',
 'penvy.poetry',
 'penvy.python',
 'penvy.setup',
 'penvy.shell',
 'penvy.string',
 'penvy.tear_down']

package_data = \
{'': ['*'], 'penvy.conda': ['activate.d/*', 'deactivate.d/*']}

entry_points = \
{'console_scripts': ['penvy-init = penvy.init:main']}

setup_kwargs = {
    'name': 'penvy',
    'version': '1.0.4b1',
    'description': 'Pyfony framework development environment initializer',
    'long_description': "# Penvy - Pyfony development environment\n\nfor the [Pyfony framework](https://github.com/pyfony/pyfony)\n\n### What it does:\n\n* Prepares the **Conda-based python dev environment** in the project's **.venv directory**\n* Installs the [Poetry package manager](https://python-poetry.org/) into the user's home dir\n* Installs all the dependencies defined in project's **poetry.lock** file\n* Sets conda activation & deactivation scripts (mostly setting environment variables based on the project's **.env file**)\n* Copies the project's **.env file** from the **.env.dist** template file\n* Adds `poetry install --no-root` to post-merge GIT hook \n",
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/penvy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
