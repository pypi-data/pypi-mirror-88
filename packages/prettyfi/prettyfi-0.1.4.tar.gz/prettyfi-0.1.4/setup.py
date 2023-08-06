# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prettyfi']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['prettyfi = prettyfi.main:main']}

setup_kwargs = {
    'name': 'prettyfi',
    'version': '0.1.4',
    'description': 'Simple tool to prettify your files',
    'long_description': '|py_versions| |build_statuses| |pypi_versions|\n\n.. |py_versions| image:: https://img.shields.io/pypi/pyversions/prettyfi?style=flat-square\n    :alt: python versions\n\n.. |build_statuses| image:: https://img.shields.io/github/workflow/status/s3rius/prettyfi/Testing%20and%20publish?style=flat-square\n    :alt: build status\n\n.. |pypi_versions| image:: https://img.shields.io/pypi/v/prettyfi?style=flat-square\n    :alt: pypi version\n    :target: https://pypi.org/project/prettyfi/\n\nPrettify your files with one command\n====================================\n\nPrettyfi usage\n**************\n\nusage: prettyfi [-h] [-c CONFIG] files [files ...]\n\nSimple utility to make your files prettier.\n\npositional arguments:\n  files                 Files to sort\n\noptional arguments:\n    --help                  show help message and exit\n    --config=config_path    path to configuration file\n\n.. code:: bash\n\n    prettyfi "prettyfi/main.py" "pyproject.toml" # Will make this files beautiful\n\nPrettify configuration\n**********************\n\nDefault config file location is "~/.prettyfirc".\n\nConfig file format:\n\n.. code:: bash\n\n    .<ext> $ pretty_command {file}\n    # Where "ext" -> your file extension,\n    # {file} -> stub for actual file,\n    # For example:\n    .py   $ isort {file}\n    .java $ rm {file}',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s3rius/prettyfi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
