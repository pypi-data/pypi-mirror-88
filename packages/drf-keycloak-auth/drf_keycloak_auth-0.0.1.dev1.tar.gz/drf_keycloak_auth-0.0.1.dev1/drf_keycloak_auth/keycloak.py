""" module for app specific keycloak connection """
from typing import Dict, List

from django.conf import settings
from keycloak import KeycloakOpenID


try:
    keycloak_openid = KeycloakOpenID(
        server_url=settings.KEYCLOAK_CONFIG['KEYCLOAK_SERVER_URL'],
        realm_name=settings.KEYCLOAK_CONFIG['KEYCLOAK_REALM'],
        client_id=settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_ID'],
        client_secret_key=(
            settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_SECRET_KEY']
        )
    )
except KeyError as e:
    raise KeyError(
        f'invalid settings.KEYCLOAK_CONFIG: {e}'
    )


def get_resource_roles(decoded_token: Dict) -> List[str]:
    # Get roles from access token
    resource_access_roles = []
    try:
        resource_access_roles = (
            decoded_token['resource_access']
            [settings.KEYCLOAK_CONFIG['KEYCLOAK_CLIENT_ID']]
            ['roles']
        )
        return [f'role:{x}' for x in resource_access_roles]
    except Exception as _:
        return []
