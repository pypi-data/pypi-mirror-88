""" Settings config for the drf_keycloak_auth application """
import datetime
import os

from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'DRF_KEYCLOAK_AUTH', None)

DEFAULTS = {
    'KEYCLOAK_SERVER_URL': os.getenv('KEYCLOAK_SERVER_URL'),
    'KEYCLOAK_REALM': os.getenv('KEYCLOAK_REALM'),
    'KEYCLOAK_CLIENT_ID': os.getenv('KEYCLOAK_CLIENT_ID'),
    'KEYCLOAK_CLIENT_SECRET_KEY': os.getenv('KEYCLOAK_CLIENT_SECRET_KEY'),
    'KEYCLOAK_AUTH_HEADER_PREFIX':
        os.getenv('KEYCLOAK_AUTH_HEADER_PREFIX', 'Bearer'),
    'KEYCLOAK_MANAGE_LOCAL_USER':
        os.getenv('KEYCLOAK_MANAGE_LOCAL_USER', True),
    'KEYCLOAK_MANAGE_LOCAL_GROUPS':
        os.getenv('KEYCLOAK_MANAGE_LOCAL_GROUPS', False),
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
