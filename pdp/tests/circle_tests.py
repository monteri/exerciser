from django.urls import reverse_lazy

import pytest

from pdp.models import Circle


@pytest.mark.django_db
def test_list_circles(user, auth_client):
    response = auth_client.get(
        reverse_lazy("api:list_circles"), headers=auth_client.headers
    )

    assert response.status_code == 200


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
