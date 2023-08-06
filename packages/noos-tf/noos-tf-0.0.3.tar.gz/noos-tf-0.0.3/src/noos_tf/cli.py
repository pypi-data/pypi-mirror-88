# Using `invoke` as library
# http://docs.pyinvoke.org/en/stable/concepts/library.html
import os

from invoke import Collection, Program, task

from . import __version__, api


@task
def update(ctx, variable="", value="", workspace="", organisation=None, token=None):
    """Update variable in Terraform cloud."""
    organisation = organisation or os.getenv("TERRAFORM_USER")
    token = token or os.getenv("TERRAFORM_TOKEN")
    assert organisation is not None, "Missing Terraform Cloud organisation."
    assert token is not None, "Missing Terraform Cloud token."
    api.update_workspace_variable(organisation, workspace, token, variable, value)
    print(f"Updated Terraform {variable} for {workspace}")


@task
def run(ctx, message="", workspace="", organisation=None, token=None):
    """Run a plan in Terraform cloud."""
    organisation = organisation or os.getenv("TERRAFORM_USER")
    token = token or os.getenv("TERRAFORM_TOKEN")
    assert organisation is not None, "Missing Terraform Cloud organisation."
    assert token is not None, "Missing Terraform Cloud token."
    url = api.run_workspace_plan(organisation, workspace, token, message)
    print(f"Running Terraform plan for {workspace}: {url}")


ns = Collection()
ns.add_task(update)
ns.add_task(run)


main = Program(namespace=ns, version=__version__)
