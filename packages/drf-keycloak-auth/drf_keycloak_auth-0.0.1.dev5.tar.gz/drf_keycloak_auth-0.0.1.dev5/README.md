# DRF Keycloak Auth

## Requirements


* Python >= 3.4
* Django
* Django Rest Framework
* Python Keycloak


## Installation

```
$ pip install drf-keycloak-auth
```

Add the application to your project's `INSTALLED_APPS` in `settings.py`.

```
INSTALLED_APPS = [
    ...
    'drf_keycloak_auth',
]
```

In your project's `settings.py`, add this to the `REST_FRAMEWORK` configuration. Note that if you want to retain access to the browsable API for locally created users, then you will probably want to keep `rest_framework.authentication.SessionAuthentication` too.

```
REST_FRAMEWORK = {
  ...
  'DEFAULT_AUTHENTICATION_CLASSES': [
    ...
    'rest_framework.authentication.SessionAuthentication',
    'drf_keycloak_auth.authentication.KeycloakAuthentication',
  ]
}
```

and add this to the `MIDDLEWARE` configuration to parse roles from the JWT

```
MIDDLEWARE = [
    ...
    'drf_keycloak_auth.middleware.KeycloakMiddleware'
]
```


The `drf_keycloak_auth` application comes with the following settings as default, which can be overridden in your project's `settings.py` file. Make sure to nest them within `DRF_KEYCLOAK_AUTH` as below:


```
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
```

All you need to do now is have your client code handle the Keycloak authentication flow, retrieve the access_token for the user, and then use the access_token for the user in an `Authorization` header in requests to your API.

```
Bearer <token>
```

Roles will be present in `request.roles` with a `role:` prefix, e.g.:

```
['role:admin', 'a4a9be6e-bd04-42f8-9377-27d9db82216f']
```

except for the authenticated user's pk field, e.g. for a user model using uuid's as primary key:

```
['role:user', 'a4a9be6e-bd04-42f8-9377-27d9db82216f']
```

where the pk can be used for checking object ownership.


Voila!

## Contributing

* Please raise an issue/feature and name your branch 'feature-n' or 'issue-n', where 'n' is the issue number.
