from django.contrib.auth import authenticate
from django.http import JsonResponse

from ninja import Router

from pdp.api.serializers import LoginInput
from pdp.api.utils.token_utils import create_tokens, decode_token

auth_router = Router()


@auth_router.post("/login/")
def login(request, input: LoginInput):
    user = authenticate(request, username=input.username, password=input.password)
    if user:
        access_token, refresh_token = create_tokens(user.id)
        return JsonResponse(
            {"access_token": access_token, "refresh_token": refresh_token}
        )
    return JsonResponse({"error": "Invalid credentials"}, status=401)


@auth_router.post("/refresh/")
def refresh_token(request, refresh: str):
    payload = decode_token(refresh, "refresh")
    if not payload:
        return JsonResponse({"error": "Invalid token"}, status=401)

    access_token, _ = create_tokens(payload["user_id"])
    return JsonResponse({"access_token": access_token})
