from django.contrib.auth import authenticate
from django.http import JsonResponse

from ninja import Router
from ninja.errors import HttpError

from pdp.api.serializers import LoginInput, RefreshInput
from pdp.api.services.token_utils import create_tokens, decode_token

auth_router = Router()


@auth_router.post("/login/")
def login(request, input: LoginInput):
    user = authenticate(request, username=input.username, password=input.password)
    if user:
        access_token, refresh_token = create_tokens(user.id)
        return JsonResponse(
            {"access_token": access_token, "refresh_token": refresh_token}
        )
    raise HttpError(status_code=401, message="Invalid credentials")


@auth_router.post("/refresh/")
def refresh_token(request, input: RefreshInput):
    payload = decode_token(input.refresh, "refresh")
    if not payload:
        raise HttpError(status_code=401, message="Invalid token")

    access_token, _ = create_tokens(payload["user_id"])
    return JsonResponse({"access_token": access_token})
