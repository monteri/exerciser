import datetime

from django.conf import settings

import jwt


def create_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256", exp=expiration)
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None
