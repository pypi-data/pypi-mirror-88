# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['noos_tf', 'noos_tf.base']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'noos-tf',
    'version': '0.0.1',
    'description': 'HashiCorp Terraform Cloud API client',
    'long_description': "[![CircleCI](https://circleci.com/gh/noosenergy/noos-terraform.svg?style=svg&circle-token=5d70bf41e76bbad2a187da8db5c0c39f691db452)](https://circleci.com/gh/noosenergy/noos-terraform)\n\n# Noos Energy Terraform Client\n\nA Python client wrapping up HashiCorp's Terraform Cloud API.\n\n## Quickstart\n\n### Installation\n\nOn Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,\n\n    $ brew install poetry\n\n### Development\n\nTests run via `py.test`:\n\n    $ make test\n\nLinting taking care by `flake8` and `mypy`:\n\n    $ make lint\n\nAnd formatting overviewed by `black` and `isort`:\n\n    $ make format\n",
    'author': 'Noos Energy',
    'author_email': 'contact@noos.energy',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noosenergy/noos-terraform',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
