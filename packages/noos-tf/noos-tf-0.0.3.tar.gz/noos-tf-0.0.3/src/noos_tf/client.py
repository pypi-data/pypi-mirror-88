# https://www.terraform.io/docs/cloud/api/index.html
from http import client as http_client
from typing import Dict

from .base import auth_client


__all__ = ["TerraformClient"]


class TerraformAuth(auth_client.HTTPTokenAuth):
    default_header = "Authorization"
    default_value = "Bearer"


class TerraformClient(auth_client.AuthClient):
    default_base_url = "https://app.terraform.io/api/"

    default_headers = {"Content-Type": "application/vnd.api+json"}
    default_auth_class = TerraformAuth

    def get_workspace_id(self, organization: str, workspace: str) -> str:
        """Get the ID of a given workspace for a organization."""
        response = self._get(
            path=f"v2/organizations/{organization}/workspaces/{workspace}",
            statuses=(http_client.OK,),
        )
        return response["data"]["id"]

    def get_variable_ids(self, organization: str, workspace: str) -> Dict[str, str]:
        """Get variable IDs stored onto a given workspace for a organization."""
        params = {
            "filter[organization][name]": organization,
            "filter[workspace][name]": workspace,
        }
        response = self._get(
            path="v2/vars",
            params=params,
            statuses=(http_client.OK,),
        )
        return {var["attributes"]["key"]: var["id"] for var in response["data"]}

    def update_variable(self, variable_id: str, value: str) -> None:
        """Update the value of a variable stored onto a given workspace for a organization."""
        data = {
            "data": {
                "type": "vars",
                "id": variable_id,
                "attributes": {"value": value},
            }
        }
        self._patch(
            path=f"v2/vars/{variable_id}",
            data=data,
            statuses=(http_client.OK,),
        )

    def run_plan(self, workspace_id: str, message: str) -> str:
        """Run a plan onto a given workspace for a organization."""
        data = {
            "data": {
                "type": "runs",
                "attributes": {"is-destroy": False, "message": message},
                "relationships": {
                    "workspace": {"data": {"type": "workspaces", "id": workspace_id}}
                },
            }
        }
        response = self._post(
            path="v2/runs",
            data=data,
            statuses=(http_client.CREATED,),
        )
        return response["data"]["id"]
