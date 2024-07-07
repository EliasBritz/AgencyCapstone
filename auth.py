import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from config import AUTH_DOMAIN, ALGORITHMS, API_AUDIENCE

# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
   # check if authorization is not in request
    if 'Authorization' not in request.headers:
        raise AuthError('Authorization header is expected', 401)
    
    # get the token   
    auth_header = request.headers['Authorization']

    try:
        header_parts = auth_header.split(' ')
    except Exception as e:
        raise AuthError('Authorization header must be in the format "bearer token"', 401) from e

    # check if token is valid
    if len(header_parts) != 2:
        raise AuthError('Authorization header must be in the format "bearer token"', 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError('Authorization header must start with "bearer"', 401)
    return header_parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError as e:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401) from e

        except jwt.JWTClaimsError as e:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401) from e
        
        except Exception as e:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400) from e
  
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def requires_auth(permission='', Test_config=False):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = None
            if not Test_config:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator