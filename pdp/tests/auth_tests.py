import json

from django.urls import reverse

import pytest

from pdp.api.services.token_utils import create_tokens


@pytest.mark.django_db
def test_login_successful(anonymous_client, user):
    login_url = reverse("api:login")  # Assuming 'login' is the name of your login route
    response = anonymous_client.post(
        login_url,
        data={
            "username": "testuser",
            "password": "password123",
        },
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.content)
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.django_db
def test_login_failed(anonymous_client):
    login_url = reverse("api:login")
    response = anonymous_client.post(
        login_url,
        data={
            "username": "testuser",
            "password": "wrongpassword",
        },
        content_type="application/json",
    )
    assert response.status_code == 401
    data = json.loads(response.content)
    assert "detail" in data
    assert data["detail"] == "Invalid credentials"


@pytest.mark.django_db
def test_refresh_token_successful(anonymous_client, user):
    _, refresh_token = create_tokens(user.id)
    refresh_url = reverse("api:refresh_token")
    response = anonymous_client.post(
        refresh_url, data={"refresh": refresh_token}, content_type="application/json"
    )
    print("HEYY", response.content)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert "access_token" in data


@pytest.mark.django_db
def test_refresh_token_failed(anonymous_client):
    refresh_url = reverse("api:refresh_token")
    response = anonymous_client.post(
        refresh_url,
        data={"refresh": "invalid_token"},
        content_type="application/json",
    )
    assert response.status_code == 401
    data = json.loads(response.content)
    assert "detail" in data
    assert data["detail"] == "Invalid token"
