""" add a keycloak authentication class specific to Django Rest Framework """
from typing import Tuple, Dict
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework import (
    authentication,
    exceptions,
)

from .keycloak import keycloak_openid
from .settings import api_settings
from . import __title__

log = logging.getLogger(__title__)
User = get_user_model()


class KeycloakAuthentication(authentication.TokenAuthentication):
    keyword = api_settings.KEYCLOAK_AUTH_HEADER_PREFIX

    def authenticate_credentials(
        self,
        token: str
    ) -> Tuple[AnonymousUser, Dict]:
        """ Attempt to verify JWT from Authorization header with Keycloak """
        log.debug('KeycloakAuthentication.authenticate_credentials')
        try:
            user = None
            # Checks token is active
            decoded_token = keycloak_openid.introspect(token)
            is_active = decoded_token.get('active', False)
            if not is_active:
                raise exceptions.AuthenticationFailed(
                    'invalid or expired token'
                )
            if api_settings.KEYCLOAK_MANAGE_LOCAL_USER is not True:
                log.info(
                    'KeycloakAuthentication.authenticate_credentials: '
                    f'{decoded_token}'
                )
                user = AnonymousUser()
            else:
                username = decoded_token['sub']
                email = decoded_token['email']
                # django stores first_name and last_name as empty strings
                # by default, not None
                first_name = decoded_token.get('given_name', '')
                last_name = decoded_token.get('family_name', '')
                try:
                    user = User.objects.get(username=username)
                    user_values = (user.email, user.first_name, user.last_name,)
                    token_values = (email, first_name, last_name,)
                    if user_values != token_values:
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()
                except ObjectDoesNotExist:
                    log.warn(
                        'KeycloakAuthentication.authenticate_credentials - '
                        f'ObjectDoesNotExist: {username} does not exist'
                    )
                if user is None:
                    user = User.objects.create_user(
                        username,
                        email,
                        None  # if None set_unusable_password() will be called.
                    )
            log.info(
                'KeycloakAuthentication.authenticate_credentials: '
                f'{user} - {decoded_token}'
            )
            return (user, decoded_token)
        except Exception as e:
            log.error(
                'KeycloakAuthentication.authenticate_credentials - '
                f'Exception: {e}'
            )
            raise exceptions.AuthenticationFailed()
