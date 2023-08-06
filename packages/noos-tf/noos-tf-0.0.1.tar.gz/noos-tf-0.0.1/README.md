[![CircleCI](https://circleci.com/gh/noosenergy/noos-terraform.svg?style=svg&circle-token=5d70bf41e76bbad2a187da8db5c0c39f691db452)](https://circleci.com/gh/noosenergy/noos-terraform)

# Noos Energy Terraform Client

A Python client wrapping up HashiCorp's Terraform Cloud API.

## Quickstart

### Installation

On Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,

    $ brew install poetry

### Development

Tests run via `py.test`:

    $ make test

Linting taking care by `flake8` and `mypy`:

    $ make lint

And formatting overviewed by `black` and `isort`:

    $ make format
