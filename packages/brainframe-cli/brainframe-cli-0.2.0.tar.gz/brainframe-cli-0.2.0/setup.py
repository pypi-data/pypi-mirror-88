# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commands']

package_data = \
{'': ['*']}

install_requires = \
['distro>=1.5,<2.0',
 'packaging>=20.4,<21.0',
 'python-i18n>=0.3,<0.4',
 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['brainframe = brainframe.cli.main:main']}

setup_kwargs = {
    'name': 'brainframe-cli',
    'version': '0.2.0',
    'description': 'Makes installing and managing a BrainFrame server easy',
    'long_description': "==============\nBrainFrame CLI\n==============\n\nThe BrainFrame CLI is a tool for installing and managing a BrainFrame server.\n\nInstallation\n------------\n\nThe CLI is installable with Pip. Ubuntu 18.04 and 20.04 are officially\nsupported, but other versions of Linux are expected to work as well.\n\nOn Ubuntu:\n\n.. code-block::\n\n    sudo -H pip3 install brainframe-cli\n\nUpgrading\n---------\n\nPip can be used to upgrade to a new version.\n\n.. code-block::\n\n    sudo -H pip3 install --upgrade brainframe-cli\n\nUsage\n-----\n\nTo install BrainFrame, simply run the ``install`` command as root:\n\n.. code-block::\n\n    sudo brainframe install\n\nBrainFrame can then be controlled like a normal Docker Compose application\nusing the ``compose`` command, which can be run from any directory.\n\n.. code-block::\n\n    brainframe compose up -d\n\nFor more information, take a look at the `Getting Started guide`_.\n\n.. _`Getting Started guide`: https://aotu.ai/docs/getting_started/\n\nContributing\n------------\n\nWe happily take community contributions! If there's something you'd like to\nwork on, but you're not sure how to start, feel free to create an issue on\nGithub and we'll try to point you in the right direction.\n\nWe use a couple formatting tools to keep our code style consistent. If you get\nany CI failures, you can run the following commands to automatically format\nyour code to fit our guidelines:\n\n.. code-block:: bash\n\n    poetry run isort .\n    poetry run black .\n\n",
    'author': 'Aotu',
    'author_email': 'info@aotu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aotuai/brainframe_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
