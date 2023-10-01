from django.contrib.auth import authenticate

from ninja import Router

from pdp.api.serializers import LoginInput
from pdp.api.utils.token_utils import create_token

auth_router = Router()


@auth_router.post("/login/")
def login(request, input: LoginInput):
    user = authenticate(request, username=input.username, password=input.password)
    if user:
        token_payload = {"username": user.username}
        token = create_token(token_payload)
        return {"token": token}
    return {"error": "Invalid credentials"}, 401
