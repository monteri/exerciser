from ninja.security import HttpBearer

from pdp.api.services.token_utils import decode_token


class AuthenticatedUser(HttpBearer):
    def authenticate(self, request, token: str):
        payload = decode_token(token)
        return payload


auth = AuthenticatedUser()
