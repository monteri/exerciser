import datetime

from django.conf import settings

import jwt


def create_tokens(user_id: int):
    access_expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    access_token = jwt.encode(
        {"user_id": user_id, "exp": access_expiration, "type": "access"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    refresh_token = jwt.encode(
        {"user_id": user_id, "exp": refresh_expiration, "type": "refresh"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    return access_token, refresh_token


def decode_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != token_type:
            return None
        return payload
    except jwt.PyJWTError:
        return None
