from django.contrib.auth.models import User
from django.urls import reverse_lazy

import pytest

from pdp.models import Circle


@pytest.mark.django_db
def test_full_text_search(user, auth_client):
    test_circle = Circle.objects.create(
        name="Test Circle",
        description="This is a test circle for full-text search.",
        status="TO_DO",
        user=user,
    )

    test_user = User.objects.create(
        username="test_user",
        email="test_user@example.com",
        first_name="Test",
        last_name="User",
    )

    # Make a request to the full_text_search endpoint
    response = auth_client.get(
        f"{reverse_lazy('api:full_text_search')}?query=test",
        headers=auth_client.headers,
    )

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the response contains the expected structure with "users" and "circles"
    assert "users" in response.json()
    assert "circles" in response.json()

    # Check if the test circle is present in the "circles" result
    assert any(
        test_circle.name == circle["name"] for circle in response.json()["circles"]
    )

    # Check if the test user is present in the "users" result
    assert any(
        test_user.username == user["username"] for user in response.json()["users"]
    )
