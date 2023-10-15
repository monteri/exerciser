from django.contrib.auth.models import User
from django.urls import reverse_lazy

import pytest

from pdp.models import Circle


@pytest.mark.django_db
def test_list_circles(auth_client):
    # Step 1: Create some test data
    user1 = User.objects.create(
        username="testuser1", password="password123", first_name="John", last_name="Doe"
    )
    user2 = User.objects.create(
        username="testuser2",
        password="password123",
        first_name="Jane",
        last_name="Smith",
    )

    # Step 2: Fetch data from the endpoint
    response = auth_client.get(
        reverse_lazy("api:list_circles"), headers=auth_client.headers
    )
    assert response.status_code == 200
    data = response.json()

    # Check the data
    assert len(data) == 2  # We have created 2 users, so there should be 2 circles

    circle_names = [circle_data["circle"]["name"] for circle_data in data]
    assert f"{user1.first_name} {user1.last_name}" in circle_names
    assert f"{user2.first_name} {user2.last_name}" in circle_names

    # Step 3: Test caching by hitting the endpoint again
    cached_response = auth_client.get(
        reverse_lazy("api:list_circles"), headers=auth_client.headers
    )
    assert cached_response.status_code == 200
    cached_data = cached_response.json()

    assert data == cached_data


@pytest.mark.django_db
def test_create_circle(user, auth_client):
    circle_data = {
        "name": "Test Circle",
        "description": "Test Description",
        "status": "TO_DO",
    }

    response = auth_client.post(
        reverse_lazy("api:create_circle"),
        data=circle_data,
        content_type="application/json",
        headers=auth_client.headers,
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_retrieve_circle(user, auth_client):
    circle = Circle.objects.create(
        name="Test Circle",
        description="Test Description",
        status="TO_DO",
        user=user,
    )

    # Use the retrieve_circle route with the circle_id parameter
    response = auth_client.get(
        reverse_lazy("api:retrieve_circle", kwargs={"circle_id": circle.id}),
        headers=auth_client.headers,
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_update_circle(user, auth_client):
    circle = Circle.objects.create(
        name="Test Circle",
        description="Test Description",
        status="TO_DO",
        user=user,
    )
    circle_data = {
        "name": "Updated Circle",
        "description": "Updated Description",
        "status": "IN_PROGRESS",
    }
    response = auth_client.put(
        reverse_lazy("api:update_circle", kwargs={"circle_id": circle.id}),
        data=circle_data,
        content_type="application/json",
        headers=auth_client.headers,
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_circle(user, auth_client):
    circle = Circle.objects.create(
        name="Test Circle",
        description="Test Description",
        status="TO_DO",
        user=user,
    )
    response = auth_client.delete(
        reverse_lazy("api:delete_circle", kwargs={"circle_id": circle.id}),
        headers=auth_client.headers,
    )

    assert response.status_code == 200
