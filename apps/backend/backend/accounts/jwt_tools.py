import jwt
from jwt import decode as jwt_decode

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

def generate(obj_user):
    refresh = RefreshToken.for_user(obj_user)
    return refresh.access_token

def verify(token):
    payload = False
    result = True
    msg = "access"
    try:
        payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        result = False
        msg = "Signature has expired."
    except jwt.DecodeError:
        result = False
        msg = "Error decoding signature."
    except jwt.InvalidTokenError:
        result = False
        msg = "Invalid token."

    return result, msg

