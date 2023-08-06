""" module for app specific keycloak connection """
from typing import Dict, List

from keycloak import KeycloakOpenID

from .settings import api_settings

try:
    keycloak_openid = KeycloakOpenID(
        server_url=api_settings.KEYCLOAK_SERVER_URL,
        realm_name=api_settings.KEYCLOAK_REALM,
        client_id=api_settings.KEYCLOAK_CLIENT_ID,
        client_secret_key=api_settings.KEYCLOAK_CLIENT_SECRET_KEY
    )
except KeyError as e:
    raise KeyError(
        f'invalid settings: {e}'
    )


def get_resource_roles(decoded_token: Dict) -> List[str]:
    # Get roles from access token
    resource_access_roles = []
    try:
        resource_access_roles = (
            decoded_token['resource_access']
            [api_settings.KEYCLOAK_CLIENT_ID]
            ['roles']
        )
        return [f'role:{x}' for x in resource_access_roles]
    except Exception as _:
        return []
