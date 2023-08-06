# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['noos_tf', 'noos_tf.base']

package_data = \
{'': ['*']}

install_requires = \
['invoke', 'requests']

entry_points = \
{'console_scripts': ['noostf = noos_tf.cli:main.run']}

setup_kwargs = {
    'name': 'noos-tf',
    'version': '0.0.3',
    'description': 'HashiCorp Terraform Cloud API client',
    'long_description': '[![CircleCI](https://circleci.com/gh/noosenergy/noos-terraform.svg?style=svg&circle-token=5d70bf41e76bbad2a187da8db5c0c39f691db452)](https://circleci.com/gh/noosenergy/noos-terraform)\n\n# Noos Energy Terraform Client\n\nA Python client wrapping up HashiCorp\'s Terraform Cloud API.\n\n## Installation\n\nPackage available from the [PyPi repository](https://pypi.org/project/noos-tf/):\n\n    $ pip install noos-tf\n\n## Usage as a library\n\nImport the namespace within your project,\n\n```python\nimport os\nimport noos_tf\n\n# Instantiate client\ntf_client = noos_tf.TerraformClient()\n\n# Authenticate client\ntf_client.set_auth_header(token=os.getenv("TERRAFORM_TOKEN"))\n```\n\nThen query directly from the Terraform Cloud API ; as a example:\n\n* a workspace ID:\n```python\ntf_client.get_workspace_id("myOrganisation", "myWorkspace")\n```\n\n* the variable IDs from a given workspace:\n```python\ntf_client.get_variable_ids("myOrganisation", "myWorkspace")\n```\n\nThe library offers as well some helper functions for more involved workflows, such as:\n\n* updating a variable value:\n```python\nnoos_tf.update_workspace_variable(\n    "myOrganisation",\n    "myWorkspace",\n    os.getenv("TERRAFORM_TOKEN"),\n    "myVariable",\n    "new_value",\n)\n```\n\n* running and applying a plan:\n```python\nnoos_tf.run_workspace_plan(\n    "myOrganisation",\n    "myWorkspace",\n    os.getenv("TERRAFORM_TOKEN"),\n    "Test run",\n)\n```\n\n## Usage as a command line tool\n\nThe above helper functions could be accessed directly from the command line.\n\n```\n$ noostf\n\nUsage: noostf [--core-opts] <subcommand> [--subcommand-opts] ...\n\nSubcommands:\n\n  run      Run a plan in Terraform cloud.\n  update   Update variable in Terraform cloud.\n```\n\n### Development\n\nOn Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,\n\n    $ brew install poetry\n\nThis project is shipped with a Makefile, which is ready to do basic common tasks.\n\n```\n$ make\n\nhelp                           Display this auto-generated help message\nclean                          Clean project from temp files / dirs\nformat                         Run auto-formatting linters\nlint                           Run python linters\ntest                           Run pytest with all tests\npackage                        Build project wheel distribution\nrelease                        Publish wheel distribution to PyPi\n```\n',
    'author': 'Noos Energy',
    'author_email': 'contact@noos.energy',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noosenergy/noos-terraform',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
