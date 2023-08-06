# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['python_jam']
install_requires = \
['aiohttp>=3.7,<4.0', 'python-jwt>=3.3,<4.0']

setup_kwargs = {
    'name': 'python-jam',
    'version': '0.1.0',
    'description': 'Asynchronous python Library for justauthenticate.me authentication',
    'long_description': '# python_jam\n\n[![Build Status](https://travis-ci.org/rickh94/python-jam.svg?branch=main)](https://travis-ci.org/rickh94/python-jam)\n\nAn asynchronous python implementation\nof [Just Authenticate Me](https://justauthenticate.me)\'s REST Api.\n\n# Installation\n\nInstall normally from pypi.org:\n\n`pip install python-jam`\n\nIt depends on [aiohttp](https://github.com/aio-libs/aiohttp), so if aiohttp is installed\nwith extras or speedups, those will be used automatically. It will also\nuse [ujson](https://github.com/ultrajson/ultrajson) for serialization if installed. (\nDefaults to build-in json)\n\n## Basic Usage\n\nCreate the JustAuthenticateMe object by supplying the AppId from you Just Authenticate\nMe app, then call the corresponding functions as needed. The primary ones are in the\nexample below.\n\n```python\nfrom python_jam import (\n    JustAuthenticateMe, JAMUnauthorized, JAMBadRequest,\n    JAMNotVerified\n)\n\njam = JustAuthenticateMe(\'APP_ID\')\n\ntry:\n    await jam.authenticate(\'user@example.com\')\nexcept JAMBadRequest as e:\n    print("Something went wrong", e)\n\ntry:\n    headers, claims = await jam.verify_token(\'user_id_token\')\nexcept JAMNotVerified:\n    print("Unauthorized, invalid token")\n\ntry:\n    new_token = await jam.refresh(\'user_refresh_token\')\nexcept JAMBadRequest as e:\n    print("Refresh not allowed", e)\nexcept JAMUnauthorized:\n    print("invalid refresh token")\n```\n\n## Available Methods\n\nThese are the methods available on a JustAuthenticateMe instance. All Exception inherit\nfrom `JustAuthenticateMeError`. This is also the exception raised by an unexpected\nerror. If the JustAuthenticateMe api returns a message with the error, that is passed\nthrough as exception text.\n\n- `jam.authenticate(email)` - Initialize authentication flow for a user given an email\n  address. Returns `None` on success. Raises `JAMBadRequest` when a 400 bad request is\n  received from justauthenticate.me (usually an invalid email) or `JAMNotFound` When a\n  404 not found is received back from justauthenticate.me\n\n- `jam.verify_token(id_token)` - Verify a JustAuthenticateMe token against jwks (loaded\n  lazily). Call with parameter `id_token` (jwt) from JustAuthenticateMe.\n  Returns `headers, claims`: headers and claims encoded in the user jwt. (passed through\n  from [python-jwt](https://github.com/davedoesdev/python-jwt)) or\n  raises `JAMNotVerified` if verification fails on a token.\n\n- `jam.refresh(refresh_token)` - Refresh id tokens with refresh token. `refresh_token`:\n  user\'s refreshToken from JustAuthenticateMe. Returns: new idToken (JWT) from\n  JustAuthenticateMe. Raises `JAMBadRequest` when app doesn\'t allow refresh or request\n  is malformed. Raises `JAMInvalid` when the refresh token was invalid. Raises\n  `JAMNotFound` when the appId or refresh token was not found.\n\n- `jam.delete_refresh_token(id_token, refresh_token)` - Delete a user\'s refresh token.\n  (i.e. logout) Called with `id_token`: User\'s id token (JWT) from Just Authenticate Me,\n  and `refresh_token`: The refresh token to delete. Returns `None` or\n  raises `JAMUnauthorized` when the id_token is invalid or\n  `JAMNotFound` when the refresh_token or app_id cannot be found\n\n- `jam.delete_all_refresh_tokens(id_token)` - Delete all of a user\'s refresh tokens.\n  (i.e. logout) Called with `id_token`: User\'s id token (JWT) from Just Authenticate Me.\n  Returns `None` or raises `JAMUnauthorized` when the id_token is invalid.\n',
    'author': 'Rick Henry',
    'author_email': 'rickhenry@rickhenry.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
