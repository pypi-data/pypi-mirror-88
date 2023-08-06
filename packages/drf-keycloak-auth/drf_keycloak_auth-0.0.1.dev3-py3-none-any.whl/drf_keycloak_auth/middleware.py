import logging
from typing import List

from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import Group

from .keycloak import get_resource_roles
from . import __title__
from .settings import api_settings

log = logging.getLogger(__title__)


class KeycloakMiddleware:

    def __init__(self, get_response):     
        # Django response
        self.get_response = get_response

    def __call__(self, request):
        log.debug('KeycloakMiddleware.__call__')
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs) -> None:
        """
        middleware lifecyle method where view has been determined
        
        SimpleLazyObject required as KeycloakMiddleware is called BEFORE
        KeycloakAuthentication
        """
        log.debug('KeycloakMiddleware.process_view')
        # SimpleLazyObject required as KeycloakMiddleware is called BEFORE KeycloakAuthentication
        request.roles = SimpleLazyObject(lambda: self._bind_roles_to_request(request))

    def _bind_roles_to_request(self, request) -> List[str]:
        """ try to add roles from authenticated keycloak user """
        roles = []
        try:
            roles += get_resource_roles(request.auth)
            roles.append(str(request.user.pk))
        except Exception as e:
            log.warn(
                f'KeycloakMiddleware._bind_roles_to_request - Exception: {e}'
            )

        if api_settings.KEYCLOAK_MANAGE_LOCAL_GROUPS is True:
            groups = self._get_or_create_groups(roles)
            self._refresh_user_groups(request, groups)

        log.info(f'KeycloakMiddleware.bind_roles_to_request: {roles}')
        return roles

    def _get_or_create_groups(self, roles: List[str]) -> List[Group]:
        groups = []
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                log.info(
                    'KeycloakMiddleware._get_or_create_groups - created: '
                    f'{group.name}'
                )
            else:
                log.info(
                    'KeycloakMiddleware._get_or_create_groups - exists: '
                    f'{group.name}'
                )
            groups.append(group)
        return groups

    def _refresh_user_groups(self, request, groups: List[Group]) -> None:
        try:
            # request.user.groups.clear()
            log.info(
                'KeycloakMiddleware._refresh_user_groups: '
                f'{[x.name for x in groups]}'
            )
            request.user.groups.set(groups)  # clears no longer existing groups
        except Exception as e:
            log.warn(
                f'KeycloakMiddleware._refresh_user_groups - exception: {e}'
            )
